from nameko.events import event_handler, BROADCAST
from nameko.rpc import rpc

class ServiceB:
    """ Event listening service. """
    name = "service_b"

    # whenever friendlyservice triggers 'hi' event
    @event_handler("friendlyservice", "hi", handler_type=BROADCAST,reliable_delivery=False)
    def handle_event(self, payload):
        print("service received:", payload, self)

