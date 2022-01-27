from tkinter import *

#Included with imports at top of program
import sys
import webbrowser
import os
from time import sleep

class MyApp:

    def __init__(self):
        self.file="/home/pi/Desktop/"
        self.window = Tk()
        #Included directly after imports at top of program
        self.window.overrideredirect(True)
        self.window.overrideredirect(False)
        self.window.attributes("-fullscreen", True)
        # personnaliser cette fenetre
        self.window.title("app")
        self.window.geometry("1080x720")
        #self.window.minsize(480,360)

        #Disable the Mouse Pointer
        self.window.config(cursor="none")

        self.fullscreen = Frame(self.window, bg="#888989")
        self.fullscreen.pack_propagate(0)
        self.fullscreen.pack(fill=BOTH,side=LEFT, expand=YES)

        self.space = Frame(self.fullscreen,bd=0,highlightthickness=0)#, bg="#a6a6a6"
        self.space.pack_propagate(0)
        self.space.pack(fill='both', side=RIGHT, expand=YES)

        #Background sur le fullscreen
        self.space.config(background='#191619',bd=0,highlightthickness=0)
        self.bg = PhotoImage(file=f'{self.file}peugeot3.png')
        self.bg_label =  Label(self.space, image=self.bg,bd=0,highlightthickness=0)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    

        #### Variable
        self.bue_arriere_status=False
        self.bue_avant_status=False

        bue_avant_status_get = self.get_data("manuel_auto_pareprise_fan=")
        if bue_avant_status_get == "21" or bue_avant_status_get == "11":
            self.bue_avant_status=True
        

        self.menu = Frame(self.fullscreen,width=110, height=580, bg='#888989',bd=1)
        self.menu.pack_propagate(0)
        self.menu.pack(side=LEFT, expand=False)
        self.create_MenuBar()
        self.init_Menu_Home()
        self.init_Menu_Fan()
        self.clear_widgets()
        #self.show_Menu_Home()
        self.show_Menu_Fan()
        #cmd='sudo screen -d -m /home/pi/Desktop/start.sh'
        #cmd = 'sudo systemctl start networking.service && sudo systemctl start wpa_supplicant.service && sudo systemctl start ssh.service && sudo systemctl start dhcpcd'
        #os.system(cmd)
        cmd='sudo screen -d -m /home/pi/Desktop/start.sh'
        os.system(cmd)

    def clear_widgets(self):
        #Home
        self.clear_home()
        # FAN
        self.clear_Menu_Fan()

    #########################################################################
    #                             Menu BAR                                  #
    #########################################################################
    def create_MenuBar(self):
        #self.menu = Frame(self.window,bg='#41B77F',bd=1)
        #self.menu = Frame(self.window,bg='#888989',bd=1)


        ### Home
        self.image_home = PhotoImage(file=f'{self.file}Images/Menu/Home.png').zoom(1) #.subsample(32)
        self.image_home = self.image_home.subsample(5, 5)
        self.button_home = Button(self.menu,image=self.image_home,bg='#888989',fg='#41B77F',command=self.show_Menu_Home)
        self.button_home.pack(pady=25)
        #self.menu.pack(expand=NO,side=LEFT)
        ### FAN
        self.image_fan = PhotoImage(file=f"{self.file}Images/Menu/FAN.png").zoom(1) #.subsample(32)
        self.image_fan = self.image_fan.subsample(5, 5)
        self.up_button = Button(self.menu,image=self.image_fan,bg='#888989',fg='#41B77F',command=self.show_Menu_Fan)
        self.up_button.pack(pady=25)

        ### ShutDown
        self.image_shut = PhotoImage(file=f"{self.file}Images/Menu/shutdown.png").zoom(1) #.subsample(32)
        self.image_shut = self.image_shut.subsample(5, 5)
        self.button_shut = Button(self.menu,image=self.image_shut,bg='#888989',fg='#41B77F',command=self.shutdown)
        self.button_shut.pack(pady=25)

        self.menu.pack(expand=NO,side=LEFT)

    def open_netflix(self):
        webbrowser.open_new("https://www.netflix.com/browse")

    #######################################################################
    #                                FAN                                  #
    #######################################################################
    def clear_Menu_Fan(self):
        if 'menu_fan' in dir(self):
            self.menu_fan.pack_forget()
            #self.menu_fan.grid_forget()

    def show_Menu_Fan(self):
        self.clear_widgets()
        #self.menu_fan.grid(fill='both')
        self.menu_fan.pack(fill='both',expand=YES)#,side=BOTTOM
    
    def init_Menu_Fan(self):
        #bd=1, bg='#4d4d7f'
        self.menu_fan = Frame(self.space,width=700,height=500,bg='#4d4d7f',bd=0,highlightthickness=0)#bg='#41B77F',##############"" test enleve des bord blanc sur les icone 



        #self.slider_Chaud_droit_label = Label(self.menu_fan,text="",bg='#4d4d7f',bd=0,highlightthickness=0)
        #self.slider_Chaud_droit_label.grid(ipady=70,row=0,columnspan=3)

        self.label_espace = Label(self.menu_fan,text="",bg='#4d4d7f',bd=0,highlightthickness=0)
        self.label_espace.grid(ipady=70,row=1,column=0)
        self.label_espace_droite = Label(self.menu_fan,text="",bg='#4d4d7f',bd=0,highlightthickness=0)
        self.label_espace_droite.grid(ipady=70,row=1,column=3)


        #### BOUTTON TEMPERATURE
        ### Slider Gauche
        self.slider_Chaud_gauche = Scale(
        self.menu_fan,from_=0,to=23,orient='horizontal',command=self.slider_changed_chaud_Gauche,width=70,
        troughcolor='#343b48',highlightcolor="#55aaff",showvalue=0,bd=0,bg="#4d4d7f")
        self.slider_Chaud_gauche.grid(pady=0,row=3,column=0)
        self.slider_Chaud_gauche['state'] = 'normal'
        value_slider_gauche_data = self.convert_Temp_fan_datafile_to_slide("RIGHT")
        self.slider_Chaud_gauche.set(value_slider_gauche_data)
        self.slider_Chaud_gauche_label = Label(self.menu_fan,bg="#4d4d7f",fg="#e77100",font=("Courrier", 30),text=self.convert_Temp_fan_slide_to_tmp(value_slider_gauche_data))
        self.slider_Chaud_gauche_label.grid(pady=30,stick=S,row=2,column=0)

        ### Slider Droit
        self.slider_Chaud_droit = Scale(
        self.menu_fan,from_=0,to=23,orient='horizontal',command=self.slider_changed_chaud_droit,width=70,
        troughcolor='#343b48',highlightcolor="#55aaff",showvalue=0,bd=0,bg="#4d4d7f")
        self.slider_Chaud_droit.grid(pady=0,row=3,column=2)
        self.slider_Chaud_droit['state'] = 'normal'
        value_slider_droit_data = self.convert_Temp_fan_datafile_to_slide("LEFT")
        self.slider_Chaud_droit.set(value_slider_droit_data)
        self.slider_Chaud_droit_label = Label(self.menu_fan,bg="#4d4d7f",fg="#e77100",font=("Courrier", 30),text=self.convert_Temp_fan_slide_to_tmp(value_slider_droit_data))
        self.slider_Chaud_droit_label.grid(pady=30,stick=S,row=2,column=2)

        ### Slider Puissance ventilo
        #self.slider_speed_fan = Scale(    ##### 0 = OFF , la puisance du ventilo = valeur -1 soit 1= 00 dans la trame 
        #self.menu_fan,from_=8,to=0,orient='vertical',command=self.slider_change_fan_speed,width=70,
        #troughcolor='#343b48',highlightcolor="#55aaff",showvalue=0,bd=0,bg="#4d4d7f")
        #self.slider_speed_fan.grid(pady=20,row=2,column=1)
        #self.slider_speed_fan['state'] = 'normal'

        #self.slider_speed_fan_label = Label(self.menu_fan,bg="#4d4d7f",fg="#e77100",font=("Courrier", 30),
        #text=self.get_speed_fan())
        #self.slider_speed_fan_label.grid(stick=S,row=2,column=1)


        ### Recyclage D'air
        self.image_recycle_aire = PhotoImage(file=f'{self.file}Images/Fan/Recycle_{self.get_data("recycle_air_fan=")}.png').zoom(1) #.subsample(32)
        self.image_recycle_aire = self.image_recycle_aire.subsample(6, 6)
        self.button_image_recycle_aire = Button(self.menu_fan,image=self.image_recycle_aire,bg='#4d4d7f', fg='#4d4d7f',
        activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.Recyclage_d_air_click)
        self.button_image_recycle_aire.grid(row=3,column=1)



        ### Boutton Ventilo
        self.image_speed_fan_up = PhotoImage(file=f'{self.file}Images/Fan/Speed.png').zoom(1) #.subsample(32)
        self.image_speed_fan_up = self.image_speed_fan_up.subsample(6, 6)
        self.button_image_speed_fan_up = Button(self.menu_fan,image=self.image_speed_fan_up,bg='#4d4d7f', fg='#4d4d7f',
        activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.fan_speed_up)
        self.button_image_speed_fan_up.grid(ipady=50,stick=N,row=1,column=1)

        self.image_speed_fan_down = PhotoImage(file=f'{self.file}Images/Fan/Speed.png').zoom(1) #.subsample(32)
        self.image_speed_fan_down = self.image_speed_fan_down.subsample(8, 8)
        self.button_image_speed_fan_down = Button(self.menu_fan,image=self.image_speed_fan_down,bg='#4d4d7f', fg='#4d4d7f',
        activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.fan_speed_down)
        self.button_image_speed_fan_down.grid(ipady=0,stick=S,row=1,column=1)

        self.slider_speed_fan_label = Label(self.menu_fan,bg="#4d4d7f",fg="#e77100",font=("Courrier", 30),
        text=self.status_fan_speed())
        self.slider_speed_fan_label.grid(stick=N,row=2,column=1)

        ### Bouton HAUT

        self.image_fan_bue_avant = PhotoImage(file=f'{self.file}Images/Fan/bue_{self.bue_avant_status}_False.png').zoom(1) #.subsample(32)
        self.image_fan_bue_avant = self.image_fan_bue_avant.subsample(3, 3)
        self.button_image_fan_bue_avant = Button(self.menu_fan,image=self.image_fan_bue_avant,bg='#4d4d7f', fg='#4d4d7f',
        activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.bue_one_click)
        #self.button_image_fan_bue_avant.pack(padx=15,pady=50,anchor=CENTER)
        self.button_image_fan_bue_avant.grid(row=0,column=0)

        self.image_auto = PhotoImage(file=f'{self.file}Images/Fan/manuel_auto_{self.get_data("manuel_auto_pareprise_fan=")}.png').zoom(1) #.subsample(32)
        self.image_auto = self.image_auto.subsample(3, 3)
        self.button_image_auto = Button(self.menu_fan,image=self.image_auto,bg='#4d4d7f', fg='#4d4d7f',activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.auto_ac_manuel_fan)
        self.button_image_auto.grid(row=0,column=1)

        self.image_fan_s_c = PhotoImage(file=f'{self.file}Images/Fan/position_{self.get_data("position_fan=")}.png').zoom(1) #.subsample(32)
        self.image_fan_s_c = self.image_fan_s_c.subsample(3, 3)
        self.button_image_fan_s_c = Button(self.menu_fan,image=self.image_fan_s_c,bg='#4d4d7f', fg='#4d4d7f',activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.position_fan)
        self.button_image_fan_s_c.grid(row=0,column=2)

        self.menu_fan.pack_forget()

    ################################################### Recylage D'aire FAN ############################

    def Recyclage_d_air_click(self):
        recycle_air = self.get_data("recycle_air_fan=")
        if recycle_air == "00": ### SI Désactiver alors activer
            self.data_change('recycle_air_fan=00','recycle_air_fan=30')
        else:
            self.data_change('recycle_air_fan=30','recycle_air_fan=00')

        self.image_recycle_aire = PhotoImage(file=f'{self.file}Images/Fan/Recycle_{self.get_data("recycle_air_fan=")}.png').zoom(1) #.subsample(32)
        self.image_recycle_aire = self.image_recycle_aire.subsample(6, 6)
        self.button_image_recycle_aire.configure(image=self.image_recycle_aire)

    ######################################### TEMPERATURE FAN     ######################################

    def slider_changed_chaud_Gauche(self,var):
        self.slider_Chaud_gauche_label.configure(text=self.convert_Temp_fan_slide_to_tmp(var))
        ### Edite file 
        self.data_change(f'temp_fan_LEFT={self.get_data("temp_fan_LEFT=")}',f'temp_fan_LEFT={self.convert_Temp_fan_to_hexa(self.convert_Temp_fan_slide_to_tmp(var))}')

    def slider_changed_chaud_droit(self,var):
        self.slider_Chaud_droit_label.configure(text=self.convert_Temp_fan_slide_to_tmp(var))
        ### Edite file 
        self.data_change(f'temp_fan_RIGHT={self.get_data("temp_fan_RIGHT=")}',f'temp_fan_RIGHT={self.convert_Temp_fan_to_hexa(self.convert_Temp_fan_slide_to_tmp(var))}')

    def convert_Temp_fan_slide_to_tmp(self,nb): ## nb entre 0 23 to température
        if nb == "0": ### Erreur de ma part 
            return "LO" 
        elif nb == "1":
            return "14"
        elif nb == "2":
            return "15"
        elif nb == "3":
            return "16"
        elif nb == "4":
            return "17"
        elif nb == "5":
            return "18"
        elif nb == "6":
            return "18.5"
        elif nb == "7":
            return "19"
        elif nb == "8":
            return "19.5"
        elif nb == "9":
            return "20"
        elif nb == "10":
            return "20.5"
        elif nb == "11":
            return "21"
        elif nb == "12":
            return "21"
        elif nb == "13":
            return "21.5"
        elif nb == "14":
            return "22"
        elif nb == "15":
            return "22.5"
        elif nb == "16":
            return "23"
        elif nb == "17":
            return "23.5"
        elif nb == "18":
            return "24"
        elif nb == "19":
            return "25"
        elif nb == "20":
            return "26"
        elif nb == "21":
            return "27"
        elif nb == "22":
            return "28"
        elif nb == "23":
            return "HI"
            
    def convert_Temp_fan_to_hexa(self,tmp):## Temp == 20.5 ou LO etc
        if tmp == "LO":
            return "00"
        elif tmp == "14":
            return "01"
        elif tmp == "15":
            return "02"
        elif tmp == "16":
            return "03"
        elif tmp == "17":
            return "04"
        elif tmp == "18":
            return "05"
        elif tmp == "18.5":
            return "06"
        elif tmp == "19":
            return "07"
        elif tmp == "19.5":
            return "08"
        elif tmp == "20":
            return "09"
        elif tmp == "20.5":
            return "0A"
        elif tmp == "21":
            return "0B"
        elif tmp == "21.5":
            return "0C"
        elif tmp == "22":
            return "0D"
        elif tmp == "22.5":
            return "0E"
        elif tmp == "23":
            return "0F"
        elif tmp == "23.5":
            return "10"
        elif tmp == "24":
            return "11"
        elif tmp == "25":
            return "12"
        elif tmp == "26":
            return "13"
        elif tmp == "27":
            return "14"
        elif tmp == "28":
            return "15"
        elif tmp == "HI":
            return "16"

    def convert_Temp_fan_datafile_to_slide(self,cote): ### 01 = 1 ou 0A = 10
        tmp_slide = int(self.get_data(f'temp_fan_{cote}='), base=16)
        return tmp_slide

    ######################################### AUTO FAN     ######################################

    def auto_ac_manuel_fan(self):
        manuel_auto_fan = self.get_data("manuel_auto_pareprise_fan=")
        after_manuel_auto_fan = manuel_auto_fan
        if manuel_auto_fan == "20":
            manuel_auto_fan = "00"  ### AUTO & A/C
        elif manuel_auto_fan == "00":
            manuel_auto_fan = "22"  ## Manuel
        elif manuel_auto_fan == "22":
            manuel_auto_fan = "20"  ## AUTO
        
        elif manuel_auto_fan == "11" or manuel_auto_fan == "21": ##### Manuel = 11 et à 22  sinon désavtiver la bue avant
            manuel_auto_fan = "20"  ## AUTO Update image de bue avant désactiver
            self.image_fan_bue_avant = PhotoImage(file=f'{self.file}Images/Fan/bue_{self.bue_arriere_status}_False.png').zoom(1) #.subsample(32)
            self.image_fan_bue_avant = self.image_fan_bue_avant.subsample(3, 3)
            self.button_image_fan_bue_avant.configure(image=self.image_fan_bue_avant)
            
        self.data_change(f'manuel_auto_pareprise_fan={after_manuel_auto_fan}',f'manuel_auto_pareprise_fan={manuel_auto_fan}')
        self.image_auto = PhotoImage(file=f'{self.file}Images/Fan/manuel_auto_{manuel_auto_fan}.png').zoom(1) #.subsample(32)
        self.image_auto = self.image_auto.subsample(3, 3)
        self.button_image_auto.configure(image=self.image_auto)

    ######################################### POSITION FAN ######################################
    def position_fan(self):
        pos = self.get_data("position_fan=")
        pos = int(pos)
        after_pos = pos
        if pos == 60:
            pos = 40
        elif pos == 40:
            pos = 30
        elif pos == 30 :
            pos = 50
        elif pos == 50:
            pos = 20
        elif pos == 20:
            pos = 60
        self.data_change(f'position_fan={after_pos}',f'position_fan={pos}')
        self.im = PhotoImage(file=f'{self.file}Images/Fan/position_{pos}.png').zoom(1) #.subsample(32)
        self.im = self.im.subsample(3, 3)
        self.button_image_fan_s_c.configure(image=self.im)

    ######################################### BUE ######################################
    def bue_one_click(self):
        ## de bases tous off
        if self.bue_arriere_status == False and self.bue_avant_status == False: ## Activer bue avant 
            self.bue_avant()
            self.bue_avant_status = True
        elif self.bue_arriere_status == False and self.bue_avant_status == True: ## Activer bue arriere 
            self.bue_avant()
            self.bue_avant_status = False
            sleep(0.2)
            self.bue_arriere()
            self.bue_arriere_status = True
        elif self.bue_arriere_status == True and self.bue_avant_status == False: ## Activer bue avant&arriere 
            self.bue_avant()
            self.bue_avant_status = True
        elif self.bue_arriere_status == True and self.bue_avant_status == True: ## Désactiver bue avant&arriere 
            self.bue_avant()
            self.bue_avant_status = False
            sleep(0.2)
            self.bue_arriere()
            self.bue_arriere_status = False
        ### Image Update
        self.image_fan_bue_avant = PhotoImage(file=f'{self.file}Images/Fan/bue_{self.bue_arriere_status}_{self.bue_avant_status}.png').zoom(1) #.subsample(32)
        self.image_fan_bue_avant = self.image_fan_bue_avant.subsample(3, 3)
        self.button_image_fan_bue_avant.configure(image=self.image_fan_bue_avant)

        ### UPDATE MANUEL A/C
        manuel_auto_fan = self.get_data("manuel_auto_pareprise_fan=")
        if manuel_auto_fan != "62":
            self.image_auto = PhotoImage(file=f'{self.file}Images/Fan/manuel_auto_{self.get_data("manuel_auto_pareprise_fan=")}.png').zoom(1) #.subsample(32)
            self.image_auto = self.image_auto.subsample(3, 3)
            self.button_image_auto.configure(image=self.image_auto)

    def bue_avant(self):
        status_bue = self.get_data_octet_1()
        #if status_bue == "A2":
        #    self.data_change(f'manuel_auto_pareprise_fan=A2',f'manuel_auto_pareprise_fan=21')
        #status_bue = int(status_bue)
        if status_bue == 21 or status_bue == 11 or status_bue == "A2": ## Si la souflerier es active alors désactiver
            self.data_change(f'manuel_auto_pareprise_fan={status_bue}',f'manuel_auto_pareprise_fan=22')
        else:                           
            self.data_change(f'manuel_auto_pareprise_fan={status_bue}',f'manuel_auto_pareprise_fan=21')     #Activer la souflerie

    def bue_arriere(self):
        status_bue = self.get_data_octet_1()
        #status_bue = int(status_bue)
        self.data_change(f'manuel_auto_pareprise_fan={status_bue}',f'manuel_auto_pareprise_fan=62')

    def get_data_octet_1(self):
        with open(f'{self.file}data.txt') as f:
            lines = f.readlines()
            for line in lines:
                if "manuel_auto_pareprise_fan=" in line:
                    return line.replace("manuel_auto_pareprise_fan=","").replace("\n","")
                    break

    ################################################### SPEED FAN ############################
    def slider_change_fan_speed(self,var):### 0  ### PAS UTILISER à SUPPRIMER 
        speed=int(var)-1
        fan_speed = self.get_speed_fan()
        if fan_speed == "0F": ## Condition à rajouter car bug
            self.fan_speed_up()
        elif int(fan_speed) < int(hex(speed).replace("x","")):
            self.fan_speed_up()
        else:
            self.fan_speed_down()
        #sleep(0.5)
        #self.slider_speed_fan_label.configure(text=self.get_speed_fan()) ### UPdate Label
        self.slider_speed_fan_label.configure(text=speed) ### UPdate Label
        #self.slider_speed_fan.set(var)

        manuel_auto_fan = self.get_data("manuel_auto_pareprise_fan=")
        if manuel_auto_fan != "62":
            self.image_auto = PhotoImage(file=f'{self.file}Images/Fan/manuel_auto_{self.get_data("manuel_auto_pareprise_fan=")}.png').zoom(1) #.subsample(32)
            self.image_auto = self.image_auto.subsample(3, 3)
            self.button_image_auto.configure(image=self.image_auto)

    def status_fan_speed(self):
        speed = self.get_speed_fan()
        speed = int(speed, base=16)
        if speed == 15:
            speed = "OFF"
        return speed

    def fan_speed_up(self):
        after_speed = self.get_speed_fan()
        after_speed = int(after_speed, base=16)
        print(str(after_speed))
        if after_speed == 15:## Activer la clim
            self.data_change(f'speed_fan=0F',### DATA SPEED
            'speed_fan=00')
            
            self.data_change('manuel_auto_pareprise_fan=A2',### ACTIVE 1 Otect passage en manuel 
            'manuel_auto_pareprise_fan=22')

            manuel_auto_fan = self.get_data("manuel_auto_pareprise_fan=")### UPDATE IMAGE MANUEL
            if manuel_auto_fan != "62":
                self.image_auto = PhotoImage(file=f'{self.file}Images/Fan/manuel_auto_{self.get_data("manuel_auto_pareprise_fan=")}.png').zoom(1) #.subsample(32)
                self.image_auto = self.image_auto.subsample(3, 3)
                self.button_image_auto.configure(image=self.image_auto)
        elif after_speed != 7:
            self.data_change(f'speed_fan={str(self.convert_speed_fan(after_speed))}',### DATA SPEED
            f'speed_fan={str(self.convert_speed_fan(after_speed+1))}')
        self.slider_speed_fan_label.configure(text=self.status_fan_speed())

    def fan_speed_down(self):
        after_speed = self.get_speed_fan()
        after_speed = int(after_speed, base=16)
        #print(int(after_speed, base=16))
        if after_speed == 0:## Désactiver car clim à 0 puis il la down soit -1
            self.data_change('manuel_auto_pareprise_fan=22',### ACTIVE 1 Otect passage en manuel 
            'manuel_auto_pareprise_fan=A2')
            self.data_change('speed_fan=00',### DATA SPEED
            'speed_fan=0F')

            manuel_auto_fan = self.get_data("manuel_auto_pareprise_fan=")### UPDATE IMAGE MANUEL
            if manuel_auto_fan != "62":
                self.image_auto = PhotoImage(file=f'{self.file}Images/Fan/manuel_auto_{self.get_data("manuel_auto_pareprise_fan=")}.png').zoom(1) #.subsample(32)
                self.image_auto = self.image_auto.subsample(3, 3)
                self.button_image_auto.configure(image=self.image_auto)
        else:
            self.data_change(f'speed_fan={str(self.convert_speed_fan(after_speed))}',### DATA SPEED
            f'speed_fan={str(self.convert_speed_fan(after_speed-1))}')
        self.slider_speed_fan_label.configure(text=self.status_fan_speed())

    def get_speed_fan(self):
        with open(f'{self.file}data.txt') as f:
            lines = f.readlines()
            for line in lines:
                if "speed_fan=" in line:
                    #print(line.replace("speed_fan=",""))
                    return line.replace("speed_fan=","").replace("\n","")
                    break

    def convert_speed_fan(self,nb):
        return hex(nb).replace("x","") 

    #########################################################################
    #                                Home                                   #
    #########################################################################

    def show_Menu_Home(self):
        self.clear_widgets()
        self.menu_home.pack(fill='both',expand=YES)
        
    def clear_home(self):
        if 'label_title' in dir(self):
            self.menu_home.pack_forget()
            #self.label_title.destroy()
            #self.button_netflix.destroy()

    def init_Menu_Home(self):
        self.menu_home = Frame(self.space,width=300,height=200,bd=0,highlightthickness=0)
        self.create_widgets()

        #Background sur le fullscreen
        self.menu_home.config(background='#030303',bd=0,highlightthickness=0)
        self.menu_home_bg = PhotoImage(file=f'{self.file}peugeot3.png')
        self.menu_home_bg_label =  Label(self.menu_home, image=self.menu_home_bg,bd=0,highlightthickness=0)
        self.menu_home_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.menu_home_bg_label.lower()   #### Pour qu'il deceande du premier plan 

        self.menu_home.pack_forget()

    def create_widgets(self):
        self.create_title()
        self.create_netflix_button()
    
    def create_netflix_button(self):
        ### Menu Netflix
        self.image_netflix = PhotoImage(file=f"{self.file}Images/Home/netflix.png").zoom(1) #.subsample(32)
        self.image_netflix = self.image_netflix.subsample(7)
        self.button_netflix = Button(self.menu_home,image=self.image_netflix,bg='#888989',command=self.open_netflix)
        self.button_netflix.pack(padx=10,anchor=NW)


        
        #self.button_netflix = Button(self.space,text="Netflix",font=("Courrier",25), bg='white',fg='#41B77F',command=self.open_netflix)
        #self.button_netflix.pack(anchor=NW)

    def create_title(self):
        self.label_title = Label(self.menu_home, text="207 CC", font=("Courrier", 30), bg='#5d6efc',
                            fg='white')
        self.label_title.place()
    
    #########################################################################
    #                                SHUTOWN                                #
    #########################################################################
    def shutdown(self):
        os.system("poweroff")

    #########################################################################
    #                         Changer DATA FILE                             #
    #########################################################################
    def data_change(self,after,new):
        fin = open(f"{self.file}data.txt", "rt")
        data = fin.read()
        data = data.replace(f'{after}', f'{new}')
        fin.close()
        fin = open(f"{self.file}data.txt", "wt")
        fin.write(data)
        fin.close()

    def get_data(self,key):
        with open(f'{self.file}data.txt') as f:
            lines = f.readlines()
            for line in lines:
                if key in line:
                    return line.replace(key,"").replace("\n","")
                    break

    def create_circle(self,x, y, r, canvasName): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1)

# afficher
app = MyApp()
app.window.mainloop()