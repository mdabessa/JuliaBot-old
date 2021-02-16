from random import randint
import discord
import modules.database as db
import modules.entity as entity


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
        if cmd != None:
            if cmd['price'] == 0:
                valor = 'Grátis'
            else:
                valor = cmd['price']

            if cmd['permission'] == 0:
                perm = 'Livre'
            elif cmd['permission'] == 1:
                perm = 'Apenas admins'
            else:
                perm = 'DEBUG'

            emb = discord.Embed(title=cmd['name'], color=0xe6dc56)

            emb.add_field(name='Descrição:', value=cmd['description'], inline=False)
            emb.add_field(name='Valor:', value=valor, inline=False)
            emb.add_field(name='Nivel de Permissão:', value=perm, inline=False)

            await message.channel.send(embed=emb)
        else:
            raise entity.CommandError(f'Nenhum comando com o nome {commandpar} existe!')
entity.command(name='help', func=_help, desc='Listar todos os comandos e suas descrições.')

async def coins(message, commandpar, connection, bot):
    if len(message.mentions) == 1:
        for mentioned in message.mentions:
            points = db.getpoints(mentioned.id, message.guild.id, connection)
            await message.channel.send(f'{mentioned.name} possui {points}')

    else:
        points = db.getpoints(message.author.id, message.guild.id, connection)
        await message.channel.send(f'{message.author.mention}, você possui {points}')
entity.command(name='coins', func=coins, desc='Verificar os pontos.')


async def coinsrank(message, commandpar, connection, bot):
    rank = db.rankpoints(message.guild.id, connection)
    if rank == None:   
        raise entity.CommandError('Não foi possivel execultar esta ação!')

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
entity.command(name='rank', func=coinsrank, desc='Top coins do servidor.')

async def roulette(message, commandpar, connection, bot):
    if commandpar != None:
        roulettechance = 33 #x/100
        p = db.getpoints(message.author.id, message.guild.id, connection)

        if commandpar == 'all':
            points = p
        else:
            try:
                points = int(commandpar)
            except:
                raise entity.CommandError('Não posso roletar nada que não seja um numero inteiro :pensive:')

        if points < p:
            if randint(0,100) < roulettechance:
                db.addpoints(message.author.id,message.guild.id, points, connection)
                await message.channel.send(f'{message.author.mention} Ganhou [+{points}] coins! :money_mouth:')
            else:
                db.subpoints(message.author.id, message.guild.id, points, connection)
                await message.channel.send(f'{message.author.mention} Perdeu [-{points}] coins! :sob:')

        if points == p:
            if randint(0,100) < roulettechance:
                db.addpoints(message.author.id,message.guild.id, points, connection)
                await message.channel.send(f'{message.author.mention} roletou tudo e ganhou [+{points}] coins, dobrando sua fortuna! :sunglasses:')
            else:
                db.subpoints(message.author.id, message.guild.id, points, connection)
                await message.channel.send(f'{message.author.mention} roletou tudo e perdeu [-{points}] zerando seus pontos! :rofl: :rofl: :rofl:')
        if points > p:
            raise entity.CommandError('Voce não possui pontos suficiente!')
    else:
        raise entity.CommandError('Quantos coins você quer roletar? :thinking:')
entity.command(name='roulette', func=roulette, desc=f'Roletar pontos.')

async def spam(message, commandpar, connection, bot):
    if commandpar !=None:
        cmdpar = commandpar.split()
        if len(cmdpar) >= 2:
            try:
                number = int(cmdpar[0])
            except:
                raise entity.CommandError('Quantas vezes?')
            
            if number > 10:
                raise entity.CommandError('O limite do spam é 10 vezes!')

            msg = str(' '.join(cmdpar[1:]))
            
            for i in range(0,number):
                await message.channel.send(f'{msg}')
        else:
            raise entity.CommandError('Falta algo nesse comando!')
    else:
        raise entity.CommandError('Quantas vezes? Spam do que?')
entity.command(name='spam', func=spam , desc=f'Spam de mensagens.', cost=2500)

async def cmdsay(message, commandpar, connection, bot):
    if commandpar != None:
        await message.channel.send(commandpar)
    else:
        raise('Falta algo nesse comando')
entity.command(name='say', func=cmdsay , desc=f'Fazer o bot dizer algo.', cost=500)

async def mute(message, commandpar, connection, bot):
    if commandpar !=None:
        time = 15
        for user in message.mentions:
            if str(user.id)+str(message.channel.id) in entity.mutes:
                await message.channel.send(f'{user.name} ja esta silenciado! :zipper_mouth:')
                return
            entity.timer.timer(str(user.id)+str(message.channel.id),time)
            entity.mutes.append(str(user.id)+str(message.channel.id))
            await message.channel.send(f'{user.name} foi silenciado por {time} segundos! :mute:')
    else:
        raise entity.CommandError('Falta algo nesse comando!')
