class Singleton(object):
    _inst = None

    def __new__(cls):
        if not cls._inst:
            cls._inst = super(Singleton,cls).__new__(cls)
        return cls._inst

class Borg(object):
    _sharedState = {}
    def __init__(self):
        self.__dict__ = Borg._sharedState

if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()
    print "s1 == s2 " , s1 == s2

    b1 = Borg()
    b1.var1 = 'shankar'
    b2 = Borg()
    print "b1 == b2", b1 == b2
    print b2.var1
