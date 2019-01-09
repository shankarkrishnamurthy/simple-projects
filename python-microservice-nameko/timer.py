from nameko.timer import timer

class Service:
    name ="service"

    @timer(interval=3)
    def ping(self):
        # method executed every 3 seconds
        print("pong")
