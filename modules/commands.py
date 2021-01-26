from modules.base import *
from random import randint
import discord


async def _help(message, commandpar, connection, bot): 
    if commandpar == None:
    
        cmds = [cmd for cmd in command.commands if cmd.perm == 0]
        mod_cmds = [cmd for cmd in command.commands if cmd.perm == 1] 
        
        emb = discord.Embed(title='Lista de Comandos', description=f'{command.prefix}help [comando]', color=0xe6dc56)

        emb.add_field(name=f'Comandos Gerais', value=f'{", ".join([cmd.name for cmd in cmds])}', inline=False)
        emb.add_field(name=f'Comandos de Admin', value=f'{", ".join([cmd.name for cmd in mod_cmds])}', inline=False)

        await message.channel.send(embed=emb)
    
    else:
        c = 0
        for cmd in command.commands:
            if cmd.name == commandpar:
                await message.channel.send(f'Comando: {cmd.name} | Descrição: {cmd.desc} | Valor: {cmd.cost}c')
                c = 1

        if c == 0:
            raise Exception('Nenhum comando encontrado.')


command(name='help', func=_help, desc='Listar todos os comandos e suas descrições.')

async def coins(message, commandpar, connection, bot):
    if len(message.mentions) == 1:
        for mentioned in message.mentions:
            points = getpoints(mentioned.id, message.guild.id, connection)
            await message.channel.send(f'{mentioned.name} possui {points}')

    else:
        points = getpoints(message.author.id, message.guild.id, connection)
        await message.channel.send(f'{message.author.mention}, você possui {points}')
command(name='coins', func=coins, desc='Verificar os pontos.')


async def coinsrank(message, commandpar, connection, bot):
    rank = rankpoints(message.guild.id, connection)
    if rank == None:   
        raise Exception('Não foi possivel execultar esta ação!')

    emb = discord.Embed(title='Rank', color=0xe6dc56)
    for num, i in enumerate(rank):
        user = bot.get_user(int(i[1]))
        points = i[2]

        if num == 0:
            medal = ':first_place:'
        if num == 1:
            medal = ':second_place:'
        if num == 2:
            medal = ':third_place:'
        if num == 3:
            medal = ':four:'
        if num == 4:
            medal = ':five:'
        

        emb.add_field(name=f'{medal}{user.name}', value=f':coin:{points}c', inline=False)
    
    await message.channel.send(embed=emb)
command(name='rank', func=coinsrank, desc='Top coins do servidor.')


async def coinsglobalrank(message, commandpar, connection, bot):
    rank = globalrankpoints(connection)
    if rank == None:   
        raise Exception('Não foi possivel execultar esta ação!')

    emb = discord.Embed(title='Rank Global', color=0xe6dc56)
    for num, i in enumerate(rank):
        user = bot.get_user(int(i[1]))
        points = i[2]

        if num == 0:
            medal = ':first_place:'
        if num == 1:
            medal = ':second_place:'
        if num == 2:
            medal = ':third_place:'
        if num == 3:
            medal = ':four:'
        if num == 4:
            medal = ':five:'
        

        emb.add_field(name=f'{medal}{user.name}', value=f':coin:{points}c', inline=False)
    
    await message.channel.send(embed=emb)
command(name='globalrank', func=coinsglobalrank, desc='Top coins global.')

async def roulette(message, commandpar, connection, bot):
    if commandpar != None:
        roulettechance = 33 #x/100
        p = getpoints(message.author.id, message.guild.id, connection)

        if commandpar == 'all':
            points = p
        else:
            try:
                points = int(commandpar)
            except:
                raise Exception('Não posso roletar nada que não seja um numero inteiro :pensive:')

        if points < p:
            if randint(0,100) < roulettechance:
                addpoints(message.author.id,message.guild.id, points, connection)
                await message.channel.send(f'{message.author.mention} Ganhou [+{points}] coins! :money_mouth:')
            else:
                subpoints(message.author.id, message.guild.id, points, connection)
                await message.channel.send(f'{message.author.mention} Perdeu [-{points}] coins! :sob:')

        if points == p:
            if randint(0,100) < roulettechance:
                addpoints(message.author.id,message.guild.id, points, connection)
                await message.channel.send(f'{message.author.mention} roletou tudo e ganhou [+{points}] coins, dobrando sua fortuna! :sunglasses:')
            else:
                subpoints(message.author.id, message.guild.id, points, connection)
                await message.channel.send(f'{message.author.mention} roletou tudo e perdeu [-{points}] zerando seus pontos! :rofl: :rofl: :rofl:')
        if points > p:
            raise Exception('Voce não possui pontos suficiente!')
    else:
        raise Exception('Quantos coins você quer roletar? :thinking:')
