from random import randint
import discord
import modules.database as db
import modules.entity as entity


category = 'Diversão'
entity.Command.newcategory(category, ':game_die:Diversão.')


async def cmdsay(message, commandpar, connection, bot):
    if commandpar != None:
        await message.channel.send(commandpar)
    else:
        raise('Falta algo nesse comando')
entity.Command(name='say', func=cmdsay , category=category, desc=f'Fazer o bot dizer algo.', aliases=['dizer', 'falar'], args=[['texto', '*']], cost=500)


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

    for eve in entity.Event.events:
        if eve.name == 'duel':
            cache = eve.getcache(str(message.guild.id))
            if cache != None:
                if cache == True:
                    eve.clear(str(message.guild.id))
                else:
                    raise entity.CommandError('Ja existe um duelo em andamento!')
            

            await eve.create([message, points], str(message.guild.id))
entity.Command(name='duel', func=_duel, category=category, desc=f'Duele contra alguem valendo coins!', aliases=['duelo', 'x1'], args=[['coins', '*'], ['pessoa', '*']])