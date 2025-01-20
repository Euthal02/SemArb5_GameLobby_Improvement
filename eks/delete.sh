#!/bin/bash
eksctl delete cluster --name eks-cluster
ALB_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AWSLoadBalancerControllerIAMPolicy`].Arn' --output text)
DNS_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AllowExternalDNSUpdatesPolicy`].Arn' --output text)
CERT_MANAGER_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`cert-manager-acme-dns01-route53`].Arn' --output text)
aws iam delete-policy --policy-arn=$ALB_POLICY_ARN
aws iam delete-policy --policy-arn=$DNS_POLICY_ARN
aws iam delete-policy --policy-arn=$CERT_MANAGER_POLICY_ARN