command(name='roulette', func=roulette, desc=f'Roletar pontos.')

async def spam(message, commandpar, connection, bot):
    if commandpar !=None:
        cmdpar = commandpar.split()
        if len(cmdpar) >= 2:
            try:
                number = int(cmdpar[0])
            except:
                raise Exception('Quantas vezes?')
            
            if number > 10:
                raise Exception('O limite do spam é 10 vezes!')

            msg = str(' '.join(cmdpar[1:]))
            
            for i in range(0,number):
                await message.channel.send(f'{msg}')
        else:
            raise Exception('Falta algo nesse comando!')
    else:
        raise Exception('Quantas vezes? Spam do que?')
command(name='spam', func=spam , desc=f'Spam de mensagens.', cost=2500)

async def cmdsay(message, commandpar, connection, bot):
    if commandpar != None:
        await message.channel.send(commandpar)
    else:
        raise('Falta algo nesse comando')
command(name='say', func=cmdsay , desc=f'Fazer o bot dizer algo.', cost=500)

async def mute(message, commandpar, connection, bot):
    global mutes
    if commandpar !=None:
        time = 15
        for user in message.mentions:
            if str(user.id)+str(message.channel.id) in mutes:
                await message.channel.send(f'{user.name} ja esta silenciado! :zipper_mouth:')
                return
            timer.timer(str(user.id)+str(message.channel.id),time)
            mutes.append(str(user.id)+str(message.channel.id))
            await message.channel.send(f'{user.name} foi silenciado por {time} segundos! :mute:')
    else:
        raise Exception('Falta algo nesse comando!')
command(name='mute', func=mute , desc=f'Silenciar alguem por alguns segundos.', cost=500)

async def setcoins(message, commandpar, connection, bot):
    if commandpar != None:
        try:
            pointspar = int(commandpar.split()[0])
        except:
            raise Exception('Só numeros inteiros podem ser definidos como coins')

        try:
            if len(message.mentions) > 0:
                names = []
                for user in message.mentions:
                    names.append(user.name)
                    setpoints(user.id,message.guild.id,int(pointspar),connection)
                
                await message.channel.send(f'Coins definido como {pointspar} para : {", ".join(names)}')
            else:
                setpoints(message.author.id,message.guild.id,int(pointspar),connection)
                await message.channel.send(f'{message.author.mention} Seus Coins foram definido para {pointspar}')
        except:
            raise Exception('Não foi possivel realizar esta ação :worried:')

    else:
        raise Exception('Quantos coins ???')
command(name='setcoins', func=setcoins , desc=f'Definir os seus pontos, ou os dos usuarios marcados.', perm=1)

async def addcoins(message, commandpar, connection, bot):
    if commandpar != None:
        try:
            pointspar = int(commandpar.split()[0])
        except:
            raise Exception('Pontos tem que ser um numero inteiro!')

        try:
            if len(message.mentions) > 0:
                names = []
                for user in message.mentions:
                    names.append(user.name)
                    addpoints(user.id,message.guild.id,int(pointspar), connection)
                
                await message.channel.send(f'{pointspar} Coins adicionados para : {", ".join(names)}')
            else:
                addpoints(message.author.id,message.guild.id,int(pointspar),connection)
                await message.channel.send(f'{message.author.mention} Foram adicionados {pointspar} coins.')
        except:
            raise Exception('Não foi possivel realizar esta ação :worried:')
    else:
        raise Exception('Quantos pontos?')
command(name='addcoins', func=addcoins , desc=f'Adicionar pontos.', perm=1)

async def subcoins(message, commandpar, connection, bot):
    if commandpar != None:
        try:
            pointspar = int(commandpar.split()[0])
        except:
            raise Exception('Pontos tem que ser um numero inteiro!')

        try:
            if len(message.mentions) > 0:
                names = []
                for user in message.mentions:
                    names.append(user.name)
                    subpoints(user.id,message.guild.id,int(pointspar), connection)
                
                await message.channel.send(f'{pointspar} Coins foram removidos de : {", ".join(names)}')
            else:
                subpoints(message.author.id,message.guild.id,int(pointspar), connection)
                await message.channel.send(f'{message.author.mention} Foram removidos {pointspar} coins.')
        except:
            raise Exception('Não foi possivel realizar esta ação! :worried:')
    else:
        raise Exception('Quantos pontos?')
