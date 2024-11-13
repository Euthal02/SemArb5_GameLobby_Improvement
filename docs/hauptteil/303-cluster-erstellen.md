---
layout: default
title: 3.3 Cluster erstellen
parent: 3. Hauptteil
nav_order: 303
---

# 3.3 Cluster erstellen

Um den Cluster zu erstellen wird ein Account innerhalb der vorhin erwähnten "admin" Gruppe genutzt und ein Access Key erstellt.

Mit diesem Access Key kann anschliessend die lokale AWS CLI konfiguriert werden.

Als Standard Region wurde Zürich ausgewählt, dies aus keinem spezifischen Grund.

```bash
mka@Tuxedo-Laptop:~$ aws configure
AWS Access Key ID [None]: **************
AWS Secret Access Key [None]: **************
Default region name [None]: eu-central-2
Default output format [None]: json
```

## VPC erstellen

Nun kann man mit dem erstellen der effektiven Ressourcen beginnen. Angefangen mit einem VPC.

```bash
mka@Tuxedo-Laptop:~$ aws ec2 create-vpc --cidr-block 10.0.0.0/16
{
    "Vpc": {
        "CidrBlock": "10.0.0.0/16",
        "DhcpOptionsId": "dopt-********",
        "State": "pending",
        "VpcId": "vpc-*******",
        "OwnerId": "********",
        "InstanceTenancy": "default",
        "Ipv6CidrBlockAssociationSet": [],
        "CidrBlockAssociationSet": [
            {
                "AssociationId": "vpc-cidr-assoc-**********",
                "CidrBlock": "10.0.0.0/16",
                "CidrBlockState": {
                    "State": "associated"
                }
            }
        ],
        "IsDefault": false
    }
}
mka@Tuxedo-Laptop:~$
```

### Subnetze im VPC

Ein VPC in AWS erstreckt sich bekanntlich über mehrere Availability-Zones.

Für unsere Zwecke ist aber ein Subentz pro Availability Zone gefordert. Zumindest anhand der Anleitung, dies entspricht aber auch dem Grundgedanken von mehreren Hosts in unterschiedlichen Zonen.

Dies wird folgendermassen erreicht.

```bash
mka@Tuxedo-Laptop:~$ aws ec2 create-subnet --vpc-id vpc-********** --cidr-block 10.0.1.0/24 --availability-zone eu-central-2a
{
    "Subnet": {
        "AvailabilityZone": "eu-central-2a",
        "AvailabilityZoneId": "euc2-az1",
        "AvailableIpAddressCount": 251,
        "CidrBlock": "10.0.1.0/24",
        "DefaultForAz": false,
        "MapPublicIpOnLaunch": false,
        "State": "available",
        "SubnetId": "subnet-**********",
        "VpcId": "vpc-**********",
        "OwnerId": "**********",
        "AssignIpv6AddressOnCreation": false,
        "Ipv6CidrBlockAssociationSet": [],
        "SubnetArn": "arn:aws:ec2:eu-central-2:**********:subnet/subnet-**********",
        "EnableDns64": false,
        "Ipv6Native": false,
        "PrivateDnsNameOptionsOnLaunch": {
            "HostnameType": "ip-name",
            "EnableResourceNameDnsARecord": false,
            "EnableResourceNameDnsAAAARecord": false
        }
    }
}
mka@Tuxedo-Laptop:~$ aws ec2 create-subnet --vpc-id vpc-********** --cidr-block 10.0.2.0/24 --availability-zone eu-central-2b
{
    "Subnet": {
        "AvailabilityZone": "eu-central-2b",
        "AvailabilityZoneId": "euc2-az2",
        "AvailableIpAddressCount": 251,
        "CidrBlock": "10.0.2.0/24",
        "DefaultForAz": false,
        "MapPublicIpOnLaunch": false,
        "State": "available",
        "SubnetId": "subnet-**********",
        "VpcId": "vpc-**********",
        "OwnerId": "**********",
        "AssignIpv6AddressOnCreation": false,
        "Ipv6CidrBlockAssociationSet": [],
        "SubnetArn": "arn:aws:ec2:eu-central-2:**********:subnet/subnet-**********",
        "EnableDns64": false,
        "Ipv6Native": false,
        "PrivateDnsNameOptionsOnLaunch": {
            "HostnameType": "ip-name",
            "EnableResourceNameDnsARecord": false,
            "EnableResourceNameDnsAAAARecord": false
        }
    }
}
mka@Tuxedo-Laptop:~$
```

## Security Group

