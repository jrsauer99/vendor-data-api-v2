PROFILE="jrsauer99"

echo "Updating Dependencies..."
./build_dependencies.sh

echo "Copying Dependencies to S3..."
aws s3 cp packages.zip s3://vendor-data-resources/code/packages.zip --profile $PROFILE

echo "Copying Job File for Step to S3..."
aws s3 cp vendor_data.py s3://vendor-data-resources/code/jobs/vendor_data.py --profile $PROFILE

echo "Copying EMR Config to S3..."
aws s3 cp configs/emr_configs.json s3://vendor-data-resources/code/configs/emr_configs.json --profile $PROFILE

aws emr create-cluster \
    --profile $PROFILE \
    --region us-east-1 \
    --release-label emr-6.1.0 \
    --instance-groups InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m5.xlarge InstanceGroupType=CORE,InstanceCount=2,InstanceType=m5.2xlarge \
    --auto-terminate \
    --configurations file://./configs/emr_configs.json \
    --use-default-roles \
    --enable-debugging \
    --applications Name=Spark Name=Hadoop Name=Ganglia Name=Zeppelin \
    --name="test kinesis" \
    --log-uri s3://vendor-data-resources/logs/ \
    --steps '[{"Type":"CUSTOM_JAR","Name":"Spark App","Jar":"command-runner.jar","ActionOnFailure":"CONTINUE","Args":["spark-submit", "--master=yarn","--deploy-mode=cluster","--py-files=s3://vendor-data-resources/code/packages.zip", "s3://vendor-data-resources/code/jobs/vendor_data.py"]}]'
    

