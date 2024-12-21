import tkinter as tk
from tkinter import  ttk       
import PerodicThread 
import time
from  BRK_FOVEA_1 import BrkFovea_1 
import PatientInfo
from globalvar import pageDisctonary
from globalvar import globaladc
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
from globalvar import currentPatientInfo
from tkinter import font
from header import HeaderComponent

switch = 20
contt_fva = 34.5
Font = ("Arial",15)
Font1 = ("Arial",15)
Font2 = ("Arial",20)
intervel = globaladc.get_cff_delay()
select = 1
cffValue_frq_x =820
cffValue_frq_y = 40





class CustomLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        # Create custom font matching Helvetica 26
        custom_font = font.Font(
            family="Helvetica",
            size=26
        )
        
        # Default styling matching the PyQt label
        default_style = {
            'font': custom_font,
            'bg': 'black',
            'fg': 'white',
            'width': 5,  # Approximate width to match 111 pixels
            'height': 1,  # Approximate height to match 51 pixels
            'borderwidth': 2,
            'relief': 'solid',
            'justify': 'center'
        }
        
        # Update default styling with any provided kwargs
        default_style.update(kwargs)
        
        # Initialize the label with our styling
        super().__init__(parent, **default_style)
        
        # Place the label (matching QRect(580, 30, 111, 51))
        self.place(x=700, y=30)



class CustomListbox(tk.Listbox):
    def __init__(self, parent, font_family="Helvetica", font_size=20, **kwargs):
        # Create custom font
        custom_font = font.Font(
            family=font_family,
            size=font_size
        )
        
        # Default styling
        default_style = {
            'font': custom_font,
            'width': 6,
            'bg': 'black',
            'fg': 'red',
            'selectmode': 'single',
            'selectbackground': '#3d3d3d',  # Darker grey for selection
            'selectforeground': 'red',      # Keep text red when selected
            'relief': 'solid',
            'highlightthickness': 0,        # Remove focus highlight
            'activestyle': 'none',  
            'justify': 'center',   
            "borderwidth":2                # Remove active item underline
        }
        
        # Update default styling with any provided kwargs
        default_style.update(kwargs)
        
        # Initialize the listbox with our styling
        super().__init__(parent, **default_style)
        
        # Bind events for hover effects (optional)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, event):
        """Optional hover effect"""
        self.configure(borderwidth=0)
    
    def on_leave(self, event):
        """Reset border on mouse leave"""
        self.configure(borderwidth=0)


def hardware():
        CffFovea.handleuserButton()
        
