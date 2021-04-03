import modules.database as db
import modules.entity as entity


category = 'Moderação'
entity.Command.newcategory(category, ':shield:Moderação.')


async def c_event(message, commandpar, connection, bot):
    if commandpar != None:
        marc = 0
        for eve in entity.Event.events:
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
entity.Command(name='c_event', func=c_event , category=category, desc=f'Criar um evento.', aliases=['c_evento', 'createevent', 'criarevento'], args=[['evento', '*']], perm=1)



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

    db.additem(message.guild.id, item_name, price, connection)
    await message.channel.send(f'Item: `{item_name}` foi adicionado a loja por `{price}` coins!')
entity.Command(name='additem', func=shopadditem, category=category, desc=f'Adicionar um item a loja.', aliases=['adicionaritem'], args=[['preço', '*'], ['item', '*']], perm=1)


async def shopdelitem(message, commandpar, connection, bot):
    if commandpar == None:
        raise entity.CommandError('Qual item irá deletar?')

    try:
        item = int(commandpar)
    except:
        raise entity.CommandError('O item tem que ser referenciado com o um `ID`.')

    items = db.getshop(message.guild.id, connection)

    marc = 0
    for i in items:
        if i[1] == item:
            marc = 1
            db.delitem(message.guild.id, item, connection)
            await message.channel.send(f'{message.author.mention} removeu o item `{i[1]} - {i[2]}` da loja!')

    if marc == 0:
        raise entity.CommandError(f'{message.author.mention} o item `{commandpar}` não existe.')
entity.Command(name='delitem', func=shopdelitem, category=category, desc=f'Deletar itens da loja.', aliases=['deleteitem', 'deletaritem', 'removeritem', 'removeitem'], args=[['id do item', '*']], perm=1)
