from server import Chatbot
from classifier import Classifier
import json

THRESHOLD = 20


def lambda_handler(event, context):
    path: str = event["requestContext"]["http"]["path"]
    category = None
    scores = None

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

        if body.get("counter", 0) % 5 == 4:
            try:
                scores = json.loads(bot.evaluate())
                print(scores)
                scores = {
                    k: v
                    for k, v in sorted(scores.items(), key=lambda item: -item[1])
                    if v > 0
                }
                total_score = sum(filter(lambda v: v > 1, scores.values()))
                print(total_score)
                if total_score > THRESHOLD:
                    category, scores = classifier.classify(scores)
                    scores = {k: v for k, v in scores.items() if v > 1}
            except Exception as e:
                print(e)
                pass
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"reason": "invalid path " + path}),
        }
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "reply": reply,
                "context": list(bot.messages_history),
                "evaluation": {
                    "finish": category is not None,
                    "category": category,
                    "scores": scores,
                },
            }
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
        if resp["evaluation"]["finish"]:
            print(resp["evaluation"])
        print(resp["reply"])
        message = input(">>> ")
        dummy_request = {
            "requestContext": {"http": {"path": "/reply"}},
            "body": json.dumps(
                {"message": message, "context": resp["context"], "counter": 5}
            ),
        }
