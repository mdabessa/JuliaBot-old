from random import randint
import discord
import modules.database as db
import modules.entity as entity


category = 'Moderação'
entity.command.newcategory(category, ':shield:Moderação.')


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
            await message.channel.send(f'{user.name} foi silenciado por `{time}` segundos :mute: ')
    else:
        raise entity.CommandError('Falta algo!')
entity.command(name='mastermute', func=mastermute , category=category, desc=f'Silenciar alguem, sem limite de tempo.', args=[['segundos', '*'], ['pessoa', '*,']], perm=1)


async def c_event(message, commandpar, connection, bot):
    if commandpar != None:
        marc = 0
        for eve in entity.event.events:
            if eve.command_create == False:
                continue
            if eve.name == commandpar:
                eve.clear(str(message.guild.id))
                await message.channel.send(f'{message.author.mention} evento `{eve.name}` criado com sucesso!')
                await eve.create([message.channel], str(message.guild.id))
                marc = 1

        if marc == 0:
            raise entity.CommandError('Nenhum evento com esse nome')
    else:
        raise entity.CommandError('Falta algo!')
entity.command(name='c_event', func=c_event , category=category, desc=f'Criar um evento.', args=[['evento', '*']], perm=1)
