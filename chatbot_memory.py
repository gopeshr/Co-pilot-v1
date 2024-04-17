from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatCohere
import os

os.environ['COHERE_API_KEY'] = "HnNAY4N9Q3kmCRY6pJOzOXUbtMUopHW03MLp55zp"

template = """You are a teacher in physics for High School student. Given the text of question, it is your job to write a answer that question with example.
{chat_history}
Human: {question}
AI:
"""
prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=template)
memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm = ChatCohere(model="command", temperature=0.5),
    prompt=prompt_template,
    verbose=True,
    memory=memory,
)

llm_chain.predict(question="What is the formula for Gravitational Potential Energy (GPE)?")

result = llm_chain.predict(question="What was the previous question?")
print(result)

while True:
    query = input("YOU: ")
    if query == "quit":
        break
    else:
        response = llm_chain.predict(question = query)
        print(f'AI: {response}')