entity.command(name='mute', func=mute , desc=f'Silenciar alguem por alguns segundos.', cost=500)

async def setcoins(message, commandpar, connection, bot):
    if commandpar != None:
        try:
            pointspar = int(commandpar.split()[0])
        except:
            raise entity.CommandError('Só numeros inteiros podem ser definidos como coins')

        try:
            if len(message.mentions) > 0:
                names = []
                for user in message.mentions:
                    names.append(user.name)
                    db.setpoints(user.id,message.guild.id,int(pointspar),connection)
                
                await message.channel.send(f'Coins definido como {pointspar} para : {", ".join(names)}')
            else:
                db.setpoints(message.author.id,message.guild.id,int(pointspar),connection)
                await message.channel.send(f'{message.author.mention} Seus Coins foram definido para {pointspar}')
        except:
            raise entity.CommandError('Não foi possivel realizar esta ação :worried:')

    else:
        raise entity.CommandError('Quantos coins ???')
entity.command(name='setcoins', func=setcoins , desc=f'Definir os seus pontos, ou os dos usuarios marcados.', perm=1)

async def addcoins(message, commandpar, connection, bot):
    if commandpar != None:
        try:
            pointspar = int(commandpar.split()[0])
        except:
            raise entity.CommandError('Pontos tem que ser um numero inteiro!')

        try:
            if len(message.mentions) > 0:
                names = []
                for user in message.mentions:
                    names.append(user.name)
                    db.addpoints(user.id,message.guild.id,int(pointspar), connection)
                
                await message.channel.send(f'{pointspar} Coins adicionados para : {", ".join(names)}')
            else:
                db.addpoints(message.author.id,message.guild.id,int(pointspar),connection)
                await message.channel.send(f'{message.author.mention} Foram adicionados {pointspar} coins.')
        except:
            raise entity.CommandError('Não foi possivel realizar esta ação :worried:')
    else:
        raise entity.CommandError('Quantos pontos?')
entity.command(name='addcoins', func=addcoins , desc=f'Adicionar pontos.', perm=1)

async def subcoins(message, commandpar, connection, bot):
    if commandpar != None:
        try:
            pointspar = int(commandpar.split()[0])
        except:
            raise entity.CommandError('Pontos tem que ser um numero inteiro!')

        try:
            if len(message.mentions) > 0:
                names = []
                for user in message.mentions:
                    names.append(user.name)
                    db.subpoints(user.id,message.guild.id,int(pointspar), connection)
                
                await message.channel.send(f'{pointspar} Coins foram removidos de : {", ".join(names)}')
            else:
                db.subpoints(message.author.id,message.guild.id,int(pointspar), connection)
                await message.channel.send(f'{message.author.mention} Foram removidos {pointspar} coins.')
        except:
            raise entity.CommandError('Não foi possivel realizar esta ação! :worried:')
    else:
        raise entity.CommandError('Quantos pontos?')
entity.command(name='subcoins', func=subcoins , desc=f'Remover pontos.', perm=1)

async def mastermute(message, commandpar, connection, bot):
    if commandpar !=None:
        try:
            time = int(commandpar.split()[0])
        except:
            raise entity.CommandError('Quanto tempo?')

        for user in message.mentions:
            if str(user.id)+str(message.channel.id) in entity.mutes:
                await message.channel.send(f'{user.name} ja esta silenciado :zipper_mouth:')
                return
            entity.timer.timer(str(user.id)+str(message.channel.id),time)
            entity.mutes.append(str(user.id)+str(message.channel.id))
            await message.channel.send(f'{user.name} foi silenciado por {time} segundos :mute: ')
    else:
        raise entity.CommandError('Falta algo!')
entity.command(name='mastermute', func=mastermute , desc=f'Silenciar alguem, sem limite de tempo.', perm=1)

async def c_event(message, commandpar, connection, bot):
    if commandpar != None:
        marc = 0
        for eve in entity.event.events:
            if eve.command_create == False:
                continue
            if eve.name == commandpar:
                eve.clear(str(message.guild.id))
                await message.channel.send(f'{message.author.mention} evento {eve.name} criado com sucesso!')
                await eve.create([message.channel], str(message.guild.id))
                marc = 1

        if marc == 0:
            raise entity.CommandError('Nenhum evento com esse nome')
    else:
        raise entity.CommandError('Falta algo!')
