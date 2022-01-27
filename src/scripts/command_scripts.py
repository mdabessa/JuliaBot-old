import modules.database as db
import modules.entity as entity
import modules.utils as utils
from discord import Embed
from random import randint
import jikanpy as jk
from time import sleep


async def duel(cache, par, bot):
    if cache['status'] == 'created':
        msg = par[0]
        points = par[1]
        vs = msg.mentions[0]

        m = await msg.channel.send(f'{msg.author.mention} desafia {vs.mention} para um duelo valendo `{points}` coins!')

        await m.add_reaction('👍')
        await m.add_reaction('👎')

        cache['message'] = m
        cache['points'] = points
        cache['author'] = msg.author
        cache['vs'] = vs
        cache['status'] = 'started'
    else:
        m = cache['message']
        points = cache['points']
        author = cache['author']
        vs = cache['vs']

        react = par[0]
        emoji = par[1]
        if emoji == '👍' and vs == react:
            if randint(0,1) == 1:
                await m.channel.send(f'{vs.mention} aceitou o duelo e venceu! `{points}` coins // {author.mention} perdeu `{points}` coins :sob:')
                db.subpoints(author.id, m.guild.id, points, bot.db_connection)
                db.addpoints(vs.id, m.guild.id, points, bot.db_connection)

            else:
                await m.channel.send(f'{vs.mention} aceitou o duelo e perdeu! `{points}` coins // {author.mention} ganhou `{points}` coins :sunglasses:')
                db.subpoints(vs.id, m.guild.id, points, bot.db_connection)
                db.addpoints(author.id, m.guild.id, points, bot.db_connection)

            cache['status'] = 0
        elif emoji == '👎' and react in [vs, author]:
            await m.channel.send(f'{react.mention} recusou o duelo!')

            cache['status'] = 0
entity.Script.new_function(duel, tag='command', limit_by_name=1)


async def roulette(cache, par, bot):
    if cache['status'] == 'created':
        channel = par[0]
        author = par[1]
        points = par[2]


        m = await channel.send(f'{author.mention}, Tem certeza que deseja roletar `{points}` coins?')
        await m.add_reaction('👍')
        await m.add_reaction('👎')

        cache['chance'] = par[3]
        cache['points'] = points
        cache['author'] = author
        cache['message'] = m
        cache['status'] = 'started'

    else:
        react = par[0]
        emoji = par[1]
        message = cache['message']
        roulette_chance = cache['chance']
        points = cache['points']
        author = cache['author']

        if emoji == '👍' and author == react:
            p = db.getpoints(author.id, message.guild.id, bot.db_connection)

            if points < p:
                if randint(0,100) < roulette_chance:
                    db.addpoints(author.id,message.guild.id, points, bot.db_connection)
                    await message.channel.send(f'{author.mention} Ganhou `{points}` coins! :money_mouth:')
                else:
                    db.subpoints(author.id, message.guild.id, points, bot.db_connection)
                    await message.channel.send(f'{author.mention} Perdeu `{points}` coins! :sob:')

            elif points == p:
                if randint(0,100) < roulette_chance:
                    db.addpoints(author.id,message.guild.id, points, bot.db_connection)
                    await message.channel.send(f'{author.mention} roletou tudo e ganhou `{points}` coins, dobrando sua fortuna! :sunglasses:')
                else:
                    db.subpoints(author.id, message.guild.id, points, bot.db_connection)
                    await message.channel.send(f'{author.mention} roletou tudo e perdeu `{points}` coins, zerando seus pontos! :rofl: :rofl: :rofl:')
            
            else:
                await message.channel.send(f'{author.mention}, Voce não possui pontos suficiente!')

            cache['status'] = 0
        elif emoji == '👎' and author == react:
            await message.channel.send(f'{react.mention} cancelou a roleta! :no_entry_sign:')
            cache['status'] = 0
