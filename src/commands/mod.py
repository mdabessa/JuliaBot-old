import modules.database as db
import modules.entity as entity
from discord import Embed


category = 'Moderação'
entity.Command.newcategory(category, ':shield:Moderação.')


async def c_event(message, commandpar, bot):
    if commandpar != None:
        eve = entity.Script.fetch_function(commandpar)
        if len(eve) == 0:
            raise entity.CommandError('Nenhum evento com esse nome!')
        
        eve = eve[0]
        try:
            scr = entity.Script(f'created_{commandpar}_{message.guild.id}', eve['name'], message.guild.id, time_out=30)
            await message.channel.send(f'{message.author.mention} evento `{eve["name"]}` criado com sucesso!')
        except entity.Script.ScriptIndiceLimit:
            prefix = db.getserver(message.guild.id, bot.db_connection)['prefix']
            raise entity.CommandError(f'{message.author.mention}, Número `máximo` de eventos simultâneos atingido!, finalize os eventos que ja estão ocorrendo ou'+
                f'utilize o comando `{prefix}clean_events`, para deletar todos os eventos que estão ocorrendo no momento.')
        except Exception as e:
            print(e)

        await scr.execute([message.channel], bot)
    else:
        raise entity.CommandError('Você precisa declarar qual evento você quer criar!')
entity.Command(name='c_event', func=c_event , category=category, desc=f'Criar um evento.', aliases=['c_evento', 'createevent', 'criarevento'], args=[['evento', '*']], perm=1)


async def clean_events(message, commandpar, bot):
    scripts = entity.Script.fetch_script(message.id, by='guild_id')
    for i in range(len(scripts)):
        scripts[0].close()

    await message.add_reaction('✅')
entity.Command(name='clean_events', func=clean_events, category=category, desc='Limpar todos os eventos.', aliases=['limpar_eventos', 'le'], perm=1)


async def setcoins(message, commandpar, bot):
    if commandpar != None:
        try:
            pointspar = int(commandpar.split()[0])
        except:
            raise entity.CommandError('Só `numeros inteiros` podem ser definidos como coins')

        try:
            if len(message.mentions) > 0:
                names = []
                for user in message.mentions:
                    names.append(user.name)
                    db.setpoints(user.id, message.guild.id, int(pointspar), bot.db_connection)
                
                await message.channel.send(f'Coins definido como `{pointspar}` para : {", ".join(names)}')
            else:
                db.setpoints(message.author.id, message.guild.id, int(pointspar), bot.db_connection)
                await message.channel.send(f'{message.author.mention} Seus Coins foram definido para `{pointspar}`')
        except:
            raise entity.CommandError('Não foi possivel realizar esta ação :worried:')

    else:
        raise entity.CommandError('Quantos coins ?')
entity.Command(name='setcoins', func=setcoins , category=category, desc=f'Definir os seus pontos, ou os dos usuarios marcados.', aliases=['definircoins', 'defcoins'], args=[['coins', '*'], ['pessoa', 'º']], perm=1)


async def addcoins(message, commandpar, bot):
    if commandpar != None:
        try:
            pointspar = int(commandpar.split()[0])
        except:
            raise entity.CommandError('Pontos tem que ser um `numero inteiro`!')

        try:
            if len(message.mentions) > 0:
                names = []
                for user in message.mentions:
                    names.append(user.name)
                    db.addpoints(user.id,message.guild.id,int(pointspar), bot.db_connection)
                
                await message.channel.send(f'`{pointspar}` Coins adicionados para : {", ".join(names)}')
            else:
                db.addpoints(message.author.id,message.guild.id,int(pointspar), bot.db_connection)
                await message.channel.send(f'{message.author.mention} Foram adicionados `{pointspar}` coins.')
        except:
            raise entity.CommandError('Não foi possivel realizar esta ação :worried:')
    else:
        raise entity.CommandError('Quantos pontos?')
entity.Command(name='addcoins', func=addcoins , category=category, desc=f'Adicionar pontos.', aliases=['adicionarcoins'], args=[['coins', '*'], ['pessoa', 'º']], perm=1)


