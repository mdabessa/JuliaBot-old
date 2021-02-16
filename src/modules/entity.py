import time
import traceback
import modules.database as db

mutes = []


class CommandError(Exception):
    pass


class command():
    commands = []
    def __init__(self, name, func, desc='Nothing', cost=0, perm=0):
        self.name = name
        self.func = func
        self.desc = desc
        self.cost = cost
        self.perm = perm

        command.commands.append(self)

    async def execute(self, message, param, connection, bot):
        await self.func(message, param, connection, bot)


    @classmethod
    async def trycommand(cls, message, content, connection, masterid, bot):
        contlist = content.split()
        contcommand = str(contlist[0]).lower()

        if len(contlist) > 1:
            commandpar = ' '.join(contlist[1:])
        else:
            commandpar = None


        cmd = command.getcommand(message.guild.id, contcommand,connection)
        if cmd == None:
            return

        if cmd['active'] == 0:
            return

        if cmd['permission'] == 2:
            if message.author.id != masterid:
                await message.channel.send('Voce não possui permissão para isto! :sob:')
                return

        if cmd['permission'] >= 1:
            if not message.author.guild_permissions.administrator:
                await message.channel.send('Voce não possui permissão para isto! :sob:')
                return

        if cmd['price'] > 0:
            points = db.getpoints(message.author.id, message.guild.id, connection)
            if points < cmd['price']:
                await message.channel.send(f'{message.author.mention}, Voce não possui coins suficiente, custo do comando é de {cmd["price"]}')
                return
            else:
                await message.channel.send(f'{message.author.mention} comprou {cmd["name"]} [-{cmd["price"]}]')
                db.subpoints(message.author.id, message.guild.id, cmd['price'], connection)

        if cmd['overwritten'] == 0:
            try:
                _cmd = [x for x in command.commands if x.name == cmd['name']][0]
                await _cmd.execute(message, commandpar, connection, bot)
            except CommandError as e:
                await message.channel.send(e)
                if cmd['price'] > 0:
                    db.addpoints(message.author.id, message.guild.id, cmd['price'], connection)
            except Exception:
                traceback.print_exc()
        else:
            await message.channel.send(cmd['message'])


    @classmethod
    def getcommand(cls, guildid, name, connection):
        _command = db.getservercommand(guildid, name, connection)
        if _command == None:
            for cmd in command.commands:
                if cmd.name == name:
                    _cmd = ['', cmd.name, '', cmd.desc, cmd.perm, cmd.cost, 1, 0]
                    leg = ['serverid', 'name', 'message', 'description', 'permission', 'price', 'active', 'overwritten']
                    result = dict(zip(leg, _cmd))
                    return result
        else:
            return _command

    @classmethod
    def getallcommands(cls, guildid, connection):
        _commands = db.getallserverscommands(guildid, connection)

        for cmd in command.commands:
            c = 0
            for i in _commands:
                if i['name'] == cmd.name:
                    c = 1

            if c == 1:
                continue

            _cmd = ['', cmd.name, '', cmd.desc, cmd.perm, cmd.cost, 1, 0]
            leg = ['serverid', 'name', 'message', 'description', 'permission', 'price', 'active', 'overwritten']
            _commands.append(dict(zip(leg, _cmd)))

        return _commands


class event():
    events = []
    def __init__(self, name:str, createfunc, executefunc, trigger='react', desc='Nothing', command_create=True, loop_event_create=True):
        self.name = name
        self.createfunc = createfunc
        self.exec = executefunc
        self.desc = desc
        self.trigger = trigger
        self.command_create = command_create
        self.loop_event_create = loop_event_create
        self.cache = dict()
        event.events.append(self)

    async def create(self, par, ind:str):
        cache = self.getcache(ind)

        if cache == None:
            cache = await self.createfunc(par)
            self.cache[ind] = cache


    async def execute(self, par, ind:str):
        cache = self.getcache(ind)

        if cache == None:
            return
        
        if cache == True:
            self.clear(ind)
            return

        cache = await self.exec(par, cache)
        self.cache[ind] = cache


    def msgvalidation(self, msg, ind:str):
        cache = self.getcache(ind)
        if cache == None:
            return False
        
        if cache == True:
            return False

        if cache[0] == msg:
            return True
        else:
            return False


    def getcache(self, ind):
        ind = str(ind)
        try:
            cache = self.cache[ind]
        except:
            cache = None

        return cache


    def clear(self, ind:str):
        if self.getcache(ind) != None:
            self.cache.pop(ind)


class timer():
    timers = []

    @classmethod
    def timer(cls, ind, segs, recreate=False):
        timenow = time.time()

        check = 0
        for i in cls.timers:
            if i[0] == ind:
                check = 1
                if (timenow - i[1]) >= i[2]:
                    cls.timers.remove(i)
                    if recreate:
                        cls.timers.append([ind,timenow,segs])

                    return True
                else:
                    return False
        
        if check == 0:
            if segs > 0:
                cls.timers.append([ind,timenow,segs])
            return False