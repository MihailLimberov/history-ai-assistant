import openai
from groq import Groq
from abc import ABC, abstractmethod
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

class AgentBase(ABC):
    def __init__(self,name,max_retries=2,verbose=True):
      self.name = name
      self.max_retries = max_retries
      self.verbose = verbose

    @abstractmethod
    def execute(self,*args,**kwargs):
        pass

    def call_openai(self,messages,temperature=0.5,max_tokens=350):
        retries = 0
        while retries < self.max_retries:
            try:
                if self.verbose:
                    logger.info(f"[{self.name}] sends message to OpenAI")
                    for msg in messages:
                         logger.debug(f" {msg['role']}: {msg['content']}")
                response = client.chat.completions.create(
                    model = "llama-3.3-70b-versatile",
                    messages= messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                reply = response.choices[0].message.content
                if self.verbose:
                    logger.info(f"[{self.name} received response: {reply}]")
                return reply
            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] error During OpenAI call: {e}.Retry {retries}/{self.max_retries}")
        raise Exception(f"[{self.name}] Failed to get response from OpenAI after {self.max_retries} retries.")
         
