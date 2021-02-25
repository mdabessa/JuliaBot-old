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