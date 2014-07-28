CloudFormation with Eucalyptus
==============================
* __Eucalyptus 4.0 - Ec2, IAM, CloudWatch, ELB, AutoScaling actions__
* __Eucalyptus 4.1 - S3 actions and wait conditions__

### Demo
* creating stack (troposphere and euca2ools)
* View stack status
* Ec2 actions, S3 actions and wait condition
* Delete stack cleans up resources

### Tools
* [AWS Java SDK] (https://github.com/aws/aws-sdk-java)
* [Boto] (https://github.com/boto/boto)
* [Troposphere] (https://github.com/cloudtools/troposphere)
* [euca2ools] (https://github.com/eucalyptus/euca2ools)
* [Eucalobo] (https://github.com/viglesiasce/EucaLobo)


### Ec2 Actions
Using Boto and Troposphere create a stack that will
* run instance
* create a volume and attach the volume to the instance
* Inspect using Eucalobo
* Delete stack (all resources cleaned up)

### Bucket Actions
```
euform-create-stack --template-file buckets.json bucket-test
```
* Create buckets
* specify ACLs
* Specify versioning
* lifecycle rules
* AWS java SDK to inspect the buckets
* Delete stack (all resources cleaned up)

### Wait Condition
```
euform-create-stack --template-file wait_condition.json -p ImageId=emi-bedcd5aa -p KeyName=adminkey wait-stack
```
* run instance with wait condition of apache being configured
* stack will not be complete until then
* monitor the progress by "euform-describe-stacks"
* Once complete, you should have an instance running apache.
* Delete stack (all resources cleaned up)
