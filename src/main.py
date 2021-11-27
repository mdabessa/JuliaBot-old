from sys import path
path.insert(0, '/src')

import psycopg2
from discord import Intents
from os import environ
from environs import Env
import modules.entity as entity
from commands import *
from scripts import *


env = Env()
env.read_env()

db_URL = environ['DATABASE_URL']
token = environ['DiscordToken']
master_id = int(environ['master_id'])
log_chat = bool(int(environ['log_chat']))

connection = psycopg2.connect(db_URL, sslmode='allow')

intents = Intents.all()
bot = entity.Client(db_connection=connection, master_id=master_id, intents=intents, print_chat=log_chat)
bot.run(token)
