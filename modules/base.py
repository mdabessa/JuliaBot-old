from os import environ
from environs import Env
import time, discord
import traceback


env = Env()
env.read_env()

db_url = environ['DATABASE_URL']
token = environ['DiscordToken']
masterid = int(environ['master_id'])
debug = bool(int(environ['debug']))

mutes = []


class CommandError(Exception):
    pass


class command():
    commands = []
    prefix = 'j!'
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


        cmd = getcommand(message.guild.id, contcommand,connection)
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
            points = getpoints(message.author.id, message.guild.id, connection)
            if points < cmd['price']:
                await message.channel.send(f'{message.author.mention}, Voce não possui coins suficiente, custo do comando é de {cmd["price"]}')
                return
            else:
                await message.channel.send(f'{message.author.mention} comprou {cmd["name"]} [-{cmd["price"]}]')
                subpoints(message.author.id, message.guild.id, cmd['price'], connection)

        if cmd['overwritten'] == 0:
            try:
                _cmd = [x for x in command.commands if x.name == cmd['name']][0]
                await _cmd.execute(message, commandpar, connection, bot)
            except CommandError as e:
                await message.channel.send(e)
                if cmd['price'] > 0:
                    addpoints(message.author.id, message.guild.id, cmd['price'], connection)
            except Exception:
                traceback.print_exc()
        else:
            await message.channel.send(cmd['message'])


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


def getpoints(userid, guildid, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
        """
        SELECT * FROM Users WHERE ServerId = '{sid}' and UserId = '{uid}'

        """.format(uid=str(userid), sid=str(guildid))
        )
        result = cursor.fetchall()
        points = result[0][2]
    except:
        cursor.execute(
            """
            INSERT INTO Users(ServerId, UserId, Points)
            VALUES('{sid}', '{uid}', 0)
            """.format(uid=str(userid), sid=str(guildid))
        )
        connection.commit()
        points = 0

    
    return points 


def setpoints(userid, guildid, points, connection):
    cursor = connection.cursor()
    getpoints(userid,guildid, connection)
    cursor.execute(
    """
    UPDATE Users
    SET Points = {p}
    WHERE ServerId='{sid}' and UserId='{uid}'
    """.format(p=points,sid=str(guildid),uid=str(userid))
    )
    connection.commit()


def addpoints(userid, guildid, points, connection):
    p = getpoints(userid, guildid, connection)
    setpoints(userid, guildid, p + points, connection)


def subpoints(userid, guildid, points, connection):
    p = getpoints(userid, guildid, connection)
    if points > p:
        setpoints(userid,guildid, 0, connection)
    else:
        setpoints(userid, guildid, (p - points), connection)


def rankpoints(guildid, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
        """
        SELECT * FROM Users
        WHERE ServerId = '{sid}'
        ORDER BY Points DESC
        LIMIT 5
        """.format(sid=str(guildid))
        )
        result = cursor.fetchall()

        return result
    except:
        return None


def getshop(guildid, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
        """
        SELECT * FROM Shop
        WHERE ServerId = '{sid}'
        ORDER BY Price Desc
        """.format(sid=str(guildid))
        )
        result = cursor.fetchall()

        return result
    except:
        return []


def additem(guildid, item_name, price, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
        INSERT INTO Shop(ServerId, name, price)
        VALUES('{sid}', '{n}', '{p}')
                
    '''.format(sid=str(guildid), n=item_name, p=price)
    )
    connection.commit()


def delitem(guildid, itemid, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
        DELETE FROM Shop
        WHERE itemid = {iid} AND serverid = '{sid}';
                
    '''.format(sid=str(guildid), iid=itemid)
    )
    connection.commit()


def getcommand(guildid, name, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
        SELECT * FROM Commands
        WHERE ServerId = '{sid}' AND Name = '{n}' 

    '''.format(sid=str(guildid), n=str(name))
    )
    leg = ['serverid', 'name', 'message', 'description', 'permission', 'price', 'active', 'overwritten']
    r = cursor.fetchone()
    try:
        result = dict(zip(leg, r))
        return result
    except:
        c = 0
        for cmd in command.commands:
            if cmd.name == name:
                c=1
                _cmd = ['', cmd.name, '', cmd.desc, cmd.perm, cmd.cost, 1, 0]
                result = dict(zip(leg, _cmd))
                return result
        
        if c == 0:
            return None


def getallcommands(guildid, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
        SELECT * FROM Commands
        WHERE ServerId = '{gid}'

    '''.format(gid=str(guildid))
    )

    r = cursor.fetchall()
    leg = ['serverid', 'name', 'message', 'description', 'permission', 'price', 'active', 'overwritten']
    result = [dict(zip(leg, i)) for i in r]

    for cmd in command.commands:
        c = 0
        for i in result:
            if i['name'] == cmd.name:
                c = 1

        if c == 1:
            continue

        _cmd = ['', cmd.name, '', cmd.desc, cmd.perm, cmd.cost, 1, 0] 
        result.append(dict(zip(leg, _cmd)))
        


    return result


def addcommand(guildid, connection, name, message='', description='', permission=0, price=0, active=1, overwritten=1):
    cursor = connection.cursor()

    cursor.execute(
    """
    INSERT INTO Commands(ServerId, Name, Message, Description, Permission, Price, Active, Overwritten)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
    """,
    (str(guildid), str(name).lower(), str(message), str(description), int(permission), int(price), int(active), int(overwritten))
    )
    
    connection.commit()


def delcommand(guildid, connection, name):
    cursor = connection.cursor()
    cursor.execute(
    '''
    DELETE FROM Commands WHERE ServerId='{gid}' AND Name='{n}'
    '''.format(gid=str(guildid), n=name)
    )
    connection.commit()