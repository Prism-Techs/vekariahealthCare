# patient_registration.py
import tkinter as tk
from header import HeaderComponent
from custom_widgets import CustomEntry, RadioButtonGroup
import json
from datetime import datetime
import os

class PatientRegistrationForm:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1024x600")
        self.window.configure(bg='black')
        self.window.title("Patient Registration")

        # Initialize header
        self.header = HeaderComponent(
            self.window,
            "Macular Densitometer                                                  Patient-Registration"
        )

        # Main content frame
        self.content_frame = tk.Frame(self.window, bg='black')
        self.content_frame.place(x=20, y=120, width=981, height=460)

        # Create form fields
        self.create_form_fields()
        
        # Create submit button
        self.create_submit_button()

    def create_form_fields(self):
        # Basic Information
        self.create_label_entry("1st Name", 0, 20)
        self.create_label_entry("Mid. Name", 344, 20)
        self.create_label_entry("Surname", 670, 20)
        self.create_label_entry("DOB", 0, 80)
        self.create_label_entry("Aadhaar", 346, 80)
        self.create_label_entry("Mobile", 676, 80)

        # Radio Button Groups
        self.gender_group = RadioButtonGroup(
            self.content_frame,
            [("Male", "male"), ("Female", "female")],
            157, 140
        )

        self.alcohol_group = RadioButtonGroup(
            self.content_frame,
            [("Yes", "yes"), ("No", "no")],
            157, 200
        )

        # Add other radio groups similarly...

        # Create labels for radio groups
        labels = [
            ("Gender", 0, 140),
            ("Alcohol", 0, 200),
            ("Smoking", 0, 260),
            ("Food Habit", 0, 320),
            ("Eye Side", 450, 140),
            ("Blood Pressure", 450, 200),
            ("Diabetes", 450, 260)
        ]

        for text, x, y in labels:
            tk.Label(
                self.content_frame,
                text=text,
                font=('Helvetica Neue', 16),
                bg='black',
                fg='white'
            ).place(x=x, y=y)

    def create_label_entry(self, label_text, x, y):
        tk.Label(
            self.content_frame,
            text=label_text,
            font=('Helvetica Neue', 16),
            bg='black',
            fg='white'
        ).place(x=x, y=y)

        entry = CustomEntry(self.content_frame)
        entry.place(x=x + 141, y=y, width=190, height=31)
        return entry

    def create_submit_button(self):
        submit_btn = tk.Button(
            self.content_frame,
            text="SUBMIT",
            font=('Arial', 24, 'bold'),
            bg='black',
            fg='white',
            relief='solid',
            bd=1,
            command=self.save_patient_data
        )
        submit_btn.place(x=410, y=390, width=161, height=51)

    def save_patient_data(self):
        # Implement save functionality
        pass

if __name__ == "__main__":
    app = PatientRegistrationForm()
    app.window.mainloop()