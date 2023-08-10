'''
Test Telegram Webhook.

Copyright (C) 2023 Dr. Sergey Kolevatov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

'''

import config
import telebot
from aiohttp import web
import ssl

WEBHOOK_LISTEN = "0.0.0.0"

bot = telebot.TeleBot( config.TOKEN )

app = web.Application()

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
help_string.append("*Test bot* - just a bot.\n\n")
help_string.append("/start - greetings\n")
help_string.append("/help - shows this help")

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello, I am a bot")

@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(message.chat.id, "".join(help_string), parse_mode="Markdown")

context = ssl.SSLContext()
context.load_cert_chain( config.CERTIFICATE_PATH, config.PRIVATE_KEY_PATH )

web.run_app(
    app,
    host=WEBHOOK_LISTEN,
    port=config.PORT,
    ssl_context=context,
)
