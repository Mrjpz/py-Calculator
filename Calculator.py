import sys
import re
from collections import deque
from math import sqrt
from functools import partial
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QLabel, QTextEdit, QPushButton, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QStackedWidget, QFrame, QMenu, QWidgetAction, QLineEdit, QTextBrowser




class MainWindow(QMainWindow):
    def updateHistoryDisplay(self):
            self.historyLabel.setText("\n".join(self.queue))
            if len(self.queue) > 15:
                self.queue.popleft()
            txt=len(self.queue)#temp code
            print(txt)#temp code
            
    @Slot()
    def history(self):
        if self.historyLabel.isVisible():
            self.historyLabel.hide()
            self.label.show()
        else:
            self.historyLabel.show()
            self.label.hide()
            
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
        elif text == 'C':
            equation = '0'
            self.label.setText(equation)
        elif text == 'CE':
            equation = '0' #needs to be fixed
            self.label.setText(equation)
        elif text == '1/(x)':
            equation = '1/(' + equation + ")"
            equation = equation.replace("1/(x)", '')
            self.label.setText(equation)
        elif text == 'x²':
            equation = equation + '²'
            equation = equation.replace('x²', '')
            self.label.setText(equation) #Takes care of gui
        elif text == '√':
            equation = equation.replace('√', '')
            equation = '√' + equation
            self.label.setText(equation) #Takes care of gui
        elif text == '%':
            operators = ['x','÷','-','+']
            ind = equation.index('%')
            for i in equation:
                if i in operators:
                    op = i
            ind2 = equation.index(op)
            percentage = '.'+equation[ind2+1:ind]
            one_hundred_percent = equation[:ind2]            
            n = str(float(percentage) * float(one_hundred_percent))
            equation = equation[:ind2+1] + n +equation[ind:]
            print(equation)
            self.label.setText(equation)
        elif text == '+/-':
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', equation) #find all the numebrs in the equaion
            tmp = int(numbers[-1])                               #find the last number typed
            if tmp > 0:                                          #if the number is positive make it negitive and if its negitive make it positive
                tmp = -abs(tmp)
            else:
                tmp = abs(tmp)
            equation = equation[:equation.rfind(numbers[-1])] + str(tmp) 
            self.label.setText(equation)
        else:
            self.label.setText(equation)
        
        #take care of percentage
        if text == '=' and '%' in equation:
            equation = equation.replace('%=','')
            self.total = eval(str(equation))
            app = str(equation) + '=' + str(self.total)
            self.queue.append(app)
            self.updateHistoryDisplay()
            self.label.setText(str(self.total))
            self.solved = True

        #take care of square root        
        elif text == '=' and "√" in equation:
            tmp = str(equation)
            equation = equation.replace('√', '')
            equation = equation.replace('=','')
            equation =  sqrt(int(equation))
            self.total = str(equation)
            app = tmp + str(self.total)
            self.queue.append(app)
            self.updateHistoryDisplay()
            self.label.setText(self.total)
            self.solved = True
        
        #take care of +,-,*,/, and square
        elif text == "=":
            if "²" in equation:
                tmp = str(equation)
                equation = equation.replace('²=', '')
                equation =  equation + '**2'
            elif 'x' in equation:
                tmp = str(equation)
                equation = equation.replace("x", '*')
            elif '÷' in equation:
                tmp = str(equation)
                equation = equation.replace("÷","/")
            else:
                tmp = str(equation)
            equation = equation.rstrip("=")
            self.total = eval(equation)
            app = tmp + str(self.total)
            self.queue.append(app)
            self.updateHistoryDisplay()
            self.label.setText(str(self.total))
            self.solved = True
        
        
                
    def __init__(self):
        super().__init__()
        
        size_tup = [320, 500]
        # Create the mian window size
        self.setWindowTitle('Calculator')
        
        
        self.resize(size_tup[0], size_tup[1])
        
        # Create invisible backround
        self.invisible_backround = QWidget()
        
        # Create buttons
        buttons = ['⌫','C','CE','%','÷','√','x²','1/(x)','x','9','8','7','-','6','5','4','+','3','2','1','=', '.', '0','+/-']
        # Create history button
        history_button = QPushButton('≡')
        history_button.clicked.connect(self.history)
        
        
        # Create a history Qlabel
        self.historyLabel = QLabel("History", alignment = Qt.AlignmentFlag.AlignTop)
        self.historyLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.historyLabel.hide()  # Hide history object initially
        
        # Set the fixed size of the history label
        self.historyLabel.setFixedWidth(300)
        self.historyLabel.setFixedHeight(300)
       
        
        
        # Create a grid layout and add the buttons
        grid_layout = QGridLayout()
        for i, button in enumerate(buttons):
            #print('button', button)
            row = i // 4
            #print('row', row)
            col = 3-(i % 4)
            #print('col', col)
            button = QPushButton(buttons[i])
            button.clicked.connect(self.emit_number)
            grid_layout.addWidget(button, row, col)
            
        # Create a vertical layout
        layout = QVBoxLayout()
        
        # Create a box for text based input to be displayed
        self.label = QLabel(self)
        self.label.setText("0")

        
        
        layout.insertWidget(0, history_button, alignment=Qt.AlignmentFlag.AlignRight)#temp placement it moves whenever you open the history button 
        layout.addWidget(self.invisible_backround)
        layout.addWidget(self.label)
        layout.insertWidget(0, self.historyLabel)
        layout.addLayout(grid_layout)
        
        
       
        
        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget of the main window
        self.setCentralWidget(central_widget)
        
        
        self.solved = False #bool Flag to see if problem is solved
        self.total = 0 #int Flag to see the total
        self.queue = deque()# make queue for history
        
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

'''
*current task*


make a settings button
make a color wheel

style the calculator **LAST TASK**
color wheel hue types
#test

** Current bugs known bugs
*Whenever you take the total of an equation and try and add more to it. The contents of the equation are deleted and you cant add to the total.
'''