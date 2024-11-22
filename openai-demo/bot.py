from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key=os.getenv("AZURE_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version="2023-10-01-preview"
)

def parse_response(chat_response):
    try:
        # Split the response into the rap and styles
        rap, styles = chat_response.split("ANSWER:")
        
        # Extract each style by splitting on the specific keys
        body_style = styles.split("body_style:")[1].split("h1_style:")[0].strip().strip('"')
        h1_style = styles.split("h1_style:")[1].split("form_style:")[0].strip().strip('"')
        form_style = styles.split("form_style:")[1].split("response_style:")[0].strip().strip('"')
        response_style = styles.split("response_style:")[1].split("animations:")[0].strip().strip('"')
        animations = styles.split("animations:")[1].strip()

        # Return the rap and all styles as separate values
        return rap.strip(), body_style, h1_style, form_style, response_style, animations
    except Exception as e:
        raise ValueError(f"Error parsing response: {e}")

def ask_question(question):
    messages = [
        {
            "role": "system",
            "content": """
            You are a rapper. Write me a rap verse based on the topic I give you. After the rap, provide CSS styling that matches the vibe of the rap. Follow these exact rules:

            1. Your response must start with a rap verse.
            2. After the verse, provide an `ANSWER:` section in this strict format:
            ANSWER:
            body_style: "..."
            h1_style: "..."
            form_style: "..."
            response_style: "..."
            animations: "..."

            3. Each style must only contain CSS for the specified placeholder:
            - `body_style`: Styling for the `<body>` element.
            - `h1_style`: Styling for the `<h1>` element.
            - `form_style`: Styling for the `<div>` containing the form.
            - `response_style`: Styling for the `<div>` containing the bot's response.
            - `animations`: Full animation definitions using `@keyframes`.

            4. Use animations with `@keyframes`, and make them relevant to the style. Example:
            animations: "@keyframes fadeIn {0% {opacity: 0;} 100% {opacity: 1;}}"

            5. Do not include any additional text, explanations, or comments outside of the rap verse and the `ANSWER:` section.
            """
        },
        {"role": "user", "content": question}
    ]
    
    response = client.chat.completions.create(
        model="GPT-4",
        messages=messages
    )

    rap, body_style, h1_style, form_style, response_style, animations = parse_response(response.choices[0].message.content)

    # Return parsed components
    return rap, body_style, h1_style, form_style, response_style, animations
