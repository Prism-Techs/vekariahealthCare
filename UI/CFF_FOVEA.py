import tkinter as tk
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

# Global variables and constants
switch = 20
contt_fva = 34.5
Font = ("Arial", 15)
Font1 = ("Arial", 15)
Font2 = ("Arial", 20)
intervel = globaladc.get_cff_delay()
select = 1
cffValue_frq_x = 820
cffValue_frq_y = 40





def hardware():
        CffFovea.handleuserButton()

class CffFovea:
    def __init__(self, root):
        """Initialize the CffFovea class with basic setup."""
        self.root = root
        self.frame = tk.Frame(root, bg='black')
        
        # Initialize state variables
        self.initialize_state_variables()
        
        # Create frames
        self.header_frame = tk.Frame(self.frame, bg='#1f2836', height=41)
        self.content_frame = tk.Frame(self.frame, bg='#1f2836')
        
        # Initialize UI elements (create but don't place them yet)
        self.initialize_ui_elements()

    def initialize_state_variables(self):
        """Initialize all state variables."""
        self.response_count = 0  
        self.skip_event = True
        self.threadCreated = False
        self.worker_cff = PerodicThread.PeriodicThread(intervel, self)
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0 
        self.response_array = [0, 0, 0, 0, 0]

    def initialize_ui_elements(self):
        """Create UI elements without placing them."""
        # Value display labels
        self.cffValue_min = tk.Label(self.content_frame, text='    ', font=Font, bg='white')
        self.cffValue_max = tk.Label(self.content_frame, text='    ', font=Font, bg='white')
        self.cffValue_frq = tk.Label(self.content_frame, text='    ', font=Font, bg='#F7F442')
        
        # Trial list and action label
        self.trialList = tk.Listbox(self.content_frame, font=Font1, width=6)
        self.patentActionflabel = tk.Label(self.content_frame, 
                                         text="Patient's side Button \n Begins Trial",
                                         font=Font1, bg='white')
        
        # Navigation buttons
        self.home_btn = tk.Button(self.content_frame, text="Home",
                                font=Font2, command=self.on_home,
                                bg='black', fg='white', relief='solid', bd=1)
        self.next_btn = tk.Button(self.content_frame, text="Next",
                                font=Font2, command=self.on_next,
                                bg='black', fg='white', relief='solid', bd=1)

    def Load(self):
        """Load and place all UI elements."""
        # Reset variables
        self.initialize_state_variables()
        
        # Setup header
        self.setup_header()
        
        # Setup main content
        self.setup_content()
        
        # Create side buttons
        self.create_side_buttons()

    def setup_header(self):
        """Setup header section with logo and title."""
        self.header_frame.pack(fill='x')

        try:
            logo = Image.open("VHC Logo.png")
            logo = logo.resize((44, 23))
            self.logo_img = ImageTk.PhotoImage(logo)
            self.logo_label = tk.Label(self.header_frame, image=self.logo_img, bg='#1f2836')
            self.logo_label.place(x=0, y=10)
        except:
            print("Logo image not found")

        # Header labels
        tk.Label(self.header_frame, text="Vekaria Healthcare", 
                font=('Helvetica Neue', 16, 'bold'), bg='#1f2836', fg='white').place(x=60, y=0)
        tk.Label(self.header_frame, text="V1.0",
                font=('Helvetica Neue', 14), bg='#1f2836', fg='white').place(x=930, y=0)

        # Main title
        tk.Label(self.frame, 
                text="Macular Densitometer                                                          CFF Fovea Test",
                font=Font2, bg='black', fg='white').place(x=0, y=40)

    def setup_content(self):
        """Setup main content area with all controls."""
        self.content_frame.place(x=280, y=110, width=711, height=441)

        # CFF label
        cfflabel = tk.Label(self.content_frame, text='CFF FOVEA :', 
                           font=Font, bg='#1f2836', fg='white')
        cfflabel.place(x=140, y=10)

        # Place value display elements
        self.cffValue_min.place(x=150, y=40)
        self.cffValue_max.place(x=220, y=40)
        self.cffValue_frq.place(x=520, y=30)
        self.trialList.place(x=520, y=60)
        self.patentActionflabel.place(x=100, y=100)

        # Status buttons
        self.setup_status_buttons()
        
        # Navigation buttons
        self.home_btn.place(x=300, y=380)
        self.next_btn.place(x=440, y=380)

    def setup_status_buttons(self):
        """Setup the status buttons."""
        machine_ready = tk.Button(self.content_frame, text="Machine Ready",
                                font=('Arial', 14, 'bold'), bg='#1a472a', fg='#4CAF50')
        machine_ready.place(x=50, y=230)

        flicker_start = tk.Button(self.content_frame, text="Flicker Start",
                                font=('Arial', 14, 'bold'), bg='#4d3319', fg='#FFA500')
        flicker_start.place(x=53, y=284)

        flicker_visible = tk.Button(self.content_frame, text="Flicker Visible",
                                  font=('Arial', 14, 'bold'), bg='#4d1f1f', fg='#ff4444')
        flicker_visible.place(x=50, y=340)

    def create_side_buttons(self):
        """Create side navigation buttons."""
        buttons = [
            ("Flicker Demo", 150, 'black'),
            ("CFF Fovea", 210, 'white'),
            ("BRK Fovea", 270, 'black'),
            ("CFF Para-Fovea", 330, 'black'),
            ("BRK Para-Fovea", 390, 'black'),
            ("Test Result", 450, 'black')
        ]

        for text, y, bg_color in buttons:
            btn = tk.Button(self.frame, text=text, font=Font,
                          width=20, bg=bg_color,
                          fg='white' if bg_color == 'black' else 'black',
                          relief='solid', bd=2)
            btn.place(x=10, y=y)

    def handleuserButton(self, switch=switch):
        """Handle user button press events."""
        globaladc.get_print('handle to be implemented')
        jmp = False
        self.patient_switch_desable()
        time.sleep(0.15)        
        
        if self.skip_event:
            self.handle_skip_event()
        else:
            self.handle_response_event()
            jmp = self.process_response()
        
        if not jmp:
            if self.skip_event:
                time.sleep(0.2) 
                globaladc.buzzer_3()            
            self.patient_switch_enable()

    def handle_skip_event(self):
        """Handle skip event logic."""
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

    def handle_response_event(self):
        """Handle response event logic."""
        self.skip_event = True
        time.sleep(0.5)

    def process_response(self):
        """Process user response and update display."""
        if not self.threadCreated:
            return False

        self.response_array[self.response_count] = self.freq_val
        self.trialList.insert(self.response_count, self.response_array[self.response_count])                
        self.min_apr = globaladc.get_cff_f_min_cal(self.response_count, self.freq_val)  
        self.response_count += 1
        self.cffValue_min.config(text=self.min_apr)

        if self.response_count == 5:
            return self.complete_test()
            
        self.cffValue_frq.config(text=self.freq_val)
        return False

    def complete_test(self):
        """Complete the test and process final results."""
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
        return True

    def patient_switch_enable(self):
        """Enable patient switch."""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(switch, GPIO.RISING, callback=self.handleuserButton)
    
    def patient_switch_desable(self):
        """Disable patient switch."""
        GPIO.remove_event_detect(switch)
    
    def show(self):
        """Show the frame and initialize values."""
        self.frame.place(width=1024, height=600)
        self.reset_values()
        globaladc.cff_Fovea_Prepair()
        self.run_therad()
        globaladc.blue_led_off()
    
    def hide(self):
        """Hide the frame and stop the thread."""
        self.stop_therad()
        self.frame.place_forget()
    
    def reset_values(self):
        """Reset all values to initial state."""
        self.cffValue_min.config(text='     ')
        self.cffValue_max.config(text='     ')
        self.cffValue_frq.config(text='     ')
        self.trialList.delete(0, tk.END)
        self.freq_val_start = contt_fva
        self.freq_val = self.freq_val_start
        self.response_array = [0, 0, 0, 0, 0]
        self.response_count = 0
        self.min_apr = 0
        self.max_apr = 0
        self.skip_event = True
        self.threadCreated = False

    def run_therad(self):
        """Start the periodic thread."""
        self.worker_cff = PerodicThread.PeriodicThread(intervel, self)
        if not self.worker_cff.isStarted:
            self.worker_cff.start()
            self.patient_switch_enable()
    
    def stop_therad(self):
        """Stop the periodic thread."""
        if hasattr(self, 'worker_cff') and self.worker_cff.isStarted:
            self.worker_cff.stop()
            self.worker_cff.kill()
            self.patient_switch_desable()
            self.skip_event = True
            self.threadCreated = False
    
    def periodic_event(self):
        """Handle periodic events."""
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

    def on_home(self):
        """Handle home button click."""
        pageDisctonary['CffFovea'].hide()
        pageDisctonary['MainScreen'].show()

    def on_next(self):
        """Handle next button click."""
        pageDisctonary['CffFovea'].hide()
        pageDisctonary['BrkFovea_1'].show()

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1024x612')
    app = CffFovea(root)
    app.Load()
    app.show()
    root.mainloop()