class CffFovea :
    def __init__(self, frame):
        self.frame = frame
        self.frame.config(bg='black')
        self.response_count = 0  
        self.skip_event =True
        self.threadCreated =False
        self.worker_cff = PerodicThread.PeriodicThread(intervel,self)
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0 
        self.response_array = [0,0,0,0,0]
        self.content_frame = tk.Frame(self.frame, bg='#1f2836')
        self.freques_frame = tk.Frame(self.content_frame,bg="black")
        self.trialList = CustomListbox(self.content_frame)
        self.patentActionflabel = tk.Label (self.content_frame, text='Patient\'s side Button \n Begins Traial',font=Font1,bg='white')
        self.cff_label =tk.Label(self.freques_frame, text="CFF Fovea",
                                font=('Helvetica Neue', 22),
                                bg='black', fg='white')
        self.cffValue_min =tk.Label(self.freques_frame, text="23.5",
                                 font=('Helvetica Neue', 28),
                                 bg='black', fg='white')
        self.cffValue_max = tk.Label(self.freques_frame, text="23.5",
                                 font=('Helvetica Neue', 28),
                                 bg='black', fg='white')
        self.cffValue_frq = CustomLabel(self.content_frame, text='    ')  


        self.status_frame = tk.Frame(self.content_frame, bg='#1f2836')
        self.status_frame.place(relx=0.1, rely=0.5)
        
        self.status_label = tk.Label(self.status_frame, text="Test Status",
                                   font=('Helvetica Neue', 18),
                                   bg='#1f2836', fg='white')
        self.status_label.pack(pady=10)


        
        
        self.btn_ready = tk.Button(self.status_frame, text="Machine Ready",
                          font=('Arial', 14, 'bold'),
                          bg="#1a472a", fg='#4CAF50',
                          width=15, height=1,
                          relief='raised')
        
        self.btn_flicker_start = tk.Button(self.status_frame, text="Flicker Start",
                          font=('Arial', 14, 'bold'),
                          bg="#4d3319", fg='#FFA500',
                          width=15, height=1,
                          relief='raised')
        
        self.btn_flicker_visible = tk.Button(self.status_frame, text="Flicker Visible",
                          font=('Arial', 14, 'bold'),
                          bg="#4d1f1f", fg='#ff4444',
                          width=15, height=1,
                          relief='raised')

        self.blinking_buttons = {}
        self.is_blinking = False



    def blink_button(self, button, interval=500):
        """
        Fixed button blinking implementation
        """
        button_id = str(id(button))
        
        # If button is already blinking, don't start a new blink
        if button_id in self.blinking_buttons:
            return
            
        # Store initial colors immediately
        initial_bg = button.cget('bg')
        initial_fg = button.cget('fg')
        
        # Initialize blinking state for this button with original colors
        self.blinking_buttons[button_id] = {
            'button': button,
            'after_id': None,
            'original_colors': (initial_bg, initial_fg),
            'is_original': True  # Track whether showing original colors
        }
        
        def toggle_colors():
            if button_id not in self.blinking_buttons:
                return
                
            if self.blinking_buttons[button_id]['is_original']:
                # Switch to alternate colors
                button.configure(
                    bg=self.blinking_buttons[button_id]['original_colors'][1],
                    fg=self.blinking_buttons[button_id]['original_colors'][0]
                )
            else:
                # Switch back to original colors
                button.configure(
                    bg=self.blinking_buttons[button_id]['original_colors'][0],
                    fg=self.blinking_buttons[button_id]['original_colors'][1]
                )
            
            # Toggle the state
            self.blinking_buttons[button_id]['is_original'] = not self.blinking_buttons[button_id]['is_original']
            
            # Schedule next blink
            self.blinking_buttons[button_id]['after_id'] = self.frame.after(interval, toggle_colors)
        
        # Start the blinking
        toggle_colors()


    def stop_specific_blink(self, button):
        """
        Improved method to stop specific button blinking
        """
        button_id = str(id(button))
        
        if button_id in self.blinking_buttons:
            # Cancel the scheduled after event
            if self.blinking_buttons[button_id]['after_id']:
                self.frame.after_cancel(self.blinking_buttons[button_id]['after_id'])
            
            # Restore original colors
            if self.blinking_buttons[button_id]['original_colors']:
                orig_bg, orig_fg = self.blinking_buttons[button_id]['original_colors']
                button.configure(bg=orig_bg, fg=orig_fg)
            
            # Remove button from blinking dictionary
            del self.blinking_buttons[button_id]

    def stop_all_blinking(self):
        """
        Stop all buttons from blinking
        """
        button_ids = list(self.blinking_buttons.keys())
        for button_id in button_ids:
            button = self.blinking_buttons[button_id]['button']
            self.stop_specific_blink(button)



    def handleuserButton(self,switch):
        globaladc.get_print('handle to be implemented')
        jmp = False
        self.patient_switch_desable()
        time.sleep(0.15)        
        if self.skip_event:
            # self.stop_all_blinking()  # Clear any existing blinks
            # self.blink_button(self.btn_flicker_start)  # Start blinking flicker start button
            self.threadCreated=True
            if self.response_count == 0:
                self.freq_val_start = self.freq_val_start
            elif self.response_count == 1:
                self.freq_val_start = self.min_apr + 6.5
            elif self.response_count == 2:
                self.freq_val_start = self.min_apr + 6.5
            elif self.response_count == 3:
                self.freq_val_start = self.min_apr + 6.5
            elif self.response_count == 4:
                self.freq_val_start = self.min_apr + 6.5
            elif self.response_count == 5:
                self.freq_val_start = self.min_apr + 6.5
            else :
                self.freq_val_start = self.min_apr + 6.5
            self.freq_val=self.freq_val_start   
            #globaladc.buzzer_1() 
            globaladc.fliker_start_g()
            time.sleep(0.2)             
            self.skip_event = False            
        else :
            self.skip_event = True
            time.sleep(0.5) 
            #globaladc.buzzer_1()  
            #globaladc.green_led_on()      
           
            if  self.threadCreated :
                #self.stop_therad()                                              
                self.stop_all_blinking()
                self.response_array[self.response_count] = self.freq_val
                self.trialList.insert(self.response_count,self.response_array[self.response_count])                
                self.min_apr = globaladc.get_cff_f_min_cal(self.response_count, self.freq_val)  
                self.response_count = self.response_count + 1
                #self.min_apr = globaladc.cff_min(self.min_apr,self.freq_val)                    
                self.cffValue_min.config(text = self.min_apr)  

                # Blink flicker visible button
                # self.blink_button(self.btn_flicker_visible)
                time.sleep(1)  # Show flicker visible for a moment           
                if self.response_count == 5 :
                    self.max_apr =  globaladc.get_cff_f_max_cal()                        
                    self.cffValue_max.config(text = self.max_apr)                    
                    str_data = 'self.max_apr=' + str(self.max_apr)
                    globaladc.get_print(str_data)            
                    self.stop_therad()                                               
                    #average the min max values and store in Guli
                    avgval = globaladc.get_cff_f_avg_cal()
                    # globaladc.put_cff_fovea_frq(avgval)
                    log_data = "CFF_F-"+str(avgval)
                    currentPatientInfo.log_update(log_data)                    
                    time.sleep(1)
                    globaladc.buzzer_3()
                    globaladc.get_print('done')
                    pageDisctonary['CffFovea'].hide()
                    pageDisctonary['BrkFovea_1'].show()
                    self.patient_switch_desable()
                    jmp = True          
                # else:
                #     # Prepare for next trial
                #     time.sleep(0.5)
                #     self.stop_all_blinking()
                #     self.blink_button(self.btn_ready)  # Show machine ready for next trial   
                self.cffValue_frq.config(text = self.freq_val)  
        if not jmp:
            if self.skip_event:
                time.sleep(0.2) 
                globaladc.buzzer_3()  
                self.stop_specific_blink(self.btn_flicker_start) 
            self.patient_switch_enable() 



    def patient_switch_enable(self) :
        globaladc.get_print('patient_switch_enable')
        GPIO.setwarnings(True) # Ignore warning for now
        GPIO.setmode(GPIO.BCM) # Use physical pin numbering
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        try:
            GPIO.add_event_detect(switch, GPIO.RISING, callback=self.handleuserButton)
        except RuntimeError:
            # Event detection is already set up, so you can either ignore or log this
            print("GPIO event detection already set up")


        # GPIO.add_event_detect(switch,GPIO.RISING,callback=self.handleuserButton) #CffFovea


    def patient_switch_desable(self) :
            globaladc.get_print('patient_switch_desable')
            GPIO.remove_event_detect(switch)

   



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


    def Load(self):
        self.response_count = 0  
        self.skip_event =True
        self.threadCreated =False
        self.worker_cff = PerodicThread.PeriodicThread(intervel,self)
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0 
        self.response_array = [0,0,0,0,0]
        # cfflabel = tk.Label (self.frame, text='CFF FOVEA :',font=Font)
        # cfflabel.place (x=420, y=50)

        self.cffValue_frq.place (x=600, y=35)        
        # self.patentActionflabel.place (x=200, y=180)
        self.trialList.place (x=604, y=100)
        
        self.header = HeaderComponent(
            self.frame,
            "Macular Densitometer                                                          CFF Fovea Test"
        )
        
        self.header.set_wifi_callback(lambda _ : globaladc.buzzer_3())

        self.create_side_buttons()
        self.content_frame.place(x=280, y=110, width=711, height=441)
        self.freques_frame.place(relx=0.3, rely=0.1, width=291, height=126)
        self.cff_label.pack(pady=10)
        self.cffValue_min.pack(side='left',pady=10 ,padx=10)
        self.cffValue_max.pack(side='right',pady=10 ,padx=10)
        # self.cff_value1.pack(side='left', padx=10)
        # self.wifi_label.place(x=868, y=5)
        self.btn_ready.pack(pady=5)
        self.btn_flicker_start.pack(pady=5)
        self.btn_flicker_visible.pack(pady=5)
        self.blink_button(self.btn_ready)



        def onfw():
            pageDisctonary['CffFovea'].hide()
            pageDisctonary['MainScreen'].show()

        def onbw():
            pageDisctonary['CffFovea'].hide()
            pageDisctonary['BrkparaFovea'].show()
        #pageDisctonary['MainScreen'].show()

        fwButton = tk.Button (self.frame,
                                    text=">>", font=Font2,
                                    command=onfw, bg='Green',
                                    width=10)
        
        bwButton = tk.Button (self.frame,
                                    text="<<", font=Font2,
                                    command=onbw, bg='Green',
                                    width=10)

        # fwButton.place(x=620,y=500)
        # bwButton.place(x=420, y=500)    

    def show(self):
        self.cffValue_min.config(text = '     ')
        self.cffValue_max.config(text = '     ')
        self.cffValue_frq.config(text = '     ')
        self.trialList.delete(0,tk.END)
        self.frame.place(width=1024,height=600)
        # self.patentActionflabel.place(x=200, y=180)
        globaladc.cff_Fovea_Prepair() # run this while loding cff Fovea screen        
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.response_array = [0,0,0,0,0]
        self.response_count = 0 
        self.min_apr = 0
        self.max_apr = 0 
        self.skip_event = True
        self.threadCreated=False
        self.run_therad() 
        globaladc.blue_led_off()   
    
    def hide(self): 
        self.stop_therad()
        self.frame.place_forget()
        
    def run_therad(self):
        globaladc.get_print("worker_cff thread started")        
        self.worker_cff = PerodicThread.PeriodicThread(intervel,self)
        if not self.worker_cff.isStarted :
            self.worker_cff.start()
            self.patient_switch_enable()
        
    def stop_therad(self):
        globaladc.get_print("worker_cff thread stopped")
        if self.worker_cff.isStarted :
            self.worker_cff.stop()  
            self.worker_cff.kill()
            self.patient_switch_desable()
            self.skip_event = True
            self.threadCreated=False

    def print_min(self):
        globaladc.get_print('from dac CffFovea.min_apr = ',self.min_apr)

    def periodic_event(self):
        if not self.skip_event :
            self.freq_val = round((self.freq_val - 0.5),1)
            self.cffValue_frq.config(text = self.freq_val)
            if self.freq_val <  5 :
                self.skip_event = True
                self.threadCreated=False
                self.freq_val = self.freq_val_start
                self.cffValue_frq.config(text = self.freq_val)
                globaladc.buzzer_3()
            globaladc.put_cff_fovea_frq(self.freq_val)
        else :
            globaladc.put_cff_fovea_frq(35)
            globaladc.get_print('CF')   
            

    def getName():
        return "CffFovea"


#test Run class
if __name__ == '__main__':
    window = tk.Tk()  
    CffFovea.Load(window)
    CffFovea.show()