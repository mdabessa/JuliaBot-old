from exfunc import *
from random import randint
from os import environ
from environs import Env


env = Env()
env.read_env()

masterid = int(environ['master_id'])


roulettechance = 25 #x/100
mutes = []


async def bhelp(message, commandpar, connection):
    text = '=================== \n'
    for cmd in command.commands:
        text += f'{cmd.name}: \n'
        text += f'{cmd.desc} \n'
    text += '==================='
    await message.channel.send(text)
command(name='help', func=bhelp, desc='Listar todos os comandos e suas descrições.')

async def coins(message, commandpar, connection):
    if len(message.mentions) == 1:
        for mentioned in message.mentions:
            points = getpoints(mentioned.id, message.guild.id, connection)
            await message.channel.send(f'{mentioned.name} possui {points}')

    else:
        points = getpoints(message.author.id, message.guild.id, connection)
        await message.channel.send(f'{message.author.mention}, você possui {points}')
command(name='coins', func=coins, desc='Verificar os pontos.')

async def roulette(message, commandpar, connection):
    if commandpar != None:
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
                await message.channel.send(f'{message.author.mention} Perdeu [{points}] coins! :sob:')

        if points == p:
            if randint(0,100) < roulettechance:
                addpoints(message.author.id,message.guild.id, points, connection)
                await message.channel.send(f'{message.author.mention} roletou tudo e ganhou [+{points}] coins, dobrando sua fortuna! :sunglasses:')
            else:
                subpoints(message.author.id, message.guild.id, points, connection)
                await message.channel.send(f'{message.author.mention} roletou tudo e perdeu [{points}] zerando seus pontos! :rofl: :rofl: :rofl:')
        if points > p:
            raise Exception('Voce não possui pontos suficiente!')
    else:
        raise Exception('Quantos coins voçe quer roletar? :thinking:')
command(name='roulette', func=roulette, desc=f'Roletar pontos.')

async def spam(message, commandpar, connection):
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
command(name='spam', func=spam , desc=f'Spam de mensagens.', cost=500)

async def mute(message, commandpar, connection):
    global mutes
    if commandpar !=None:
        time = 15
        for user in message.mentions:
            if str(message.author.id)+str(message.channel.id) in mutes:
                await message.channel.send(f'{user.name} ja esta silenciado! :zipper_mouth:')
                return
            timer(str(message.author.id)+str(message.channel.id),time)
            mutes.append(str(message.author.id)+str(message.channel.id))
            await message.channel.send(f'{user.name} foi silenciado por {time} segundos! :mute:')
    else:
        raise Exception('Falta algo nesse comando!')
command(name='mute', func=mute , desc=f'Silenciar alguem por alguns segundos.', cost=500)

async def setcoins(message, commandpar, connection):
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

async def addcoins(message, commandpar, connection):
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

async def subcoins(message, commandpar, connection):
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

async def mastermute(message, commandpar, connection):
    global mutes
    if commandpar !=None:
        try:
            time = int(commandpar.split()[0])
        except:
            raise Exception('Quanto tempo?')

        for user in message.mentions:
            if str(message.author.id)+str(message.channel.id) in mutes:
                await message.channel.send(f'{user.name} ja esta silenciado :zipper_mouth:')
                return
            timer(str(message.author.id)+str(message.channel.id),time)
            mutes.append(str(message.author.id)+str(message.channel.id))
            await message.channel.send(f'{user.name} foi silenciado por {time} segundos :mute: ')
    else:
        raise Exception('Falta algo!')
command(name='mastermute', func=mastermute , desc=f'Silenciar alguem, sem limite de tempo.', perm=1)

async def c_event(message, commandpar, connection):
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

async def exe(message, commandpar, connection):
    if commandpar != None:
        cont = commandpar.split()
        text = f'Executando: {cont[0]}'
        
        if len(cont) > 1:
            text += ' [' + ' '.join(cont[1:]) + ']'

        m = await message.channel.send(text)
        await command.trycommand(m, commandpar, connection, masterid)

    else:
        raise('Falta algo nesse comando')
command(name='exec', func=exe , desc=f'Executar um comando através do bot.', perm=1)

async def cmdsay(message, commandpar, connection):
    if commandpar != None:
        await message.channel.send(commandpar)
    else:
        raise('Falta algo nesse comando')
command(name='say', func=cmdsay , desc=f'Fazer o bot dizer algo.', perm=1)