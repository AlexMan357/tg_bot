import telebot
from settings import BotSettings

bot_settings = BotSettings()

bot_token = bot_settings.token
bot = telebot.TeleBot(bot_token.get_secret_value(), parse_mode=None)
