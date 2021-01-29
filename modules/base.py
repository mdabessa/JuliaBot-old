from os import environ
from environs import Env
import time, discord



env = Env()
env.read_env()

db_url = environ['DATABASE_URL']
token = environ['DiscordToken']
masterid = int(environ['master_id'])
debug = bool(int(environ['debug']))

mutes = []


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
        contcommand = contlist[0]

        if len(contlist) > 1:
            commandpar = ' '.join(contlist[1:])
        else:
            commandpar = None


        for cmd in command.commands:
            if cmd.name == contcommand:
                if cmd.perm == 2:
                    if message.author.id != masterid:
                        await message.channel.send('Voce não possui permissão para isto :sob:')
                        return

                if cmd.perm == 1:
                    if not message.author.guild_permissions.administrator:
                        await message.channel.send('Voce não possui permissão para isto :sob:')
                        return

                if cmd.cost > 0:
                    points = getpoints(message.author.id, message.guild.id, connection)
                    if points < cmd.cost:
                        await message.channel.send(f'{message.author.mention}, Voce não possui coins suficiente, custo do comando é de {cmd.cost}')
                        return
                    else:
                        await message.channel.send(f'{message.author.mention} comprou {cmd.name} [-{cmd.cost}]')
                        subpoints(message.author.id, message.guild.id, cmd.cost, connection)

                try:
                    await cmd.execute(message, commandpar, connection, bot)
                except Exception as e:
                    await message.channel.send(e)
                    if cmd.cost > 0:
                        addpoints(message.author.id, message.guild.id, cmd.cost, connection)
                    

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
        self.cache = None
        event.events.append(self)

    async def create(self, par:list):
        if self.cache == None:
            self.cache = await self.createfunc(par)
    
    async def execute(self, par):
        if self.cache == None:
            return
        
        if self.cache == True:
            self.clear()
            return

        self.cache = await self.exec(par, self.cache)

    def msgvalidation(self, msg):#Validação generica de mensagem, validaçoes mais complexas, apenas dentro da funcão execute
        if self.cache == None:
            return False
        
        if self.cache == True:
            return False

        if self.cache[0] == msg:
            return True
        else:
            return False

    def clear(self):
        self.cache = None


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