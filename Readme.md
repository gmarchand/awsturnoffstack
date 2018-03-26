# Turn off Stack

## Introduction
Read docs/intro.md

### How to develop

Init env variables with a `.env` file
git sta
```
S3_BUCKET=
SNS_SEND_DELETION=
SNS_SEND_CANCELATION=
SNS_RCV_MSG=
SNS_RCV_DEL_ACT=
REQUEST_BIN=
```

`make help`

if you want to deploy the slack stack

`make update-stack DEST=slack/ STACK_NAME=switchoffslack`

