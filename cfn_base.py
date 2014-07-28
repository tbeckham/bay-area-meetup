# Software License Agreement (BSD License)
#
# Copyright (c) 2009-2013, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Tony Beckham tony@eucalyptus.com
#
# There are a few variables to set specific to your environment
# endpoint
# aws_access_key_id
# aws_secret_access_key
# KeyName
# AMI
#


import boto
from boto.regioninfo import RegionInfo
from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Ref, Template
import troposphere.ec2 as ec2

region = RegionInfo()
region.endpoint = "CLC IP"
region.name = "eucalyptus"
stack_name = "test-stack-1"

tester = boto.connect_cloudformation(region=region, port=8773, path="/services/CloudFormation", is_secure=False,
                                     aws_access_key_id="your access key",
                                     aws_secret_access_key="your secret key")

template = Template()

keyname_param = template.add_parameter(Parameter("KeyName",
                                                 Description="Name of an existing EC2 KeyPair to enable SSH access to the instance",
                                                 Type="String", ))

template.add_mapping('RegionMap', {"": {"AMI": "emi to use"}})

for i in xrange(2):
    ec2_instance = template.add_resource(ec2.Instance("Instance{0}".format(i),
                                                      ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
                                                      InstanceType="t1.micro", KeyName=Ref(keyname_param),
                                                      SecurityGroups=["default"], UserData=Base64("80")))
    vol = template.add_resource(ec2.Volume("Volume{0}".format(i), Size="1",
                                           AvailabilityZone=GetAtt("Instance{0}".format(i), "AvailabilityZone")))
    mount = template.add_resource(ec2.VolumeAttachment("MountPt{0}".format(i), InstanceId=Ref("Instance{0}".format(i)),
                                                       VolumeId=Ref("Volume{0}".format(i)), Device="/dev/vdc"))
# tester.delete_stack(stack_name)

stack = tester.create_stack(stack_name, template.to_json(), parameters=[("KeyName", "your key name")])