command(name='subcoins', func=subcoins , desc=f'Remover pontos.', perm=1)

async def mastermute(message, commandpar, connection, bot):
    global mutes
    if commandpar !=None:
        try:
            time = int(commandpar.split()[0])
        except:
            raise Exception('Quanto tempo?')

        for user in message.mentions:
            if str(user.id)+str(message.channel.id) in mutes:
                await message.channel.send(f'{user.name} ja esta silenciado :zipper_mouth:')
                return
            timer.timer(str(user.id)+str(message.channel.id),time)
            mutes.append(str(user.id)+str(message.channel.id))
            await message.channel.send(f'{user.name} foi silenciado por {time} segundos :mute: ')
    else:
        raise Exception('Falta algo!')
command(name='mastermute', func=mastermute , desc=f'Silenciar alguem, sem limite de tempo.', perm=1)

async def c_event(message, commandpar, connection, bot):
    if commandpar != None:
        marc = 0
        for eve in event.events:
            if eve.name == commandpar:
                eve.clear()
                await message.channel.send(f'{message.author.mention} evento {eve.name} criado com sucesso!')
                await eve.create([message.channel])
                marc = 1

        if marc == 0:
            raise Exception('Nenhum evento com esse nome')
    else:
        raise Exception('Falta algo!')
command(name='c_event', func=c_event , desc=f'Criar um evento.', perm=1)

async def exe(message, commandpar, connection, bot):
    if commandpar != None:
        cont = commandpar.split()
        text = f'Executando: {cont[0]}'
        
        if len(cont) > 1:
            text += ' [' + ' '.join(cont[1:]) + ']'

        m = await message.channel.send(text)
        await command.trycommand(m, commandpar, connection, masterid, bot)

    else:
        raise Exception('Falta algo nesse comando!')
command(name='exec', func=exe , desc=f'Executar um comando através do bot.', perm=1)

async def setprefix(message, commandpar, connection, bot):
    if commandpar != None:
        cont = commandpar.split()
        command.prefix = cont[0]
        await bot.change_presence(activity=discord.Game(f'{command.prefix}help'))
        await message.channel.send(f'Prefixo de comandos mudado para {command.prefix}')

    else:
        raise Exception('Falta os parametros do comando!')
command(name='setprefix', func=setprefix , desc=f'Mude o prefixo de comandos do bot.', perm=1)

async def ping(message, commandpar, connection, bot):
    lt = int(round(bot.latency, 3)*1000)
    await message.channel.send(f'Pong! {lt}')
command(name='ping', func=ping , desc=f'Pong!')


async def shop(message, commandpar, connection, bot):
    items = getshop(message.guild.id, connection)

    if len(items) == 0:
        await message.channel.send('Esse servidor não possui itens a venda!')

    else:
        emb = discord.Embed(title='Loja', color=0xe6dc56)

        for i in items:
            emb.add_field(name=f'{i[2]}', value=f':coin:{i[3]}c', inline=True)
        
        await message.channel.send(embed=emb)
command(name='shop', func=shop, desc=f'Loja de itens')

async def shopadditem(message, commandpar, connection, bot):
    if commandpar == None:
        raise Exception('Falta parametros!')

    cmdpar = commandpar.split()
    if len(cmdpar) < 2:
        raise Exception('Falta parametros!')

    try:
        price = int(cmdpar[0])
    except:
        raise Exception('Qual é o preco do item?')
    
    item_name = ' '.join(cmdpar[1:])

    additem(message.guild.id, item_name, price, connection)
    await message.channel.send(f'Item: {item_name} foi adicionado a loja por {price} coins!')
command(name='additem', func=shopadditem, desc=f'Adicionar um item a loja!', perm=1)

async def buyitem(message, commandpar, connection, bot):
    if commandpar == None:
        raise Exception('Qual item ira comprar ?')
    
    items = getshop(message.guild.id, connection)
    
    marc = 0
    for i in items:
        if i[2] == commandpar:
            marc = 1
            points = getpoints(message.author.id, message.guild.id, connection)

            if i[3] > points:
                raise Exception('Coins insuficientes!')

            subpoints(message.author.id, message.guild.id, i[3], connection)
            await message.channel.send(f'{message.author.mention} comprou {i[2]} por {i[3]}c.')

    if marc == 0:
        raise Exception(f'{message.author.mention} o item {commandpar} não existe.')
command(name='buy', func=buyitem, desc=f'Comprar um item.')