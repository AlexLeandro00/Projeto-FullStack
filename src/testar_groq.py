from dotenv import load_dotenv
from groq import Groq
import os


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

reposta = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Diga oi em uma frase curta"}
    ]
)
print(reposta.choices[0].message.content)