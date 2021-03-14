from nameko.standalone.events import event_dispatcher
from time import sleep

CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}

dispatch = event_dispatcher(CONFIG, mandatory=True)
for i in range(3):
    dispatch("friendlyservice", "hi", "payload whatever "+str(i))
