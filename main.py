import LLMhandle

LLM = LLMhandle.LLM()

LLM.wakeup()

while True:
    question = input("Question: ")
    if question == "q":
        break
    LLM.respond(question)
