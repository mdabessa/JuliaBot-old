from sys import path
path.insert(0, '/src')

import psycopg2
from discord import Intents
from os import environ
from environs import Env
import modules.entity as entity
from commands import *
from events import *


env = Env()
env.read_env()

db_url = environ['DATABASE_URL']
token = environ['DiscordToken']
master_id = int(environ['master_id'])

connection = psycopg2.connect(db_url, sslmode='require')

intents = Intents.all()
bot = entity.Client(db_connection=connection, master_id=master_id, intents=intents)
bot.run(token)