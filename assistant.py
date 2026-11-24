from openai import OpenAI
from dotenv import load_dotenv
from tool_manager import execute_tool
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

    roles = {
        "1": "You're a friendly teacher. Explain every concept in simple language with real-life examples.",
        "2": "You're a senior Python Developer. Explain programming concepts clearly and always include Python examples.",
        "3": "You're an experienced travel guide. Recommend places, food, transportation, and travel tips.",
        "4": "You're a motivational coach. Encourage the user and give practical advice with a positive attitude.",
        "5": "You're a professional interviewer. Ask one interview question at a time and provide feedback after each answer.",
        "6": "You're an experienced legal advisor. Explain legal concepts in simple language, but never claim to provide formal legal advice."
    }

    print("\nChoose your assistant:\n")
    print("1. Teacher")
    print("2. Python Expert")
    print("3. Travel Guide")
    print("4. Motivational Coach")
    print("5. Interviewer")
    print("6. Legal Advisor")

    choice = input("\nEnter your Choice: ")

    messages = [
        {"role": "system",
         "content": roles.get(choice, "You're a helpful AI Assistant.")}
    ]

    print("\nHello, I'm ready to help you.\n")
    print("Type 'quit' anytime to exit.\n")

    while True:
        user_input = input("\nYou (Ask a question or type 'quit' to exit): ")

        if user_input.lower() == "quit":
            print("\nAI: Goodbye! Have a great day.")
            break

        tool_result = execute_tool(user_input)
        if tool_result:
            print(f"\nAI: {tool_result}")
            continue

        messages.append({"role": "user", "content": user_input})

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