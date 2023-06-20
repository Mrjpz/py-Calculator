import sys
from functools import partial
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QStackedWidget, QFrame




class MainWindow(QMainWindow):
    @Slot(str)
    def emit_number(self, text):
        # Button and text variables
        button = self.sender()
        text = button.text()
        # Represents the equation aka what you see on the screen
        equation = self.label.text()
        
        if self.solved:
            equation = "0"
            self.label.setText(equation)
            self.solved = False
        if button and equation == "0" :
            equation = equation[1:]
        
        # adds the text to the equaion 
        equation += text
        
        
        if text == '⌫' and equation != '0':
            equation = equation[:-2]
            self.label.setText(equation)
        if text == 'C':
            equation = '0'
            self.label.setText(equation)
        if text == 'CE':
            equation = '0'
            self.label.setText(equation)
        if text == '1/(x)':
            equation = '1/(' + equation + ")"
            equation = equation.replace("1/(x)", '')
            self.label.setText(equation)
        if text == 'x²':
            equation = equation + '²'
            equation = equation.replace('x²', '')
            self.label.setText(equation) #Takes care of gui
        if text == '√':
            equation = '0'
            self.label.setText(equation) #needs fix
        if text == '%':
            equation = '0'
            self.label.setText(equation) #needs fix
        else:
            self.label.setText(equation)
        
        #take care of square root
        if text == '=' and "²" in equation:
                equation = equation.replace('²=', '')
                equation =  equation + '**2'
                print('equation',equation)
                self.total = eval(equation)
                self.label.setText(str(self.total))
                self.solved = True
                
                           
        #take care of +,-,*, and /
        elif text == "=":
            if 'x' in equation:
                equation = equation.replace("x", '*')
            if '÷' in equation:
                equation = equation.replace("÷","/")
            equation = equation.rstrip("=")
            self.total = eval(equation)
            self.label.setText(str(self.total))
            self.solved = True
            
          
                
        
        

    def __init__(self):
        super().__init__()

        # Create the mian window size
        self.setWindowTitle('Calculator')
        self.resize(320, 500)
        
        # Create buttons
        buttons = ['⌫','C','CE','%','÷','√','x²','1/(x)','x','9','8','7','-','6','5','4','+','3','2','1','=', '.', '0','+/-']
        
        # Create a grid layout and add the buttons
        grid_layout = QGridLayout()
        for i, button in enumerate(buttons):
            row = i // 4
            col = 3-(i % 4)
            button = QPushButton(buttons[i])
            button.clicked.connect(self.emit_number)
            grid_layout.addWidget(button, row, col)
            
        # Create a vertical layout
        layout = QVBoxLayout()
        
        # Create a box for text based input to be displayed
        self.label = QLabel(self)
        self.label.setText("0")
        layout.addWidget(self.label)
        layout.addLayout(grid_layout)
        
        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget of the main window
        self.setCentralWidget(central_widget)
        
        self.solved = False #bool Flag to see if problem is solved
        self.total = 0 #int Flag to see the total
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

'''
*current task*

fix the rest of my buttons
create button for the stack history
use a stack as history(try and use a visual window to see what is stacked)
make a settings button
make a color wheel

style the calculator **LAST TASK**
color wheel hue types

'''