entity.command(name='c_event', func=c_event , desc=f'Criar um evento.', perm=1)

async def exe(message, commandpar, connection, bot):
    if commandpar != None:
        cont = commandpar.split()
        text = f'Executando: {cont[0]}'
        
        if len(cont) > 1:
            text += ' [' + ' '.join(cont[1:]) + ']'

        m = await message.channel.send(text)
        await entity.command.trycommand(m, commandpar, connection, '', bot)

    else:
        raise entity.CommandError('Falta algo nesse comando!')
entity.command(name='exec', func=exe , desc=f'Executar um comando através do bot.', perm=2)

async def setprefix(message, commandpar, connection, bot):
    if commandpar != None:
        cont = commandpar.split()
        prefix = cont[0]
        db.editserver(message.guild.id, connection, 'prefix', prefix)
        await message.channel.send(f'Prefixo de comandos mudado para {prefix}')

    else:
        raise entity.CommandError('Falta os parametros do comando!')
entity.command(name='setprefix', func=setprefix , desc=f'Mude o prefixo de comandos do bot.', perm=1)

async def getprefix(message, commandpar, connection, bot):
    prefix = db.getserver(message.guild.id, connection)['prefix']
    await message.channel.send(f'O prefixo do server é: {prefix}')
entity.command(name='prefix', func=getprefix , desc=f'Retorna o prefixo do bot no servidor.')

async def ping(message, commandpar, connection, bot):
    lt = int(round(bot.latency, 3)*1000)
    await message.channel.send(f'Pong! {lt}')
entity.command(name='ping', func=ping , desc=f'Pong!')


async def shop(message, commandpar, connection, bot):
    items = db.getshop(message.guild.id, connection)

    if len(items) == 0:
        await message.channel.send('Esse servidor não possui itens a venda!')

    else:
        emb = discord.Embed(title='Loja', color=0xe6dc56)

        for i in items:
            emb.add_field(name=f'{i[1]} - {i[2]}', value=f':coin:{i[3]}c', inline=True)
        
        emb.set_footer(text=f'{db.getserver(message.guild.id, connection)["prefix"]}buy [id]')
        await message.channel.send(embed=emb)
entity.command(name='shop', func=shop, desc=f'Loja de itens')

async def shopadditem(message, commandpar, connection, bot):
    if commandpar == None:
        raise entity.CommandError('Falta parametros!')

    cmdpar = commandpar.split()
    if len(cmdpar) < 2:
        raise entity.CommandError('Falta parametros!')

    try:
        price = int(cmdpar[0])
    except:
        raise entity.CommandError('Qual é o preco do item?')
    
    item_name = ' '.join(cmdpar[1:])

    db.additem(message.guild.id, item_name, price, connection)
    await message.channel.send(f'Item: {item_name} foi adicionado a loja por {price} coins!')
entity.command(name='additem', func=shopadditem, desc=f'Adicionar um item a loja!', perm=1)

async def buyitem(message, commandpar, connection, bot):
    if commandpar == None:
        raise entity.CommandError('Qual item ira comprar ?')
    
    try:
        item = int(commandpar)
    except:
        raise entity.CommandError('O item tem que ser referenciado com o um ID.')

    items = db.getshop(message.guild.id, connection)
    
    marc = 0
    for i in items:
        if i[1] == item:
            marc = 1
            points = db.getpoints(message.author.id, message.guild.id, connection)

            if i[3] > points:
                raise entity.CommandError('Coins insuficientes!')

            db.subpoints(message.author.id, message.guild.id, i[3], connection)
            await message.channel.send(f'{message.author.mention} comprou [{i[1]} - {i[2]}] por {i[3]}c.')

    if marc == 0:
        raise entity.CommandError(f'{message.author.mention} o item {commandpar} não existe.')
entity.command(name='buy', func=buyitem, desc=f'Comprar um item.')

async def shopdelitem(message, commandpar, connection, bot):
    if commandpar == None:
        raise entity.CommandError('Qual item irá deletar?')

    try:
        item = int(commandpar)
    except:
        raise entity.CommandError('O item tem que ser referenciado com o um ID.')

    items = db.getshop(message.guild.id, connection)

    marc = 0
    for i in items:
        if i[1] == item:
            marc = 1
            db.delitem(message.guild.id, item, connection)
            await message.channel.send(f'{message.author.mention} removeu o item [{i[1]} - {i[2]}] da loja!')

    if marc == 0:
        raise entity.CommandError(f'{message.author.mention} o item {commandpar} não existe.')
entity.command(name='delitem', func=shopdelitem, desc=f'Deletar itens da loja.', perm=1)


