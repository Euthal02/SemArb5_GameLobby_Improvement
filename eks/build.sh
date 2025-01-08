#!/bin/bash

# general control variables
CLUSTER_NAME=eks-cluster
REGION=eu-central-2
DNS_ZONE=semesterarbeit.com

# set up eks cluster
eksctl create cluster --name=$CLUSTER_NAME --region=$REGION --version=1.31 --node-ami-family=AmazonLinux2 --nodes=2 --nodes-min=1 --nodes-max=3 --ssh-access --ssh-public-key=semesterarbeit_admin_access --max-pods-per-node=20 --with-oidc
# eksctl utils update-cluster-vpc-config --cluster=$CLUSTER_NAME --private-access=true --approve
# eksctl upgrade cluster --name=$CLUSTER_NAME --approve

# remove remainders from old deployments
ALB_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AWSLoadBalancerControllerIAMPolicy`].Arn' --output text)
DNS_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AllowExternalDNSUpdatesPolicy`].Arn' --output text)
if [ -n "$ALB_POLICY_ARN" ]; then
  aws iam delete-policy --policy-arn="${ALB_POLICY_ARN}"
fi
if [ -n "$DNS_POLICY_ARN" ]; then
  aws iam delete-policy --policy-arn="${DNS_POLICY_ARN}"
fi

# aws loadbalancer in k8s
wget https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/refs/heads/main/docs/install/iam_policy.json
aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json --no-cli-pager
ALB_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AWSLoadBalancerControllerIAMPolicy`].Arn' --output text)
eksctl create iamserviceaccount --cluster=$CLUSTER_NAME --namespace=kube-system --name=aws-load-balancer-controller --role-name AmazonEKSLoadBalancerControllerRole --attach-policy-arn=$ALB_POLICY_ARN --approve --override-existing-serviceaccounts
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=eks-cluster --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
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


NAMESPACE_CONTROLLER="arc-systems"
INSTALLATION_NAME="arc-runner-set"
NAMESPACE_RUNNERS="arc-runners"
GITHUB_CONFIG_URL="https://github.com/Euthal02/SemArb4_GameLobby"
GITHUB_PAT=$(awk -F "=" '/GITHUB_PAT/ {print $2}' config.ini)
helm install arc --namespace "${NAMESPACE_CONTROLLER}" --create-namespace oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
# get github pat from config.ini
helm install "${INSTALLATION_NAME}" --namespace "${NAMESPACE_RUNNERS}" --create-namespace --set githubConfigUrl="${GITHUB_CONFIG_URL}" --set githubConfigSecret.github_token="${GITHUB_PAT}" oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set

# remove downloaded files
rm -f crds.yaml
rm -f iam_policy.json
rm -f external-dns-policy.conf
rm -f trust-policy.json
