#!/bin/bash

# generate raw data
DATE=$(date +%Y-%m-%dT%H:%M:%S)
FILE=./raw/${DATE}-raw-data.csv

echo "date,order,client,product,quantity" > ${FILE}
echo "${DATE},1,Alfred,Socks,4" >> ${FILE}
echo "${DATE},2,Alberto,Short,1" >> ${FILE}
echo "${DATE},3,Gustave,Coat,x" >> ${FILE} # x is not a number
echo "${DATE},4,Raimondo,Undies,7" >> ${FILE}
echo "${DATE},5,Kilian,Belt,2" >> ${FILE}
echo "${DATE},,Gilian,Glasses,1" >> ${FILE} # empty order

# upload raw data to S3
aws s3 cp ${FILE} s3://ref-pipeline-data-bucket-lazgar/raw/

# trigger pipeline
aws glue start-trigger \
    --name ref-pipeline-trigger