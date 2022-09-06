

class loadBalancer:
    def __init__(self, session):
        self.elb = session.client('elbv2')
        # self.ec2 = EC2(session)

    def create_target_group(self, vpc_id, target_group_name="assesment"):
        response = self.elb.create_target_group(Name=target_group_name, Protocol='HTTP', Port=80, VpcId=vpc_id)
        return response['TargetGroups'][0]['TargetGroupArn']
    
    def register_target_group(self, target_group, instance_id):
        self.elb.register_targets(TargetGroupArn=target_group,Targets=[{'Id': instance_id,}],)
    
    def create_load_balancer(self, securitygroup, subnets) -> any:
        response = self.elb.create_load_balancer(Name='assesment',
                Subnets=subnets,
                SecurityGroups=[
                    securitygroup,
                ],
                Scheme='internal',
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': 'Assessment'
                    },
                ],
                Type='application',
                IpAddressType='ipv4'
            )
        return response

    def create_listerners(self, TargetGroupArn, LoadBalancerArn):
        response = self.elb.create_listener(
                    DefaultActions=[
                        {
                            'TargetGroupArn': TargetGroupArn,
                            'Type': 'forward',
                        },
                    ],
                    LoadBalancerArn=LoadBalancerArn,
                    Port=80,
                    Protocol='HTTP',
                )
        return response
