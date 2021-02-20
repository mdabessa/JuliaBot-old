import sys
sys.path.insert(0, '/src')

import psycopg2, discord, traceback
from os import environ
from environs import Env
from random import randint, choice
import modules.database as db
import modules.entity as entity
from commands import *
from events import *


class botclient(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(f'{len(self.guilds)} servers!'))
        
        for guild in self.guilds:
            if db.getserver(guild.id, connection) == None:
                db.addserver(guild.id, connection)

        entity.command.newcategory('personalizado', ':paintbrush:Personalizados.')

        print(f'{self.user} esta logado em {len(self.guilds)} grupos!')
        print('Pronto!')


    async def on_message(self, message):
        if message.author == self.user:
            return

        #add (pointsqt) points every (pointstime) seconds
        pointstime = 300
        pointsqt = 100

        if entity.timer.timer('point_time_'+str(message.guild.id), pointstime, recreate=1):
            for member in message.guild.members:
                if member.status == 'offline' or (member.bot == True and member.id != self.user.id):
                    continue
                
                db.addpoints(member.id,message.guild.id,pointsqt, connection)


        if str(message.author.id)+str(message.channel.id) in entity.mutes:
            if entity.timer.timer(str(message.author.id)+str(message.channel.id),0):
                entity.mutes.remove(str(message.author.id)+str(message.channel.id))
            else:
                await message.delete()
                return
        

        if entity.timer.timer('event_time_'+str(message.guild.id), randint(1000,10000), recreate=1) == True:
            eve = choice([i for i in entity.event.events if i.loop_event_create])
            eve.clear(str(message.guild.id))
            await eve.create([message.channel], str(message.guild.id))
                     

        try:
            print(f'{message.guild} #{message.channel} //{message.author} : {message.content}')

            server = db.getserver(message.guild.id, connection)
            
            prefix = server['prefix']
            channel = server['commandchannel']


            if channel == None:
                pass
            elif self.get_channel(int(channel)) == None:
                db.editserver(message.guild.id, connection, 'commandchannel', None)
                channel = None

            if message.content == f'<@!{self.user.id}>':
                helpstr = f'{prefix}help para lista de comandos.'
                

                if channel != None:
                    helpstr += f'\nCanal de comandos: <#{channel}>'

                await message.channel.send(helpstr)
                return


            if message.content[0:len(prefix)] == prefix:
                if channel == None:
                    pass
                elif int(channel) != message.channel.id:
                    return

                content = message.content[len(prefix):]
                await entity.command.trycommand(message, content, connection, masterid, self)
 

            for eve in entity.event.events:
                if eve.trigger == 'message':
                    await eve.execute([message, connection], str(message.guild.id))

        except Exception as e:
            print(e)
            traceback.print_exc()
        

    async def on_reaction_add(self, reaction, user):
        if user == self.user:
            return

        for eve in entity.event.events:
            if eve.msgvalidation(reaction.message, str(reaction.message.guild.id)) and eve.trigger == 'react':
                await eve.execute([user,reaction.emoji, connection], str(reaction.message.guild.id))

    async def on_guild_join(self, guild):
        if db.getserver(guild.id, connection) == None:
                db.addserver(guild.id, connection)


env = Env()
env.read_env()

db_url = environ['DATABASE_URL']
token = environ['DiscordToken']
masterid = int(environ['master_id'])

connection = psycopg2.connect(db_url, sslmode='require')

intents = discord.Intents.all()
bot = botclient(intents=intents)
bot.run(token)