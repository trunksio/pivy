import redis
from random import SystemRandom


r = redis.StrictRedis(host='localhost', port=6379, db=0,decode_responses=True)



'''create keystore'''
def create_keystore(codebook):
    '''range 32 - 127 ascii'''
    key =[]
    value = []
    for x in range (32,127,1):
        for y in range(32,127,1):
            for z in range(32,127,1):
                key.append(str(chr(x)+chr(y)+chr(z)))
                value.append(str(chr(x)+chr(y)+chr(z)))
    cryptorand = SystemRandom()
    cryptorand.shuffle(value)
    for i in range(0,len(key),1):
        r.set(codebook +":"+key[i],value[i])
        r.set(codebook + ":D:" + value[i], key[i])

def tokenise(target,codebook):
    tl = len(target)
    '''pad to at least 9 chars with special chr(127) ~'''
    #if tl < 10:
    #    target = padfoot(target,10)
    tl = len(target)
    for i in range(0,tl,1):
        s = target[i:i+3]
        if len(s) < 3:
            s = padfoot(s,3)

        tok = r.get(codebook+':'+s)

        target = target[:i] + str(tok) + target[i+3:]

    return target


def padfoot(target, val):
    for i in range(len(target),val):
        target = target + chr(126)
    return target
def depad(target):
    if target.endswith(chr(126)):
        target = target[:-1]
        target = depad(target)
    return target

def detokenise(target,codebook):

    tl = len(target)
    '''pad to at least 9 chars with special chr(127) ~'''

    tl = len(target)
    for i in range(tl,2,-1):
        s = target[i-3:i]


        tok = r.get(codebook+':'+s)

        target = target[:i-3] + str(tok) + target[i:]

    return target


def reversed_string(a_string):
    return a_string[::-1]


def main():
    #create_keystore("Surname")
    var = tokenise('Lewis','Surname')
    print('1:'+var)
    var = reversed_string(var)
    print('2:'+var)
    var = tokenise(var, 'Surname')
    print('3:'+var)

    out = detokenise(var,'Surname:D')
    print('4:'+out)
    out = depad(out)
    out = reversed_string(out)
    print('5:'+out)
    out = depad(out)
    out = detokenise(out, 'Surname:D')
    print('6:'+out)
    out = depad(out)
    print('7:'+out)

if __name__ == '__main__':
    main()
