

class EC2:
    def __init__(self, session):
        self.ec2 = session.resource('ec2')

        
    def create_ec2(self, vpc, subnet, instancetype='t2.micro', image='ami-0c2ab3b8efb09f272') -> any:
        # print(vpc.id)
        securitygroup = self.create_ssh_security_group(name="sg_"+subnet.id,vpc=vpc)
        # self.create_key_pair(self)
        instances = self.ec2.create_instances(
            ImageId=image,
            InstanceType=instancetype,
            MaxCount=1,
            MinCount=1,
            NetworkInterfaces=[{
                'SubnetId': subnet.id,
                'DeviceIndex': 0,
                'AssociatePublicIpAddress': True,
                'Groups': [securitygroup.group_id]
            }],
            KeyName='assessment')
        return instances

    def create_ssh_security_group(self, vpc, cidr='0.0.0.0/0', protocol='tcp', fport=22, tport=22, name='ssh'):
        securitygroup = self.ec2.create_security_group(GroupName=name, Description='only allow SSH traffic', VpcId=vpc.id)
        securitygroup.authorize_ingress(CidrIp=cidr, IpProtocol=protocol, FromPort=fport, ToPort=tport)
        securitygroup.authorize_ingress(CidrIp=cidr, IpProtocol=protocol, FromPort=80, ToPort=80)
        return securitygroup
    
    
    def create_key_pair(self):
        outfile = open('assessment.pem', 'w')
        key_pair = self.ec2.create_key_pair(KeyName='assessment')
        KeyPairOut = str(key_pair.key_material)
        outfile.write(KeyPairOut)