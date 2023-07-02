import pyqtgraph as pg
from PyQt5 import QtGui,QtWidgets

DEGREE_SMB = u'\N{DEGREE SIGN}'

class Graph(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("graph")

        labelStyle = {'color': '#FFF', 'font-size': '14pt'}
        font = QtGui.QFont('serif',14)


        self.tempPl = self.addPlot(row=0, col=0)
        self.tempPl.setLabel('left', "T", units=DEGREE_SMB+'C',**labelStyle)
        # Adjust the label offset
        self.tempPl.getAxis('left').setWidth(100)
        self.tempPl.setLabel('bottom', "time", units='sec',**labelStyle)

        
        self.setBackground(background='#25272b')
               
        self.tempPl.getAxis('left').setPen('#fcfcc7')
        self.tempPl.getAxis('left').tickFont = font

if __name__ == '__main__':
    pass