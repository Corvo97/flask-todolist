import telebot

# Configurações do Telebot
KEY = '6091223597:AAGsA4nzcEwgVMelinpo5pNPAA7S1OSW0A0'
# 1039393330 ID do meu chat privado do Telegram
TELEGRAM_ID = [-4106741130, ] # lista de IDs que recebem notificações do sistema.
bot = telebot.TeleBot(KEY)

# Envio de mensagem via bot (telegram)
def sendBroadcast(msg):
    for i in TELEGRAM_ID:
        bot.send_message(i, msg)

