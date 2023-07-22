from typing import Tuple, List
import openai
from transformers import (
    RobertaTokenizerFast,
    TFRobertaForSequenceClassification,
    pipeline,
)
from collections import deque
import os

openai.api_key = os.getenv("API_KEY")

class OpenAIBot:
    def __init__(self, prompts: List[str] = [], max_messages_size: int = 20):
        self.prompts = prompts
        self.prompt_messages = deque(list(map(lambda s: {"role": "system", "content": s}, self.prompts)))
        self.MAXLEN = max_messages_size * 2
        self.messages_history = deque([], self.MAXLEN)

    def ask_for_reply(self, message=None):
        if message is not None:
            self.messages_history.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=list(self.prompt_messages + self.messages_history)
        )
        reply = response.choices[0].message
        self.messages_history.append({"role": "assistant", "content": reply})
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
    def __init__(self, max_messages_size: int = 20):
        PROMPTS: Tuple[str] = (
            "Description: You are a digital psychology assistant from a company named 'Warm' named 'GoodFriend'. Your goal is to get information from me by doing a conversation with me.",
            "Persona: You are a sociably and friendly Indonesian. ALWAYS speak Indonesian at any time. Don't be to stiff, feel free use some Indonesian slang like 'nih', 'kok', 'iyaa', 'banget', etc.",
            "RULE: Do not give a long reply. You are the psychologist, not the patient. In general try not to give more than 3 sentences.",
            "Task: Retrieve these informations from your patient:\nFaintness or dizziness\nPains in the heart or chest\nNausea or upset stomach\nTrouble getting your breath.",
            "Scope: The scope of your questions should be in the last 7 days",
            "RULE: if patient don't give useful answer, DO NOT REINTRODUCE YOURSELF. instead, ask them open questions",
            "RULE: Don't give all question at once and don't directly ask them. When you have all the information, directly output the result using this tag <OUTPUT>result</OUTPUT>",
        )
        super().__init__(PROMPTS, max_messages_size)

    def start_chat(self):
        return self.ask_for_reply()

    def send_message(self, message: str) -> str:
        return self.ask_for_reply(message)
