def getpoints(userid, guildid, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
        """
        SELECT points FROM Users WHERE ServerId = '{gid}' and UserId = '{uid}'

        """.format(uid=str(userid), gid=str(guildid))
        )
        result = cursor.fetchone()
        points = result[0]
    except:
        cursor.execute(
            """
            INSERT INTO Users(ServerId, UserId, Points)
            VALUES('{gid}', '{uid}', 0)
            """.format(uid=str(userid), gid=str(guildid))
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
    WHERE ServerId='{gid}' and UserId='{uid}'
    """.format(p=points,gid=str(guildid),uid=str(userid))
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
        WHERE ServerId = '{gid}'
        ORDER BY Points DESC
        LIMIT 5
        """.format(gid=str(guildid))
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
        WHERE ServerId = '{gid}'
        ORDER BY Price Desc
        """.format(gid=str(guildid))
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
        VALUES('{gid}', '{n}', '{p}')
                
    '''.format(gid=str(guildid), n=item_name, p=price)
    )
    connection.commit()


def delitem(guildid, itemid, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
        DELETE FROM Shop
        WHERE itemid = {iid} AND serverid = '{gid}';
                
    '''.format(gid=str(guildid), iid=itemid)
    )
    connection.commit()


def getservercommand(guildid, name, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
        SELECT * FROM Commands
        WHERE ServerId = '{gid}' AND Name = '{n}' 

    '''.format(gid=str(guildid), n=str(name))
    )
    leg = ['serverid', 'name', 'message', 'description', 'permission', 'price', 'active', 'overwritten']
    r = cursor.fetchone()

    try:
        result = dict(zip(leg, r))
        result['category'] = 'personalizado'
        result['args'] = []
        return result
    except:    
        return None


def getallserverscommands(guildid, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
        SELECT * FROM Commands
        WHERE ServerId = '{gid}'

    '''.format(gid=str(guildid))
    )

    r = cursor.fetchall()
    leg = ['serverid', 'name', 'message', 'description', 'permission', 'price', 'active', 'overwritten']
    
    result = []
    for res in r:
        _res = dict(zip(leg, res))
        _res['category'] = 'personalizado'
        _res['args'] = []
        result.append(_res)
    
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


def addserver(guildid, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
        INSERT INTO servers(ServerId)
        VALUES('{gid}')
    '''.format(gid=str(guildid))
    )
    connection.commit()


def getserver(guildid, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
    SELECT * FROM servers WHERE ServerId = '{gid}'
    '''.format(gid=str(guildid))
    )
    r = cursor.fetchone()

    leg = ['prefix', 'commandchannel']

    if r != None:
        result = dict(zip(leg, r[1:]))
    else:
        result = None
    
    return result


def editserver(guildid, connection, key, value):
    cursor = connection.cursor()
    cursor.execute(
    '''
    UPDATE servers
    SET {col_name} = %s
    WHERE ServerId=%s
    '''.format(col_name=key), (value,str(guildid))
    )
    connection.commit()