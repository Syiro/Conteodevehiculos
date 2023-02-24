from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ErrorDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(QDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("!!ERROR!!")
        label = QLabel("Modo de configuracion no establecido correctamente", self)
        button = QPushButton('Aceptar', self)
        button.clicked.connect(self.accept)
        
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(button)
        self.setFixedSize(400, 100)
        
class URLDialog(QDialog):
    urlEntered = pyqtSignal(str)
    def __init__(self, parent=None):
        super(URLDialog, self).__init__(parent)
        # Crear un QLineEdit para que el usuario ingrese la URL
        self.url_edit = QLineEdit()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ingrese la URL del video:"))
        layout.addWidget(self.url_edit)
        
        # Crear un botón para aceptar la URL
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
    def accept(self):
        # Emitir la señal urlEntered con el valor de la URL ingresada
        url = self.url_edit.text()
        self.urlEntered.emit(url)
        super().accept()