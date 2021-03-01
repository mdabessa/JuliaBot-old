from random import randint
import discord
import modules.database as db
import modules.entity as entity


category = 'Diversão'
entity.command.newcategory(category, ':game_die:Diversão.')


async def spam(message, commandpar, connection, bot):
    if commandpar !=None:
        cmdpar = commandpar.split()
        if len(cmdpar) >= 2:
            try:
                number = int(cmdpar[0])
            except:
                raise entity.CommandError('Quantas vezes?')
            
            if number > 10:
                raise entity.CommandError('O limite do spam é `10` vezes!')

            msg = str(' '.join(cmdpar[1:]))
            
            for i in range(0,number):
                await message.channel.send(f'{msg}')
        else:
            raise entity.CommandError('Falta algo nesse comando!')
    else:
        raise entity.CommandError('Quantas vezes? Spam do que?')
entity.command(name='spam', func=spam , category=category, desc=f'Spam de mensagens.', args=[['quantidade', '*'], ['texto', '*']], cost=2500)


async def cmdsay(message, commandpar, connection, bot):
    if commandpar != None:
        await message.channel.send(commandpar)
    else:
        raise('Falta algo nesse comando')
entity.command(name='say', func=cmdsay , category=category, desc=f'Fazer o bot dizer algo.', args=[['texto', '*']], cost=500)


async def mute(message, commandpar, connection, bot):
    if commandpar !=None:
        time = 15
        for user in message.mentions:
            if str(user.id)+str(message.channel.id) in entity.mutes:
                await message.channel.send(f'{user.name} ja esta silenciado! :zipper_mouth:')
                return
            entity.timer.timer(str(user.id)+str(message.channel.id),time)
            entity.mutes.append(str(user.id)+str(message.channel.id))
            await message.channel.send(f'{user.name} foi silenciado por `{time}` segundos! :mute:')
    else:
        raise entity.CommandError('Falta algo nesse comando!')
entity.command(name='mute', func=mute , category=category, desc=f'Silenciar alguem por alguns segundos.', args=[['pessoa', '*º']], cost=500)


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
entity.command(name='duel', func=_duel, category=category, desc=f'Duele contra alguem valendo coins!', args=[['coins', '*'], ['pessoa', '*']])