async def subcoins(message, commandpar, bot):
    if commandpar != None:
        try:
            pointspar = int(commandpar.split()[0])
        except:
            raise entity.CommandError('Pontos tem que ser um `numero inteiro`!')

        try:
            if len(message.mentions) > 0:
                names = []
                for user in message.mentions:
                    names.append(user.name)
                    db.subpoints(user.id,message.guild.id,int(pointspar), bot.db_connection)
                
                await message.channel.send(f'`{pointspar}` Coins foram removidos de : {", ".join(names)}')
            else:
                db.subpoints(message.author.id,message.guild.id,int(pointspar), bot.db_connection)
                await message.channel.send(f'{message.author.mention} Foram removidos `{pointspar}` coins.')
        except:
            raise entity.CommandError('Não foi possivel realizar esta ação! :worried:')
    else:
        raise entity.CommandError('Quantos pontos?')
entity.Command(name='subcoins', func=subcoins , category=category, desc=f'Remover pontos.', aliases=['removercoins', 'removecoins'], args=[['coins', '*'], ['pessoa', 'º']], perm=1)


async def shopadditem(message, commandpar, bot):
    if commandpar == None:
        raise entity.CommandError('Falta parametros!')

    cmdpar = commandpar.split()
    if len(cmdpar) < 2:
        raise entity.CommandError('Falta parametros!')

    try:
        price = int(cmdpar[0])
    except:
        raise entity.CommandError('Qual é o preco do item?')
    
    item_name = ' '.join(cmdpar[1:])

    db.additem(message.guild.id, message.author.id, item_name, price, bot.db_connection)
    await message.channel.send(f'Item: `{item_name}` foi adicionado a loja por `{price}` coins!')
entity.Command(name='additem', func=shopadditem, category=category, desc=f'Adicionar um item a loja.', aliases=['adicionaritem'], args=[['preço', '*'], ['item', '*']], perm=1)


async def shopdelitem(message, commandpar, bot):
    if commandpar == None:
        raise entity.CommandError('Qual item irá deletar?')

    try:
        item = int(commandpar)
    except:
        raise entity.CommandError('O item tem que ser referenciado com o um `ID`.')

    i = db.getitem(message.guild.id, item, bot.db_connection)


    if i != None:
        db.delitem(message.guild.id, item, bot.db_connection)
        await message.channel.send(f'{message.author.mention} removeu o item `{i["itemid"]} - {i["name"]}` da loja!')

    else:
        raise entity.CommandError(f'{message.author.mention} o item `{commandpar}` não existe.')
entity.Command(name='delitem', func=shopdelitem, category=category, desc=f'Deletar itens da loja.', aliases=['deleteitem', 'deletaritem', 'removeritem', 'removeitem'], args=[['id do item', '*']], perm=1)


async def pin(message, commandpar, bot):
    if commandpar == None:
        raise entity.CommandError('Está faltando parâmetros neste comando!')
    
    else:
        emb = Embed(title='Mensagem Fixada!', description=commandpar, color=bot.color)
        scr = entity.Script(f'pinned_message_{message.guild.id}', 'pin', message.guild.id, time_out=86400)
        await scr.execute([message.channel, emb], bot)
entity.Command(name='pin', func=pin, category=category, desc=f'Fixar uma mensagem no servidor.', aliases=['pinar', 'fix', 'fixar'], args=[['Mensagem', '*']], perm=1)


async def unpin(message, commandpar, bot):
    scr = entity.Script.fetch_script(f'pinned_message_{message.guild.id}', by='refname')
    if len(scr) > 0:
        scr = scr[0]
        scr.close()
        await message.channel.send('Menssagem desfixada!')

    else:
        raise entity.CommandError('Não existe nenhuma mensagem fixada!')
entity.Command(name='unpin', func=unpin, category=category, desc=f'Desfixar uma mensagem fixada com o comando "pin".', aliases=['despinar', 'unfix', 'desfixar'], args=[['Mensagem', '*']], perm=1)
