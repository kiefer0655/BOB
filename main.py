from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import re

import tts_handle

from confighandle import CONFIG

using_model = CONFIG["LLM"]["model"]
port = CONFIG["LLM"]["port"]
streaming = CONFIG["LLM"]["streaming"]


model = OllamaLLM(model=using_model
                  ,base_url=f"http://localhost:{port}")

template = """
{question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

#prewarm

print(f"loading {using_model}")
chain.invoke({"question":"."})
print(f"{using_model} launched")

while True:

    question = input("Question: ")
    if question == "q":
        break

    tts_buffer = ""

    for chunk in chain.stream({"question": question}):
        
        print(chunk, end="", flush=True)
        
        tts_buffer += chunk
        if re.search(r"[.!?]\s$", tts_buffer):
            tts_handle.speak(tts_buffer.strip())
            tts_buffer = ""
    
    tts_handle.speak(tts_buffer.strip())

    print()