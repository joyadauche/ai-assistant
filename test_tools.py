from tools import (
  get_current_time, 
  roll_dice,
  generate_password,
  read_text_file)
from retriever import load_documents, retrieve

print(get_current_time())
print(roll_dice())
print(generate_password())
print(read_text_file("data/notes.txt"))
print(read_text_file("data/shopping_list.txt"))

documents = load_documents()
for filename, content in documents.items():
  print(f"{filename}: {content}")
  print("-"*40)

print(retrieve("Python"))