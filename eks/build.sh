#!/bin/bash

# general control variables
CLUSTER_NAME=eks-cluster
REGION=eu-central-2
DNS_ZONE=semesterarbeit.com

# set up eks cluster
eksctl create cluster --name=$CLUSTER_NAME --region=$REGION --version=1.31 --node-ami-family=AmazonLinux2 --nodes=2 --nodes-min=1 --nodes-max=3 --ssh-access --ssh-public-key=semesterarbeit_admin_access --max-pods-per-node=20 --with-oidc

# remove remainders from old deployments
ALB_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AWSLoadBalancerControllerIAMPolicy`].Arn' --output text)
DNS_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AllowExternalDNSUpdatesPolicy`].Arn' --output text)
CERT_MANAGER_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`cert-manager-acme-dns01-route53`].Arn' --output text)
if [ -n "$ALB_POLICY_ARN" ]; then
  aws iam delete-policy --policy-arn="${ALB_POLICY_ARN}"
fi
if [ -n "$DNS_POLICY_ARN" ]; then
  aws iam delete-policy --policy-arn="${DNS_POLICY_ARN}"
fi
if [ -n "$CERT_MANAGER_POLICY_ARN" ]; then
  aws iam delete-policy --policy-arn="${CERT_MANAGER_POLICY_ARN}"
fi

# aws loadbalancer in k8s
wget https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/refs/heads/main/docs/install/iam_policy.json
aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json --no-cli-pager
ALB_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AWSLoadBalancerControllerIAMPolicy`].Arn' --output text)
eksctl create iamserviceaccount --cluster=$CLUSTER_NAME --namespace=kube-system --name=aws-load-balancer-controller --role-name AmazonEKSLoadBalancerControllerRole --attach-policy-arn=$ALB_POLICY_ARN --approve --override-existing-serviceaccounts
helm install --repo https://aws.github.io/eks-charts aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=eks-cluster --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
wget https://raw.githubusercontent.com/aws/eks-charts/master/stable/aws-load-balancer-controller/crds/crds.yaml
kubectl apply -f crds.yaml

# install external dns
cat > external-dns-policy.conf << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:ChangeResourceRecordSets"
      ],
      "Resource": [
        "arn:aws:route53:::hostedzone/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "route53:ListHostedZones",
        "route53:ListResourceRecordSets",
        "route53:ListTagsForResource"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
EOF
aws iam create-policy --policy-name "AllowExternalDNSUpdatesPolicy" --policy-document file://external-dns-policy.conf --no-cli-pager
DNS_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AllowExternalDNSUpdatesPolicy`].Arn' --output text)
eksctl create iamserviceaccount --cluster="${CLUSTER_NAME}" --namespace=default --name=external-dns --role-name=AllowExternalDNSUpdatesRole --attach-policy-arn=$DNS_POLICY_ARN --approve --override-existing-serviceaccounts
DNS_ROLE_ARN=$(aws iam get-role --role-name AllowExternalDNSUpdatesRole --query 'Role.[Arn]' --output text)
helm install external-dns oci://registry-1.docker.io/bitnamicharts/external-dns --set provider=aws --set aws.region=eu-central-2 --set domainFilters[0]=$DNS_ZONE --set policy=sync --set aws.roleArn=$DNS_ROLE_ARN --set serviceAccount.create=false --set serviceAccount.name=external-dns

# install cert manager
helm install cert-manager cert-manager --repo https://charts.jetstack.io --namespace cert-manager --set crds.enabled=true --create-namespace 
aws iam create-policy --policy-name cert-manager-acme-dns01-route53 --description "This policy allows cert-manager to manage ACME DNS01 records in Route53 hosted zones. See https://cert-manager.io/docs/configuration/acme/dns01/route53" --policy-document file:///dev/stdin <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "route53:GetChange",
      "Resource": "arn:aws:route53:::change/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "route53:ChangeResourceRecordSets",
        "route53:ListResourceRecordSets"
      ],
      "Resource": "arn:aws:route53:::hostedzone/*"
    },
    {
      "Effect": "Allow",
      "Action": "route53:ListHostedZonesByName",
      "Resource": "*"
    }
  ]
}
EOF
CERT_MANAGER_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`cert-manager-acme-dns01-route53`].Arn' --output text)
eksctl create iamserviceaccount --name cert-manager-acme-dns01-route53 --namespace cert-manager --cluster "${CLUSTER_NAME}" --role-name cert-manager-acme-dns01-route53 --attach-policy-arn "${CERT_MANAGER_POLICY_ARN}" --approve
cat > rbac.yaml << EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: cert-manager-acme-dns01-route53-tokenrequest
  namespace: cert-manager
rules:
  - apiGroups: ['']
    resources: ['serviceaccounts/token']
    resourceNames: ['cert-manager-acme-dns01-route53']
    verbs: ['create']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cert-manager-acme-dns01-route53-tokenrequest
  namespace: cert-manager
subjects:
  - kind: ServiceAccount
    name: cert-manager
    namespace: cert-manager
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: cert-manager-acme-dns01-route53-tokenrequest
EOF
kubectl apply -f rbac.yaml
CERT_MANAGER_ROLE_ARN=$(aws iam get-role --role-name cert-manager-acme-dns01-route53 --query 'Role.[Arn]' --output text)
cat > letsencrypt-issuer.yaml << EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: marcokaelin@gmx.net
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - dns01:
        route53:
          region: ${REGION}
          role: ${CERT_MANAGER_ROLE_ARN}
          auth:
            kubernetes:
              serviceAccountRef:
                name: cert-manager-acme-dns01-route53

EOF
kubectl apply -f letsencrypt-issuer.yaml

# remove downloaded files
rm -f crds.yaml
rm -f rbac.yaml
rm -f letsencrypt-issuer.yaml
rm -f iam_policy.json
rm -f external-dns-policy.conf
rm -f trust-policy.json