```bash
mka@Tuxedo-Laptop:~$ aws ec2 create-security-group --group-name eks-node-group --description "EKS Node Group" --vpc-id vpc-08e20d377549d4455
{
    "GroupId": "sg-**********"
}
mka@Tuxedo-Laptop:~$
```

### Inbound Rules

```bash
mka@Tuxedo-Laptop:~$ aws ec2 authorize-security-group-ingress --group-id sg-************ --protocol tcp --port 22 --cidr 0.0.0.0/0
{
    "Return": true,
    "SecurityGroupRules": [
        {
            "SecurityGroupRuleId": "sgr-**********",
            "GroupId": "sg-**********",
            "GroupOwnerId": "**********",
            "IsEgress": false,
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "CidrIpv4": "0.0.0.0/0"
        }
    ]
}
mka@Tuxedo-Laptop:~$ aws ec2 authorize-security-group-ingress --group-id sg-************ --protocol tcp --port 80 --cidr 0.0.0.0/0
{
    "Return": true,
    "SecurityGroupRules": [
        {
            "SecurityGroupRuleId": "sgr-**********",
            "GroupId": "sg-**********",
            "GroupOwnerId": "**********",
            "IsEgress": false,
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "CidrIpv4": "0.0.0.0/0"
        }
    ]
}
mka@Tuxedo-Laptop:~$ aws ec2 authorize-security-group-ingress --group-id sg-************ --protocol tcp --port 443 --cidr 0.0.0.0/0
{
    "Return": true,
    "SecurityGroupRules": [
        {
            "SecurityGroupRuleId": "sgr-**********",
            "GroupId": "sg-**********",
            "GroupOwnerId": "**********",
            "IsEgress": false,
            "IpProtocol": "tcp",
            "FromPort": 443,
            "ToPort": 443,
            "CidrIpv4": "0.0.0.0/0"
        }
    ]
}
mka@Tuxedo-Laptop:~$
```

## EKS Cluster

```bash
mka@Tuxedo-Laptop:~$ aws eks create-cluster --name eks-cluster --role-arn arn:aws:iam::**********:role/eksClusterRole --resources-vpc-config subnetIds=subnet-**********,subnet-**********,security
GroupIds=sg-**********
{
    "cluster": {
        "name": "eks-cluster",
        "arn": "arn:aws:eks:eu-central-2:**********:cluster/eks-cluster",
        "createdAt": 1731511678.911,
        "version": "1.31",
        "roleArn": "arn:aws:iam::**********:role/eksClusterRole",
        "resourcesVpcConfig": {
            "subnetIds": [
                "subnet-**********",
                "subnet-**********"
            ],
            "securityGroupIds": [
                "sg-**********"
            ],
            "vpcId": "vpc-**********",
            "endpointPublicAccess": true,
            "endpointPrivateAccess": false,
            "publicAccessCidrs": [
                "0.0.0.0/0"
            ]
        },
        "kubernetesNetworkConfig": {
            "serviceIpv4Cidr": "172.20.0.0/16",
            "ipFamily": "ipv4"
        },
        "logging": {
            "clusterLogging": [
                {
                    "types": [
                        "api",
                        "audit",
                        "authenticator",
                        "controllerManager",
                        "scheduler"
                    ],
                    "enabled": false
                }
            ]
        },
        "status": "CREATING",
        "certificateAuthority": {},
        "platformVersion": "eks.10",
        "tags": {}
    }
}
mka@Tuxedo-Laptop:~$
```

Damit ist der Cluster bereits erstellt, besitzt aber noch keine Nodes.

![EKS Cluster Up](../ressources/images/aws/eks_cluster_up.PNG)

```bash
mka@Tuxedo-Laptop:~$ aws eks describe-cluster --name eks-cluster
{
    "cluster": {
        "name": "eks-cluster",
        "arn": "arn:aws:eks:eu-central-2:**********:cluster/eks-cluster",
        "createdAt": 1731511678.911,
        "version": "1.31",
        "endpoint": "https://EE18D1A425212EE10C34D84A556C9846.yl4.eu-central-2.eks.amazonaws.com",
        "roleArn": "arn:aws:iam::**********:role/eksClusterRole",
        "resourcesVpcConfig": {
            "subnetIds": [
                "subnet-0b8ab87d15caaee61",
                "subnet-09297e96ff32f9e7f"
            ],
            "securityGroupIds": [
                "sg-05620a5b6f319f81c"
            ],
            "clusterSecurityGroupId": "sg-**********",
            "vpcId": "vpc-**********",
            "endpointPublicAccess": true,
            "endpointPrivateAccess": false,
            "publicAccessCidrs": [
                "0.0.0.0/0"
            ]
        },
        "kubernetesNetworkConfig": {
            "serviceIpv4Cidr": "172.20.0.0/16",
            "ipFamily": "ipv4"
        },
        "logging": {
            "clusterLogging": [
                {
                    "types": [
                        "api",
                        "audit",
                        "authenticator",
                        "controllerManager",
                        "scheduler"
                    ],
                    "enabled": false
                }
            ]
        },
        "identity": {
            "oidc": {
                "issuer": "https://oidc.eks.eu-central-2.amazonaws.com/id/EE18D1A425212EE10C34D84A556C9846"
            }
        },
        "status": "ACTIVE",
        "certificateAuthority": {
            "data": "**********"
        },
        "platformVersion": "eks.10",
        "tags": {}
    }
}
mka@Tuxedo-Laptop:~$
```

