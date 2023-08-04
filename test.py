import config
import telebot
from aiohttp import web
import ssl

WEBHOOK_LISTEN = "0.0.0.0"
WEBHOOK_PORT = config.PORT

WEBHOOK_SSL_CERT = config.CERTIFICATE_PATH
WEBHOOK_SSL_PRIV = config.PRIVATE_KEY_PATH

API_TOKEN = config.TOKEN
bot = telebot.TeleBot(API_TOKEN)

app = web.Application()

# process only requests with correct bot token
async def handle(request: web.Request ) -> web.Response:
    print("handle")
    request_body_dict = await request.json()
    update = telebot.types.Update.de_json(request_body_dict)
    bot.process_new_updates([update])
    return web.Response()

async def handle2(request: web.Request ) -> web.Response:
    print("handle2")
    request_body_dict = await request.json()
    update = telebot.types.Update.de_json(request_body_dict)
    bot.process_new_updates([update])
    return web.Response(text="Hello, world")


app.add_routes([web.get("/", handle),web.post("/", handle2)])

#app.router.add_post("/", handle)

#app.router.add_get("/", handle2)

help_string = []
help_string.append("*Some bot* - just a bot.\n\n")
help_string.append("/start - greetings\n")
help_string.append("/help - shows this help")

# - - - messages

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Ololo, I am a bot")

@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(message.chat.id, "".join(help_string), parse_mode="Markdown")

# - - -

context = ssl.SSLContext()
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

# start aiohttp server (our bot)
web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=WEBHOOK_PORT,
    ssl_context=context,
)
