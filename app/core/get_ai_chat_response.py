import os
from dotenv import load_dotenv
from typing import List
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY2")
genai.configure(api_key=api_key)

class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

def get_gemini_response(messages: List[Message], language="en", context=None):
    history = ""
    for m in messages:
        role = "You" if m.role == "user" else "Assistant"
        history += f"{role}: {m.content}\n"

    context_line = f"\nContext: {context}" if context else ""

    prompt = f"""
You are an intelligent farming assistant.
Answer in clear, helpful, and localized language ({language}).{context_line}

Conversation so far:
{history}

Now continue the conversation based on the last question.

After your direct answer, return exactly 3 suggested follow-up questions the user might ask or should know.

Use the format below (exactly):
[Your answer text]

---suggestions---
- Question 1
- Question 2
- Question 3
"""

    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt).text
    print("Response: \n", response)

    if '---suggestions---' in response:
        reply, suggestion_block = response.split('---suggestions---', 1)
        suggestions = [line.strip("- ").strip() for line in suggestion_block.strip().splitlines() if line.strip()]
    else:
        reply = response.strip()
        suggestions = []

    return reply.strip(), suggestions



# Test case
if __name__ == "__main__":
    test_messages = [
        Message(role="user", content="Is there any cure for cassava mosaic disease?"),
        Message(role="Assistant", content="Unfortunately, there's no cure for cassava mosaic disease (CMD) once a plant is infected.  The virus persists in the plant's system.  Management focuses on prevention and minimizing the impact through resistant varieties and good farming practices."),
        Message(role="user", content="What cultural practices can help reduce the spread of CMD?"),
    ]

    reply, suggestions = get_gemini_response(messages=test_messages)

    print(" AI Reply:\n")
    print(reply)
    print("\n Suggested Questions:")
    for s in suggestions:
        print("-", s)
