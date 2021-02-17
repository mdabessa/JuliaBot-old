from random import randint
import discord
import modules.database as db
import modules.entity as entity

category = 'Core'

async def _help(message, commandpar, connection, bot): 
    if commandpar == None:
        
        cmds = entity.command.getallcommands(message.guild.id, connection)

        general_cmds = [cmd for cmd in cmds if cmd['permission'] == 0]
        mod_cmds = [cmd for cmd in cmds if cmd['permission'] == 1] 
        
        prefix = db.getserver(message.guild.id, connection)['prefix']
        emb = discord.Embed(title='Lista de Comandos', description=f'{prefix}help [comando]', color=0xe6dc56)

        emb.add_field(name=f'Comandos Gerais', value=f'{", ".join([cmd["name"] for cmd in general_cmds])}', inline=False)
        emb.add_field(name=f'Comandos de Admin', value=f'{", ".join([cmd["name"] for cmd in mod_cmds])}', inline=False)

        await message.channel.send(embed=emb)
    
    else:
        cmd = entity.command.getcommand(message.guild.id, commandpar, connection)
        prefix = db.getserver(message.guild.id, connection)['prefix']
        if cmd != None:
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

            emb = discord.Embed(title=f'{prefix}{cmd["name"]}'.upper(), color=0xe6dc56)

            emb.add_field(name='Descrição:', value=cmd['description'], inline=False)
            emb.add_field(name='Valor:', value=valor, inline=False)
            emb.add_field(name='Categoria:', value=cmd['category'], inline=False)
            emb.add_field(name='Nivel de Permissão:', value=perm, inline=False)

            await message.channel.send(embed=emb)
        else:
            raise entity.CommandError(f'Nenhum comando com o nome {commandpar} existe!')
entity.command(name='help', func=_help, category=category, desc='Listar todos os comandos e suas descrições.')


async def getprefix(message, commandpar, connection, bot):
    prefix = db.getserver(message.guild.id, connection)['prefix']
    await message.channel.send(f'O prefixo do server é: {prefix}')
entity.command(name='prefix', func=getprefix , category=category, desc=f'Retorna o prefixo do bot no servidor.')


async def ping(message, commandpar, connection, bot):
    lt = int(round(bot.latency, 3)*1000)
    await message.channel.send(f'Pong! {lt}')
entity.command(name='ping', func=ping , category=category, desc=f'Pong!')