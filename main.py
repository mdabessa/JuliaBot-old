import psycopg2, discord
from random import randint, choice
from modules.base import *
from modules.commands import *
from modules.events import *


class botclient(discord.Client):
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(f'{command.prefix}help'))
        print(f'{self.user} logou em {len(self.guilds)} grupos!')

        for guild in self.guilds:
            nick = guild.me.nick
            if nick == None:
                continue
            else:
                await guild.me.edit(nick=None)
        
        print('Ready!')


    async def on_message(self, message):
        global mutes
        if message.author == self.user:
            return
        

        #add (pointsqt) points every (pointstime) seconds
        pointstime = 300
        pointsqt = 100

        if timer.timer('point_time_'+str(message.guild.id), pointstime, recreate=1):
            for member in message.guild.members:
                if member.status == 'offline':
                    continue
                
                addpoints(member.id,message.guild.id,pointsqt, connection)


        if str(message.author.id)+str(message.channel.id) in mutes:
            if timer.timer(str(message.author.id)+str(message.channel.id),0):
                mutes.remove(str(message.author.id)+str(message.channel.id))
            else:
                await message.delete()
                return
        

        if timer.timer('event_time_'+str(message.guild.id), randint(1000,10000), recreate=1) == True:
            eve = choice(event.events)
            eve.clear()
            await eve.create([message.channel])
                     

        try:
            print(f'{message.guild} #{message.channel} //{message.author} : {message.content}')

        
            if message.content[0:len(command.prefix)] == command.prefix:
                content = message.content[len(command.prefix):]
                await command.trycommand(message, content, connection, masterid, self)
 

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
        for guild in self.guilds:
            nick = guild.me.nick
            if nick == None:
                continue
            else:
                await guild.me.edit(nick=None)
                


connection = psycopg2.connect(db_url, sslmode='require')


intents = discord.Intents.all()
bot = botclient(intents=intents)
bot.run(token)