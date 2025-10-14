import sys
import json
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout,QPushButton,QLineEdit,QHBoxLayout,QComboBox,
                             QMessageBox, QLabel,QStackedWidget,
                             QRadioButton,QFrame,QCheckBox)
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI for DinoRunner")
        self.setWindowIcon(QIcon("images/player/walk2.png"))
        self.setGeometry(700,300,1000,600)
        self.stacked_widget=QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.page1=QWidget()
        self.page_standard=QWidget()
        self.page_experimental=QWidget()
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page_standard)
        self.stacked_widget.addWidget(self.page_experimental)
        #first page
        #background
        self.background1 = QLabel(self.page1)
        self.background1.setPixmap(QPixmap("images/intro/sfondo_gui.png"))
        self.background1.setGeometry(0, 0, 1000, 600)
        self.background1.setScaledContents(True)
        self.background1.lower()
        self.overlay = QLabel(self.page1)
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        #widgets intro
        self.title=QLabel("DINO RUNNER 🦖")
        self.selectmode=QLabel("Available modes:",self.page1)
        self.experiment_image=QLabel(self.page1)
        pix_exp = QPixmap("images/intro/experiment.png").scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.experiment_image.setPixmap(pix_exp)
        self.standard_image=QLabel(self.page1)
        pix_std = QPixmap("images/player/jump.png").scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.standard_image.setPixmap(pix_std)
        self.radiostd=QRadioButton("Standard mode")
        self.radioexp=QRadioButton("Experimental mode")
        self.submitbotton=QPushButton("Submit", self.page1)
        self.values_dict={}
        self.optionals_dict={}
        self.values_dict.update({"Dino_mass":50,"Grass_frict":0.40,"Sand_frict":0.30,"Asphalt_frict":0.70,"Ice_frict":0.08,"Air_coeff":0.9,"Coll_coeff":1,"Gravity":9.81,"Wind_strenght":5})
        self.optionals_dict.update({"Wind":True,"Surfaces":True,"Air resistance":True,"Trampolines":True})
        self.initUI_1()
        #standard page
        #background
        self.background_std = QLabel(self.page_standard)
        self.background_std.setPixmap(QPixmap("images/standard/background.png"))
        self.background_std.setGeometry(0, 0, 1000, 600)
        self.background_std.setScaledContents(True)
        self.background_std.lower()
        self.overlay_std = QLabel(self.page_standard)
        self.overlay_std.setGeometry(0, 0, self.width(), self.height())
        self.overlay_std.lower()
        #widgets
        self.friction_std=QComboBox(self.page_standard)
        self.friction_std.addItems(["Coeff. of friction of grass","Coeff. of friction sand","Coeff. of friction asphalt","Coeff. of friction ice"])
        self.frictioninf_std=QLabel("")
        self.massinf_std=QLabel("Dino's mass=50kg",self.page_standard)
        self.aircoeff_std=QLabel("Air resistance coeff.=0.9",self.page_standard)
        self.springcoeff_std=QLabel("Collision coeff.=1",self.page_standard)
        self.gravity_std=QLabel("Gravity=9.81m/s^2",self.page_standard)
        self.wind_std=QLabel("Wind=5",self.page_standard)
        self.intro_std=QLabel("These values are fixed\n For different settings,\n select experimental mode 🧪",self.page_standard)
        self.playbbutton_std=QPushButton("PLAY!")
        self.goback_std=QPushButton("<-Previous")
        self.standard_dino=QLabel(self.page_standard)
        pix_std_dino = QPixmap("images/player/walk2.png").scaled(450, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.standard_dino.setPixmap(pix_std_dino)
        self.widget_frame = QFrame(self.page_standard)
        self.initUI_standard()
        #experimental page
        #background
        self.background_exp = QLabel(self.page_experimental)
        self.background_exp.setPixmap(QPixmap("images/experimental/background.png"))
        self.background_exp.setGeometry(0, 0, 1000, 600)
        self.background_exp.setScaledContents(True)
        self.background_exp.lower()
        self.overlay_exp = QLabel(self.page_experimental)
        self.overlay_exp.setGeometry(0, 0, self.width(), self.height())
        self.overlay_exp.lower()
        #widgets
        self.intro_exp=QLabel("You can create your game,\n you can change all the parameters⚙️",self.page_experimental)
        self.menu_exp=QComboBox(self.page_experimental)
        self.menu_exp.addItems(["Dino_mass","Grass_frict","Sand_frict","Asphalt_frict","Ice_frict", "Air_coeff", "Coll_coeff","Gravity","Wind_strenght"])
        self.showinf_exp=QLabel("",self.page_experimental)
        self.edit_exp=QLineEdit(self.page_experimental)
        self.modify_button_exp=QPushButton("Modify",self.page_experimental)
        self.goback_exp=QPushButton("<-Previous",self.page_experimental)
        self.playbbutton_exp=QPushButton("Play",self.page_experimental)
        self.widget_frame_exp=QFrame(self.page_experimental)
        self.experimental_dino=QLabel(self.page_experimental)
        pix_exp_dino = QPixmap("images/experimental/dinolab.png").scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.experimental_dino.setPixmap(pix_exp_dino)
        self.wind_exp=QCheckBox(text="Wind")
        self.air_frict=QCheckBox(text="Air Resistance")
        self.change_surfaces=QCheckBox(text="Different surfaces")
        self.trampolines_exp=QCheckBox(text="trampolines")
        self.checkboxes_list=[self.wind_exp,self.air_frict,self.change_surfaces,self.trampolines_exp]
        self.widget_check=QFrame(self.page_experimental)
        self.initUI_experimental()

    def initUI_1(self):
        self.submitbotton.setFixedSize(250,70)

        vbox_main=QVBoxLayout()
        vbox_label=QVBoxLayout()
        vbox_label.addWidget(self.title,alignment=Qt.AlignCenter)
        vbox_label.addWidget(self.selectmode,alignment=Qt.AlignCenter)
        hbox_modes=QHBoxLayout()
        hbox_imagestd=QHBoxLayout()
        hbox_imagestd.addSpacing(20)
        hbox_imagestd.addWidget(self.standard_image,alignment=Qt.AlignLeft)
        hbox_radiostd=QHBoxLayout()
        hbox_radiostd.addWidget(self.radiostd,alignment=Qt.AlignLeft)
        vbox_standard=QVBoxLayout()
        vbox_standard.addLayout(hbox_imagestd)
        vbox_standard.addLayout(hbox_radiostd)
        hbox_imageexp=QHBoxLayout()
        hbox_imageexp.addSpacing(250)
        hbox_imageexp.addWidget(self.experiment_image)
        hbox_radioexp=QHBoxLayout()
        hbox_radioexp.addWidget(self.radioexp,alignment=Qt.AlignRight)
        vbox_experiment=QVBoxLayout()
        vbox_experiment.addLayout(hbox_imageexp)
        vbox_experiment.addLayout(hbox_radioexp)
        hbox_modes.addLayout(vbox_standard)
        hbox_modes.addLayout(vbox_experiment)
        hbox_button=QHBoxLayout()
        hbox_button.addWidget(self.submitbotton,alignment=Qt.AlignCenter)
        vbox_main.addLayout(vbox_label,stretch=1)
        vbox_main.addLayout(hbox_modes,stretch=3)
        vbox_main.addLayout(hbox_button,stretch=1)
        self.page1.setLayout(vbox_main)

        self.page1.setStyleSheet(
        "font-size:30px;"
        "padding:10px;"
        "font-family: Comic Sans MS;"
        "color: white;"
        "background-color: rgba(0, 0, 0, 150);"
        "font-weight: bold;"
        "padding: 5px;"
        "border-radius: 5px;")
        self.title.setStyleSheet("""
        font-size:70px;
        font-family: Arial;
        color: white;
        background-color: rgba(0, 0, 0, 150);
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
        """)
        self.submitbotton.setStyleSheet("""
        QPushButton {
        background-color: #ffcc00;
        color: black;
        font-size: 30px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        }
        QPushButton:hover {
        background-color: #ffaa00;
        }
        """)
        self.overlay.setStyleSheet("""
        background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(0,0,0,180),
        stop:1 rgba(0,0,0,50)
        );
        """)
        self.experiment_image.setStyleSheet("background-color: None;")
        self.standard_image.setStyleSheet("background-color: None;")

        self.submitbotton.clicked.connect(self.change_page)

    def change_page(self):
        if not self.radiostd.isChecked() and not self.radioexp.isChecked():
            QMessageBox.warning(self, "Error", "Please select a mode")
            return
        elif self.radiostd.isChecked():
            self.stacked_widget.setCurrentWidget(self.page_standard)
        elif self.radioexp.isChecked():
            self.stacked_widget.setCurrentWidget(self.page_experimental)

    def initUI_standard(self):
        self.widget_frame.setFixedWidth(500)
        self.goback_std.setFixedSize(250,70)
        self.playbbutton_std.setFixedSize(300,70)

        vbox_full=QVBoxLayout()
        hbox_central_std=QHBoxLayout()
        vbox_widgets=QVBoxLayout()
        vbox_widgets.addWidget(self.massinf_std)
        vbox_widgets.addWidget(self.aircoeff_std)
        vbox_widgets.addWidget(self.springcoeff_std)
        vbox_widgets.addWidget(self.gravity_std)
        vbox_widgets.addWidget(self.wind_std)
        vbox_widgets.addWidget(self.friction_std)
        vbox_widgets.addWidget(self.frictioninf_std)
        self.widget_frame.setLayout(vbox_widgets)
        hbox_central_std.addWidget(self.widget_frame)
        hbox_central_std.addWidget(self.standard_dino,alignment=Qt.AlignRight)
        hbox_button_std=QHBoxLayout()
        hbox_button_std.addWidget(self.goback_std,alignment=Qt.AlignLeft)
        hbox_button_std.addWidget(self.playbbutton_std,alignment=Qt.AlignRight)
        vbox_full.addWidget(self.intro_std,alignment=Qt.AlignCenter,stretch=1)
        vbox_full.addLayout(hbox_central_std,stretch=3)
        vbox_full.addSpacing(30)
        vbox_full.addLayout(hbox_button_std,stretch=1)
        self.page_standard.setLayout(vbox_full)

        self.page_standard.setStyleSheet("""
        font-size:30px;
        font-family: Comic Sans MS;
        color: white;
        background-color: rgba(0, 0, 0, 150);
        font-weight: bold;
        border-radius: 5px;
        """)
        self.goback_std.setStyleSheet("""
        QPushButton {
        background-color: #6560E9;
        color: white;
        font-size: 30px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        }
        QPushButton:hover {
        background-color: #ffaa00;
        }
        """)
        self.playbbutton_std.setStyleSheet("""
        QPushButton {
        background-color: #F11012;
        color: white;
        font-size: 30px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        }
        QPushButton:hover {
        background-color: #ffaa00;
        }
        """)
        self.overlay_std.setStyleSheet("""
        background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(0,0,0,180),
        stop:1 rgba(0,0,0,50)
        );
        """)
        self.intro_std.setStyleSheet("""
        font-size:40px;
        font-family: Arial;
        color: white;
        background-color: rgba(0, 0, 0, 150);
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
        """)
        self.widget_frame.setStyleSheet("""
        background-color: rgba(0,0,0,150);
        border-radius: 10px;
        """)
        self.standard_dino.setStyleSheet("background-color: None;")

        self.goback_std.clicked.connect(self.previous)
        self.friction_std.currentIndexChanged.connect(self.update_frictioninf)
        self.playbbutton_std.clicked.connect(self.play_game)

    def previous(self):
        self.stacked_widget.setCurrentWidget(self.page1)

    def update_frictioninf(self,index):
        if index==0:
            self.frictioninf_std.setText("Grass: 0.40")
        if index==1:
            self.frictioninf_std.setText("Sand: 0.30")
        if index==2:
            self.frictioninf_std.setText("Asphalt: 0.70")
        if index==3:
            self.frictioninf_std.setText("Ice: 0.08")

    def play_game(self):
       config = {
        "values": self.values_dict,
        "optionals": self.optionals_dict,
        }
       with open("config.json", "w") as f:
         json.dump(config, f, indent=4)
    
       self.close()
       subprocess.Popen(["python", "dino_game.py"])
       
    
    def initUI_experimental(self):
        self.widget_frame_exp.setFixedWidth(480)
        self.widget_check.setFixedWidth(480)
        self.goback_exp.setFixedSize(250,70)
        self.modify_button_exp.setFixedSize(250,70)
        self.playbbutton_exp.setFixedSize(250,70)

        vbox_full_exp=QVBoxLayout()
        hbox_intro_exp=QHBoxLayout()
        hbox_central_exp=QHBoxLayout()
        vbox_widget_exp=QVBoxLayout()
        vbox_check_exp=QVBoxLayout()
        hbox_intro_exp.addWidget(self.intro_exp)
        hbox_intro_exp.addWidget(self.experimental_dino)
        vbox_widget_exp.addWidget(self.menu_exp)
        vbox_widget_exp.addWidget(self.showinf_exp)
        vbox_widget_exp.addWidget(self.edit_exp)
        self.widget_frame_exp.setLayout(vbox_widget_exp)
        vbox_check_exp.addWidget(self.wind_exp)
        vbox_check_exp.addWidget(self.air_frict)
        vbox_check_exp.addWidget(self.change_surfaces)
        vbox_check_exp.addWidget(self.trampolines_exp)
        self.widget_check.setLayout(vbox_check_exp)
        hbox_central_exp.addWidget(self.widget_frame_exp)
        hbox_central_exp.addWidget(self.widget_check)
        hbox_button_exp=QHBoxLayout()
        hbox_button_exp.addWidget(self.goback_exp,alignment=Qt.AlignLeft)
        hbox_button_exp.addWidget(self.modify_button_exp,alignment=Qt.AlignCenter)
        hbox_button_exp.addWidget(self.playbbutton_exp,alignment=Qt.AlignRight)
        vbox_full_exp.addLayout(hbox_intro_exp)
        vbox_full_exp.addLayout(hbox_central_exp)
        vbox_full_exp.addLayout(hbox_button_exp)
        self.page_experimental.setLayout(vbox_full_exp)

        self.page_experimental.setStyleSheet("""
        font-size:30px;
        font-family: Comic Sans MS;
        color: white;
        background-color: rgba(0, 0, 0, 150);
        font-weight: bold;
        border-radius: 5px;
        """)
        self.goback_exp.setStyleSheet("""
        QPushButton {
        background-color: #6560E9;
        color: white;
        font-size: 30px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        }
        QPushButton:hover {
        background-color: #ffaa00;
        }
        """)
        self.playbbutton_exp.setStyleSheet("""
        QPushButton {
        background-color: #F11012;
        color: white;
        font-size: 30px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        }
        QPushButton:hover {
        background-color: #ffaa00;
        }
        """)
        self.modify_button_exp.setStyleSheet("""
        QPushButton {
        background-color: #60C638;
        color: white;
        font-size: 30px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        }
        QPushButton:hover {
        background-color: #ffaa00;
        }
        """)
        self.overlay_exp.setStyleSheet("""
        background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(0,0,0,180),
        stop:1 rgba(0,0,0,50)
        );
        """)
        self.intro_exp.setStyleSheet("""
        font-size:30px;
        font-family: Arial;
        color: white;
        background-color: rgba(0, 0, 0, 150);
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
        """)
        self.widget_frame_exp.setStyleSheet("""
        background-color: rgba(0,0,0,150);
        border-radius: 10px;
        """)
        self.experimental_dino.setStyleSheet("background-color: None;")

        self.goback_exp.clicked.connect(self.previous)
        self.menu_exp.currentIndexChanged.connect(self.update_showinf)
        self.modify_button_exp.clicked.connect(self.modify_value)
        self.playbbutton_exp.clicked.connect(self.play_game)
        for checkboxes in self.checkboxes_list:
           checkboxes.stateChanged.connect(self.checkboxes_input)

    def update_showinf(self, index=None):
        if index is None:
         index = self.menu_exp.currentIndex()
        match index:
            case 0:
             self.showinf_exp.setText(f"Current value:{self.values_dict["Dino_mass"]}kg")
             self.edit_exp.setPlaceholderText("Standard value: 50kg")
            case 1:
             self.showinf_exp.setText(f"Current value:{self.values_dict["Grass_frict"]}")
             self.edit_exp.setPlaceholderText("Standard value: 0.40")
            case 2:
             self.showinf_exp.setText(f"Current value:{self.values_dict["Sand_frict"]}")
             self.edit_exp.setPlaceholderText("Standard value: 0.30")
            case 3:
             self.showinf_exp.setText(f"Current value:{self.values_dict["Asphalt_frict"]}")
             self.edit_exp.setPlaceholderText("Standard value: 0.70")
            case 4:
             self.showinf_exp.setText(f"Current value:{self.values_dict["Ice_frict"]}")
             self.edit_exp.setPlaceholderText("Standard value: 0.08")
            case 5:
             self.showinf_exp.setText(f"Current value:{self.values_dict["Air_coeff"]}")
             self.edit_exp.setPlaceholderText("Standard value: 0.9")
            case 6:
             self.showinf_exp.setText(f"Current value:{self.values_dict["Coll_coeff"]}")
             self.edit_exp.setPlaceholderText("Standard value: 1")
            case 7:
             self.showinf_exp.setText(f"Current value:{self.values_dict["Gravity"]}")
             self.edit_exp.setPlaceholderText("Standard value: 9.81m/s^2")
            case 8:
             self.showinf_exp.setText(f"Current value:{self.values_dict["Wind_strenght"]}")
             self.edit_exp.setPlaceholderText("Default value: 5")
              
    def modify_value(self):
     key = self.menu_exp.currentText()
     text=self.edit_exp.text().strip().replace(",",".")
     try:
        value = float(text)
     except (ValueError, TypeError):
        QMessageBox.warning(self, "Error", "Please insert a number")
        return
     self.values_dict[key] = value
     self.edit_exp.clear()
     self.update_showinf(self.menu_exp.currentIndex())

    def checkboxes_input(self):
     if self.air_frict.isChecked():
        if "Air_coeff" not in self.values_dict:
            self.values_dict["Air_coeff"] = 0.9
        self.optionals_dict["Air resistance"] = True
     else:
        self.optionals_dict["Air resistance"] = False
     if self.trampolines_exp.isChecked():
        if "Coll_coeff" not in self.values_dict:
            self.values_dict["Coll_coeff"] = 1
        self.optionals_dict["Trampolines"] = True
     else:
        self.optionals_dict["Trampolines"] = False
     self.optionals_dict["Wind"] = self.wind_exp.isChecked()
     self.optionals_dict["Surfaces"] = self.change_surfaces.isChecked()
     self.update_showinf()
             
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()