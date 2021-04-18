import discord
import jikanpy as jk
import modules.database as db
import modules.entity as entity


category = 'Animes'
entity.Command.newcategory(category, ':japanese_goblin:Animes.')


async def anime_channel(message, commandpar, connection, bot):
    if commandpar == None:
        server = db.getserver(message.guild.id, connection)
        channel = server['anime_channel']    
        if channel != None:
            channel = bot.get_channel(int(channel))

        prefix = server['prefix']

        if channel == None:
            await message.channel.send(f'O servidor `{message.guild}` não possui um canal para as notifições de animes.')
        else:
            await message.channel.send(f'Canal de notificações de animes: <#{channel.id}>\n' +
            f'Para mudar o canal de animes, utilize `{prefix}animechannel #canal` ou `{prefix}anime_channel .` para desabilitar as notificações de animes em todos os canais.'
            )
    else:
        if commandpar == '.':
            db.editserver(message.guild.id, connection, 'anime_channel', None)
            await message.channel.send(f'As notificações de animes foram desabilitadas.')

        else:
            channel = commandpar
            rep = ['<','#','>']
            for r in rep:
                channel = channel.replace(r, '')

            try:
                channel = bot.get_channel(int(channel))
            except:
               raise entity.CommandError(f'Nenhum canal com esse nome, marque o canal com `#` para selecionar o canal desejado.')

            if channel == None:
                raise entity.CommandError(f'Nenhum canal com esse nome, marque o canal com `#` para selecionar o canal desejado.')
            
            db.editserver(message.guild.id, connection, 'anime_channel', str(channel.id))
            await message.channel.send(f'O canal de notificações de animes foi definido para `<#{channel.id}>`')
entity.Command(name='animechannel', func=anime_channel, category=category, desc=f'Define o canal de notificações de novos episódios de animes.', aliases=['animecanal', 'ac', 'canalanime'], args=[['canal', '*']], perm=1)


async def add_anime(message, commandpar, connection, bot):
    if commandpar!=None:
        jikan = jk.Jikan()
        try:
            anime = jikan.search('anime', commandpar)['results'][0]
        except:
            raise entity.CommandError('Não consegui achar nenhum anime com esse nome.')
        scr = entity.Script(f'add_anime_confirm_{message.guild.id}', 'add_anime_confirm', message.guild.id, time_out=20)
        await scr.execute([message.channel, message.author, anime], bot)

    else:
        raise entity.CommandError('Falta os parametros do comando!')
entity.Command(name='add_anime', func=add_anime, category=category, desc=f'Marque um anime para você ser notificado quando lancar episódio novo.', aliases=['aa'], args=[['anime', '*']])


async def del_anime(message, commandpar, connection, bot):
    if commandpar!=None:
        jikan = jk.Jikan()
        try:
            anime = jikan.search('anime', commandpar)['results'][0]
        except:
            raise entity.CommandError('Não consegui achar nenhum anime com esse nome.')
        scr = entity.Script(f'del_anime_confirm_{message.guild.id}', 'del_anime_confirm', message.guild.id, time_out=20)
        await scr.execute([message.channel, message.author, anime], bot)

    else:
        raise entity.CommandError('Falta os parametros do comando!')
entity.Command(name='del_anime', func=del_anime, category=category, desc=f'Remova um anime da sua lista de notificações.', aliases=['da'], args=[['anime', '*']])