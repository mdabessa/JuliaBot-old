import modules.database as db
import modules.entity as entity


category = 'Moderação'
entity.Command.newcategory(category, ':shield:Moderação.')


async def c_event(message, commandpar, connection, bot):
    if commandpar != None:
        eve = entity.Script.fetch_function(commandpar)
        if len(eve) == 0:
            raise entity.CommandError('Nenhum evento com esse nome!')
        
        eve = eve[0]
        try:
            scr = entity.Script(f'created_{commandpar}_{message.guild.id}', eve['name'], time_out=30)
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


async def clean_events(message, commandpar, connection, bot):
    scripts = entity.Script.get_scripts()
    for i in range(len(scripts)):
        scripts[0].close()

    await message.add_reaction('✅')
entity.Command(name='clean_events', func=clean_events, category=category, desc='Limpar todos os eventos.', aliases=['limpar_eventos', 'le'], perm=1)


async def setcoins(message, commandpar, connection, bot):
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
                    db.setpoints(user.id,message.guild.id,int(pointspar),connection)
                
                await message.channel.send(f'Coins definido como `{pointspar}` para : {", ".join(names)}')
            else:
                db.setpoints(message.author.id,message.guild.id,int(pointspar),connection)
                await message.channel.send(f'{message.author.mention} Seus Coins foram definido para `{pointspar}`')
        except:
            raise entity.CommandError('Não foi possivel realizar esta ação :worried:')

    else:
        raise entity.CommandError('Quantos coins ?')
entity.Command(name='setcoins', func=setcoins , category=category, desc=f'Definir os seus pontos, ou os dos usuarios marcados.', aliases=['definircoins', 'defcoins'], args=[['coins', '*'], ['pessoa', 'º']], perm=1)


async def addcoins(message, commandpar, connection, bot):
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
                    db.addpoints(user.id,message.guild.id,int(pointspar), connection)
                
                await message.channel.send(f'`{pointspar}` Coins adicionados para : {", ".join(names)}')
            else:
                db.addpoints(message.author.id,message.guild.id,int(pointspar),connection)
                await message.channel.send(f'{message.author.mention} Foram adicionados `{pointspar}` coins.')
        except:
            raise entity.CommandError('Não foi possivel realizar esta ação :worried:')
    else:
        raise entity.CommandError('Quantos pontos?')
entity.Command(name='addcoins', func=addcoins , category=category, desc=f'Adicionar pontos.', aliases=['adicionarcoins'], args=[['coins', '*'], ['pessoa', 'º']], perm=1)


async def subcoins(message, commandpar, connection, bot):
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
                    db.subpoints(user.id,message.guild.id,int(pointspar), connection)
                
                await message.channel.send(f'`{pointspar}` Coins foram removidos de : {", ".join(names)}')
            else:
                db.subpoints(message.author.id,message.guild.id,int(pointspar), connection)
                await message.channel.send(f'{message.author.mention} Foram removidos `{pointspar}` coins.')
        except:
            raise entity.CommandError('Não foi possivel realizar esta ação! :worried:')
    else:
        raise entity.CommandError('Quantos pontos?')
entity.Command(name='subcoins', func=subcoins , category=category, desc=f'Remover pontos.', aliases=['removercoins', 'removecoins'], args=[['coins', '*'], ['pessoa', 'º']], perm=1)


async def shopadditem(message, commandpar, connection, bot):
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

    db.additem(message.guild.id, message.author.id, item_name, price, connection)
    await message.channel.send(f'Item: `{item_name}` foi adicionado a loja por `{price}` coins!')
entity.Command(name='additem', func=shopadditem, category=category, desc=f'Adicionar um item a loja.', aliases=['adicionaritem'], args=[['preço', '*'], ['item', '*']], perm=1)


async def shopdelitem(message, commandpar, connection, bot):
    if commandpar == None:
        raise entity.CommandError('Qual item irá deletar?')

    try:
        item = int(commandpar)
    except:
        raise entity.CommandError('O item tem que ser referenciado com o um `ID`.')

    i = db.getitem(message.guild.id, item, connection)


    if i != None:
        db.delitem(message.guild.id, item, connection)
        await message.channel.send(f'{message.author.mention} removeu o item `{i["itemid"]} - {i["name"]}` da loja!')

    else:
        raise entity.CommandError(f'{message.author.mention} o item `{commandpar}` não existe.')
entity.Command(name='delitem', func=shopdelitem, category=category, desc=f'Deletar itens da loja.', aliases=['deleteitem', 'deletaritem', 'removeritem', 'removeitem'], args=[['id do item', '*']], perm=1)
