from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key=os.getenv("AZURE_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version="2023-10-01-preview"
)

def parse_response(chat_response):
    rap = chat_response.split("ANSWER:")[0]
    chat_response = chat_response.split("ANSWER:")[1]
    body_style = chat_response.split("body_style:")[1]
    header_style = chat_response.split("h1_style:")[1]
    form_style = chat_response.split("form_style:")[1]
    response_style = chat_response.split("response_style:")[1]
    return rap, body_style, header_style, form_style, response_style

def ask_question(question):
    messages = [
        {
            "role": "system",
            "content": """You are a rapper, write me a rap song about the topic I give you. Then at the end of the song, after a - return some CSS styling, in-line HTML, that will encompass the vibe of that rap song. If you are using pictures from somewhere, make sure you use the internet URL, because there are no pictures in this folder. This is my HTML CODE:
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>RAP BOT!</title>
            </head>
            <body style="{{body_style}}">
                <h1 style="{{h1_style}}">RAP IT!</h1>
                <div class="form-div" style="{{form_style}}">
                    <form method="POST">
                        <label>Question:</label>
                        <!-- the double {} pulls the variable from our python script -->
                        <input name="question" type="text" value={{my_question}}><br><br>
                        <input type="submit" value="Submit"><br><br>
                    </form>
                </div>
                <div style="{{response_style}}"><p>{{bot_response}}</p></div>
            </body>
            </html>
            
            Please answer like this so I can parse it properly, and spell everything properly as well:
            ANSWER:
            body_style:
            h1_style:
            form_style:
            response_style:
            """
        },
        {"role": "user", "content": question}
    ]
    
    response = client.chat.completions.create(
        model="GPT-4",
        messages=messages
    )

    rap, body_style, h1_style, form_style, response_style = parse_response(response.choices[0].message.content)

    print("rap")
    print("------")
    print(rap)

    print("body_style")
    print("------")
    print(body_style)

    print("h1")
    print("------")
    print(h1_style)

    print("form")
    print("------")
    print(form_style)

    print("response")
    print("------")
    print(response_style)

    return rap, body_style, h1_style, form_style, response_style
