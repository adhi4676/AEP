import os
import groq

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    raise ValueError("GROQ_API_KEY not found!")

client = Groq(api_key=api_key)

print("Groq client initialized successfully!")

MAX_HISTORY_MESSAGES = 5
system_prompt = """
# Identity

You are the Business Operations AI Assistant.

You help small and medium-sized software companies
identify and manage business opportunities.

# Responsibilities

1. Identify potential customer segments.
2. Analyze customer problems.
3. Suggest lead-generation strategies.
4. Prepare personalized business communications.
5. Help organize business workflows.

# Communication Rules

1. Be professional and concise.
2. Use headings and bullet points where appropriate.
3. Give practical recommendations.
4. Ask clarifying questions when information is missing.
5. Never invent company research or claim external actions.

# Important Limitations

You currently do not have access to:
- Internet search.
- Company databases.
- Email accounts.
- External business systems.

If a task requires these capabilities,
explain that you cannot execute it yet.
"""

print("\nBusiness Operations AI Assistant")
print("Type 'exit' to quit.\n")

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    
]
def remove_failed_user_message(messages):
    if messages and messages[-1]["role"] == "user":
        messages.pop()

def trim(messages):
    system_message = messages[0]

    conv = messages[1:]

    conv = conv[-MAX_HISTORY_MESSAGES:]

    if conv:
        if conv[0]["role"]=="assistant":
            conv=conv[1:]

    return [system_message] + conv

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Assistant: Goodbye!")
        break

    if not user_input:
        continue

    if user_input.lower() == "reset":
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        print("Assistant: Conversation reset!\n")
        continue

    messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )
    messages.append({
    "role": "user",
    "content": user_input
    })

    messages = trim(messages)
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            max_completion_tokens=300,
            stream=True
        )

        answer = ""

        try:
            for chunk in response:

                if chunk.choices:
                    content = chunk.choices[0].delta.content

                    if content:
                        print(content, end="", flush=True)
                        answer += content

        except KeyboardInterrupt:
            print("\nGeneration interrupted.")
        
        if answer:
            messages.append(
                {
                    "role":"assistant",
                    "content":answer
                }
            )
        messages = trim(messages)
    except groq.AuthenticationError:
        remove_failed_user_message(messages)
        print("\nAuthentication failed. Check your API key.")

    except groq.RateLimitError:
        remove_failed_user_message(messages)
        print("\nRate limit reached. Please wait.")

    except groq.APITimeoutError:
        remove_failed_user_message(messages)
        print("\nRequest timed out.")

    except groq.APIConnectionError:
        remove_failed_user_message(messages)
        print("\nConnection problem. Check your internet.")

    except groq.APIStatusError as e:
        remove_failed_user_message(messages)
        print(f"\nAPI error. Status code: {e.status_code}")

    except groq.APIError as e:
        remove_failed_user_message(messages)
        print(f"\nGroq error: {e}")

    except Exception as e:
        remove_failed_user_message(messages)

        print("\nAn unexpected error occurred.")
        print("Error type:", type(e).__name__)
        print("Error details:", e)
    