## Nodes

```bash
mka@Tuxedo-Laptop:~$ aws eks create-nodegroup --cluster-name eks-cluster --nodegroup-name eks-cluster-node-group-subnet1 --node-role arn:aws:iam::**********:role/AmazonEKSNodeRole --subnets subnet-********** --scaling-config minSize=2,maxSize=2,desiredSize=2 --instance-types t3.micro --ami-type AL2_x86_64 --remote-access ec2SshKey=semesterarbeit_admin_access
{
    "nodegroup": {
        "nodegroupName": "eks-cluster-node-group-subnet1",
        "nodegroupArn": "arn:aws:eks:eu-central-2:**********:nodegroup/eks-cluster/eks-cluster-node-group-subnet1/0cc99316-fa16-8c0e-346d-bf395ae181aa",
        "clusterName": "eks-cluster",
        "version": "1.31",
        "releaseVersion": "1.31.0-20241109",
        "createdAt": 1731512367.896,
        "modifiedAt": 1731512367.896,
        "status": "CREATING",
        "capacityType": "ON_DEMAND",
        "scalingConfig": {
            "minSize": 2,
            "maxSize": 2,
            "desiredSize": 2
        },
        "instanceTypes": [
            "t3.micro"
        ],
        "subnets": [
            "subnet-0b8ab87d15caaee61"
        ],
        "remoteAccess": {
            "ec2SshKey": "semesterarbeit_admin_access"
        },
        "amiType": "AL2_x86_64",
        "nodeRole": "arn:aws:iam::**********:role/AmazonEKSNodeRole",
        "diskSize": 20,
        "health": {
            "issues": []
        },
        "updateConfig": {
            "maxUnavailable": 1
        },
        "tags": {}
    }
}
mka@Tuxedo-Laptop:~$ aws eks create-nodegroup --cluster-name eks-cluster --nodegroup-name eks-cluster-node-group-subnet2 --node-role arn:aws:iam::**********:role/AmazonEKSNodeRole --subnets subnet-**********
f9e7f --scaling-config minSize=2,maxSize=2,desiredSize=2 --instance-types t3.micro --ami-type AL2_x86_64 --remote-access ec2SshKey=semesterarbeit_admin_access
{
    "nodegroup": {
        "nodegroupName": "eks-cluster-node-group-subnet2",
        "nodegroupArn": "arn:aws:eks:eu-central-2:**********:nodegroup/eks-cluster/eks-cluster-node-group-subnet2/86c99317-5294-7bce-f5b3-82f9bed93012",
        "clusterName": "eks-cluster",
        "version": "1.31",
        "releaseVersion": "1.31.0-20241109",
        "createdAt": 1731512412.929,
        "modifiedAt": 1731512412.929,
        "status": "CREATING",
        "capacityType": "ON_DEMAND",
        "scalingConfig": {
            "minSize": 2,
            "maxSize": 2,
            "desiredSize": 2
        },
        "instanceTypes": [
            "t3.micro"
        ],
        "subnets": [
            "subnet-09297e96ff32f9e7f"
        ],
        "remoteAccess": {
            "ec2SshKey": "semesterarbeit_admin_access"
        },
        "amiType": "AL2_x86_64",
        "nodeRole": "arn:aws:iam::**********:role/AmazonEKSNodeRole",
        "diskSize": 20,
        "health": {
            "issues": []
        },
        "updateConfig": {
            "maxUnavailable": 1
        },
        "tags": {}
    }
}
mka@Tuxedo-Laptop:~$
```

## Kubectl