async def _duel(message, commandpar, connection, bot):
    if commandpar == None:
        raise entity.CommandError('Falta parametros!')

    if len(message.mentions) == 0:
        raise entity.CommandError('Contra quem?')

    try:
        points = int(commandpar.split()[0])
    except:
        points = 0

    vs = message.mentions[0]

    if db.getpoints(vs.id, message.guild.id, connection) < points:
        raise entity.CommandError(f'{vs.name} não possui pontos suficientes!')

    if db.getpoints(message.author.id, message.guild.id, connection) < points:
        raise entity.CommandError(f'{message.author.mention} Você não possui pontos suficientes!')

    for eve in entity.event.events:
        if eve.name == 'duel':
            cache = eve.getcache(str(message.guild.id))
            if cache != None:
                if cache == True:
                    eve.clear(str(message.guild.id))
                else:
                    raise entity.CommandError('Ja existe um duelo em andamento!')
            

            await eve.create([message, points], str(message.guild.id))
entity.command(name='duel', func=_duel, desc=f'Duele contra alguem valendo coins!')

async def addcmd(message, commandpar, connection, bot):
    if commandpar == None:
        raise entity.CommandError('Falta parametros!')

    if len(commandpar.split(',')) != 3:
        raise entity.CommandError('Parametros invalidos!')

    commandpar = commandpar.split(',')

    if ' ' in commandpar[0] or ':' in commandpar[0]:
        raise entity.CommandError('O nome do comando não pode conter nenhum espaço ou dois pontos ":".')

    if entity.command.getcommand(message.guild.id, commandpar[0], connection) != None:
        raise entity.CommandError('Um comando com esse nome ja existe!')

    db.addcommand(message.guild.id, connection, commandpar[0], commandpar[1], commandpar[2])
    await message.channel.send(f'Comando adicionado com sucesso!\nComando: {commandpar[0]}\nMensagem: {commandpar[1]}\nDescrição: {commandpar[2]}')
entity.command(name='addcmd', func=addcmd, desc=f'Adicione um comando personalizado! // [prefixo]addcmd [nome,mensagem,desrição]', perm=1)

async def delcmd(message, commandpar, connection, bot):
    if commandpar == None:
        raise entity.CommandError('Falta parametros!')

    cmd = entity.command.getcommand(message.guild.id, commandpar, connection)
    if cmd == None:
        raise entity.CommandError(f'O comando com o nome {commandpar} não existe!')

    if cmd['overwritten'] == 0:
        await message.channel.send(f'O comando {commandpar} é um comando próprio da {bot.user.mention}, ele não pode ser deletado!')
    else:
        db.delcommand(message.guild.id, connection, commandpar)
        await message.channel.send(f'O comando {commandpar} foi deletado com sucesso!')
entity.command(name='delcmd', func=delcmd, desc=f'Delete um comando personalizado!', perm=1)


async def commandchannel(message, commandpar, connection, bot):
    if commandpar == None:
        server = db.getserver(message.guild.id, connection)
        channel = server['commandchannel']
        prefix = server['prefix']

        if channel == None:
            await message.channel.send(f'O servidor {message.guild} permite comandos em qualquer canal!\n' +
            f'Para mudar o canal de comandos, utilize [{prefix}cmdchannel #canal] ou [{prefix}cmdchannel .] para poder utilizar comandos em todos os canais.')
        else:
            channel = bot.get_channel(int(channel))
            await message.channel.send(f'Canal de comandos: <#{channel.id}>\n' +
            f'Para mudar o canal de comandos, utilize [{prefix}cmdchannel #canal] ou [{prefix}cmdchannel .] para poder utilizar comandos em todos os canais.'
            )
    else:
        if commandpar == '.':
            db.editserver(message.guild.id, connection, 'commandchannel', None)
            await message.channel.send(f'Comandos agora podem ser utilizados em qualquer canal.')

        else:
            channel = commandpar
            rep = ['<','#','>']
            for r in rep:
                channel = channel.replace(r, '')

            try:
                channel = bot.get_channel(int(channel))
            except:
               raise entity.CommandError(f'Nenhum canal com esse nome, marque o canal com # para selecionar o canal desejado.')

            if channel == None:
                raise entity.CommandError(f'Nenhum canal com esse nome, marque o canal com # para selecionar o canal desejado.')
            
            db.editserver(message.guild.id, connection, 'commandchannel', str(channel.id))
            await message.channel.send(f'O canal de comandos foi definido para <#{channel.id}>')


entity.command(name='cmdchannel', func=commandchannel, desc=f'Modifique o canal de comandos!', perm=1)