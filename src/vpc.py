import boto3



class VPC:


    def __init__(self, session):
        self.ec2 = session.resource('ec2')
        self.ec2Client = session.client('ec2')
        


    def create_aws_vpc(self, ip):
        vpc = self.ec2.create_vpc(CidrBlock=ip)
        vpc.create_tags(Tags=[{"Key": "Name", "Value": "assessment"}])  
        vpc.wait_until_available()
        # print(vpc.id)
        return vpc
    


    def enable_vpc_dns(self, vpc):
        self.ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
        self.ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )



    def create_private_subnet(self, vpc, cidr, availabilityzone) -> any:
        print(vpc.id)
        subnet = self.ec2.create_subnet(CidrBlock=cidr, 
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'assessment_'+availabilityzone
                            },
                        ]
                    },
                ],
            VpcId=vpc.id,  AvailabilityZone=availabilityzone)
            #print(subnet)
            # create a route table and a public route
        routetable = vpc.create_route_table()
        routetable.associate_with_subnet(SubnetId=subnet.id)
        return subnet