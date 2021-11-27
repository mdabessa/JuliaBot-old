from random import randint
from time import time
import datetime
import discord
import modules.database as db
import modules.entity as entity
import modules.utils as utils


category = 'Core'
entity.Command.newcategory(category, ':brain:Core.')


async def _help(message, commandpar, bot): 
    if commandpar == None:
        prefix = db.getserver(message.guild.id, bot.db_connection)['prefix']
        emb = discord.Embed(title='Lista de Comandos', description=f'{prefix}help `comando`', color=bot.color)

        commands = entity.Command.getallcommands(message.guild.id, bot.db_connection)
        categories = entity.Command.getcategories()
        
        count = 0
        for c in categories:
            if c[2] == False:
                continue
            
            if len(entity.Command.getcommandsbycategory(c[0], message.guild.id, bot.db_connection)) == 0:
                continue

            
            text = ''
            for cmd in commands:
                if cmd['category'] == c[0]:
                    text += f'[`{cmd["name"]}`](https://www.google.com "{cmd["description"]}") '
                
            count =+ 1
            emb.add_field(name=c[1], value=text, inline=True)

        for i in range(0, count%3):
            emb.add_field(name='** **', value='** **', inline=True)

        await message.channel.send(embed=emb)

    else:
        cmd = entity.Command.getcommand(message.guild.id, commandpar, bot.db_connection)
        prefix = db.getserver(message.guild.id, bot.db_connection)['prefix']
        if cmd != None:
            par = prefix + cmd['name'] + ' '
            for i in cmd['args']:
                par += f'`{i[0]}`{i[1]} '
            
            aliases = ''
            for i in cmd['aliases']:
                aliases += f'`{i}` '

            if cmd['price'] == 0:
                valor = 'Grátis.'
            else:
                valor = cmd['price']

            if cmd['permission'] == 0:
                perm = 'Livre.'
            elif cmd['permission'] == 1:
                perm = 'Apenas admins.'
            else:
                perm = 'DEBUG.'

            emb = discord.Embed(title=f'{prefix}{cmd["name"]}'.upper(), color=bot.color)

            emb.add_field(name='Descrição:', value=cmd['description'], inline=False)
            if cmd['args'] != []:
                emb.add_field(name='Parametros:', value=par, inline=False)
            emb.add_field(name='Valor:', value=valor, inline=False)
            emb.add_field(name='Categoria:', value=cmd['category']+'.', inline=False)
            if cmd['aliases'] != []:
                emb.add_field(name='Aliases:', value=aliases, inline=False)
            emb.add_field(name='Nivel de Permissão:', value=perm, inline=False)

            await message.channel.send(embed=emb)
        else:
            raise entity.CommandError(f'Nenhum comando com o nome {commandpar} existe!')
entity.Command(name='help', func=_help, category=category, desc='Listar todos os comandos e suas descrições.', aliases=['ajuda', 'h'], args=[['comando', '']])


async def getprefix(message, commandpar, bot):
    prefix = db.getserver(message.guild.id, bot.db_connection)['prefix']
    await message.channel.send(f'O prefixo do servidor é: `{prefix}`')
entity.Command(name='prefix', func=getprefix , category=category, desc=f'Retorna o prefixo do bot no servidor.', aliases=['prefixo'])


async def ping(message, commandpar, bot):
    t = time()
    m = await message.channel.send(f'Ping!')
    t = int((time() - t)*1000)

    await m.edit(content=f'Pong!  `{t}ms`')
entity.Command(name='ping', func=ping , category=category, desc=f'Retorna a latência do bot.', aliases=['latency', 'latencia'])


async def remindme(message, commandpar, bot):
    if commandpar == None:
        raise entity.CommandError('Você precisa especificar quando!')

    partime = commandpar.split()[0]
    
    future = utils.fdate(partime, datetime.datetime.now())
    if future == None:
        raise entity.CommandError('Parâmetros inválidos!')

    db.addreminder(message.guild.id, message.channel.id, message.id, message.author.id, future, bot.db_connection)
    await message.reply(f'Eu irei te notificar no dia `{future.strftime("%d/%m/%Y %H:%M")}`!')
entity.Command(name='remindme', func=remindme, category=category, desc='O bot irá te notificar no dia desejado, relembrando sua mensagem!', aliases=['rm', 'relembreme', 'lembrete', 'remind', 'clock'], args=[['tempo', '*']])


async def chatclear(message, commandpar, bot):
    text = ''.join(['** **\n' for x in range(0, 30)])
    await message.channel.send(text)
entity.Command(name='upchat', func=chatclear, category=category, desc='"Limpe" o chat do discord!', aliases=['subirchat'], perm=1)
