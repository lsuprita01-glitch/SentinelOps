
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key or api_key == "PASTE_YOUR_GROQ_KEY_HERE":
    raise ValueError("Groq API key is missing. Check your .env file.")

client = Groq(api_key=api_key)

try:
    print("Connecting to Groq AI...")

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are SentinelOps, an AI cybersecurity "
                    "incident response assistant. Only discuss "
                    "defensive security and safe simulations."
                )
            },
            {
                "role": "user",
                "content": (
                    "A simulated server experienced 45 failed "
                    "login attempts in 3 minutes. Suggest three "
                    "defensive actions."
                )
            }
        ],
        temperature=0.2,
        max_completion_tokens=500
    )

    print("\nSENTINELOPS AI RESPONSE:\n")
    print(response.choices[0].message.content)

    print("\nSUCCESS! Groq is connected.")

except Exception as error:
    print("Groq connection failed:", error)

finally:
    client.close()
