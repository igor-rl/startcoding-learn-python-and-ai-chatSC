# ==========================================================
# Estudo de Caso 1 - ChatSC - Criando Seu Assistente de Programação Python, em Python
# ==========================================================

# Importa módulo para interagir com o sistema operacional
import os

# Importa a biblioteca Streamlit para criar a interface web interativa
import streamlit as st

# Importa a classe Groq para se conectar à API da plataforma Groq e acessar o LLM
from groq import Groq

# Importa função para carregar variáveis de ambiente de um arquivo .env
from dotenv import load_dotenv

# ==========================================================
# 🔹 Carrega as variáveis de ambiente do arquivo .env
# ==========================================================
load_dotenv()

# ==========================================================
# 🔹 Configurações da página Streamlit
# ==========================================================
st.set_page_config(
    page_title="ChatSC",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# 🔹 Prompt personalizado que define o comportamento da IA
# ==========================================================
CUSTOM_PROMPT = """
Você é o "ChatSC", um assistente de IA especialista em programação, com foco principal em Python. 
Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:
1.  **Foco em Programação**: Responda apenas a perguntas relacionadas a programação, algoritmos, estruturas de dados, bibliotecas e frameworks. 
    Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é exclusivamente em auxiliar com código.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. 
      O código deve ser bem comentado para explicar as partes importantes.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante 
      para a documentação oficial da Linguagem Python (docs.python.org) ou da biblioteca em questão.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# ==========================================================
# 🔹 Lê a chave da Groq do arquivo .env (se existir)
# ==========================================================
env_api_key = os.getenv("GROQ_API_KEY")

# ==========================================================
# 🔹 Barra lateral
# ==========================================================
with st.sidebar:
    st.title("🤖 ChatSC")
    st.markdown("Um assistente de IA focado em programação Python.")

    # Exibe campo para inserir API Key apenas se não estiver no .env
    if not env_api_key:
        groq_api_key = st.text_input(
            "Insira sua API Key Groq",
            type="password",
            help="Obtenha sua chave em https://console.groq.com/keys"
        )
    else:
        groq_api_key = env_api_key

    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")
    st.markdown("🔗 [StartCoding](https://scoding.vercel.app)")

# ==========================================================
# 🔹 Cabeçalho principal
# ==========================================================
st.title("StartCoding - ChatSC")
st.title("Assistente Pessoal de Programação Python")
st.caption("Faça sua pergunta sobre a Linguagem Python e obtenha código, explicações e referências.")

# ==========================================================
# 🔹 Histórico de mensagens
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 🔹 Inicializa cliente da Groq
# ==========================================================
client = None

if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)
    except Exception as e:
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()
else:
    st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# ==========================================================
# 🔹 Entrada do usuário
# ==========================================================
if prompt := st.chat_input("Qual sua dúvida sobre Python?"):

    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Armazena mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Monta mensagens para envio à API
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}] + st.session_state.messages

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Chama API da Groq
                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model="openai/gpt-oss-20b",
                    temperature=0.7,
                    max_tokens=2048,
                )

                sc_ai_resposta = chat_completion.choices[0].message.content

                # Exibe resposta
                st.markdown(sc_ai_resposta)

                # Salva no histórico
                st.session_state.messages.append({"role": "assistant", "content": sc_ai_resposta})

            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

# ==========================================================
# 🔹 Rodapé
# ==========================================================
st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>ChatSC - Parte Integrante do Curso de Linguagem Python e IA da StartCoding</p>
    </div>
    """,
    unsafe_allow_html=True
)
