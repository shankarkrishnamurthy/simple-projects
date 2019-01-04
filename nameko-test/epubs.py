from nameko.events import EventDispatcher
from nameko.timer import timer

class FriendlyService(object):

    name = "friendlyservice"
    dispatch = EventDispatcher()
    global cnt
    cnt = 1

    @timer(interval=3)
    def say_hello(self):
        global cnt
        print ("Sending msg ",cnt, self)
        self.dispatch("hi", "what ever " + str(cnt))
        cnt += 1
