import discord
import psycopg2
from random import randint, choice
from exfunc import * 
from commands import *
from events import *


connection = psycopg2.connect(db_url, sslmode='require')


class MyClient(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(f'{prefix}help para ajuda!'))
        print(f'{self.user} logou em {len(self.guilds)} grupos!')
        #Acessar arquivos da guild e funcoes especificas a logar nelas
        for guild in self.guilds:

            #Evitar nicks ofencivos
            nick = guild.me.nick
            if nick == None:
                continue
            else:
                await guild.me.edit(nick=None)
        
        print('Ready')


    async def on_message(self, message):
        global mutes
        if message.author == self.user:
            return
        

        #add points com o tempo
        if timer('pointsloop', pointstime, recreate=True):
            for member in message.guild.members:
                if member.status == 'offline':
                    continue
                
                addpoints(member.id,message.guild.id,pointsqt, connection)


        if str(message.author.id)+str(message.channel.id) in mutes:
            if timer(str(message.author.id)+str(message.channel.id),0):
                mutes.remove(str(message.author.id)+str(message.channel.id))
            else:
                await message.delete()
                return
        

        if timer('event', randint(1000,10000), recreate=1) == True:
            eve = choice(event.events)
            eve.clear()
            await eve.create([message.channel])
                     

        try:
            print(f'{message.guild} #{message.channel} //{message.author} : {message.content}')

            if message.content[0:len(prefix)] == prefix:
                content = message.content[len(prefix):]
                await command.trycommand(message, content, connection, masterid)
                
            for eve in event.events:
                if eve.att == 'message':
                    await eve.execute([message, connection])

        except Exception as e:
            print(e)
        

    async def on_reaction_add(self, reaction, user):
        if user == self.user:
            return
        

        for eve in event.events:
            if eve.msgvalidation(reaction.message) and eve.att == 'react':
                await eve.execute([user,reaction.emoji, connection])



    async def on_member_update(self, before, after):
        #Evitar nicks ofencivos
        for guild in self.guilds:
            nick = guild.me.nick
            if nick == None:
                continue
            else:
                await guild.me.edit(nick=None)
                

intents = discord.Intents.all()
client = MyClient(intents=intents)
client.run(token)