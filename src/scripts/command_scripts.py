import modules.database as db
import modules.entity as entity
import modules.utils as utils
from discord import Embed
from random import randint, shuffle, choice


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