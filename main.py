import os
import httpx

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


def main():
    print("Hello from langchain-course!")
    information = "India"
    prompt = PromptTemplate(
        input_variables=["information"],
        template="What is the capital of {information}?",
    )
    # Test-only: disable TLS cert verification.
    insecure_http_client = httpx.Client(verify=False)
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        http_client=insecure_http_client,
    )
    chain = prompt | model
    response = chain.invoke(prompt.format(information=information))
    print(response.content)


if __name__ == "__main__":
    main()
