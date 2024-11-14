from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QPushButton, QSpinBox, 
                              QDoubleSpinBox, QGroupBox, QStatusBar, QFrame,
                              QStackedWidget, QLineEdit, QFormLayout, QTableWidget,
                              QTableWidgetItem, QDateEdit, QTextEdit, QMessageBox,
                              QComboBox)
from PySide6.QtCore import Qt, Slot, QDate
from PySide6.QtGui import QPainter, QColor, QPen
import sys
import numpy as np
from datetime import datetime
import hashlib
import sqlite3

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create form
        form = QFormLayout()
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Doctor", "Technician", "Admin"])
        
        form.addRow("Username:", self.username_edit)
        form.addRow("Password:", self.password_edit)
        form.addRow("Role:", self.role_combo)
        
        # Add login button
        self.login_button = QPushButton("Login")
        
        # Layout arrangement
        layout.addStretch()
        layout.addLayout(form)
        layout.addWidget(self.login_button)
        layout.addStretch()

class PatientRegistrationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create form
        form = QFormLayout()
        
        self.first_name_edit = QLineEdit()
        self.last_name_edit = QLineEdit()
        self.dob_edit = QDateEdit()
        self.dob_edit.setCalendarPopup(True)
        self.id_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.medical_history = QTextEdit()
        
        form.addRow("First Name:", self.first_name_edit)
        form.addRow("Last Name:", self.last_name_edit)
        form.addRow("Date of Birth:", self.dob_edit)
        form.addRow("Patient ID:", self.id_edit)
        form.addRow("Phone:", self.phone_edit)
        form.addRow("Email:", self.email_edit)
        form.addRow("Medical History:", self.medical_history)
        
        # Add registration button
        self.register_button = QPushButton("Register Patient")
        
        layout.addLayout(form)
        layout.addWidget(self.register_button)

class DoctorDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Patient list
        self.patient_table = QTableWidget()
        self.patient_table.setColumnCount(4)
        self.patient_table.setHorizontalHeaderLabels(["ID", "Name", "DOB", "Last Visit"])
        
        # Controls
        controls_layout = QHBoxLayout()
        self.view_patient_button = QPushButton("View Patient")
        self.new_measurement_button = QPushButton("New Measurement")
        self.view_history_button = QPushButton("View History")
        
        controls_layout.addWidget(self.view_patient_button)
        controls_layout.addWidget(self.new_measurement_button)
        controls_layout.addWidget(self.view_history_button)
        
        layout.addWidget(self.patient_table)
        layout.addLayout(controls_layout)

