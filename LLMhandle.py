from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import re

import tts_handle

from confighandle import CONFIG

class LLM:
    def __init__(self) -> None:
        
        self.using_model    = CONFIG["LLM"]["model"]
        self.port           = CONFIG["LLM"]["port"]

        self.streaming      = CONFIG["LLM"]["streaming"]
        self.withTTS        = CONFIG["TTS"]["Enable"]


        self.model = OllamaLLM(model=self.using_model
                          ,base_url=f"http://localhost:{self.port}")

        template = """{question}"""

        prompt = ChatPromptTemplate.from_template(template)

        self.chain = prompt | self.model

        self.respond = {
                (False, False): self.GetPureTextOutput,
                (True,  False): self.GetPureTextStreamOutput,
                (False, True):  self.GetTTSOutput,
                (True,  True):  self.GetTTSStreamOutput,
            }[(self.streaming, self.withTTS)]

    def PromptLLM(self,text):
        """
        Prompt the LLM with text
        return Single Block Str Output
        """
        try:
            respone = self.chain.invoke({"question":text})
            return respone
        except:
            return "Error! Ollama Not Responing"
    
    def PromptLLMStreaming(self,text):
        """
        Prompt the LLM with text
        return RealTime Streaming iterable Str Output
        """
        try:
            return self.chain.stream({"question": text})
        except:
            return iter(["Error! Ollama Not Responing"])

    def wakeup(self):
        print(f"Waking {self.using_model}")
        self.PromptLLM("")
        print(f"{self.using_model} Waked")

    def GetTTSOutput(self,text):
        """
        Prompt the LLM with text and Get TTS respond
        """
        output = self.PromptLLM(text)
        print(output)
        tts_handle.speak(output)

    def GetTTSStreamOutput(self,text):
        """
        Prompt the LLM with text and Get Streaming TTS respond
        """
        tts_buffer = ""

        for chunk in self.PromptLLMStreaming(text):

            print(chunk, end="", flush=True)
            tts_buffer += chunk
            if re.search(r"[.!?]\s$", tts_buffer):
                tts_handle.speak(tts_buffer.strip())
                tts_buffer = ""

        tts_handle.speak(tts_buffer.strip())
        print()
    
    def GetPureTextOutput(self,text):
        """
        Prompt the LLM with text respond
        """
        output = self.PromptLLM(text)
        print(output)

    def GetPureTextStreamOutput(self,text):
        """
        Prompt the LLM with text and Get Streaming TTS respond
        """
        for chunk in self.PromptLLMStreaming(text):
            print(chunk, end="", flush=True)
        
        print()