from tkinter import tk
from tkinter import ttk
import time
import RPi.GPIO as GPIO
from PIL import Image, ImageTk
from BRK_FOVEA_1 import BrkFovea_1
import PatientInfo
from globalvar import pageDisctonary
from globalvar import globaladc
from globalvar import currentPatientInfo
import PerodicThread

# Global variables
switch = 20
contt_fva = 34.5
Font = ("Arial", 15)
Font1 = ("Arial", 15)
Font2 = ("Arial", 20)
intervel = globaladc.get_cff_delay()
select = 1
cffValue_frq_x = 820
cffValue_frq_y = 40

class CffFovea:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg='black')
        self.frame.place(x=0, y=0, width=1024, height=612)
        
        # Initialize variables from old implementation
        self.response_count = 0
        self.skip_event = True
        self.threadCreated = False
        self.worker_cff = PerodicThread.PeriodicThread(intervel, self)  # Using global intervel
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0
        self.response_array = [0, 0, 0, 0, 0]
        
        # Create header frame
        self.header_frame = tk.Frame(self.frame, bg='#1f2836', height=41)
        self.header_frame.pack(fill='x')
        
        # Load logo (assuming you have the image file)
        try:
            logo = Image.open("VHC Logo.png")
            logo = logo.resize((44, 23))
            self.logo_img = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(self.header_frame, image=self.logo_img, bg='#1f2836')
            logo_label.place(x=0, y=10)
        except:
            print("Logo image not found")
        
        # Header labels - using global Font variables
        tk.Label(self.header_frame, text="Vekaria Healthcare", 
                font=('Helvetica Neue', 16, 'bold'), bg='#1f2836', fg='white').place(x=60, y=0)
        tk.Label(self.header_frame, text="V1.0",
                font=('Helvetica Neue', 14), bg='#1f2836', fg='white').place(x=930, y=0)
        
        # Sub header
        tk.Label(self.frame, text="Macular Densitometer                                                          CFF Fovea Test",
                font=Font2, bg='black', fg='white').place(x=0, y=40)
        
        # Side buttons
        side_buttons = [
            ("Flicker Demo", 150),
            ("CFF Fovea", 210),
            ("BRK Fovea", 270),
            ("CFF Para-Fovea", 330),
            ("BRK Para-Fovea", 390),
            ("Test Result", 450)
        ]
        
        for text, y in side_buttons:
            btn = tk.Button(self.frame, text=text, font=Font,
                          width=20, bg='black' if text != "CFF Fovea" else 'white',
                          fg='white' if text != "CFF Fovea" else 'black',
                          relief='solid', bd=2)
            btn.place(x=10, y=y)
        
        # Main content frame
        self.content_frame = tk.Frame(self.frame, bg='#1f2836')
        self.content_frame.place(x=280, y=110, width=711, height=441)
        
        # Data display
        self.data2_label = tk.Label(self.content_frame, text="24.5", 
                                  font=Font2, bg='black', fg='white')
        self.data2_label.place(x=580, y=30)
        
        # Results frame
        self.results_frame = tk.Frame(self.content_frame, bg='black', bd=3, relief='solid')
        self.results_frame.place(x=170, y=10, width=291, height=126)
        
        tk.Label(self.results_frame, text="CFF Fovea",
                font=Font2, bg='black', fg='white').place(x=10, y=10)
        self.data1_label = tk.Label(self.results_frame, text="23.5",
                                  font=Font2, bg='black', fg='white')
        self.data1_label.place(x=40, y=60)
        
        # Control buttons
        tk.Label(self.content_frame, text="Test Status",
                font=Font2, bg='#1f2836', fg='white').place(x=0, y=170)
        
        # Trial list - using global Font1
        self.trialList = tk.Listbox(self.content_frame, font=Font1, width=6)
        self.trialList.place(x=cffValue_frq_x, y=60)  # Using global position variables
        
        # Status labels - using global Font variables
        self.patentActionflabel = tk.Label(self.content_frame, 
                                         text="Patient's side Button \n Begins Trial",
                                         font=Font1, bg='white')
        self.cffValue_min = tk.Label(self.content_frame, text='    ', 
                                   font=Font, bg='white')
        self.cffValue_max = tk.Label(self.content_frame, text='    ', 
                                   font=Font, bg='white')
        self.cffValue_frq = tk.Label(self.content_frame, text='    ', 
                                   font=Font, bg='#F7F442')
        
        # Place the status labels
        self.cffValue_min.place(x=430, y=40)
        self.cffValue_max.place(x=500, y=40)
        self.cffValue_frq.place(x=cffValue_frq_x, y=cffValue_frq_y)  # Using global position variables
        self.patentActionflabel.place(x=380, y=100)

        # Navigation buttons with specified Font2
        self.home_btn = tk.Button(self.content_frame, text="Home",
                                font=Font2, bg='black', fg='white',
                                relief='solid', bd=1,
                                command=self.on_home)
        self.home_btn.place(x=300, y=380)
        
        self.next_btn = tk.Button(self.content_frame, text="Next",
                                font=Font2, bg='black', fg='white',
                                relief='solid', bd=1,
                                command=self.on_next)
        self.next_btn.place(x=440, y=380)

    def on_home(self):
        pageDisctonary['CffFovea'].hide()
        pageDisctonary['MainScreen'].show()

    def on_next(self):
        pageDisctonary['CffFovea'].hide()
        pageDisctonary['BrkFovea_1'].show()

    def handleuserButton(self, switch=switch):  # Using global switch
        globaladc.get_print('handle to be implemented')
        jmp = False
        self.patient_switch_desable()
        time.sleep(0.15)        
        
        if self.skip_event:
            self.patentActionflabel.place_forget()
            self.threadCreated = True
            
            if self.response_count == 0:
                self.freq_val_start = self.freq_val_start
            else:
                self.freq_val_start = self.min_apr + 6.5
                
            self.freq_val = self.freq_val_start   
            globaladc.fliker_start_g()
            time.sleep(0.2)             
            self.skip_event = False            
        else:
            self.skip_event = True
            time.sleep(0.5)
            
            if self.threadCreated:
                self.response_array[self.response_count] = self.freq_val
                self.trialList.insert(self.response_count, self.response_array[self.response_count])                
                self.min_apr = globaladc.get_cff_f_min_cal(self.response_count, self.freq_val)  
                self.response_count = self.response_count + 1
                self.cffValue_min.config(text=self.min_apr)                
                
                if self.response_count == 5:
                    self.max_apr = globaladc.get_cff_f_max_cal()                        
                    self.cffValue_max.config(text=self.max_apr)                    
                    avgval = globaladc.get_cff_f_avg_cal()
                    log_data = f"CFF_F-{avgval}"
                    currentPatientInfo.log_update(log_data)                    
                    time.sleep(1)
                    globaladc.buzzer_3()
                    self.hide()
                    pageDisctonary['BrkFovea_1'].show()
                    self.patient_switch_desable()
                    jmp = True
                
                self.cffValue_frq.config(text=self.freq_val)
        
        if not jmp:
            if self.skip_event:
                time.sleep(0.2) 
                globaladc.buzzer_3()            
            self.patient_switch_enable()

    def patient_switch_enable(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Using global switch
        GPIO.add_event_detect(switch, GPIO.RISING, callback=self.handleuserButton)
    
    def patient_switch_desable(self):
        GPIO.remove_event_detect(switch)  # Using global switch
    
    def show(self):
        self.frame.place(width=1024, height=600)
        self.reset_values()
        globaladc.cff_Fovea_Prepair()
        self.run_therad()
        globaladc.blue_led_off()
    
    def hide(self):
        self.stop_therad()
        self.frame.place_forget()
    
    def reset_values(self):
        self.cffValue_min.config(text='     ')
        self.cffValue_max.config(text='     ')
        self.cffValue_frq.config(text='     ')
        self.trialList.delete(0, tk.END)
        self.freq_val_start = contt_fva  # Using global contt_fva
        self.freq_val = self.freq_val_start
        self.response_array = [0, 0, 0, 0, 0]
        self.response_count = 0
        self.min_apr = 0
        self.max_apr = 0
        self.skip_event = True
        self.threadCreated = False

    def run_therad(self):
        self.worker_cff = PerodicThread.PeriodicThread(intervel, self)  # Using global intervel
        if not self.worker_cff.isStarted:
            self.worker_cff.start()
            self.patient_switch_enable()
    
    def stop_therad(self):
        if hasattr(self, 'worker_cff') and self.worker_cff.isStarted:
            self.worker_cff.stop()
            self.worker_cff.kill()
            self.patient_switch_desable()
            self.skip_event = True
            self.threadCreated = False
    
    def periodic_event(self):
        if not self.skip_event:
            self.freq_val = round((self.freq_val - 0.5), 1)
            self.cffValue_frq.config(text=self.freq_val)
            if self.freq_val < 5:
                self.skip_event = True
                self.threadCreated = False
                self.freq_val = self.freq_val_start
                self.cffValue_frq.config(text=self.freq_val)
                globaladc.buzzer_3()
            globaladc.put_cff_fovea_frq(self.freq_val)
        else:
            globaladc.put_cff_fovea_frq(35)
            globaladc.get_print('CF')

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1024x612')
    app = CffFovea(root)
    app.show()
    root.mainloop()