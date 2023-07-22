from server import Chatbot
from classifier import Classifier
import json

def lambda_handler(event, context):
    path: str = event["requestContext"]["http"]["path"]
    if path == "/":
        bot: Chatbot = Chatbot()
        reply = bot.start_chat()
    elif path == "/reply":
        body = json.loads(event["body"])
        message: str = body["message"]
        if "context" not in body:
            body["context"] = []
        context = body["context"]

        classifier = Classifier("rules.csv")

        bot: Chatbot = Chatbot(context, classifier=classifier)
        reply = bot.send_message(message)

        if len(bot.messages_history) > 10:
            scores = bot.evaluate()
            # TODO generate unique ID for every session in start_chat, then pass it in /reply
            with open("/tmp/evaluation.json", "wt") as f:
                f.write(scores)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"reason": "invalid path " + path}),
        }
    return {
        "statusCode": 200,
        "body": json.dumps(
            {"reply": reply, "context": list(bot.messages_history)}
        ),
    }


if __name__ == "__main__":
    dummy_request = {
        "requestContext": {
            "http": {
                "path": "/",
            }
        }
    }
    while True:
        resp = json.loads(lambda_handler(dummy_request, None)["body"])
        print(resp["reply"])
        message = input(">>> ")
        dummy_request = {
            "requestContext": {"http": {"path": "/reply"}},
            "body": json.dumps({"message": message, "context": resp["context"]}),
        }
