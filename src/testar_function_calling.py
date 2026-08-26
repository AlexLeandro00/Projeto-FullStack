from dotenv import load_dotenv
from groq import Groq
import os


load_dotenv()
cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

ferramentas = [
    {
        "type": "function",
        "function": {
            "name": "calcular_dias_restantes_agua",
            "description": "Calcula quantos dias faltam para a água acabar",
            "parameters": {
                "type": "object",
                "properties": {},
        }
    }
}
]

resposta = cliente.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "user", "content": "Quantos dias faltam para a água acabar?"}
    ],
    tools=ferramentas,
    tool_choice="auto"
)
mensagem = resposta.choices[0].message
print("Texto da resposta:", mensagem.content)
print("Ferramenta escolhida:", mensagem.tool_calls)