import json
import time


def lambda_handler(event, context):
    print("★★★★★")
    print(event)
    # 35秒待機する
    time.sleep(40)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "good morning world",
            }
        ),
    }
