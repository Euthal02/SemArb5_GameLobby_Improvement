#!/bin/bash

CLUSTER_NAME=eks-cluster
REGION=eu-central-2

# eksctl
eksctl create cluster --name=$CLUSTER_NAME --region=$REGION --node-ami-family=AmazonLinux2 --nodes=2 --nodes-min=1 --nodes-max=3 --ssh-access --ssh-public-key=semesterarbeit_admin_access --max-pods-per-node=20 --enable-ssm --with-oidc
eksctl utils update-cluster-vpc-config --cluster=$CLUSTER_NAME --public-access-cidrs=45.94.88.37/32 --private-access=true --approve
eksctl upgrade cluster --name=$CLUSTER_NAME --approve

# get account id
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)

# remove remainders from old deployments
aws iam delete-policy --policy-arn=arn:aws:iam::"$AWS_ACCOUNT_ID":policy/AWSLoadBalancerControllerIAMPolicy
aws iam delete-policy --policy-arn=arn:aws:iam::"$AWS_ACCOUNT_ID":policy/AllowExternalDNSUpdates

# alb in k8s
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/refs/heads/main/docs/install/iam_policy.json
aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json --no-cli-pager
eksctl create iamserviceaccount --cluster=$CLUSTER_NAME --namespace=kube-system --name=aws-load-balancer-controller --role-name AmazonEKSLoadBalancerControllerRole --attach-policy-arn=arn:aws:iam::"$AWS_ACCOUNT_ID":policy/AWSLoadBalancerControllerIAMPolicy --approve --override-existing-serviceaccounts

# install helm for preconfigured aws loadbalancer
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=eks-cluster --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
wget https://raw.githubusercontent.com/aws/eks-charts/master/stable/aws-load-balancer-controller/crds/crds.yaml
kubectl apply -f crds.yaml

# install external dns
# aws iam create-policy --policy-name "AllowExternalDNSUpdates" --policy-document file://eks/external-dns-policy.conf
# POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AllowExternalDNSUpdates`].Arn' --output text)
# eksctl create iamserviceaccount --cluster=$CLUSTER_NAME --name=external-dns --namespace=default --attach-policy-arn=$POLICY_ARN --approve --override-existing-serviceaccounts
# wget https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/main/docs/examples/external-dns.yaml
# sed -i 's/--domain-filter=external-dns-test\.my-org\.com/--domain-filter=semesterarbeit.com/g' external-dns.yaml
# kubectl apply -f external-dns.yaml

# remove downloaded files
rm -f crds.yaml
rm -f iam_policy.json
rm -f external-dns.yaml
