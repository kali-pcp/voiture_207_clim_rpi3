from curses.ascii import CAN
from distutils import command
from tkinter import *

#Included with imports at top of program
import sys
import webbrowser
import os
from time import sleep
import cv2
import PIL.Image, PIL.ImageTk
import subprocess

class MyApp:

    def __init__(self):
        #self.file="/home/tony/Documents/USB2CAN/Application_Voiture/voiture_207_clim_rpi3/"
        #self.file="/home/pi/Desktop/voiture_207_clim_rpi3/"
        #self.file=str(os.getcwd())+"/"
        dirname, filename = os.path.split(os.path.abspath(__file__))
        print("running from", dirname)
        print("file is", filename)
        self.file = dirname + "/"
        #print(os.getcwd())
        #self.file = str(subprocess.check_output("pwd", shell=True)).strip().replace("\\n'","").replace("b'","")+ "/"
        print("ici",self.file)
        ### LOAD FAN 
        self.fan = MyThread("Salut")
        print("Fan OK")
        self.fan.start()
        print("Fan Start OK")
        # VAR AFTER UPDATE SPEED
        self.manuel_auto_pareprise_fan = self.fan.manuel_auto_pareprise_fan
        self.get_recyclage_air = self.fan.get_recyclage_air()
        self.btn_bue_status = self.fan.btn_bue_status
        self.get_position_fan = self.fan.get_position_fan()

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
        self.cam_arrire = False
        
        bue_avant_status_get = self.fan.manuel_auto_pareprise_fan
        if bue_avant_status_get == "21" or bue_avant_status_get == "11":
            self.bue_avant_status=True
        
        print("--- MENU ----")
        self.menu = Frame(self.fullscreen,width=110, height=580, bg='#888989',bd=1)
        self.menu.pack_propagate(0)
        self.menu.pack(side=LEFT, expand=False)
        self.create_MenuBar()
        self.init_Menu_Home()
        self.init_Menu_Fan()
        self.clear_widgets()
        #self.show_Menu_Home()
        print("-- SHOW MENU FAN --")
        self.show_Menu_Fan()

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



    #######################################################################
    #                                FAN                                  #
    #######################################################################
    def clear_Menu_Fan(self):
        if 'menu_fan' in dir(self):
            self.menu_fan.pack_forget()

    def show_Menu_Fan(self):
        self.clear_widgets()
        #self.menu_fan.grid(fill='both')
        self.menu_fan.pack(fill='both',expand=YES)#,side=BOTTOM
    
    def init_Menu_Fan(self):
        background_color = '#c6c6dd' #4d4d7f
        self.menu_fan = Frame(self.space,width=700,height=500,bg=background_color,bd=0,highlightthickness=0)


        self.label_espace = Label(self.menu_fan,text="",bg=background_color,bd=0,highlightthickness=0)
        self.label_espace.grid(ipady=70,row=1,column=0)
        self.label_espace_droite = Label(self.menu_fan,text="",bg=background_color,bd=0,highlightthickness=0)
        self.label_espace_droite.grid(ipady=70,row=1,column=3)


        #### BOUTTON TEMPERATURE
        ### Slider Gauche OK
        self.slider_Chaud_gauche = Scale(
        self.menu_fan,from_=0,to=23,orient='horizontal',command=self.slider_changed_chaud_Gauche,width=70,
        troughcolor='#343b48',highlightcolor="#55aaff",showvalue=0,bd=0,bg="#4d4d7f")
        self.slider_Chaud_gauche.grid(pady=0,row=3,column=0)
        self.slider_Chaud_gauche['state'] = 'normal'
        value_slider_gauche_data = self.fan.temp_fan_RIGHT
        self.slider_Chaud_gauche.set(value_slider_gauche_data)
        self.slider_Chaud_gauche_label = Label(self.menu_fan,bg="#4d4d7f",fg="#e77100",font=("Courrier", 30),text=self.fan.convert_Temp_fan_slide_to_tmp(value_slider_gauche_data))
        self.slider_Chaud_gauche_label.grid(pady=30,stick=S,row=2,column=0)

        ### Slider Droit OK
        self.slider_Chaud_droit = Scale(
        self.menu_fan,from_=0,to=23,orient='horizontal',command=self.slider_changed_chaud_droit,width=70,
        troughcolor='#343b48',highlightcolor="#55aaff",showvalue=0,bd=0,bg="#4d4d7f")
        self.slider_Chaud_droit.grid(pady=0,row=3,column=2)
        self.slider_Chaud_droit['state'] = 'normal'
        value_slider_droit_data = self.fan.temp_fan_LEFT
        self.slider_Chaud_droit.set(value_slider_droit_data)
        self.slider_Chaud_droit_label = Label(self.menu_fan,bg="#4d4d7f",fg="#e77100",font=("Courrier", 30),text=self.fan.convert_Temp_fan_slide_to_tmp(value_slider_droit_data))
        self.slider_Chaud_droit_label.grid(pady=30,stick=S,row=2,column=2)

        ### Recyclage D'air OK
        self.image_recycle_aire = PhotoImage(file=f'{self.file}Images/Fan/Recycle_{self.fan.get_recyclage_air()}.png').zoom(1) #.subsample(32)
        self.image_recycle_aire = self.image_recycle_aire.subsample(6, 6)
        self.button_image_recycle_aire = Button(self.menu_fan,image=self.image_recycle_aire,bg=background_color, fg='#4d4d7f',
        activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.combineFunc(self.fan.recyclage_air, self.Update_Menu_Fan))
        self.button_image_recycle_aire.grid(row=3,column=1)



        ### Boutton Ventilo OK
        self.image_speed_fan_up = PhotoImage(file=f'{self.file}Images/Fan/Speed.png').zoom(1) #.subsample(32)
        self.image_speed_fan_up = self.image_speed_fan_up.subsample(6, 6)
        self.button_image_speed_fan_up = Button(self.menu_fan,image=self.image_speed_fan_up,bg=background_color, fg='#4d4d7f',
        activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.combineFunc(self.fan.set_speed_up , self.Update_Menu_Fan))
        #self.button_image_speed_fan_up.grid(ipady=50,stick=N,row=1,column=1)

        self.image_speed_fan_down = PhotoImage(file=f'{self.file}Images/Fan/Speed.png').zoom(1) #.subsample(32)
        self.image_speed_fan_down = self.image_speed_fan_down.subsample(8, 8)
        self.button_image_speed_fan_down = Button(self.menu_fan,image=self.image_speed_fan_down,bg=background_color, fg='#4d4d7f',
        activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.combineFunc(self.fan.set_speed_down , self.Update_Menu_Fan))
        #self.button_image_speed_fan_down.grid(ipady=0,stick=S,row=1,column=1)

        self.slider_speed_fan_label = Label(self.menu_fan,bg="#4d4d7f",fg="#e77100",font=("Courrier", 30),
        text=self.fan.get_speed)
        #self.slider_speed_fan_label.grid(stick=N,row=2,column=1)

        ### Bouton HAUT bue_avant 
        self.image_fan_bue_avant = PhotoImage(file=f'{self.file}Images/Fan/bue_{self.fan.btn_bue_status}.png').zoom(1) #.subsample(32)
        self.image_fan_bue_avant = self.image_fan_bue_avant.subsample(3, 3)
        self.button_image_fan_bue_avant = Button(self.menu_fan,image=self.image_fan_bue_avant,bg=background_color, fg='#4d4d7f',
        activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.combineFunc(self.fan.bue_one_click , self.Update_Menu_Fan))
        #self.button_image_fan_bue_avant.pack(padx=15,pady=50,anchor=CENTER)
        self.button_image_fan_bue_avant.grid(row=0,column=0)

        self.image_auto = PhotoImage(file=f'{self.file}Images/Fan/manuel_auto_{self.fan.manuel_auto_pareprise_fan}.png').zoom(1) #.subsample(32)
        self.image_auto = self.image_auto.subsample(3, 3)
        self.button_image_auto = Button(self.menu_fan,image=self.image_auto,bg=background_color, fg='#4d4d7f',activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.combineFunc(self.fan.change_position_Manuel_auto_ac , self.Update_Menu_Fan))
        self.button_image_auto.grid(row=0,column=1)

        self.image_fan_s_c = PhotoImage(file=f'{self.file}Images/Fan/position_{self.fan.get_position_fan()}.png').zoom(1) #.subsample(32)
        self.image_fan_s_c = self.image_fan_s_c.subsample(3, 3)
        self.button_image_fan_s_c = Button(self.menu_fan,image=self.image_fan_s_c,bg=background_color, fg='#4d4d7f',activebackground="#4d4d7f",borderwidth=0,bd=0,highlightthickness=0,command=self.combineFunc(self.fan.change_position_fan , self.Update_Menu_Fan))
        self.button_image_fan_s_c.grid(row=0,column=2)

        self.menu_fan.pack_forget()



    def Update_Menu_Fan(self):
        ## UPDATE MANUEL | AUTO | OFF | AUTO AC
        manuel_auto_fan = self.fan.manuel_auto_pareprise_fan ### UPDATE IMAGE MANUEL
        #if manuel_auto_fan != 0xA2:
        if self.fan.manuel_auto_pareprise_fan != manuel_auto_fan:
            self.manuel_auto_pareprise_fan = self.fan.manuel_auto_pareprise_fan ## UPDATE VAR SPEED
            self.image_auto = PhotoImage(file=f'{self.file}Images/Fan/manuel_auto_{manuel_auto_fan}.png').zoom(1) 
            self.image_auto = self.image_auto.subsample(3, 3)
            self.button_image_auto.configure(image=self.image_auto)
            ## CACHER SPEED
            if manuel_auto_fan == 0x22 or manuel_auto_fan == 0x11 or manuel_auto_fan == 0x62 or manuel_auto_fan == 0x21:
                if self.fan.get_speed() != 15:
                    self.slider_speed_fan_label.grid(stick=N,row=2,column=1)
                    self.slider_speed_fan_label.configure(text=self.fan.get_speed())
            else:
                self.button_image_speed_fan_up.grid_forget()
                self.button_image_speed_fan_down.grid_forget()
                self.slider_speed_fan_label.grid_forget()

        ## UPDATE AIR RECYCLE
        if self.get_recyclage_air != self.fan.get_recyclage_air():
            self.get_recyclage_air = self.fan.get_recyclage_air()
            self.image_recycle_aire = PhotoImage(file=f'{self.file}Images/Fan/Recycle_{self.fan.get_recyclage_air()}.png').zoom(1)
            self.image_recycle_aire = self.image_recycle_aire.subsample(6, 6)
            self.button_image_recycle_aire.configure(image=self.image_recycle_aire)

        ## UPDATE Bue 
        if self.btn_bue_status != self.fan.btn_bue_status : 
            self.btn_bue_status = self.fan.btn_bue_status
            self.image_fan_bue_avant = PhotoImage(file=f'{self.file}Images/Fan/bue_{self.fan.btn_bue_status}.png').zoom(1)
            self.image_fan_bue_avant = self.image_fan_bue_avant.subsample(3, 3)
            self.button_image_fan_bue_avant.configure(image=self.image_fan_bue_avant)

        ### POSITION FAN
        if self.get_position_fan != self.fan.get_position_fan():
            self.get_position_fan = self.fan.get_position_fan()
            self.image_fan_s_c = PhotoImage(file=f'{self.file}Images/Fan/position_{self.fan.get_position_fan()}.png').zoom(1) #.subsample(32)
            self.image_fan_s_c = self.image_fan_s_c.subsample(3, 3)
            self.button_image_fan_s_c.configure(image=self.image_fan_s_c)

    def combineFunc(self, *funcs):
        def conbinedFunc(*args,**kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return conbinedFunc 


    ######################################### TEMPERATURE FAN     ######################################

    def slider_changed_chaud_Gauche(self,var):
        self.slider_Chaud_gauche_label.configure(text=self.fan.convert_Temp_fan_slide_to_tmp(var))
        self.fan.temp_fan_LEFT = self.fan.convert_Temp_fan_to_hexa(self.fan.convert_Temp_fan_slide_to_tmp(var))

    def slider_changed_chaud_droit(self,var):
        self.slider_Chaud_droit_label.configure(text=self.fan.convert_Temp_fan_slide_to_tmp(var))
        self.fan.temp_fan_RIGHT = self.fan.convert_Temp_fan_to_hexa(self.fan.convert_Temp_fan_slide_to_tmp(var))


    #########################################################################
    #                                Home                                   #
    #########################################################################

    def show_Menu_Home(self):
        self.clear_widgets()
        self.menu_home.pack(fill='both',expand=YES)
        
    def clear_home(self):
        if 'label_title' in dir(self):
            self.menu_home.pack_forget()
            if self.cam_arrire :
                self.vid.__del__()
                self.canvas.destroy()
            
            #self.label_title.destroy()
            #self.button_netflix.destroy()

    def init_Menu_Home(self):
        self.ssh = True
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
        self.set_light()
        self.create_ssh_button()
        self.Active_WIFI()
        self.Active_Bluetooth()

    ## UPDATE 
    def Active_UPDATE(self):
        self.image_update = PhotoImage(file=f"{self.file}Images/Home/update.png").zoom(1) #.subsample(32)
        self.image_update = self.image_update.subsample(7)
        self.button_wifi = Button(self.menu_home,image=self.image_update,command=self.open_wifi)
        self.button_wifi.grid(padx=10,pady=10,row=0,column=5)

    #def open_update(self):
        #ch = os.system("pwd")
        #cmd=f'sudo screen -d -m {self.file}network.sh'
        #os.system(cmd)

    ## WIFI
    def Active_WIFI(self):
        self.image_wifi = PhotoImage(file=f"{self.file}Images/Home/wifi.png").zoom(1) #.subsample(32)
        self.image_wifi = self.image_wifi.subsample(7)
        self.button_wifi = Button(self.menu_home,image=self.image_wifi,command=self.open_wifi)
        self.button_wifi.grid(padx=10,pady=10,row=0,column=5)

    def open_wifi(self):
        cmd=f'sudo screen -d -m {self.file}network.sh'
        os.system(cmd)

    #Bluetooth
    def Active_Bluetooth(self):
        self.image_Bluetooth = PhotoImage(file=f"{self.file}Images/Home/bluetooth.png").zoom(1) #.subsample(32)
        self.image_Bluetooth = self.image_Bluetooth.subsample(7)
        self.button_Bluetooth = Button(self.menu_home,image=self.image_Bluetooth,command=self.open_Bluetooth())
        self.button_Bluetooth.grid(padx=10,pady=10,row=0,column=6)

    def open_Bluetooth(self):
        cmd=f'sudo screen -d -m {self.file}bluetooth.sh'
        os.system(cmd)

    # NETFLIX
    def create_netflix_button(self):
        ### Menu Netflix
        self.image_netflix = PhotoImage(file=f"{self.file}Images/Home/netflix.png").zoom(1) #.subsample(32)
        self.image_netflix = self.image_netflix.subsample(7)
        self.button_netflix = Button(self.menu_home,image=self.image_netflix,bg='#888989',command=self.open_netflix)
        #self.button_netflix.pack(padx=10,anchor=NW)
        self.button_netflix.grid(padx=10,pady=10,row=0,column=0)
        #self.button_netflix = Button(self.space,text="Netflix",font=("Courrier",25), bg='white',fg='#41B77F',command=self.open_netflix)
        #self.button_netflix.pack(anchor=NW)



    def open_netflix(self):
        self.video_source = 0
        #self.video_source = self.cam
        #self.cam = self.cam+1
        if self.cam_arrire :
            self.vid.__del__()
            self.canvas.destroy()
        else:
            self.vid = MyVideoCapture(self.video_source)
            self.canvas = Canvas(self.menu_home, width = self.vid.width, height = self.vid.height)
            self.canvas.place(x=0, y=0) #,relwidth=1, relheight=1
        self.cam_arrire = not self.cam_arrire

        # Button that lets the user take a snapshot
        #self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        #webbrowser.open_new("https://www.netflix.com/browse")

    def returnCameraIndexes(self):
        # checks the first 10 indexes.
        index = 0
        arr = []
        i = 10
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr

    def update(self):
    # Get a frame from the video source
        if self.cam_arrire :
            ret, frame = self.vid.get_frame()
            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image((self.vid.width/2), (self.vid.height/2), image = self.photo)
            self.window.after(self.delay, self.update)

    def set_light(self):
        # changer la luminosité 
        self.slider_luminositer = Scale(
        self.menu_home,from_=0,to=100,orient='horizontal',command=self.slider_set_light,width=70,
        troughcolor='#343b48',highlightcolor="#55aaff",showvalue=0,bd=0,bg="#4d4d7f")
        #self.slider_luminositer.pack(padx=0, pady=0,anchor=NW)
        self.slider_luminositer.grid(padx=10,pady=10,row=0,column=1)

    def slider_set_light(self,var):
        cmd=f"sudo brightnessctl -d intel_backlight -c backlight s {var}%"
        os.system(cmd)

    def create_ssh_button(self):
        ### Menu ssh
        self.image_ssh = PhotoImage(file=f"{self.file}Images/Home/ssh.png").zoom(1) #.subsample(32)
        self.image_ssh = self.image_ssh.subsample(7)
        self.button_ssh = Button(self.menu_home,image=self.image_ssh,bg='#888989',command=self.open_ssh())
        self.button_ssh.grid(padx=10,pady=10,row=0,column=2)

    def open_ssh(self):
        if self.ssh == True:
            cmd='sudo /etc/init.d/ssh stop'
            self.ssh = False
        else:
            cmd="sudo /etc/init.d/ssh start"
            self.ssh = True
        os.system(cmd)

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
    # def data_change(self,after,new):
    #     fin = open(f"{self.file}data.txt", "rt")
    #     data = fin.read()
    #     data = data.replace(f'{after}', f'{new}')
    #     fin.close()
    #     fin = open(f"{self.file}data.txt", "wt")
    #     fin.write(data)
    #     fin.close()

    #def get_data(self,key):
    #    with open(f'{self.file}data.txt') as f:
    #        lines = f.readlines()
    #        for line in lines:
    #            if key in line:
    #                return line.replace(key,"").replace("\n","")
    #                break

class MyVideoCapture:

    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #self.width = self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        #self.height = self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                    return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def returnCameraIndexes(video):
        # checks the first 10 indexes.
        index = 0
        arr = []
        i = 10
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr




from time import sleep
import can
from threading import Thread

class MyThread(Thread):

    def __init__(self,argument, **kwargs):
        super(MyThread, self).__init__(**kwargs)
        #print(subprocess.check_output("sudo modprobe vcan && sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan0", shell=True))
        test = str(subprocess.check_output("echo cc$(sudo ip a | grep can0)", shell=True)).strip().replace("\\n'","").replace("b'","")
        if len(test) > 2:
            print("oui")
            print(subprocess.check_output("sudo modprobe can_raw && sudo modprobe can_dev && sudo ip link set can0 up type can bitrate 125000 sample-point 0.875", shell=True))
        else:
            print("non") ## CREATE VIRTUAL CAN
            #subprocess.check_output("sudo ip link add dev can0 type vcan",shell=True)#&& sudo insmod /home/pi/Desktop/voiture_207_clim_rpi3/usb2can/usb_8dev.ko
            print(str(subprocess.check_output("sudo modprobe vcan && sudo ip link add dev can0 type vcan && sudo ip link set up can0 && ip a", shell=True)))
        
        self.bus = can.Bus(interface='socketcan',channel='can0',receive_own_messages=False)
        print("bus can OK")
        self.argument = argument
        self.manuel_auto_pareprise_fan = 0xA2
        self.speed_fan = 0x0F
        self.position_fan = 0x50
        self.recycle_air_fan = 0x00
        self.position_fan_save=0x50
        self.recycle_air_fan_save=0x00
        self.temp_fan_LEFT = 0x0B
        self.temp_fan_RIGHT = 0x0B
        self.manuel_auto_pareprise_fan_data_send_2_fois_max=0
        self.manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant=0
        self.btn_bue_status = 4
        self.btn_change_position_Manuel_auto_ac_status = 1
        print("can var OK")

        
    def get_speed(self):
        return self.speed_fan
    def set_speed_up(self):
        if self.speed_fan == 0x0F:
            self.speed_fan = 0
        elif self.speed_fan != 7:
            self.manuel_auto_pareprise_fan == 0x22
            self.speed_fan = self.speed_fan + 1
    def set_speed_down(self):
        if self.speed_fan != 0 and self.speed_fan != 0x0F:
            self.speed_fan = self.speed_fan - 1

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
            return 0x00
        elif tmp == "14":
            return 0x01
        elif tmp == "15":
            return 0x02
        elif tmp == "16":
            return 0x03
        elif tmp == "17":
            return 0x04
        elif tmp == "18":
            return 0x05
        elif tmp == "18.5":
            return 0x06
        elif tmp == "19":
            return 0x07
        elif tmp == "19.5":
            return 0x08
        elif tmp == "20":
            return 0x09
        elif tmp == "20.5":
            return 0x0A
        elif tmp == "21":
            return 0x0B
        elif tmp == "21.5":
            return 0x0C
        elif tmp == "22":
            return 0x0D
        elif tmp == "22.5":
            return 0x0E
        elif tmp == "23":
            return 0x0F
        elif tmp == "23.5":
            return 0x10
        elif tmp == "24":
            return 0x11
        elif tmp == "25":
            return 0x12
        elif tmp == "26":
            return 0x13
        elif tmp == "27":
            return 0x14
        elif tmp == "28":
            return 0x15
        elif tmp == "HI":
            return 0x16

    def clim_off(self):
        #A2 00 0F
        self.manuel_auto_pareprise_fan = 0xA2
        self.speed_fan = 0x0F

    def get_recyclage_air(self):
        return self.recycle_air_fan
    def recyclage_air(self):
        if self.recycle_air_fan == 0x10:
            return
        if self.recycle_air_fan == 0x00:# or self.recycle_air_fan == 0x10:
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

    ### MANUEL AUTO AC
    def change_position_Manuel_auto_ac(self):
        if self.manuel_auto_pareprise_fan == 0x11 or self.manuel_auto_pareprise_fan == 0x21 or self.manuel_auto_pareprise_fan == 0x62:
            return

        if self.btn_change_position_Manuel_auto_ac_status == 4:
            self.btn_change_position_Manuel_auto_ac_status = 0

        if self.btn_change_position_Manuel_auto_ac_status == 0: ## OFF
            self.clim_off()
        elif self.btn_change_position_Manuel_auto_ac_status == 1: ## MANUEL
            self.manuel_auto_pareprise_fan = 0x22
            self.manuel_fan_control_show()
            
        elif self.btn_change_position_Manuel_auto_ac_status == 2: ## AUTO
            self.manuel_auto_pareprise_fan = 0x20
        elif self.btn_change_position_Manuel_auto_ac_status == 3: ## AUTO A/C
            self.manuel_auto_pareprise_fan = 0x00
        
        self.btn_change_position_Manuel_auto_ac_status = self.btn_change_position_Manuel_auto_ac_status + 1

    def manuel_fan_control_show(self): ## Pour aficher les FAN
        self.speed_fan = 0x00
        app.button_image_speed_fan_up.grid(ipady=50,stick=N,row=1,column=1)
        app.button_image_speed_fan_down.grid(ipady=0,stick=S,row=1,column=1)
        app.slider_speed_fan_label.grid(stick=N,row=2,column=1)
        app.slider_speed_fan_label.configure(text=self.get_speed())
        self.btn_change_position_Manuel_auto_ac_status = 2 ## POUR QUAND ON CLIC SUR BUE ALORS QU'il ES EN MANUEL 
        #ES QUE l'on n'a plus la bue et on veux passer en auto on n'appuie pas 2 fois


    def bue_one_click(self):
        if self.btn_bue_status == 4:
            self.btn_bue_status = 0
        self.manuel_fan_control_show()
        if self.btn_bue_status == 0:## AVANT
            self.position_fan_save=self.position_fan
            self.recycle_air_fan_save=self.recycle_air_fan
            self.manuel_auto_pareprise_fan = 0x21
        elif self.btn_bue_status == 1: ## ARIRER
            self.manuel_auto_pareprise_fan = 0x62
            self.position_fan=self.position_fan_save
            self.recycle_air_fan=self.recycle_air_fan_save
        elif self.btn_bue_status == 2: ## LES DEUX
            self.position_fan_save=self.position_fan
            self.recycle_air_fan_save=self.recycle_air_fan
            self.manuel_auto_pareprise_fan = 0x21
        elif self.btn_bue_status == 3:## RIEN
            self.manuel_auto_pareprise_fan = 0x62
            self.position_fan=self.position_fan_save
            self.recycle_air_fan=self.recycle_air_fan_save
        
        self.btn_bue_status = self.btn_bue_status + 1

    def run(self):
        while True:
            if self.manuel_auto_pareprise_fan == 0xA2 and self.speed_fan != 0x0F: ## Activer la clim Car SPEED pas à OFF et clim A2
                self.manuel_auto_pareprise_fan = 0x22

            if self.manuel_auto_pareprise_fan == 0x62:### BUE à l'arriere
                if self.manuel_auto_pareprise_fan_data_send_2_fois_max == 2:
                    self.manuel_auto_pareprise_fan_data_send_2_fois_max = 0
                    if self.btn_bue_status == 2 or self.btn_bue_status == 4:
                        self.manuel_auto_pareprise_fan = 0x22 ## MANUEL
                    elif self.btn_bue_status == 3:
                        self.manuel_auto_pareprise_fan = 0x21 ## CLIM AVANT
                self.manuel_auto_pareprise_fan_data_send_2_fois_max = self.manuel_auto_pareprise_fan_data_send_2_fois_max + 1


            if self.manuel_auto_pareprise_fan == 0x21:### TRUC à l'avant
                if self.manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant == 1:
                    self.manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant=0
                    self.manuel_auto_pareprise_fan=0x11
                self.manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant = self.manuel_auto_pareprise_fan_data_send_1_fois_max_truc_avant + 1
                self.position_fan = 0x10
                self.recycle_air_fan=0x10
                app.Update_Menu_Fan()
            
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
            #print("Can Message OK")
            self.bus.send(message)
            #print("Can send OK")

            sleep(0.02)


print("Afficher")
# afficher
app = MyApp()
app.window.mainloop()


### DATA


### Image 

# Manuel / AUTO / A/C

# Manuel 0x22 = 34 = 34.png
# Manuel 0x62 = 98 = 98.png (bue)
# Manuel 0x21 = 33 = 33.png (bue)
# Manuel 0x11 = 17 = 17.png (bue)
# AUTO = 0x20 = 32 = 32.png
# AUTO & AC = 0x00 = 0 = 0.png
# OFF = 0xA2 = 162 = 162.png

# 0 = OFF 
# 1 = Manuel 
# 2 = Auto
# 3 = Auto AC
# SI ON GET ALORS
# 1 = OFF 
# 2 = Manuel 
# 3 = Auto
# 4 = Auto AC


# Recyclage d'air

# ON = 30 = 48 = 48.png
# OFF  = 10 =  16 = 16.png (bue) 
# OFF  = 00 =  0 = 0.png

### BUE
# 0 = AVANT
# 1 = ARRIERE
# 2 = les deux
# 3 = Rien
# SI ON GET ALORS
# 1 = AVANT
# 2 = ARRIERE
# 3 = Les Deux 
# 4 = rien


### CTRL + K + C = Commenter
### CTRL + K + U = Décommter
