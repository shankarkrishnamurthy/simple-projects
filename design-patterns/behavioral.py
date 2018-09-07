#Observer Pattern Begin
class ObserversIntf(object):
    def update(self, m, **kwargs):
        pass

class AmericanStockMarket(ObserversIntf):
    def update(self, m,**kwargs):
        print "American Stock market getting news: ", m, kwargs        

class EuropeanStockMarket(ObserversIntf):
    def update(self, m,**kwargs):
        print "European Stock market getting news: ", m, kwargs        

class Observable(object):
    def __init__(self):
        self._observers = []
    def register(self, observer):
        self._observers.append(observer)
    def update_observers(self, m,**kwargs):
        print kwargs
        for ob in self._observers:
            ob.update(m,**kwargs)
#Observer Pattern End

# Command Pattern Begin
class Screen(object):
    def __init__(self, t):
        self._text = t
        self._clip = ''
    def cut(self, st, en):
        self._clip = self._text[st:en]
        self._text = self._text[:st] + self._text[en:]
    def paste(self,st):
        self._text = self._text[:st] + self._clip + self._text[st:]
    def __str__(self): return self._text + ' Clip: ' + self._clip

class CommandIntf(object):
    def execute(self): pass

class CutCommand(CommandIntf):
    def __init__(self,obj,st,en):
        self._obj = obj
        self._st = st
        self._en = en
    def execute(self):
        self._obj.cut(self._st,self._en)

class PasteCommand(CommandIntf):
    def __init__(self,obj,st):
        self._obj = obj
        self._st = st
    def execute(self):
        self._obj.paste(self._st)

class ScreenInvoker(object):
    def __init__(self):
        self._cmdlist = []
        
    def store_and_exec(self, cmd):
        self._cmdlist.append(cmd)
        cmd.execute()

#Command Pattern End

if __name__ == "__main__":
    bigCompany = Observable()
    us = AmericanStockMarket()
    bigCompany.register(us)
    euro = EuropeanStockMarket()
    bigCompany.register(euro)
    bigCompany.update_observers('Important News', msg='CEO got kicked out', name='bigCompany')

    scr = Screen('Hello World!')
    print str(scr)
    cut = CutCommand(scr, 5,11)
    client = ScreenInvoker()
    client.store_and_exec(cut)
    print str(scr) 
    paste = PasteCommand(scr, 0)
    client.store_and_exec(paste)
    print str(scr) 

