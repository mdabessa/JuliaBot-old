import modules.database as db
import modules.entity as entity
import modules.utils as utils
from random import randint, shuffle, choice
from math import floor


async def gift(cache, par, bot):
    if cache['status'] == 'created':
        points = randint(1,10)*100

        channel = par[0]
        m = await channel.send(f'PRESENTE SURPRESA, REAJA PRA PEGAR `{points}` COINS!')
        await m.add_reaction('🎁')
        
        cache['points'] = points
        cache['message'] = m
        cache['status'] = 'started'
    else:
        message = cache['message']
        points = cache['points']
        user = par[0]
        db.addpoints(user.id, message.guild.id, points, bot.db_connection)
        await message.channel.send(f'{user.mention} ganhou `{points}` coins, :partying_face:')
        cache['status'] = 0
entity.Script.new_function(gift, tag='event', limit_by_name=2)

async def cards(cache, par, bot):
    if cache['status'] == 'created':
        points = [(randint(1,10)*100), (randint(1,10)*100), (randint(1,5)*(-100))]
        shuffle(points)

        channel = par[0]
        m = await channel.send(f'Escolha uma cartinha `2 boas`, `1 ruim` :flower_playing_cards:')
        await m.add_reaction('💴')
        await m.add_reaction('💶')
        await m.add_reaction('💷')
        
        cache['message'] = m
        cache['points'] = points
        cache['users'] = []
        cache['choices'] = []
        cache['status'] = 'started'
    else:
        message = cache['message']
        points = cache['points']
        user = par[0]
        emoji = par[1]

        userind = str(user.id) + str(message.guild.id)
        
        if userind in cache['users']:
            return
        
        choice = 0
        if emoji == '💴':
            choice = 1
        
        if emoji == '💶':
            choice = 2

        if emoji == '💷':
            choice = 3


        if choice != 0 and (choice not in cache['choices']):
            cache['users'].append(userind)
            cache['choices'].append(choice)
            pts = points[choice-1]
            if pts > 0:
                await message.channel.send(f'{user.mention} pegou uma das cartas `boas` e ganhou `{pts}` coins! :moneybag:')
                db.addpoints(user.id, message.guild.id, pts, bot.db_connection)
            else:
                await message.channel.send(f'{user.mention} escolheu a pior `carta` e perdeu `{-pts}` coins! :money_with_wings:')
                db.subpoints(user.id, message.guild.id, (pts*(-1)), bot.db_connection)
        if len(cache['choices']) >= 3:
            cache['status'] == 0
entity.Script.new_function(cards, tag='event', limit_by_name=2)

async def quiz(cache, par, bot):
    if cache['status'] == 'created':
        channel = par[0]

        points = randint(5,15)*100

        num1 = randint(1,100)
        num2 = randint(1,100)

        operation = ['Soma', 'Multiplicação', 'Divisão', 'Subtração']
        operator = choice(operation)

        if operator == 'Soma':
            m = await channel.send(f'O quiz chegou!, Qual resultado da soma entre [{num1}] e [{num2}] ? // ex: 5+5 -> 10')
            res = num1+num2
        if operator == 'Multiplicação':
            m = await channel.send(f'O quiz chegou!, Qual resultado da multiplicação entre [{num1}] e [{num2}] ? // ex: 5x5 -> 25')
            res = num1*num2
        if operator == 'Divisão':
            m = await channel.send(f'O quiz chegou!, Qual resultado da divisão entre [{num1}] e [{num2}] ? // ex: 1/16 -> 0.0625 -> 0.062')
            res = num1/num2
            res = utils.nround(res)
        if operator == 'Subtração':
            m = await channel.send(f'O quiz chegou!, Qual resultado da subtração entre [{num1}] e [{num2}] ? // ex: 2-4 -> -2')
            res = num1-num2

        cache['message'] = m
        cache['points'] = points
        cache['result'] = res
        cache['status'] = 'started'

    else:
        m = cache['message']
        p = cache['points']
        r = str(cache['result'])

        msg = par[0]
        if str(msg.content) == r and msg.channel.id == m.channel.id:
            await m.channel.send(f'{msg.author.mention} acertou e ganhou `{p}` coins!')
            db.addpoints(msg.author.id, msg.guild.id, p, bot.db_connection)
            cache['status'] == 0
entity.Script.new_function(quiz, tag='event', limit_by_name=2, triggers=['message'])
