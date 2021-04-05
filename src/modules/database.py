import datetime


def initdb(connection):
    cursor = connection.cursor()
    query = []

    # animes table
    query.append('''
        CREATE TABLE IF NOT EXISTS animes(
            id SERIAL,
            alid INT,
            episode INT,
            anime VARCHAR(255),
            imagelink VARCHAR(255),
            link VARCHAR(255),
            site VARCHAR(255),
            processed BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (alid, episode)
        )
    ''')
    
    # commands table
    query.append('''
        CREATE TABLE IF NOT EXISTS commands(
            serverid VARCHAR(255),
            name VARCHAR(255),
            message VARCHAR(255),
            description VARCHAR(255),
            permission int,
            price int,
            active int DEFAULT 1,
            overwritten int DEFAULT 1,
            PRIMARY KEY (serverid, name)
        )
    ''')

    # reminder table
    query.append('''
        CREATE TABLE IF NOT EXISTS reminder(
            serverid VARCHAR(255),
            channelid VARCHAR(255),
            messageid VARCHAR(255), 
            userid VARCHAR(255),
            creationdate timestamp without time zone,
            reminderdate timestamp without time zone,
            id SERIAL,
            PRIMARY KEY (id)
        )
    ''')

    # servers table
    query.append('''
        CREATE TABLE IF NOT EXISTS servers(
            serverid VARCHAR(255),
            prefix VARCHAR(10)  DEFAULT 'j!',
            commandchannel VARCHAR(255),
            eventchannel VARCHAR(255),
            auto_events boolean DEFAULT true,
            anime_channel VARCHAR(255) DEFAULT NULL,
            PRIMARY KEY (serverid)
        )
    ''')

    # shop table
    query.append('''
        CREATE TABLE IF NOT EXISTS shop(
            itemid SERIAL,
            serverid VARCHAR(255),
            userid VARCHAR(255),
            name VARCHAR(255),
            price integer,
            PRIMARY KEY ( itemid)
        )
    ''')

    # users table
    query.append('''
        CREATE TABLE IF NOT EXISTS users(
            serverid character varying(255) COLLATE pg_catalog."default" NOT NULL,
            userid character varying(255) COLLATE pg_catalog."default" NOT NULL,
            points integer NOT NULL,
            CONSTRAINT users_pkey PRIMARY KEY (serverid, userid)
        )
    ''')

    for q in query:
        cursor.execute(q)

    connection.commit()


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
        leg = ['itemid', 'serverid', 'userid', 'name', 'price']
        result = cursor.fetchall()

        return [dict(zip(leg, r)) for r in result]
    except:
        return []


def getitem(guildid, itemid, connection):
    cursor = connection.cursor()
    cursor.execute('''
    SELECT * FROM shop
    WHERE serverid = %s and itemid = %s
    ''', (str(guildid), itemid))

    result = cursor.fetchone()

    leg = ['itemid', 'serverid', 'userid', 'name', 'price']
    return dict(zip(leg, result)) if result != None else None


def additem(guildid, userid, item_name, price, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
        INSERT INTO Shop(ServerId, userid, name, price)
        VALUES('{gid}', '{uid}', '{n}', '{p}')
                
    '''.format(gid=str(guildid), uid=userid, n=item_name, p=price)
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
        result['aliases'] = []
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
        _res['aliases'] = []
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

    leg = ['prefix', 'commandchannel', 'eventchannel', 'auto_events', 'anime_channel']

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


def addreminder(serverid, channelid, messageid, userid, date, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
    INSERT INTO reminder(serverid, channelid, messageid, userid, creationdate, reminderdate)
    VALUES(%s, %s, %s, %s, %s, %s)
    ''',(str(serverid), str(channelid), str(messageid), str(userid), str(datetime.datetime.now()), date)
    )
    connection.commit()


def delreminder(rid, connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
    DELETE FROM reminder WHERE id={index}
    '''.format(index = int(rid))
    )
    connection.commit()


def getallreminder(connection):
    cursor = connection.cursor()
    cursor.execute(
    '''
    SELECT * FROM reminder ORDER BY reminderdate LIMIT 5
    '''    
    )
    
    result = cursor.fetchall()

    leg = ['serverid', 'channelid', 'messageid', 'userid', 'creationdate', 'reminderdate', 'id']
    resp = []
    for r in result:
        resp.append(dict(zip(leg, r)))

    return resp


def get_all_animes(connection, limit=None, processed=None):
    cursor = connection.cursor()
    query = 'SELECT * FROM animes '
    
    if processed != None:
        processed = bool(processed)
        query += 'WHERE processed = {p} '.format(p=processed)

    query += 'ORDER BY id ASC '

    if limit != None:
        limit = int(limit)
        query += 'LIMIT lim '.format(lim=limit)


    cursor.execute(query)
    r = cursor.fetchall()
    cursor.close()

    legend = ['id', 'alid', 'episode','anime', 'imagelink', 'link', 'site', 'processed']
    result = []
    for i in r:
        result.append(dict(zip(legend, i)))

    return result


def update_anime(anime_id, connection):
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE animes
        SET processed = TRUE
        WHERE id={i}
    '''.format(i=anime_id))

    cursor.close()
    connection.commit()
