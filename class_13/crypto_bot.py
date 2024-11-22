from openai import AzureOpenAI
import os
import requests
import json

client = AzureOpenAI(
    api_key= os.getenv("AZURE_KEY"),
    azure_endpoint= os.getenv("AZURE_ENDPOINT"),
    api_version= "2023-10-01-preview"

)

def get_crypto_price(crypto_name,fiat_currency):


messages = [
    {"role":"user", "content":"Find the current price of ethereum in Euros"}
]

functions = [
    {
    "type": "function",
    "function" : {
        "name":"get_crypto_price",
        "description": "Get prices of cryptocurrency in a specified global currency"
    },
    "parameters":
    {
        "type": "object",
        "properties" :{
            "crypto_name":{
                "type":"string",
                "description": "The name of the crypto currency that I want to look for"
            },
            "fiat_currency": {
                "type": "string",
                "description":"The fiat currency for defining the price of crypto currency"
            }
        },
        "required":["crypto_name","fiat_currency"]
    }
    }

]

response = client.chat.completions.create(
    model="GPT-4",
    messages=messages,
    tools= functions,
    tool_choice= "auto"

)

# if chat-gpt doesnt neet help this will be none, else there will be stuff
gpt_tools=response.choices[0].message.tool_calls
# we want to add response message into chatgpt history so it knows it used a function and is not just confused
response_message = response.choices[0].message


# not none
if gpt_tools:
    available_functions={
        "get_crypto_price": get_crypto_price()
    }

    messages.append(response_message)

    for gpt_tool in gpt_tools:
        function_name=gpt_tool.function.name
        function_to_call = available_functions[function_name]

else:
    print(response.choices[0].message)