entity.Script.new_function(roulette, tag='command', limit_by_name=4)


async def add_anime_confirm(cache, par, bot):
    if cache['status'] == 'created':
        channel = par[0]
        anime = par[2]

        desc = f'Nome: {anime["title"]}\n' + \
            f'Episódios: {anime["episodes"]}\n' + \
            f'Tipo: {anime["type"]}\n' + \
            f'Lançando?: {"Sim" if anime["airing"] else "Não"}\n' + \
            f'Link: [MyAnimeList]({anime["url"]})'
            

        emb = Embed(title='Confirmar anime para adicionar:', description=desc, color=bot.color)
        emb.set_thumbnail(url=anime['image_url'])

        m = await channel.send(embed=emb)
        await m.add_reaction('👍')
        await m.add_reaction('👎')

        cache['message'] = m
        cache['author'] = par[1]
        cache['anime'] = anime
        cache['status'] = 'started'
    else:
        react = par[0]
        emoji = par[1]
        message = cache['message']
        author = cache['author']
        anime = cache['anime']

        if emoji == '👍' and author == react:
            if db.verify_anime_notifier(author.id, anime['mal_id'], bot.db_connection) == None:
                db.add_anime(author.id, anime['mal_id'], bot.db_connection)
            else:
                await message.channel.send('Esse anime ja esta na sua lista de notificações.')
                await message.add_reaction('❌')
                cache['status'] = 0
                return

            await message.add_reaction('✅')
            cache['status'] = 0
        
        elif emoji == '👎' and author == react:
            await message.add_reaction('❌')
            cache['status'] = 0
entity.Script.new_function(add_anime_confirm, tag='command', limit_by_name=2)


async def del_anime_confirm(cache, par, bot):
    if cache['status'] == 'created':
        channel = par[0]
        anime = par[2]

        desc = f'Nome: {anime["title"]}\n' + \
            f'Episódios: {anime["episodes"]}\n' + \
            f'Tipo: {anime["type"]}\n' + \
            f'Lançando?: {"Sim" if anime["airing"] else "Não"}\n' + \
            f'Link: [MyAnimeList]({anime["url"]})'
            

        emb = Embed(title='Confirmar anime para remover:', description=desc, color=bot.color)
        emb.set_thumbnail(url=anime['image_url'])

        m = await channel.send(embed=emb)
        await m.add_reaction('👍')
        await m.add_reaction('👎')

        cache['message'] = m
        cache['author'] = par[1]
        cache['anime'] = anime
        cache['status'] = 'started'
    else:
        react = par[0]
        emoji = par[1]
        message = cache['message']
        author = cache['author']
        anime = cache['anime']

        if emoji == '👍' and author == react:
            if db.verify_anime_notifier(author.id, anime['mal_id'], bot.db_connection) != None:
                db.del_anime(author.id, anime['mal_id'], bot.db_connection)
            else:
                await message.channel.send('Esse anime não esta na sua lista de notificações.')
                await message.add_reaction('❌')
                cache['status'] = 0
                return

            await message.add_reaction('✅')
            cache['status'] = 0
        
        elif emoji == '👎' and author == react:
            await message.add_reaction('❌')
            cache['status'] = 0
entity.Script.new_function(del_anime_confirm, tag='command', limit_by_name=2)


