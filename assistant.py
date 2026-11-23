from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    client = OpenAI(
        base_url=os.getenv("BASE_URL"),
        api_key=os.getenv("API_KEY")
    )

    print("="*40)
    print("         My AI Assistant")
    print("="*40)

    messages = []

    while True:
        user_input = input("\nYou (Ask a question or type 'quit' to exit): ")
        messages.append({"role": "user", "content": user_input})

        if user_input.lower() == "quit":
            print("\nAI: Goodbye! Have a great day.")
            break

        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages
        )

        ai_reply = response.choices[0].message.content

        print(f"\nAI: {ai_reply}")
        messages.append({"role": "assistant", "content": ai_reply})

        # print("\n----------Conversation History----------")
        # for message in messages:
        #     print(f"{message['role'].title()}: {message['content']}")
        # print("------------------------------------------")

    
if __name__ == "__main__":
    main()