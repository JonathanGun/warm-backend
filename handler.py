from server import Chatbot
import json



def lambda_handler(event, context):
    try:
        bot: Chatbot = Chatbot()
        if event['path'] == '/':
            reply = bot.start_chat()
        elif event['path'] == '/reply':
            message: str = json.loads(event["body"])["message"]
            reply = bot.send_message(message)
        else:
            return {
                'statusCode': 400,
                "body": json.dumps({"reason": "invalid path " + event['path']})
            }
        return {
            "statusCode": 200,
            "body": json.dumps({"reply": reply["content"], "context": list(bot.messages_history)}),
        }
    except:
        return {
            "statusCode": 400,
            "body": json.dumps({"reason": '"message" is empty', "event": event}),
        }


if __name__ == "__main__":
    dummy_request = {
        "path": "/",
    }
    while True:
        print(json.loads(lambda_handler(dummy_request, None)["body"])["reply"])
        message = input(">>> ")
        dummy_request = {
            "path": "/reply",
            "body": json.dumps(
                {
                    "message": message
                }
            )
        }
