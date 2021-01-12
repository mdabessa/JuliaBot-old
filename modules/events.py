from modules.base import *
from random import randint, shuffle

async def gift(par):
    points = randint(1,10)*100

    channel = par[0]
    m = await channel.send(f'PRESENTE SURPRESA, REAJA PRA PEGAR {points} COINS!')
    await m.add_reaction('🎁')
    return [m, points]
async def exegift(param, cache):
    if cache == None:
        return cache


    message = cache[0]
    points = cache[1]
    user = param[0]
    connection = param[2]
    addpoints(user.id, message.guild.id, points, connection)
    await message.channel.send(f'{user.mention} ganhou {points} coins, :partying_face:')
    return True
event(name='gift', createfunc=gift, executefunc=exegift, desc='Quem pegar o presente primeiro leva os coins!')

async def cards(par):
    points = [(randint(1,10)*100), (randint(1,10)*100), (randint(1,5)*(-100))]
    shuffle(points)

    channel = par[0]
    m = await channel.send(f'Escolha uma cartinha (2 boas, 1 ruim) :flower_playing_cards: ')
    await m.add_reaction('💴')
    await m.add_reaction('💶')
    await m.add_reaction('💷')
    return [m , points]
async def execards(param, cache):
    message = cache[0]
    points = cache[1]
    user = param[0]
    emoji = param[1]
    connection = param[2]

    try:
        usercache = cache[2]
        choicecache = cache[3]
    except:
        usercache = []
        choicecache = []

    userind = str(user.id) + str(message.guild.id) 
    
    if userind in usercache:
        return [message, points, usercache, choicecache]
    
    choice = 0
    if emoji == '💴':
        choice = 1
    
    if emoji == '💶':
        choice = 2

    if emoji == '💷':
        choice = 3

    if choice != 0 and (choice not in choicecache):
        usercache.append(userind)
        choicecache.append(choice)
        pts = points[choice-1]
        if pts > 0:
            await message.channel.send(f'{user.mention} pegou uma das cartas boas e ganhou [+{pts}] coins! :moneybag:')
            addpoints(user.id, message.guild.id, pts, connection)
        else:
            await message.channel.send(f'{user.mention} escolheu a pior carta e perdeu [{pts}] coins! :money_with_wings:')
            subpoints(user.id, message.guild.id, (pts*(-1)), connection)
        return [message, points, usercache, choicecache]
    else:
        return [message, points, usercache, choicecache]
event(name='cards', createfunc=cards, executefunc=execards, desc='Escolha cartinhas para ganhar coins (ou perder :D)')

async def quiz(par):
    points = randint(5,15)*100

    num1 = randint(1,100)
    num2 = randint(1,100)

    res = num1*num2
    channel = par[0]
    m = await channel.send(f'O quiz chegou!, Qual resultado de {num1} multiplicado por {num2} ?')

    return [m, points, res]
async def exequiz(param, cache):
    if cache == True:
        return True

    m = cache[0]
    p = cache[1]
    r = str(cache[2])

    msg = param[0]
    connection = param[1]
    print(r)
    print(msg.content)
    if str(msg.content) == r and msg.channel.id == m.channel.id:
        await m.channel.send(f'{msg.author.mention} acertou e ganhou [+{p}] coins')
        addpoints(msg.author.id, msg.guild.id, p, connection)
        return True

    else:
        return cache
event(name='quiz', createfunc=quiz, executefunc=exequiz, desc='Responda certo a pergunta para ganhar coins!', att='message')
