#!/bin/bash
eksctl delete cluster --name eks-cluster
ALB_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AWSLoadBalancerControllerIAMPolicy`].Arn' --output text)
DNS_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AllowExternalDNSUpdatesPolicy`].Arn' --output text)
aws iam delete-policy --policy-arn=$ALB_POLICY_ARN
aws iam delete-policy --policy-arn=$DNS_POLICY_ARN