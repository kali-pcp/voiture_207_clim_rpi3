from time import sleep
import can
from threading import Thread
import time

class can_application:
    # import the library
    
    # create a bus instance
    # many other interfaces are supported as well (see documentation)
    
    def __init__(self):
        #asyncio.run(self.main())
        self.main()

    def main(self):
        #self.bus = can.Bus(interface='socketcan',channel='vcan0',receive_own_messages=False)
        self.manuel_auto_pareprise_fan=0x11
        #self.update()
        #t1 = asyncio.create_task(self.update())
        #t2 = asyncio.create_task(self.sleepd())
        #await asyncio.gather(t1, t2)
        #loop = asyncio.get_event_loop()
        #loop.ensure_future(self.update())
        print("ici")
        print("cc")
        self.sleepd()
        
        #asyncio.run(self.update())

    def getvar(self):
        return self.manuel_auto_pareprise_fan
        

    def sleepd(self):
        sleep(3)
        print("coucouc")
        self.manuel_auto_pareprise_fan=0x22
    

class MyThread(Thread):

    def __init__(self,argument, **kwargs):
        super(MyThread, self).__init__(**kwargs)
        self.bus = can.Bus(interface='socketcan',channel='vcan0',receive_own_messages=False)
        self.argument = argument
        

    def setarg(self,arg):
        self.argument = arg

    def run(self):
        while True:
            sleep(0.2)
            message = can.Message(arbitration_id=123, is_extended_id=False,data=[self.argument, 0x22, 0x33])
            self.bus.send(message)
class CAN:
    #if __name__ == '__main__':
    #    hey = MyThread(0x11)
    #    hey.start()
    #    sleep(2)
    #    hey.setarg(0x22)

    def __init__(self):
        self.fan = MyThread(0x11)
        self.fan.start()
        sleep(2)
        self.fan.setarg(0x22)
    
    def set_speed_fan(self,speed):
        self.fan.setarg(speed)

    #MyThread('2').start()
#print("la")
#can_app = can_application()