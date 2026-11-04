import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    raise ValueError("GROQ_API_KEY not found!")

client = Groq(api_key=api_key)

print("Groq client initialized successfully!")

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

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        max_completion_tokens=300,
        stream=True
    )

    answer = response.choices[0].message.content

    messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )
    

    finish_reason = response.choices[0].finish_reason

    usage = response.usage

    print("\nAI RESPONSE:")
    print(answer)

    print("\nMETADATA:")
    print("Model:", response.model)
    print("Response ID:", response.id)
    print("Finish reason:", finish_reason)

    print("\nTOKEN USAGE:")
    print("Input tokens:", usage.prompt_tokens)
    print("Output tokens:", usage.completion_tokens)
    print("Total tokens:", usage.total_tokens)
