import json
import os
import uuid

import boto3


def start_step_handler(body, type):
    sfn = boto3.client("stepfunctions")

    state_machine_arn = os.environ["STATE_MACHINE_ARN"]
    execution_id = str(uuid.uuid4())

    body = {"type": type, "data": body}

    try:
        response = sfn.start_execution(
            stateMachineArn=state_machine_arn,
            name=execution_id,
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
    "/api/hello": start_step_handler,
    "/api/check-step": check_status_handler,
}


def handler(event, context):

    # リクエストボディを取得
    body = json.loads(event["body"])
    path = event["path"]
    handler = handler_map[path]
    if path != "/api/check-step":
        type = "helloWorld" if path == "/api/hello" else "goodMorning"
        return handler(body, type)
    else:
        return handler(body)
