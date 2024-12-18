#import this
import tkinter as tk
from tkinter import Frame, ttk
from tokenize import String
from Keyboard import KeyBoard
from FlikerScreen import flikerWindow
from MainWindow import mainWindow
from CFF_FOVEA import CffFovea
from CFF_PARA_FOVEA import CffParaFovea
from Admin import Admin
from BRK_FOVEA_1 import BrkFovea_1
from BRK_FOVEA_2 import BrkparaFovea
from globalvar import pageDisctonary
from globalvar import globaladc
from globalvar import currentPatientInfo
from tkinter import messagebox
from PIL import Image, ImageTk
import os.path
import subprocess as sp
import json

Font =  ("Arial",20)
Font2 = ("Arial",10)
x = 80

class ClickableLabel(tk.Label):
    """Custom Label class that can handle click events"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Button-1>', self._on_click)
        self.callback = None
    
    def _on_click(self, event):
        globaladc.buzzer_3()  # Call the buzzer function first
        if self.callback:
            self.callback()
    
    def on_click(self, callback):
        self.callback = callback

class StatrupClass:
    def HideStartButton(self):
        self.StartButton.place_forget()

    def ShowStartButton(self):
        self.StartButton.place (x=x+220, y=500)

    def HideAdminButton(self):
        self.AdminButton.place_forget()

    def ShowAdminButton(self):
        self.AdminButton.place (x=x+10, y=500)

    def HideFlikerButton(self):
        self.FlikerDemoButton.place_forget()

    def ShowFlikerButton(self):
        self.FlikerDemoButton.place (x=x+420, y=500)

    def ShowHomeButton(self):
        self.HomeScreenButton.place (x=700,y=500)  

    def HideHomeButton(self):
        self.HomeScreenButton.place_forget()        

    def setup_header(self):
        """Setup header section with logo and title."""
        self.header_frame.pack(fill='x')

        try:
            logo = Image.open("logo.png")
            logo = logo.resize((44, 23))
            self.logo_img = ImageTk.PhotoImage(logo)
            self.logo_label = tk.Label(self.header_frame, image=self.logo_img, bg='#1f2836')
            self.logo_label.place(x=0, y=10)
        except:
            print("Logo image not found")

        # Header labels
        tk.Label(self.header_frame, text="Vekaria Healthcare", 
                font=('Helvetica Neue', 16, 'bold'), bg='#1f2836', fg='white').place(x=60, y=10)
        tk.Label(self.header_frame, text="V1.0",
                font=('Helvetica Neue', 14,'bold'), bg='#1f2836', fg='white').place(x=930, y=10)


        wifi_image = Image.open("wifi_logo.png")
        wifi_image = wifi_image.resize((41, 31), Image.LANCZOS)  # Resize to match Qt dimensions
        self.wifi_icon = ImageTk.PhotoImage(wifi_image)
                    
                    # Create the clickable WiFi icon label
        self.wifi_label = ClickableLabel(
                        self.header_frame,
                        image=self.wifi_icon,
                        bg='#1f2836'
                    )


    def __init__(self) -> None:        
        self.window = tk.Tk ()
        self.window.attributes('-fullscreen', True) 
        self.window.geometry ("1024x600")
        self.window.resizable (0, 0)
        self.header_frame = tk.Frame(self.window, bg='#1f2836', height=41)

        self.window.configure(background='#64edb4')
        self.mainFrame = Frame(self.window) 
        self.flikerFrame = Frame(self.window)
        self.cffFoveaFrame = Frame(self.window)
        self.CffParaFoveaFrame = Frame(self.window)
        self.brkf1Frame =  Frame(self.window)
        self.brkf2Frame = Frame(self.window)
        self.adminFrame = Frame(self.window)
        currentPatientInfo.log_update("System_Started")        
        self.mainFrame.config(bg='#64edb4')
        self.flikerFrame.config(bg='#64edb4')
        self.cffFoveaFrame.config(bg='#64edb4')
        self.CffParaFoveaFrame.config(bg='#64edb4')
        self.brkf1Frame.config(bg='#64edb4')
        self.brkf2Frame.config(bg='#64edb4')
        self.adminFrame.config(bg='#64edb4')
        globaladc.fan_on()
        #load all the frames
        self.mw = mainWindow(self.mainFrame)
        self.fw = flikerWindow(self.flikerFrame)
        self.brkf_1 = BrkFovea_1(self.brkf1Frame)
        self.brkf_2 = BrkparaFovea(self.brkf2Frame)
        self.cff = CffFovea(self.cffFoveaFrame)
        self.cffP =CffParaFovea(self.CffParaFoveaFrame)
        self.admin = Admin(self.adminFrame)
        
   
        #intialize the buttons
        def handleAdmin():
            globaladc.get_print ("tobe implemented")
            globaladc.buzzer_1()
            self.setup_header()
            self.ShowHomeButton()
            self.admin.show()
            self.HideAdminButton()
            self.HideFlikerButton()
            self.HideStartButton()
            currentPatientInfo.log_update("Admin_pressed")

        self.AdminButton = tk.Button (self.window,
                                    text="Admin",
                                    command=handleAdmin, font=Font,
                                    width=10)


    def handleStart(self):
        # First validate user input
        if self.mw.ValidateUserInput() == False:
            globaladc.buzzer_1()
            messagebox.showerror("Data Error", "Please enter User information")
            return

        # Check USB state
        state = self.find_usb()
        if state == 'false':
            globaladc.buzzer_1()
            messagebox.showerror("USB Error", "Please check USB Drive\n(Name:-\"USB_DEVICE\")\nInserted Properly \nif not, insert \nif inserted, remove and Re-insert")
            return

        try:
            # Get the latest patient data from JSON
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                "patient_data", f"patient_{currentPatientInfo.Name.split()[0]}.json")
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    patient_data = json.load(f)

                # Set all states from JSON data
                currentPatientInfo.setAlchohol_state("Y" if patient_data['alcohol'] == "Yes" else "N")
                currentPatientInfo.setSmoking_state("Y" if patient_data['smoking'] == "Yes" else "N")
                currentPatientInfo.setDiabetes_state("Y" if patient_data['diabetes']['has_diabetes'] == "Yes" else "N")
                currentPatientInfo.setHypertension_state("Y" if patient_data['bp']['has_bp'] == "Yes" else "N")

                # Additional data that might be useful
                if 'diabetes' in patient_data and 'value' in patient_data['diabetes']:
                    currentPatientInfo.diabetes_value = patient_data['diabetes']['value']
                if 'bp' in patient_data and 'value' in patient_data['bp']:
                    currentPatientInfo.bp_value = patient_data['bp']['value']

                globaladc.buzzer_3()
                currentPatientInfo.log_update("Start_pressed")
                self.ShowTestRunScreen()

            else:
                globaladc.buzzer_1()
                messagebox.showerror("Data Error", "Patient data not found. Please save patient information first.")
                return

        except Exception as e:
            globaladc.buzzer_1()
            messagebox.showerror("Error", f"Error loading patient data: {str(e)}")
            return
            

        self.StartButton = tk.Button (self.window,
                                    text="Start", font=Font,
                                    command=self.handleStart, bg='Green',
                                    width=10)

        
            
        self.FlikerDemoButton = tk.Button (self.window,
                                text="Flicker Demo",
                                command=self.handleFlikerDrmo,font=Font,
                                width=10)

        self.HomeScreenButton = tk.Button (self.window,
                                text="Home",
                                command=self.handleHomeScreen,font=Font,
                                width=10)

        
        
        self.saveButton = tk.Button (self.brkf1Frame,
                                 text="Save",bg='#a0f291',
                                 command=self.handleSave, font=Font,
                                 width=10)
        self.brkf_1.saveButton = self.saveButton
        
        self.saveButton_2 = tk.Button (self.brkf2Frame,
                                text="Save",bg='#a0f291',
                                command=self.handleSave_2, font=Font,
                                width=10)
        self.brkf_2.saveButton = self.saveButton_2
        
        
    def main(self):
        globaladc.all_led_off()
        globaladc.fan_on()
        pageDisctonary["MainScreen"] = self.mw        
        pageDisctonary["FlikerScreen"] = self.fw
        pageDisctonary["BrkFovea_1"] = self.brkf_1
        pageDisctonary["CffFovea"] = self.cff
        pageDisctonary["CffParaFovea"] = self.cffP
        pageDisctonary["BrkparaFovea"] = self.brkf_2    
        pageDisctonary["Admin"] = self.admin

        self.mw.Load()
        self.fw.Load()
        self.cff.Load()
        self.cffP.Load()
        self.brkf_1.Load()
        self.brkf_2.Load()
        self.admin.Load()  
        globaladc.buzzer_1()      
        self.ShowMainScreen()
        self.window.mainloop()
        globaladc.buzzer_1()

        # globaladc.main_Prepair() # run this while loading main Screen
        #Main Window Application
        
             	# run this while loding 1st blank screen
        
        
            

        #fliker Deom  
    def handleFlikerDrmo(self):
        globaladc.buzzer_1()
        self.ShowFlikerScreen()


    def handleHomeScreen(self):
        globaladc.end_process()
        globaladc.skip_main_rset()
        globaladc.buzzer_1()
        sve= globaladc.get_save_no()        
        if sve == 1 :
            home=0
            cff_fovea_frq=globaladc.get_cff_fovea_frq()
            currentPatientInfo.SetCFF_F(cff_fovea_frq)        
            F_mpod = globaladc.get_cal_f_mpod()
            currentPatientInfo.SetF_mpod(F_mpod)
            #make same for home screen        
            #state=os.path.isdir('/media/pi/USB_DEVICE')        
            state=self.find_usb()
            if(state!= 'false'):      
                globaladc.get_print('Save to file to' + currentPatientInfo.Name+'.TXT')            
                #self.patient_switch_desable()
                currentPatientInfo.Save_brk(state)
                pageDisctonary['BrkparaFovea'].hide()
                globaladc.put_save_no(0)
                self.ShowMainScreen()                
            else:
                messagebox.showerror("USB Error","Please check USB Drive Inserted Properly \nif not inserted, insert it wait for a second and Press SAVE once again \nif inserted, remove and Re-insert again Wait-a-while and Press SAVE once again")
                return
        else:
            currentPatientInfo.log_update("Home_pressed")
            self.ShowMainScreen()

            
            
           

            #intial work flow show Main Screen
    def ShowMainScreen(self):  
        #globaladc.buzzer_1()
        self.ShowAdminButton()
        self.ShowStartButton()
        self.ShowFlikerButton()
        self.HideHomeButton()
        self.fw.hide()
        self.cff.hide()
        self.cffP.hide()
        self.brkf_1.hide()
        self.admin.hide()
        self.mw.show()
        currentPatientInfo.log_update("Enter_to_Main_screeen")
        # globaladc.main_Prepair() # run this while loading main Screen

    def ShowFlikerScreen(self):
        if self.mw.ValidateUserInput() == False :
                    messagebox.showerror("USB Error","Please enter User information")
                    return                        
        globaladc.buzzer_1()
        self.HideAdminButton()
        self.HideStartButton()
        self.HideFlikerButton()
        self.ShowHomeButton()
        self.fw.show()
        self.cff.hide()
        self.admin.hide()
        self.mw.hide()
        currentPatientInfo.log_update("Enter_to_Flicker_screeen")

    def ShowTestRunScreen(self):  
        #globaladc.buzzer_1()
        self.HideAdminButton()
        self.HideFlikerButton()
        self.HideStartButton()
        self.ShowHomeButton()
        self.fw.hide()
        self.mw.hide()
        self.cff.show()
        self.cffP.hide()
        self.admin.hide()
        currentPatientInfo.log_update_pashent()
        currentPatientInfo.log_update("Enter_to_CFF_screeen")
                

    def ShowTestRunScreen_2(self):  
        #globaladc.buzzer_1()
        self.HideAdminButton()
        self.HideFlikerButton()
        self.HideStartButton()
        self.ShowHomeButton()        
        self.fw.hide()
        self.mw.hide()
        self.cff.hide()
        self.cffP.show()        
        self.ShowMainScreen()
        self.admin.hide()
        currentPatientInfo.log_update("Enter_to_CFFP_screeen")
        
        
    def find_usb(self):        
        output = sp.getoutput("df -x squashfs")    
        poss=output.find("/media")    
        if poss == -1:
            return("false")
            currentPatientInfo.log_update("Drive_not_inserted")
        else :
            out =output[poss:]
            return(out)
        
    def handleSave(self):
        cff_fovea_frq=globaladc.get_cff_fovea_frq()
        globaladc.skip_main_rset()
        currentPatientInfo.SetCFF_F(cff_fovea_frq)        
        #state=os.path.isdir('/media/pi/USB_DEVICE')        
        state=self.find_usb()
        if(state!= 'false'):
            str_data = 'Save to file to' + currentPatientInfo.Name + '.TXT'
            globaladc.get_print(str_data)             
            if self.brkf_1.depthVal.get() == 0:
                log_data = "CFF_F-"+str(cff_fovea_frq)+",F_mpod-0.00"
                currentPatientInfo.log_update(log_data)
                currentPatientInfo.Save_brk_0(state) 
            elif self.brkf_1.depthVal.get() == 19: 
                currentPatientInfo.Save_brk_19(state)
                log_data = "CFF_F-"+str(cff_fovea_frq)+",F_mpod-+1.00"
                currentPatientInfo.log_update(log_data)
            globaladc.black_screen_initialize()
            pageDisctonary['BrkFovea_1'].hide()
            self.ShowMainScreen()
        else:
            messagebox.showerror("USB Error","Please check USB Drive Inserted Properly \nif not inserted, insert it Wait-a-while and Press SAVE once again \nif inserted, remove and Re-insert wait for a second again and Press SAVE once again")
            return
        # globaladc.main_screen_initialize()
        
    def non (self):
            globaladc.get_print('non')
        
    def handleSave_2(self):
        cff_F=globaladc.get_cff_fovea_frq()
        currentPatientInfo.SetCFF_F(cff_F)       
        globaladc.skip_main_rset()
        F_mpod=globaladc.get_cal_f_mpod()
        currentPatientInfo.SetF_mpod(F_mpod)
        
        cff_p=globaladc.get_cff_para_fovea_frq()
        currentPatientInfo.SetCFF_P(cff_p)
        
        F_SD=globaladc.get_cal_f_sd()
        currentPatientInfo.SetF_SD(F_SD)
        
        #make same for home screen        
        state=os.path.isdir('/media/pi/USB_DEVICE')        
        state=self.find_usb()
        if(state!= 'false'):
            log_data = "CFF_F-"+str(cff_F)+",CFF_P-"+str(cff_p)+",F_mpod-"+str(F_mpod)+",F_SD-"+str(F_SD)
            currentPatientInfo.log_update(log_data)
            str_data = 'Save to file to' + currentPatientInfo.Name +'.TXT'
            globaladc.get_print(str_data)            
            #self.patient_switch_desable()
            self.brkf_2.saveButton.config(command=self.non,text="Bussey",bg='#f24e79')
            currentPatientInfo.Save_brk_p(state)
            globaladc.all_led_off()
            pageDisctonary['BrkparaFovea'].hide()
            self.ShowMainScreen()
            self.brkf_2.saveButton.config(command=self.handleSave_2,text="Save",bg='#a0f291')
        else:
            messagebox.showerror("USB Error","Please check USB Drive Inserted Properly \nif not inserted, insert it wait for a second and Press SAVE once again \nif inserted, remove and Re-insert again Wait-a-while and Press SAVE once again")
            return
        # globaladc.main_Prepair()
        
