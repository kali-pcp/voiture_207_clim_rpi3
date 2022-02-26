from time import sleep
import can
from threading import Thread

class MyThread(Thread):

    def __init__(self,argument, **kwargs):
        super(MyThread, self).__init__(**kwargs)
        self.bus = can.Bus(interface='socketcan',channel='vcan0',receive_own_messages=False)
        self.argument = argument
        self.manuel_auto_pareprise_fan = 0xA2
        self.speed_fan = 0x0F
        self.position_fan = 0x50
        self.recycle_air_fan = 0x00
        self.temp_fan_LEFT = 0x0B
        self.temp_fan_RIGHT = 0x0B
        self.manuel_auto_pareprise_fan_data_send_2_fois_max=0
        self.manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant=0
        
    def set_speed(self,arg):
        self.speed_fan = arg

    def clim_off(self):
        #A2 00 0F
        self.manuel_auto_pareprise_fan = 0xA2
        self.speed_fan = 0x0F

    def recyclage_air(self):
        if self.recycle_air_fan == 0x00:
            self.recycle_air_fan = 0x30
        else:
            self.recycle_air_fan = 0x00

    def change_position_fan(self):
        if self.position_fan == 0x60 : # SI SOL + PLAFONT
            self.position_fan = 0x40
        elif self.position_fan == 0x40:# SI PLAFONT
            self.position_fan = 0x30
        elif self.position_fan == 0x30:# SI CENTRE
            self.position_fan = 0x50
        elif self.position_fan == 0x50:# SI centre+sol
            self.position_fan = 0x20
        elif self.position_fan == 0x20:# SI SOL
            self.position_fan = 0x60



    def get_position_fan(self):
        return self.position_fan

    def run(self):
        while True:
            if self.manuel_auto_pareprise_fan == 0x21 or ( self.manuel_auto_pareprise_fan == 0x11 and self.speed_fan == 0x0F ):### SPEED FAN
                self.speed_fan=0x00

            if self.manuel_auto_pareprise_fan == 0x62:### BUE à l'arriere
                if self.manuel_auto_pareprise_fan_data_send_2_fois_max == 1:
                    self.manuel_auto_pareprise_fan_data_send_2_fois_max = 0
                    self.manuel_auto_pareprise_fan = 0x22
                self.manuel_auto_pareprise_fan_data_send_2_fois_max = self.manuel_auto_pareprise_fan_data_send_2_fois_max + 1


            if self.manuel_auto_pareprise_fan == 0x21:### TRUC à l'avant
                if self.manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant == 1:
                    self.manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant=0
                    self.manuel_auto_pareprise_fan=11
                self.manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant = self.manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant + 1
                self.position_fan = 0x10
                self.recycle_air_fan=0x10
            
            if self.manuel_auto_pareprise_fan == 0x11:
                self.position_fan=0x10
                self.recycle_air_fan=0x10

            message = can.Message(arbitration_id=0x1D0, is_extended_id=False,data=[
                self.manuel_auto_pareprise_fan, 
                00, 
                self.speed_fan,
                self.position_fan,
                self.recycle_air_fan,
                self.temp_fan_LEFT,
                self.temp_fan_RIGHT])
            self.bus.send(message)

            sleep(0.2)

class CAN:
    #if __name__ == '__main__':
    #    hey = MyThread(0x11)
    #    hey.start()
    #    sleep(2)
    #    hey.setarg(0x22)

    def __init__(self):
        #self.fan = MyThread(0x11)
        #self.fan.start()
        print("hey")
    
    def test(self):
        print("coucou")

#        sleep(2)
#        self.fan.setarg(0x22)
    
#    def set_speed_fan(self,speed):
#        self.fan.setarg(speed)

    #MyThread('2').start()
#print("la")
#can_app = can_application()