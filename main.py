import psycopg2, discord, traceback
from random import randint, choice
from modules.base import *
from modules.commands import *
from modules.events import *


class botclient(discord.Client):
    async def on_ready(self):
        if debug == 1:
            await self.change_presence(activity=discord.Game(f'Debug Mode'))
        else:
            await self.change_presence(activity=discord.Game(f'{len(self.guilds)} servers!'))
        
        for guild in self.guilds:
            if getserver(guild.id, connection) == None:
                addserver(guild.id, connection)

        print(f'{self.user} esta logado em {len(self.guilds)} grupos!')

        print('Pronto!')


    async def on_message(self, message):
        global mutes
        if message.author == self.user:
            return

        if debug == 1 and message.author.id != masterid:
            return
    
        #add (pointsqt) points every (pointstime) seconds
        pointstime = 300
        pointsqt = 100

        if timer.timer('point_time_'+str(message.guild.id), pointstime, recreate=1):
            for member in message.guild.members:
                if member.status == 'offline' or (member.bot == True and member.id != self.user.id):
                    continue
                
                addpoints(member.id,message.guild.id,pointsqt, connection)


        if str(message.author.id)+str(message.channel.id) in mutes:
            if timer.timer(str(message.author.id)+str(message.channel.id),0):
                mutes.remove(str(message.author.id)+str(message.channel.id))
            else:
                await message.delete()
                return
        

        if timer.timer('event_time_'+str(message.guild.id), randint(1000,10000), recreate=1) == True:
            eve = choice([i for i in event.events if i.loop_event_create])
            eve.clear(str(message.guild.id))
            await eve.create([message.channel], str(message.guild.id))
                     

        try:
            print(f'{message.guild} #{message.channel} //{message.author} : {message.content}')

            server = getserver(message.guild.id, connection)
            
            prefix = server['prefix']
            channel = server['commandchannel']


            if channel == None:
                pass
            elif self.get_channel(int(channel)) == None:
                editserver(message.guild.id, connection, 'commandchannel', None)
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
                await command.trycommand(message, content, connection, masterid, self)
 

            for eve in event.events:
                if eve.trigger == 'message':
                    await eve.execute([message, connection], str(message.guild.id))

        except Exception as e:
            print(e)
            traceback.print_exc()
        

    async def on_reaction_add(self, reaction, user):
        if user == self.user:
            return

        for eve in event.events:
            if eve.msgvalidation(reaction.message, str(reaction.message.guild.id)) and eve.trigger == 'react':
                await eve.execute([user,reaction.emoji, connection], str(reaction.message.guild.id))

    async def on_guild_join(self, guild):
        if getserver(guild.id, connection) == None:
                addserver(guild.id, connection)


connection = psycopg2.connect(db_url, sslmode='require')

intents = discord.Intents.all()
bot = botclient(intents=intents)
bot.run(token)