#accepts ints and floats
def getHours(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    #print('{:d}:{:02d}:{:02d}'.format(h, m, s)) # Python 3
    return  f'{h:d}:{m:02d}:{s:02d}' # Python 3.6+

#accepts strings
def getSeconds(time_str):
    """Get seconds from time."""
    h, m, s = str(time_str).split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)




#print(getSeconds('1:23:45'))
#print(getHours(100.5))