class DensitometerDisplay(QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.measurement = 0.0
        self.fixation_point = (200, 200)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw measurement area
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(175, 175, 50, 50)
        
        # Draw fixation point
        painter.setPen(QPen(Qt.red, 3))
        painter.drawPoint(*self.fixation_point)
        
        # Draw measurement value
        painter.drawText(10, 20, f"Density: {self.measurement:.3f}")

class MeasurementPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        # Left side - Display and controls
        left_layout = QVBoxLayout()
        self.display = DensitometerDisplay()
        
        # Measurement controls
        controls_group = QGroupBox("Measurement Controls")
        controls_layout = QVBoxLayout()
        
        wavelength_layout = QHBoxLayout()
        wavelength_label = QLabel("Wavelength (nm):")
        self.wavelength_spinbox = QSpinBox()
        self.wavelength_spinbox.setRange(400, 700)
        self.wavelength_spinbox.setValue(460)
        wavelength_layout.addWidget(wavelength_label)
        wavelength_layout.addWidget(self.wavelength_spinbox)
        
        intensity_layout = QHBoxLayout()
        intensity_label = QLabel("Intensity (cd/m²):")
        self.intensity_spinbox = QDoubleSpinBox()
        self.intensity_spinbox.setRange(0, 1000)
        self.intensity_spinbox.setValue(100)
        intensity_layout.addWidget(intensity_label)
        intensity_layout.addWidget(self.intensity_spinbox)
        
        controls_layout.addLayout(wavelength_layout)
        controls_layout.addLayout(intensity_layout)
        controls_group.setLayout(controls_layout)
        
        # Operation buttons
        self.measure_button = QPushButton("Start Measurement")
        self.save_button = QPushButton("Save Results")
        
        left_layout.addWidget(self.display)
        left_layout.addWidget(controls_group)
        left_layout.addWidget(self.measure_button)
        left_layout.addWidget(self.save_button)
        
        # Right side - Patient info and notes
        right_layout = QVBoxLayout()
        
        patient_info_group = QGroupBox("Patient Information")
        patient_info_layout = QFormLayout()
        self.patient_name_label = QLabel()
        self.patient_id_label = QLabel()
        self.patient_dob_label = QLabel()
        
        patient_info_layout.addRow("Name:", self.patient_name_label)
        patient_info_layout.addRow("ID:", self.patient_id_label)
        patient_info_layout.addRow("DOB:", self.patient_dob_label)
        patient_info_group.setLayout(patient_info_layout)
        
        # Notes section
        notes_group = QGroupBox("Measurement Notes")
        notes_layout = QVBoxLayout()
        self.notes_edit = QTextEdit()
        notes_layout.addWidget(self.notes_edit)
        notes_group.setLayout(notes_layout)
        
        right_layout.addWidget(patient_info_group)
        right_layout.addWidget(notes_group)
        
        # Add both sides to main layout
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Densitometer System")
        self.setup_ui()
        self.setup_database()
        self.create_default_users()
        
    def setup_database(self):
        # Initialize SQLite database
        self.conn = sqlite3.connect('densitometer.db')
        self.create_tables()
        
    def create_default_users(self):
            cursor = self.conn.cursor()
            
            # Default users with hashed passwords
            default_users = [
                {
                    'username': 'doctor1',
                    'password': hashlib.sha256('doctor123'.encode()).hexdigest(),
                    'role': 'Doctor'
                },
                {
                    'username': 'tech1',
                    'password': hashlib.sha256('tech123'.encode()).hexdigest(),
                    'role': 'Technician'
                },
                {
                    'username': 'admin1',
                    'password': hashlib.sha256('admin123'.encode()).hexdigest(),
                    'role': 'Admin'
                }
            ]
            
            # Add default users if they don't exist
            for user in default_users:
                try:
                    cursor.execute('''
                    INSERT INTO users (username, password, role)
                    VALUES (?, ?, ?)
                    ''', (user['username'], user['password'], user['role']))
                    self.conn.commit()
                except sqlite3.IntegrityError:
                    # User already exists, skip
                    pass

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )''')
        
        # Patients table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            dob DATE,
            patient_id TEXT UNIQUE,
            phone TEXT,
            email TEXT,
            medical_history TEXT
        )''')
        
        # Measurements table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY,
            patient_id INTEGER,
            date DATETIME,
            wavelength INTEGER,
            intensity REAL,
            density REAL,
            notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )''')
        
        self.conn.commit()
        
    def setup_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create pages
        self.login_page = LoginPage()
        self.patient_registration = PatientRegistrationPage()
        self.doctor_dashboard = DoctorDashboard()
        self.measurement_page = MeasurementPage()
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.patient_registration)
        self.stacked_widget.addWidget(self.doctor_dashboard)
        self.stacked_widget.addWidget(self.measurement_page)
        
        # Connect signals
        self.login_page.login_button.clicked.connect(self.handle_login)
        self.patient_registration.register_button.clicked.connect(self.register_patient)
        self.doctor_dashboard.new_measurement_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.measurement_page))
        self.measurement_page.measure_button.clicked.connect(self.take_measurement)
        self.measurement_page.save_button.clicked.connect(self.save_measurement)
        
        # Set initial page
        self.stacked_widget.setCurrentWidget(self.login_page)
        
        # Create status bar
        self.statusBar().showMessage("Please log in")
        
    @Slot()
    def handle_login(self):
        username = self.login_page.username_edit.text()
        password = self.login_page.password_edit.text()
        role = self.login_page.role_combo.currentText()
        
        # In a real application, verify credentials against database
        # For demo, just check if fields are filled
        if username and password:
            if role == "Doctor":
                self.stacked_widget.setCurrentWidget(self.doctor_dashboard)
                self.statusBar().showMessage(f"Welcome, Dr. {username}")
            else:
                QMessageBox.warning(self, "Access Denied", 
                                  "Only doctors can access this system")
        else:
            QMessageBox.warning(self, "Login Error", 
                              "Please enter both username and password")
    
    @Slot()
    def register_patient(self):
        # Get form data
        patient_data = {
            'first_name': self.patient_registration.first_name_edit.text(),
            'last_name': self.patient_registration.last_name_edit.text(),
            'dob': self.patient_registration.dob_edit.date().toPython(),
            'patient_id': self.patient_registration.id_edit.text(),
            'phone': self.patient_registration.phone_edit.text(),
            'email': self.patient_registration.email_edit.text(),
            'medical_history': self.patient_registration.medical_history.toPlainText()
        }
        
        # Validate data
        if not all([patient_data['first_name'], patient_data['last_name'], 
                   patient_data['patient_id']]):
            QMessageBox.warning(self, "Registration Error", 
                              "Please fill all required fields")
            return
            
        # Save to database
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO patients (first_name, last_name, dob, patient_id, 
                                phone, email, medical_history)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (patient_data['first_name'], patient_data['last_name'],
                 patient_data['dob'], patient_data['patient_id'],
                 patient_data['phone'], patient_data['email'],
                 patient_data['medical_history']))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Patient registered successfully")
            self.stacked_widget.setCurrentWidget(self.doctor_dashboard)
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Registration Error", 
                              "Patient ID already exists")
    
    @Slot()
    def take_measurement(self):
        wavelength = self.measurement_page.wavelength_spinbox.value()
        intensity = self.measurement_page.intensity_spinbox.value()
        
        # Simulate measurement
        self.measurement_page.display.measurement = np.random.normal(0.5, 0.1)
        self.measurement_page.display.update()
        self.statusBar().showMessage(
            f"Measurement taken at {wavelength}nm, {intensity}cd/m²")
    
    @Slot()
    def save_measurement(self):
        # Get current measurement data
        measurement_data = {
            'wavelength': self.measurement_page.wavelength_spinbox.value(),
            'intensity': self.measurement_page.intensity_spinbox.value(),
            'density': self.measurement_page.display.measurement,
            'notes': self.measurement_page.notes_edit.toPlainText(),
            'date': datetime.now()
        }
        
        # Save to database (in real application, associate with current patient)
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO measurements (wavelength, intensity, density, notes, date)
        VALUES (?, ?, ?, ?, ?)
        ''', (measurement_data['wavelength'], measurement_data['intensity'],
              measurement_data['density'], measurement_data['notes'],
              measurement_data['date']))
        self.conn.commit()
        
        QMessageBox.information(self, "Success", "Measurement saved successfully")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()