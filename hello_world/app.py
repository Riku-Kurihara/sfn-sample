import json
import time


def lambda_handler(event, context):
    # 35秒待機する
    time.sleep(35)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
            }
        ),
    }
