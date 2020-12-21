#!/bin/bash
set -ex
set -o pipefail

# version: 03Dec2020

##################################################
#############     SET GLOBALS     ################
##################################################



REPO_NAME="lambda-logs-to-s3-with-extensions"

GIT_REPO_URL="https://github.com/miztiik/$REPO_NAME.git"

LAYER_DIR="./layers/extensions_src"


instruction()
{
  echo "usage: ./build.sh package <stage> <region>"
  echo ""
  echo "/build.sh deploy <stage> <region> <pkg_dir>"
  echo ""
  echo "/build.sh test-<test_type> <stage>"
}

create_lambda_layer() {
cd ${LAYER_DIR}
ls -l
echo "Begin Lambda Layer Preparation. Current Working Directory `pwd`"
# chmod +x ./extensions/logs_api_http_extension.py
chmod +x ./extensions/miztiik_automation_lambda_logs_to_s3_extensions.py
pip install -r requirements.txt -t ./extensions/lib
rm -rf extension.zip
zip -r extension.zip .
echo "Lambda layer zip created successfully"
}


create_lambda_layer

