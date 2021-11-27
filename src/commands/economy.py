from random import randint
import discord
import modules.database as db
import modules.entity as entity


category = 'Economia'
entity.Command.newcategory(category, ':coin:Economia.')


async def coins(message, commandpar, bot):
    if len(message.mentions) >= 1 and len(message.mentions) <=3:
        for mentioned in message.mentions:
            points = db.getpoints(mentioned.id, message.guild.id, bot.db_connection)
            await message.channel.send(f'{mentioned.name} possui `{points}` coins.')

    else:
        points = db.getpoints(message.author.id, message.guild.id, bot.db_connection)
        await message.channel.send(f'{message.author.mention}, você possui `{points}` coins.')
entity.Command(name='coins', func=coins, category=category, desc='Verificar os pontos.', aliases=['moedas', 'money'], args=[['pessoa', 'º']])


async def coinsrank(message, commandpar, bot):
    rank = db.rankpoints(message.guild.id, bot.db_connection)
    if rank == None:   
        raise entity.CommandError('Não foi possivel execultar esta ação!')

    emb = discord.Embed(title='Rank', color=bot.color)
    for num, i in enumerate(rank):
        user = bot.get_user(int(i[1]))
        points = i[2]

        if num == 0:
            medal = ':first_place:'
        if num == 1:
            medal = ':second_place:'
        if num == 2:
            medal = ':third_place:'
        if num == 3:
            medal = ':four:'
        if num == 4:
            medal = ':five:'
        

        emb.add_field(name=f'{medal}{user.name}', value=f':coin:{points}c', inline=False)
    
    await message.channel.send(embed=emb)
entity.Command(name='rank', func=coinsrank, category=category, desc='Top coins do servidor.', aliases=['top'])


async def roulette(message, commandpar, bot):
    if commandpar != None:
        chance = 33 #x/100
        p = db.getpoints(message.author.id, message.guild.id, bot.db_connection)

        if commandpar == 'all':
            points = p
        else:
            try:
                points = int(commandpar)
            except:
                raise entity.CommandError('Não posso roletar nada que não seja um `numero inteiro` :pensive:')

        scr = entity.Script(f'roulette_{message.guild.id}', 'roulette', message.guild.id, time_out=30)
        await scr.execute([message.channel, message.author, points, chance], bot)

    else:
        raise entity.CommandError('Quantos coins você quer roletar? :thinking:')
entity.Command(name='roulette', func=roulette, category=category, desc=f'Roletar pontos.', aliases=['roletar'], args=[['coins', '*']])


async def shop(message, commandpar, bot):
    items = db.getshop(message.guild.id, bot.db_connection)

    if len(items) == 0:
        await message.channel.send('Esse servidor não possui itens a venda!')

    else:
        img = discord.File('src/images/coin.png')
        emb = discord.Embed(title='Loja de itens', color=bot.color)
        emb.set_thumbnail(url='attachment://coin.png')

        for i in items:
            emb.add_field(name=i['name'], value=f'id: {i["itemid"]}', inline=True)
        
        prefix = db.getserver(message.guild.id, bot.db_connection)["prefix"]
        emb.set_footer(text=f'{prefix}buy [id] // {prefix}iteminfo [id]')
        await message.channel.send(file=img, embed=emb)
entity.Command(name='shop', func=shop, category=category, desc=f'Loja de itens.', aliases=['loja'])


async def iteminfo(message, commandpar, bot):
    if commandpar == None:
        raise entity.CommandError('Qual item você quer ver os detalhes ?')
    try:
        item_id = int(commandpar)
    except:
        raise entity.CommandError('O item tem que ser referenciado com o um `ID`.')
    
    item = db.getitem(message.guild.id, item_id, bot.db_connection)

    if item != None:
        user = bot.get_user(int(item['userid']))
        
        emb = discord.Embed(title=item['name'], color=bot.color)
        emb.add_field(name='Valor:', value=f'{item["price"]}:coin:')
        if user != None:
            emb.set_author(name=user.name, icon_url=user.avatar_url)

        emb.set_footer(text=f'{db.getserver(message.guild.id, bot.db_connection)["prefix"]}buy {item["itemid"]}')
        await message.channel.send(embed=emb)
    else:
        raise entity.CommandError(f'{message.author.mention} o item `{commandpar}` não existe.')
entity.Command(name='iteminfo', func=iteminfo, category=category, desc='Veja as informações de um item da loja.', aliases=['ii'], args=[['id do item', '*']])


async def buyitem(message, commandpar, bot):
    if commandpar == None:
        raise entity.CommandError('Qual item ira comprar ?')
    
    try:
        item = int(commandpar)
    except:
        raise entity.CommandError('O item tem que ser referenciado com o um `ID`.')

    i = db.getitem(message.guild.id, item, bot.db_connection)
    
    if i != None:
        points = db.getpoints(message.author.id, message.guild.id, bot.db_connection)

        if i['price'] > points:
            raise entity.CommandError('Coins insuficientes!')

        db.subpoints(message.author.id, message.guild.id, i['price'], bot.db_connection)
        await message.channel.send(f'{message.author.mention} comprou `{i["itemid"]} - {i["name"]}` por `{i["price"]}c`.')

    else:
        raise entity.CommandError(f'{message.author.mention} o item `{commandpar}` não existe.')
entity.Command(name='buy', func=buyitem, category=category, desc=f'Comprar um item.', aliases=['comprar'], args=[['id do item', '*']])


async def distance(message, commandpar, bot):
    if len(message.mentions) < 1:
        raise entity.CommandError('Você precisa/deve mensionar apenas `1 pessoa`!')

    p1 = db.getpoints(message.author.id, message.guild.id, bot.db_connection)
    p2 = db.getpoints(message.mentions[0].id, message.guild.id, bot.db_connection)

    dif = p1 - p2

    if dif < 0:
        await message.channel.send(f'{message.author.mention}, {message.mentions[0].mention} possui `{abs(dif)}` coins a `mais` que você!')

    elif dif == 0:
        await message.channel.send(f'{message.author.mention}, {message.mentions[0].mention} possui a `mesma` quantidade de coins que você!')

    elif dif > 0:
        await message.channel.send(f'{message.author.mention}, {message.mentions[0].mention} possui `{dif}` coins a `menos` que você!')
entity.Command(name='distance', func=distance, category=category, desc=f'Calcula a diferença de coins entre você e outra pessoa.', aliases=['distancia', 'dist', 'distcoins', 'dc'], args=[['pessoa', '*']])
