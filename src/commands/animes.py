from discord import Embed
import jikanpy as jk
import modules.database as db
import modules.entity as entity


category = 'Animes'
entity.Command.newcategory(category, ':japanese_goblin:Animes.')


async def anime_channel(message, commandpar, bot):
    if commandpar == None:
        server = db.getserver(message.guild.id, bot.db_connection)
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
            db.editserver(message.guild.id, bot.db_connection, 'anime_channel', None)
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
            
            db.editserver(message.guild.id, bot.db_connection, 'anime_channel', str(channel.id))
            await message.channel.send(f'O canal de notificações de animes foi definido para `<#{channel.id}>`')
entity.Command(name='animechannel', func=anime_channel, category=category, desc=f'Define o canal de notificações de novos episódios de animes.', aliases=['animecanal', 'ac', 'canalanime'], args=[['canal', '*']], perm=1)


async def add_anime(message, commandpar, bot):
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


async def del_anime(message, commandpar, bot):
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


async def anime_info(message, commandpar, bot):
    if commandpar!=None:
        jikan = jk.Jikan()
        try:
            anime = jikan.search('anime', commandpar)['results'][0]
        except:
            raise entity.CommandError('Não consegui achar nenhum anime com esse nome.')
        

        emb = Embed(title=anime['title'], description=anime['synopsis'], color=bot.color)
        emb.set_thumbnail(url=anime['image_url']) 

        emb.add_field(name='Episódios:', value=anime['episodes'], inline=False)
        emb.add_field(name='Score (MyAnimeList):', value=anime['score'], inline=False)
        emb.add_field(name='Tipo:', value=anime['type'], inline=False)
        emb.add_field(name='Lançando:', value='Sim' if anime['airing'] else 'Não', inline=False)
        emb.add_field(name='Link:', value=f'[MyAnimeList]({anime["url"]})', inline=False)

        await message.channel.send(embed=emb)
    else: 
        raise entity.CommandError('Falta parametros nesse comando!')
entity.Command(name='anime_info', func=anime_info, category=category, desc=f'Informações sobre um anime.', aliases=['anime', 'ai', 'a'], args=[['anime', '*']])


async def character(message, commandpar, bot):
    if commandpar!=None:
        jikan = jk.Jikan()
        try:
            char = jikan.search('character', commandpar)['results'][0]
            emb = Embed(title=char['name'], description=' ,'.join(f'`{x}`' for x in char['alternative_names']), color=bot.color)
            emb.set_image(url=char['image_url'])

            _animes = ''
            animes = ''
            for ani in char['anime']: 
                _animes += f'[{ani["name"]}]({ani["url"]}), '
                if len(_animes) > 500:
                    break
                else:
                    animes = _animes

            if len(animes) > 0:
                animes = animes[:-2]
                emb.add_field(name='Animes:', value=animes, inline=False)



            _mangas = ''
            mangas = ''
            for manga in char['manga']:
                _mangas += f'[{manga["name"]}]({manga["url"]}), '
                if len(_mangas) > 500:
                    break
                else:
                    mangas = _mangas
    
            if len(mangas) > 0:
                mangas = mangas[:-2]
                emb.add_field(name='Mangas:', value=mangas, inline=False)


            await message.channel.send(embed=emb)
        
        except Exception as e:
            print(e)
            raise entity.CommandError('Não consegui achar nenhum personagem com esse nome.')
        
    else: 
        raise entity.CommandError('Falta parametros nesse comando!')
entity.Command(name='character', func=character, category=category, desc=f'Informações sobre um personagem.', aliases=['char', 'personagem'], args=[['char', '*']])


async def anime_list(message, commandpar, bot):
    if commandpar == None:
        animes = db.get_anime_notifier(str(message.author.id), bot.db_connection, column='userid')

        if len(animes) <= 0:
            raise entity.CommandError('Sua lista esta vazia!')

        scr = entity.Script(f'list_animes_{message.guild.id}', 'list_animes', message.guild.id, time_out=120)
        await scr.execute([message.channel, message.author, animes], bot)
    else:
        if len(message.mentions) != 0:
            user = message.mentions[0]
            animes = db.get_anime_notifier(str(user.id), bot.db_connection, column='userid')

            if len(animes) <= 0:
                raise entity.CommandError(f'A lista do(a) `{user.name}` esta vazia!')

            scr = entity.Script(f'list_animes_{message.guild.id}', 'list_animes', message.guild.id, time_out=120)
            await scr.execute([message.channel, user, animes], bot)


        else:
            raise entity.CommandError('Você precisa mencionar alguem para ver a lista dessa pessoa, ou usar o comando sem nenhum parametro para ver sua propria lista!')
entity.Command(name='anime_list', func=anime_list, category=category, desc=f'Liste todos os animes da sua lista, ou da pessoa mensionada.', aliases=['al'])
