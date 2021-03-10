import datetime


def nround(num, n=3):
    try:
        _num1, _num2 = str(num).split('.')

        if len(_num2)>n:
            r = _num1 + '.' + _num2[0:n]
            return float(r)
        else:
            return float(num)
    except:
        return float(num)



def fdate(par, date):
    num = ''
    c = 0

    param = par.replace(' ','')
    for i in param:
        try:
            num += str(int(i))
            c += 1
        except:
            break
    
    if c == 0:
        return

    if num == 0:
        return

    try:
        num = int(num)
        s = param[c:]
        s = s.lower()
    except:
        return


    leg = {
        'minute':['m', 'min', 'minute', 'minutes', 'minuto', 'minutos'],
        'hour':['h', 'hour', 'hours', 'hora', 'horas', 'hr', 'hrs'],
        'day':['d', 'day', 'days', 'dia', 'dias'],
        'mounth':['mounth', 'mounths', 'mes', 'meses', 'mês'],
        'year':['y', 'year', 'years', 'a', 'ano', 'anos']
    }


    if s in leg['minute']:
        t = num*60
    elif s in leg['hour']:
        t = num*3600
    elif s in leg['day']:
        t = num*86400
    elif s in leg['mounth']:
        t = num*2592000
    elif s in leg['year']:
        t = num*31536000
    else:
        return None

    delta = datetime.timedelta(seconds=t)

    limit = 3153600000 #100 years
    return None if t > limit else date + delta