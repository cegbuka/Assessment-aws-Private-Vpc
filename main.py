import boto3
from config.config import get_aws_keys
from src.vpc import VPC
from src.ec2 import EC2
from src.loadbalancer import loadBalancer
import time

def init_aws_session():
    access_key, secret_key, region = get_aws_keys()
    #print(access_key, secret_key, region)
    return boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)


def main():
    session = init_aws_session()
    print(session)
    vpc = VPC(session)
    ec2 = EC2(session=session)
    loadbalancer = loadBalancer(session=session)


    init_vpc = vpc.create_aws_vpc('172.16.0.0/16')
    vpc.enable_vpc_dns(init_vpc)
    subnet_a = vpc.create_private_subnet(init_vpc, '172.16.1.0/24', 'us-west-2c')
    subnet_b = vpc.create_private_subnet(init_vpc, '172.16.2.0/24', 'us-west-2a')
    subnet_c = vpc.create_private_subnet(init_vpc, '172.16.3.0/24', 'us-west-2b')

    subnets = [subnet_a.id, subnet_b.id, subnet_c.id]

    instance_a = ec2.create_ec2(vpc=init_vpc, subnet=subnet_a)
    instance_b = ec2.create_ec2(vpc=init_vpc, subnet=subnet_b)
    instance_c = ec2.create_ec2(vpc=init_vpc, subnet=subnet_c)


    print("Sleeping Script for 2min for instance to be in Running State")
    time.sleep(100)

    TargetGroupArn = loadbalancer.create_target_group(vpc_id=init_vpc.id)

    loadbalancer.register_target_group(target_group=TargetGroupArn, instance_id=instance_a[0].id)
    loadbalancer.register_target_group(target_group=TargetGroupArn, instance_id=instance_b[0].id)
    loadbalancer.register_target_group(target_group=TargetGroupArn, instance_id=instance_c[0].id)

    #Create Security Group for load balancer
    sg_elb=ec2.create_ssh_security_group(vpc=init_vpc, name=f'lb_{init_vpc.id}', tport=80, fport=80)
    elb = loadbalancer.create_load_balancer(securitygroup=sg_elb.id, subnets=subnets)
    # print(elb['LoadBalancers'][0]['LoadBalancerArn'])

    listerner = loadbalancer.create_listerners(TargetGroupArn=TargetGroupArn, LoadBalancerArn=elb['LoadBalancers'][0]['LoadBalancerArn'])



main()