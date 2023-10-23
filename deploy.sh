#!/bin/bash

# deploy AWS resources
aws cloudformation deploy \
    --template-file ./cf/pipeline.yaml \
    --stack-name ref-pipeline \
    --capabilities CAPABILITY_IAM

# deploy pyspark scripts
aws s3 cp ./scripts/ s3://ref-pipeline-scripts-bucket-lazgar/scripts/ --recursive
