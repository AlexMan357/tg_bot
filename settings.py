import os
from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr


load_dotenv()


class BotSettings(BaseSettings):
    token: SecretStr = os.getenv('TOKEN', None)
