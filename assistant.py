from openai import OpenAI
from dotenv import load_dotenv
from tool_manager import execute_tool
from tools import read_text_file
from retriever import load_documents, create_embedding
from similarity import cosine_similarity
import os

load_dotenv()

def main():
  client = OpenAI(
     base_url=os.getenv("BASE_URL"),
     api_key=os.getenv("API_KEY")
     )
  
  documents = load_documents()
  documents_embeddings = {}
  for filename, content in documents.items():
        documents_embeddings[filename] = create_embedding(content)

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
      transformed_user_input = user_input.lower()

      if transformed_user_input == "quit":
        print("\nAI: Goodbye! Have a great day.")
        break

      if transformed_user_input.startswith("what"):
          print("*"*40)
          print("I'll use RAG to answer your questions in this session!")
          print("*"*40)
          question_embedding = create_embedding(transformed_user_input)

          best_score = -1
          best_document = None

          for filename, embedding in documents_embeddings.items():
              score = cosine_similarity(question_embedding, embedding)
              if score > best_score:
                  best_score = score
                  best_document = filename

          context = documents[best_document]
          prompt = f"""
          Answer the question using only the following information.
          Context: {context}
          Question: {transformed_user_input}
          """

          response = client.chat.completions.create(
              model=os.getenv("CHAT_MODEL"),
              messages=[
                {"role": "system", "content": "Answer only from the provided context."},
                {"role": "user", "content": prompt}
                ]
          )
          print(f"\nAI: {response.choices[0].message.content}")
          continue

      if transformed_user_input.startswith("summarize"):
          filename = transformed_user_input[10:].strip()
          file_content = read_text_file("data/"+filename)

          prompt = f"""
          Summarize the following document.
          Document: {file_content}
          """

          response = client.chat.completions.create(
                    model=os.getenv("CHAT_MODEL"),
                    messages=[
                        {"role": "system", "content": roles.get(choice, "You're a helpful AI Assistant.")},
                        {"role": "user", "content": prompt}
                    ]
          )
          print(response.choices[0].message.content)
          continue

      if transformed_user_input.startswith("ask"):
          splitted_user_input = transformed_user_input.split(maxsplit=2)
          file_content = read_text_file("data/"+splitted_user_input[1])
          question = splitted_user_input[2]
          
          prompt = f"""
          You are given a document. Answer the user's question 
          using only the information present in the document.
          If the answer is not available, say:
          'I couldn't find that information in the document.'
          Document: {file_content}
          Question: {question}
          """

          response = client.chat.completions.create(
                    model=os.getenv("CHAT_MODEL"),
                    messages=[
                        {"role": "system", "content": roles.get(choice, "You're a helpful AI Assistant.")},
                        {"role": "user", "content": prompt}
                    ]
          )
          print(response.choices[0].message.content)
          continue


      tool_result = execute_tool(user_input)
      if tool_result:
          print(f"\nAI: {tool_result}")
          continue

      messages.append({"role": "user", "content": user_input})

      response = client.chat.completions.create(
          model=os.getenv("CHAT_MODEL"),
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