SHELL := /bin/bash

include .env


GIT_FQDN?=                   $(shell git config --get remote.origin.url | sed 's@\(.*\):\(.*\).git@\2@g')
GIT_REF_NAME?=               $(shell git rev-parse --abbrev-ref HEAD | tr '/' '-' )
GIT_REF_SHORT?=              $(shell git log -1|head -n1|cut -d ' ' -f2- | head -c 8)

CFN_CHANGE_SET?=             $(GIT_REF_NAME)-$(GIT_REF_SHORT)

DATE?=                       $(shell date +'%y.%m.%d %H:%M:%S')

DEST=./

# Make does not offer a recursive wildcard function, so here's one:
rwildcard=$(wildcard $1$2) $(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2))

# How to recursively find all files that match a pattern
ALL_CFN := $(call rwildcard,./,cfn_*.yaml)

help:           ## prints help
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf " > \033[36m%-20s\033[0m %s\n", $$1, $$2}'

info: ## env info
	@echo DEST = $(DEST)
	@echo GIT_FQDN = $(GIT_FQDN)
	@echo GIT_REF_NAME = $(GIT_REF_NAME)
	@echo GIT_REF_SHORT = $(GIT_REF_SHORT)
	@echo STACK_NAME = $(STACK_NAME)
	@echo S3_BUCKET = $(S3_BUCKET)
	@echo CFN_CHANGE_SET = $(CFN_CHANGE_SET)
	@echo DATE = $(DATE)
	@echo SNS_SEND_DELETION = $(SNS_SEND_DELETION)
	@echo SNS_SEND_CANCELATION = $(SNS_SEND_CANCELATION)
	@echo ALL_CFN = $(ALL_CFN)



validate-stack: ## cfn validate template
	aws cloudformation validate-template --template-body file://${DEST}cfn_template.yaml


update-slack-stack: ## update slack cfn template
	mkdir -p /tmp/slack/
	aws cloudformation package --template-file slack/cfn_template.yaml --s3-bucket ${S3_BUCKET} --output-template-file /tmp/slack/packaged-template.yaml
	aws cloudformation create-change-set --change-set-name ${CFN_CHANGE_SET} --stack-name ${SLACK_STACK_NAME} --capabilities CAPABILITY_IAM --template-body file:///tmp/slack/packaged-template.yaml --parameters ParameterKey=SlackWebHook,ParameterValue=${SLACK_WEB_HOOK} ParameterKey=SwitchOffStackName,ParameterValue=${STACK_NAME}
	aws cloudformation describe-change-set --change-set-name ${CFN_CHANGE_SET} --stack-name ${SLACK_STACK_NAME}
	sleep 10
	aws cloudformation execute-change-set --change-set-name ${CFN_CHANGE_SET} --stack-name $(SLACK_STACK_NAME)

package-stack:
	mkdir -p /tmp/${DEST}
	aws cloudformation package --template-file ${DEST}cfn_template.yaml --s3-bucket ${S3_BUCKET} --output-template-file /tmp/${DEST}packaged-template.yaml


update-stack: package-stack ## update cfn template
	aws cloudformation create-change-set --change-set-name ${CFN_CHANGE_SET} --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --template-body file:///tmp/${DEST}packaged-template.yaml
	aws cloudformation describe-change-set --change-set-name ${CFN_CHANGE_SET} --stack-name ${STACK_NAME}
	sleep 10
	aws cloudformation execute-change-set --change-set-name ${CFN_CHANGE_SET} --stack-name ${STACK_NAME}

delete-stack: ## cfn delete stack
	aws cloudformation delete-stack --stack-name ${STACK_NAME}

cfn-gitco: ## auto git commit to debut cfn
	git add .
	git commit -m "debug cfn template at ${DATE}"

cfn-watcher: cfn-gitco update-stack ## cfn file watcher

send-deletion: ## send deletion message
	aws sns publish --topic-arn "$(SNS_SEND_DELETION)" --message "launch stack termination"

send-cancelation: ## send cancelation message
	aws sns publish --topic-arn "$(SNS_SEND_CANCELATION)" --message "cancel stack termination"
send-message: ## send cancelation message
	aws sns publish --topic-arn "$(SNS_RCV_MSG)" --message "Message"

subscribe-requestbin: ## receive sns notifications to RequestBin
	aws sns subscribe --topic-arn ${SNS_SEND_DELETION} --protocol https --notification-endpoint ${REQUEST_BIN}
	aws sns subscribe --topic-arn ${SNS_SEND_CANCELATION} --protocol https --notification-endpoint  ${REQUEST_BIN}
	aws sns subscribe --topic-arn ${SNS_RCV_MSG} --protocol https --notification-endpoint  ${REQUEST_BIN}
	aws sns subscribe --topic-arn ${SNS_RCV_DEL_ACT} --protocol https --notification-endpoint  ${REQUEST_BIN}