async def list_animes(cache, par, bot):
    if cache['status'] == 'created':
        channel = par[0]
        _animes = par[2]
        animes = []
        m = await channel.send('Buscando animes...')

        cache['author'] = par[1]
        cache['index'] = 0
        cache['status'] = 'searching'
        cache['animes'] = animes
        cache['message'] = m
                
        await m.add_reaction('⬅️')
        await m.add_reaction('➡️')
        await m.add_reaction('❌')

        jikan = jk.Jikan()
        for i, _anime in enumerate(_animes):
            anime = jikan.anime(_anime['alid'])
            animes.append(anime)
            
            if len(animes) > 0:
                index = cache['index']
                anime = animes[index]
                desc = f'Nome: {anime["title"]}\n' + \
                    f'Episódios: {anime["episodes"]}\n' + \
                    f'Tipo: {anime["type"]}\n' + \
                    f'Lançando?: {"Sim" if anime["airing"] else "Não"}\n' + \
                    f'Link: [MyAnimeList]({anime["url"]})'

                emb = Embed(title='Anime:', description=desc, color=bot.color)
                emb.set_thumbnail(url=anime['image_url'])

                if i != len(_animes)-1:
                    emb.set_footer(text=f'{index+1}/{len(animes)} animes  -  Pesquisando: {len(animes)}/{len(_animes)} animes.')
                    sleep(4)
                else:
                    emb.set_footer(text=f'{index+1}/{len(animes)} animes.')
                
                await m.edit(embed=emb, content='')
            else:
                await m.edit(embed=None, content='Sua lista esta vazia!')

        cache['status'] = 'started'

    elif cache['status'] == 'searching':
        emoji = par[1]
        index = cache['index']
        animes = cache['animes']
        author = cache['author']
        m = cache['message']

        emoji_author = par[0]
        
        if emoji == '➡️':
            index += 1
            if index >= len(animes):
                index = 0

        if emoji == '⬅️':
            index -= 1
            if index < 0:
                index = len(animes)-1
        
        if emoji == '❌' and author == emoji_author:
            if index < len(animes):
                anime = animes[index]
                db.del_anime(author.id, anime['mal_id'], bot.db_connection)
                animes.remove(anime)
        
                if index >= len(animes):
                    index = len(animes) - 1

                await m.channel.send(f'`{anime["title"]}` removido da sua lista com sucesso!')
        
        cache['index'] = index

    elif cache['status'] == 'started':
        m = cache['message']
        animes = cache['animes']
        index = cache['index']
        author = cache['author']

        emoji_author = par[0]
        emoji = par[1]

        if emoji == '➡️':
            index += 1
            if index >= len(animes):
                index = 0

        if emoji == '⬅️':
            index -= 1
            if index < 0:
                index = len(animes)-1

        if emoji == '❌' and author == emoji_author:
            if index < len(animes):
                anime = animes[index]
                db.del_anime(author.id, anime['mal_id'], bot.db_connection)
                animes.remove(anime)
        
                if index >= len(animes):
                    index = len(animes) -1

                await m.channel.send(f'`{anime["title"]}` removido da sua lista com sucesso!')
                        
        cache['index'] = index
        
        if len(animes) > 0:
            anime = animes[index]
            desc = f'Nome: {anime["title"]}\n' + \
                f'Episódios: {anime["episodes"]}\n' + \
                f'Tipo: {anime["type"]}\n' + \
                f'Lançando: {"Sim" if anime["airing"] else "Não"}\n' + \
                f'Link: [MyAnimeList]({anime["url"]})'

            emb = Embed(title='Anime:', description=desc, color=bot.color)
            emb.set_thumbnail(url=anime['image_url'])
            emb.set_footer(text=f'{index+1}/{len(animes)} animes.')

            await m.edit(embed=emb, content='')
        else:
            await m.edit(embed=None, content='Sua lista esta vazia!')
entity.Script.new_function(list_animes, tag='command', limit_by_name=2)


async def pin(cache, par, bot):
    if cache['status'] == 'created':
        cache['channel'] = par[0]
        cache['embed'] = par[1]
        cache['message'] = await cache['channel'].send(embed=cache['embed'])
        cache['status'] = 'started'

    else:
        channel = par[0].channel
        m = cache['message']

        if channel.id == m.channel.id:
            await m.delete()
            
            emb = cache['embed']
            m = await channel.send(embed=emb)
            cache['message'] = m
entity.Script.new_function(pin, tag='command', limit_by_name=1, triggers=['message'])
