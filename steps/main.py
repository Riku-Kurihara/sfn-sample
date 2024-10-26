import json
import os
import uuid

import boto3


def hello_handler(body):
    sfn = boto3.client("stepfunctions")

    state_machine_arn = os.environ["STATE_MACHINE_ARN"]
    execution_id = str(uuid.uuid4())

    try:
        response = sfn.start_execution(
            stateMachineArn=state_machine_arn,
            name=execution_id,  # 実行名として execution_id を使用
            input=json.dumps(body),
        )

        return {
            "statusCode": 202,
            "body": json.dumps(
                {
                    "executionId": execution_id,
                    "executionArn": response["executionArn"],
                    "message": "Processing started",
                }
            ),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def check_status_handler(body):
    sfn = boto3.client("stepfunctions")

    execution_arn = body["executionArn"]

    try:
        response = sfn.describe_execution(executionArn=execution_arn)

        if response["status"] == "SUCCEEDED":
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {"status": "completed", "result": json.loads(response["output"])}
                ),
            }
        elif response["status"] == "RUNNING":
            return {"statusCode": 202, "body": json.dumps({"status": "processing"})}
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"status": "failed", "error": response["status"]}),
            }
    except sfn.exceptions.ExecutionDoesNotExist:
        return {"statusCode": 404, "body": json.dumps({"error": "Execution not found"})}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


handler_map = {
    "/api/hello": hello_handler,
    "/api/check-step": check_status_handler,
}


def handler(event, context):

    # リクエストボディを取得
    body = json.loads(event["body"])
    path = event["path"]
    handler = handler_map[path]
    return handler(body)