```bash
mka@Tuxedo-Laptop:~$ aws eks update-kubeconfig --region eu-central-2 --name eks-cluster
Added new context arn:aws:eks:eu-central-2:**********:cluster/eks-cluster to /home/mka/.kube/config
mka@Tuxedo-Laptop:~$ kubectl version
Client Version: v1.31.0
Kustomize Version: v5.4.2
Server Version: v1.31.2-eks-7f9249a
mka@Tuxedo-Laptop:~$ kubectl cluster-info
Kubernetes control plane is running at https://EE18D1A425212EE10C34D84A556C9846.yl4.eu-central-2.eks.amazonaws.com
CoreDNS is running at https://EE18D1A425212EE10C34D84A556C9846.yl4.eu-central-2.eks.amazonaws.com/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
mka@Tuxedo-Laptop:~$
```


## EKSCTL Command

```bash
mka@Tuxedo-Laptop:~$ eksctl create cluster --name=eks-cluster --nodes=5 --instance-types=t3.micro --region=eu-central-2 --ssh-public-key=semesterarbeit_admin_access
2024-11-13 20:47:26 [ℹ]  eksctl version 0.194.0
2024-11-13 20:47:26 [ℹ]  using region eu-central-2
2024-11-13 20:47:27 [ℹ]  setting availability zones to [eu-central-2b eu-central-2c eu-central-2a]
2024-11-13 20:47:27 [ℹ]  subnets for eu-central-2b - public:192.168.0.0/19 private:192.168.96.0/19
2024-11-13 20:47:27 [ℹ]  subnets for eu-central-2c - public:192.168.32.0/19 private:192.168.128.0/19
2024-11-13 20:47:27 [ℹ]  subnets for eu-central-2a - public:192.168.64.0/19 private:192.168.160.0/19
2024-11-13 20:47:27 [ℹ]  nodegroup "ng-7e8fea54" will use "" [AmazonLinux2/1.30]
2024-11-13 20:47:27 [ℹ]  using Kubernetes version 1.30
2024-11-13 20:47:27 [ℹ]  creating EKS cluster "eks-cluster" in "eu-central-2" region with managed nodes
2024-11-13 20:47:27 [ℹ]  will create 2 separate CloudFormation stacks for cluster itself and the initial managed nodegroup
2024-11-13 20:47:27 [ℹ]  if you encounter any issues, check CloudFormation console or try 'eksctl utils describe-stacks --region=eu-central-2 --cluster=eks-cluster'
2024-11-13 20:47:27 [ℹ]  Kubernetes API endpoint access will use default of {publicAccess=true, privateAccess=false} for cluster "eks-cluster" in "eu-central-2"
2024-11-13 20:47:27 [ℹ]  CloudWatch logging will not be enabled for cluster "eks-cluster" in "eu-central-2"
2024-11-13 20:47:27 [ℹ]  you can enable it with 'eksctl utils update-cluster-logging --enable-types={SPECIFY-YOUR-LOG-TYPES-HERE (e.g. all)} --region=eu-central-2 --cluster=eks-cluster'
2024-11-13 20:47:27 [ℹ]  default addons vpc-cni, kube-proxy, coredns were not specified, will install them as EKS addons
2024-11-13 20:47:27 [ℹ]
2 sequential tasks: { create cluster control plane "eks-cluster",
    2 sequential sub-tasks: {
        2 sequential sub-tasks: {
            1 task: { create addons },
            wait for control plane to become ready,
        },
        create managed nodegroup "ng-7e8fea54",
    }
}
2024-11-13 20:47:27 [ℹ]  building cluster stack "eksctl-eks-cluster-cluster"
2024-11-13 20:47:27 [ℹ]  deploying stack "eksctl-eks-cluster-cluster"
2024-11-13 20:47:57 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-cluster"
2024-11-13 20:48:27 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-cluster"
2024-11-13 20:49:27 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-cluster"
2024-11-13 20:50:27 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-cluster"
2024-11-13 20:51:28 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-cluster"
2024-11-13 20:52:28 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-cluster"
2024-11-13 20:53:28 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-cluster"
2024-11-13 20:54:28 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-cluster"
2024-11-13 20:54:29 [!]  recommended policies were found for "vpc-cni" addon, but since OIDC is disabled on the cluster, eksctl cannot configure the requested permissions; the recommended way to provide IAM permissions for "vpc-cni" addon is via pod identity associations; after addon creation is completed, add all recommended policies to the config file, under `addon.PodIdentityAssociations`, and run `eksctl update addon`
2024-11-13 20:54:29 [ℹ]  creating addon
2024-11-13 20:54:29 [ℹ]  successfully created addon
2024-11-13 20:54:29 [ℹ]  creating addon
2024-11-13 20:54:30 [ℹ]  successfully created addon
2024-11-13 20:54:30 [ℹ]  creating addon
2024-11-13 20:54:30 [ℹ]  successfully created addon
2024-11-13 20:56:31 [ℹ]  building managed nodegroup stack "eksctl-eks-cluster-nodegroup-ng-7e8fea54"
2024-11-13 20:56:31 [ℹ]  deploying stack "eksctl-eks-cluster-nodegroup-ng-7e8fea54"
2024-11-13 20:56:31 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-nodegroup-ng-7e8fea54"
2024-11-13 20:57:01 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-nodegroup-ng-7e8fea54"
2024-11-13 20:57:36 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-nodegroup-ng-7e8fea54"
2024-11-13 20:59:13 [ℹ]  waiting for CloudFormation stack "eksctl-eks-cluster-nodegroup-ng-7e8fea54"
2024-11-13 20:59:13 [ℹ]  waiting for the control plane to become ready
2024-11-13 20:59:14 [✔]  saved kubeconfig as "/home/mka/.kube/config"
2024-11-13 20:59:14 [ℹ]  no tasks
2024-11-13 20:59:14 [✔]  all EKS cluster resources for "eks-cluster" have been created
2024-11-13 20:59:14 [✔]  created 0 nodegroup(s) in cluster "eks-cluster"
2024-11-13 20:59:14 [ℹ]  nodegroup "ng-7e8fea54" has 5 node(s)
2024-11-13 20:59:14 [ℹ]  node "ip-192-168-53-251.eu-central-2.compute.internal" is ready
2024-11-13 20:59:14 [ℹ]  node "ip-192-168-63-145.eu-central-2.compute.internal" is ready
2024-11-13 20:59:14 [ℹ]  node "ip-192-168-67-108.eu-central-2.compute.internal" is ready
2024-11-13 20:59:14 [ℹ]  node "ip-192-168-7-48.eu-central-2.compute.internal" is ready
2024-11-13 20:59:14 [ℹ]  node "ip-192-168-78-66.eu-central-2.compute.internal" is ready
2024-11-13 20:59:14 [ℹ]  waiting for at least 5 node(s) to become ready in "ng-7e8fea54"
2024-11-13 20:59:14 [ℹ]  nodegroup "ng-7e8fea54" has 5 node(s)
2024-11-13 20:59:14 [ℹ]  node "ip-192-168-53-251.eu-central-2.compute.internal" is ready
2024-11-13 20:59:14 [ℹ]  node "ip-192-168-63-145.eu-central-2.compute.internal" is ready
2024-11-13 20:59:14 [ℹ]  node "ip-192-168-67-108.eu-central-2.compute.internal" is ready
2024-11-13 20:59:14 [ℹ]  node "ip-192-168-7-48.eu-central-2.compute.internal" is ready
2024-11-13 20:59:14 [ℹ]  node "ip-192-168-78-66.eu-central-2.compute.internal" is ready
2024-11-13 20:59:14 [✔]  created 1 managed nodegroup(s) in cluster "eks-cluster"
2024-11-13 20:59:16 [ℹ]  kubectl command should work with "/home/mka/.kube/config", try 'kubectl get nodes'
2024-11-13 20:59:16 [✔]  EKS cluster "eks-cluster" in "eu-central-2" region is ready
mka@Tuxedo-Laptop:~$ kubectl get nodes
NAME                                              STATUS   ROLES    AGE   VERSION
ip-192-168-53-251.eu-central-2.compute.internal   Ready    <none>   94s   v1.30.4-eks-a737599
ip-192-168-63-145.eu-central-2.compute.internal   Ready    <none>   98s   v1.30.4-eks-a737599
ip-192-168-67-108.eu-central-2.compute.internal   Ready    <none>   84s   v1.30.4-eks-a737599
ip-192-168-7-48.eu-central-2.compute.internal     Ready    <none>   92s   v1.30.4-eks-a737599
ip-192-168-78-66.eu-central-2.compute.internal    Ready    <none>   94s   v1.30.4-eks-a737599
mka@Tuxedo-Laptop:~$ kubectl version
Client Version: v1.31.0
Kustomize Version: v5.4.2
Server Version: v1.30.6-eks-7f9249a
mka@Tuxedo-Laptop:~$ kubectl cluster-info
Kubernetes control plane is running at https://7D84FF8A8DE6F56A20A9B69EA38F3709.yl4.eu-central-2.eks.amazonaws.com
CoreDNS is running at https://7D84FF8A8DE6F56A20A9B69EA38F3709.yl4.eu-central-2.eks.amazonaws.com/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
mka@Tuxedo-Laptop:~$
```
