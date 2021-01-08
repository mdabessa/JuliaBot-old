import psycopg2
import time


class command():
    commands = []
    def __init__(self, name, func, desc='Nothing', cost=0, perm=0):
        self.name = name
        self.func = func
        self.desc = desc
        self.cost = cost
        self.perm = perm

        command.commands.append(self)

    async def execute(self, message, param, connection):
        await self.func(message, param, connection)

    @classmethod
    async def trycommand(cls, message, content, connection, masterid):
        contlist = content.split()
        contcommand = contlist[0]

        if len(contlist) > 1:
            commandpar = ' '.join(contlist[1:])
        else:
            commandpar = None


        for cmd in command.commands:
            if cmd.name == contcommand:
                if cmd.perm == 1:
                    if message.author.id != masterid:
                        await message.channel.send('Voce não possui permissão para isto :sob: ')
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
                    await cmd.execute(message, commandpar, connection)
                except Exception as e:
                    await message.channel.send(e)
                    if cmd.cost > 0:
                        addpoints(message.author.id, message.guild.id, cmd.cost, connection)
                    

class event():
    events = []
    def __init__(self, name:str, createfunc, executefunc, att='react' , desc='Nothing'):
        self.name = name
        self.createfunc = createfunc
        self.exec = executefunc
        self.desc = desc
        self.att = att
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


timers = []
def timer(ind, segs, recreate=False):
    global timers
    timenow = time.time()

    check = 0
    for i in timers:
        if i[0] == ind:
            check = 1
            if (timenow - i[1]) >= i[2]:
                timers.remove(i)
                if recreate:
                    timers.append([ind,timenow,segs])

                return True
            else:
                return False
    
    if check == 0:
        if segs > 0:
            timers.append([ind,timenow,segs])
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
