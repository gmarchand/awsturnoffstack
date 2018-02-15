SHELL := /bin/bash

include .env
export

STACK_NAME?=        switchoff
S3_BUCKET?=         mybucket


GIT_FQDN?=                   $(shell git config --get remote.origin.url | sed 's@\(.*\):\(.*\).git@\2@g')
GIT_REF_NAME?=               $(shell git rev-parse --abbrev-ref HEAD | tr '/' '-' )
GIT_REF_SHORT?=              $(shell git log -1|head -n1|cut -d ' ' -f2- | head -c 8)

CFN_CHANGE_SET?=             $(GIT_REF_NAME)-$(GIT_REF_SHORT)

info: ## env info
	@echo GIT_FQDN = $(GIT_FQDN)
	@echo GIT_REF_NAME = $(GIT_REF_NAME)
	@echo GIT_REF_SHORT = $(GIT_REF_SHORT)
	@echo STACK_NAME = $(STACK_NAME)
	@echo S3_BUCKET = $(S3_BUCKET)
	@echo CFN_CHANGE_SET = $(CFN_CHANGE_SET)

help:           ## prints help
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf " > \033[36m%-20s\033[0m %s\n", $$1, $$2}'

validate-stack: ## cfn validate template
	aws cloudformation validate-template --template-body file://cfn_template.yaml

create-stack: lambda-package	## cfn create stack
	aws cloudformation package  --template-file cfn_template.yaml --s3-bucket ${S3_BUCKET} --output-template-file /tmp/packaged-template.yaml
	aws cloudformation deploy --template-file /tmp/packaged-template.yaml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM


update-stack: ## cfn update cfn template
	aws cloudformation package  --template-file cfn_template.yaml --s3-bucket ${S3_BUCKET} --output-template-file /tmp/packaged-template.yaml
	aws cloudformation create-change-set --change-set-name ${CFN_CHANGE_SET} --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --template-body file:///tmp/packaged-template.yaml
	aws cloudformation describe-change-set --change-set-name ${CFN_CHANGE_SET} --stack-name ${STACK_NAME}
	sleep 10
	aws cloudformation execute-change-set --change-set-name ${CFN_CHANGE_SET} --stack-name ${STACK_NAME}

delete-stack: ## cfn delete stack
	aws cloudformation delete-stack --stack-name ${STACK_NAME}

