SHELL := /bin/bash

include .env
export

STACK_NAME?=        switchoff
S3_BUCKET?=         mybucket
info: ## env info
	env

help:           ## prints help
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf " > \033[36m%-20s\033[0m %s\n", $$1, $$2}'

validate-stack: ## cfn validate template
	aws cloudformation validate-template --template-body file://cfn_template.yaml

create-stack: 	## cfn create stack
	aws cloudformation package  --template-file cfn_template.yaml --s3-bucket ${S3_BUCKET} --output-template-file /tmp/packaged-template.yaml
	aws cloudformation deploy --template-file /tmp/packaged-template.yaml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM

update-stack: ## cfn update stack
	aws cloudformation package  --template-file cfn_template.yaml --s3-bucket ${S3_BUCKET} --output-template-file /tmp/packaged-template.yaml
	aws cloudformation update-stack --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --template-body file:///tmp/packaged-template.yaml

delete-stack: ## cfn delete stack
	aws cloudformation delete-stack --stack-name ${STACK_NAME}

