import datetime


def nround(num, n=3):
    try:
        _num1, _num2 = str(num).split(".")

        if len(_num2) > n:
            r = _num1 + "." + _num2[0:n]
            return float(r)
        else:
            return float(num)
    except:
        return float(num)


def fdate(par, date):
    def extract(par):
        times = []
        l = 0
        num = ""
        word = ""
        for i in par:
            try:
                _num = str(int(i))
                if l == 1:
                    times.append([num, word])
                    l = 0
                    num = _num
                    word = ""
                else:
                    num += _num

            except:
                l = 1
                word += i

        times.append([num, word])
        return times

    param = par.replace(" ", "")
    times = extract(param)

    leg = {
        "minute": ["m", "min", "minute", "minutes", "minuto", "minutos"],
        "hour": ["h", "hour", "hours", "hora", "horas", "hr", "hrs"],
        "day": ["d", "day", "days", "dia", "dias"],
        "mounth": ["mounth", "mounths", "mes", "meses", "mês"],
        "year": ["y", "year", "years", "a", "ano", "anos"],
    }

    t = 0
    for time in times:
        if time[0] == "" or time[1] == "":
            continue

        num = int(time[0])
        word = time[1]

        if word in leg["minute"]:
            t += num * 60
        elif word in leg["hour"]:
            t += num * 3600
        elif word in leg["day"]:
            t += num * 86400
        elif word in leg["mounth"]:
            t += num * 2592000
        elif word in leg["year"]:
            t += num * 31536000
        else:
            return None

    delta = datetime.timedelta(seconds=t)

    limit = 3153600000  # 100 years
    return None if (t > limit or t == 0) else date + delta
