#Decorator Design Pattern Begin
class WindowIntf(object):
    def build(self): pass

class Window(WindowIntf):
    def build(self):
        print "Building Window"

class BaseDecorator(WindowIntf):
    def build(self):
        pass
       
class BorderDecorator(BaseDecorator):
    def __init__(self, win):
        self.win = win
    def build(self):
        print "Border is Decorated"
        self.win.build()

class VertSBDecorator(BaseDecorator):
    def __init__(self, win):
        self.win = win
    def build(self):
        print "Vertical ScrollBar is Decorated"
        self.win.build()

class HorzSBDecorator(BaseDecorator):
    def __init__(self, win):
        self.win = win
    def build(self):
        print "Horizontal ScrollBar is Decorated"
        self.win.build()
#Decorator Design pattern End

#Adapter Design Pattern Begin
class SocketIntf(object):
    pass

class EuropeanSocket(SocketIntf):
    def __init__(self):
        self.volt = 230
        self.on = 1

class AmericanKettle(SocketIntf):
    def __init__(self, obj):
        self.sock = obj
    def boil(self):
        if self.sock.on == 0:
            print 'No Power'
            return
        if self.sock.volt > 110:
            print "Kettle on Fire"
        else:
            print "Coffee Time!"

class AmericanAdapter(SocketIntf):
    def __init__(self,obj):
        self.volt = 110
        self.on = obj.on
#Adapter Design Pattern End

if __name__ == "__main__":
    #Decorator
    w = Window()
    w.build()
    print
    wb = BorderDecorator(w)
    wb.build()
    print
    vwb = VertSBDecorator(wb)
    vwb.build()
    print
    bestwin = HorzSBDecorator(vwb)
    bestwin.build()
    print

    #Adapter
    socket = EuropeanSocket()
    cm = AmericanKettle(socket)
    cm.boil()
    adapter = AmericanAdapter(socket)
    cm = AmericanKettle(adapter)
    cm.boil()
