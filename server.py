from typing import Tuple, List, Any, Optional
import openai
from classifier import Classifier
from collections import deque
import os

openai.api_key = os.getenv("API_KEY")


class OpenAIBot:
    def __init__(
        self,
        prompts: List[str] = [],
        context: List[Any] = [],
        max_messages_size: int = 20,
    ):
        self.prompts = prompts
        self.prompt_messages = deque(
            list(map(lambda s: {"role": "system", "content": s}, self.prompts))
        )
        self.MAXLEN = max_messages_size * 2
        self.messages_history = deque(context, self.MAXLEN)

    def ask_for_reply(
        self,
        message: Optional[str] = None,
        role: str = "user",
        add_to_history: bool = True,
    ):
        new_messages = deque([])
        if message is not None:
            new_messages.append({"role": role, "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=list(self.prompt_messages + self.messages_history + new_messages),
        )
        reply = response.choices[0].message["content"]
        new_messages.append({"role": "assistant", "content": reply})
        if add_to_history:
            self.messages_history.extend(new_messages)
        return reply


class Translator(OpenAIBot):
    def __init__(self):
        PROMPTS: Tuple[str] = (
            "You are given task to translate the next user prompt into English",
        )
        super().__init__(PROMPTS)

    def translate(to_translate: str) -> str:
        return self.ask_for_reply(to_translate)


class Chatbot(OpenAIBot):
    def __init__(
        self,
        context: List[Any] = [],
        max_messages_size: int = 20,
        classifier: Classifier = None,
    ):
        PROMPTS: Tuple[str] = (
            "Description: You are a digital psychology assistant from a company named 'Warm' named 'GoodFriend'. Your goal is to get information from me by doing a conversation with me.",
            "Persona: You are a sociably and friendly Indonesian. ALWAYS speak Indonesian at any time. Don't be to stiff, feel free use some Indonesian slang like 'nih', 'kok', 'iyaa', 'banget', etc.",
            "RULE: Do not give a long reply. You are the psychologist, not the patient. In general try not to give more than 3 sentences.",
            "Scope: The scope of your questions should be in the last 7 days",
            "RULE: if patient don't give useful answer, DO NOT REINTRODUCE YOURSELF. instead, ask them open questions",
            "RULE: Don't give all question at once and don't directly ask them. When you have all the information, directly output the result using this tag <OUTPUT>result</OUTPUT>",
        )
        self.classifier = classifier
        super().__init__(PROMPTS, context, max_messages_size)

    def start_chat(self):
        return self.ask_for_reply()

    def send_message(self, message: str) -> str:
        return self.ask_for_reply(message)

    def evaluate(self):
        PROMPT = (
            "Evaluate previous messages based on these symptomps separated by comma: "
            + ",".join(self.classifier.get_all_symptoms())
            + ". Your task is to give score to ALL symptoms from 0-4 where 0 is 'Not at all', 1 is 'A little bit', 2 is 'Moderately', 3 is 'Quite a bit', and 3 is 'Extremely'. When you're not sure whether you could give the score or not, give -1. Reply in JSON format and sort them by the score DESCENDING. DO NOT change the key from what I give to you."
        )
        return self.ask_for_reply(PROMPT, "system", add_to_history=False)
