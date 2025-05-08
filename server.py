from flask import Flask, request
from telegram import Bot
from telegram.request import HTTPXRequest
import asyncio

app = Flask(__name__)  # Cria a aplicação Flask (servidor)

# Token e chat_id do seu bot (credenciais do Telegram)
TELEGRAM_BOT_TOKEN = "8039103608:AAGgLFViUVlXnw8dBa1-QE-DbRgV1oCa9iI"
CHAT_ID = "1432718438"

# Cria o objeto do bot com timeout configurado corretamente
request_config = HTTPXRequest(connect_timeout=5.0, read_timeout=5.0)
bot = Bot(token=TELEGRAM_BOT_TOKEN, request=request_config)

@app.route('/alert', methods=['POST'])  # Função chamada sempre que o servidor receber um POST
def alerta():
    # Separa o campo de mensagem do JSON (caso não tenha, usa um texto padrão)
    data = request.get_json()
    mensagem = data.get("mensagem", "⚠️ Alerta de fumaça recebido!")

    print(f"Recebido: {mensagem}")

    # Função assíncrona que envia a mensagem pro Telegram
    async def send_alert():
        try:
            await bot.send_message(chat_id=CHAT_ID, text=f"🚨 {mensagem}")  # Envia a mensagem para o Telegram
            print("✅ Mensagem enviada com sucesso!")
        except Exception as e:
            print("❌ Erro ao enviar mensagem:")
            if "Timed out" in str(e):
                print("⚠️ Timeout: a API do Telegram pode estar lenta ou sem resposta.")
            print(e)

    # Corrige o erro do loop já fechado em requisições sucessivas
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        # Se o loop já estiver em execução, agenda a tarefa
        asyncio.ensure_future(send_alert())
    else:
        # Executa diretamente
        loop.run_until_complete(send_alert())

    return {"status": "Mensagem enviada com sucesso!"}, 200  # Retorna confirmação para o cliente (ESP32, curl, etc.)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Executa em todos os IPs da máquina (essencial para uso em rede)
