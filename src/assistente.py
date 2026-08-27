from dotenv import load_dotenv
from groq import Groq
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Recurso
from logica import calcular_dias_restantes
import os
import json
from logica import calcular_dias_restantes
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
Session = sessionmaker(bind=engine)

ferramentas = [
    {
        "type": "function",
        "function": {
            "name": "cadastrar_recurso",
            "description": "Cadastra um novo recurso doméstico no sistema, com nome, intervalo médio de reposição em dias, e a data da última compra",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {
                        "type": "string",
                        "description": "Nome do recurso doméstico (ex: água, gás, areia de gato)"
                    },
                    "intervalo_medio_dias": {
                        "type": "integer",
                        "description": "De quantos em quantos dias, em média, esse recurso costuma ser reposto"
                    },
                    "data_ultima_compra": {
                        "type": "string",
                        "description": "Data da última compra no formato AAAA-MM-DD. Se o usuário não informar, use a data de hoje"
                    }
                },
                "required": ["nome", "intervalo_medio_dias", "data_ultima_compra"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_dias_restantes",
            "description": "consulta quantos dias faltam para um recurso doméstico específico acabar, baseado no historico de compra",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_recurso": {
                        "type": "string",
                        "description": "Nome do recurso doméstico (ex: água, gás, areia de gato)"
                    }
                },
                "required": ["nome_recurso"]
            }
        }
    }
]


def cadastrar_recurso(nome, intervalo_medio_dias, data_ultima_compra):
    session = Session()
    data_convertida = datetime.strptime(data_ultima_compra, "%Y-%m-%d").date()
    novo_recurso = Recurso(
        nome=nome,
        intervalo_medio_dias=intervalo_medio_dias,
        data_ultima_compra=data_convertida,
        id_contato=None
    )
    session.add(novo_recurso)
    session.commit()
    session.refresh(novo_recurso)
    session.close()
    return {"id": novo_recurso.id, "nome": novo_recurso.nome, "mensagem": "Recurso cadastrado com sucesso!"}


def consultar_dias_restantes(nome_recurso):
    session = Session()
    todos_recursos = session.query(Recurso).all()
    session.close()
    nome_busca = nome_recurso.lower()
    recurso = None
    for r in todos_recursos:
        if nome_busca in r.nome.lower():
            recurso = r
            break
         
    if recurso is None:
        return {"Erro": f"Recurso '{nome_recurso}' não encontrado no banco de dados."}

    dias = calcular_dias_restantes(recurso)
    return {"nome": recurso.nome, "dias_restantes": dias}


def conversar(pergunta_usuario):
    mensagens = [
        {"role": "user", "content": pergunta_usuario}
    ]

    resposta = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=mensagens,
        tools=ferramentas,
        tool_choice="auto"
    )

    mensagem_ia = resposta.choices[0].message

    if mensagem_ia.tool_calls:
        chamada = mensagem_ia.tool_calls[0]
        nome_funcao = chamada.function.name
        argumentos = json.loads(chamada.function.arguments)

        if nome_funcao == "calcular_dias_restantes":
            resultado =  consultar_dias_restantes(argumentos["nome_recurso"])
        elif nome_funcao == "cadastrar_recurso":
            resultado = cadastrar_recurso(
                argumentos["nome"],
                argumentos["intervalo_medio_dias"],
                argumentos["data_ultima_compra"]
            )

        mensagens.append(mensagem_ia)
        mensagens.append({
            "role": "tool",
            "tool_call_id": chamada.id,
            "content": json.dumps(resultado)
        })

        resposta_final = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=mensagens
        )
        return resposta_final.choices[0].message.content

    return mensagem_ia.content


if __name__ == "__main__":
    pergunta = input("Digite sua pergunta: ")
    resposta = conversar(pergunta)
    print(resposta)