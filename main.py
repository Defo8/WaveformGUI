import sys
import json

from PyQt5.QtWidgets import *

from GenWaveForm import *
import numpy as np
import pandas as pd
import pyqtgraph as pg

gen = GenWaveForm()

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 1080, 600)
        self.setWindowTitle('Calculate')

        self.Layout0 = QVBoxLayout()
        self.LayoutMain = QHBoxLayout()
        self.LayoutWaveforms = QVBoxLayout()
        self.LayoutGraphType = QVBoxLayout()
        self.LayoutFile = QVBoxLayout()

        self.box1 = QDoubleSpinBox(self)
        self.box1.setMinimumSize(200, 50)
        self.box1.setToolTip('Zakres czasu')

        self.box2 = QSpinBox(self)
        self.box2.setMinimumSize(200, 50)
        self.box2.setToolTip('Ilość kroków')

        self.box3 = QDoubleSpinBox(self)
        self.box3.setMinimumSize(200, 50)
        self.box3.setToolTip('Amplituda')

        self.box4 = QDoubleSpinBox(self)
        self.box4.setMinimumSize(200, 50)
        self.box4.setToolTip('Częstotliwość')

        self.blank1 = QLabel(self)
        self.blank1.setText("")

        self.WaveformLabel = QLabel()
        self.WaveformLabel.setText("Generate:")
        self.LayoutWaveforms.addWidget(self.blank1)
        self.LayoutWaveforms.addWidget(self.WaveformLabel)

        self.sine = QPushButton('Sine')
        self.sine.setMaximumWidth(100)
        self.LayoutWaveforms.addWidget(self.sine)
        self.sine.clicked.connect(self.sine_Click)

        self.rectangle = QPushButton('Rectangle')
        self.rectangle.setMaximumWidth(100)
        self.LayoutWaveforms.addWidget(self.rectangle)
        self.rectangle.clicked.connect(self.rectangle_Click)

        self.triangle = QPushButton('Triangle')
        self.triangle.setMaximumWidth(100)
        self.LayoutWaveforms.addWidget(self.triangle)
        self.triangle.clicked.connect(self.triangle_Click)

        self.sawtooth = QPushButton('Sawtooth')
        self.sawtooth.setMaximumWidth(100)
        self.LayoutWaveforms.addWidget(self.sawtooth)
        self.sawtooth.clicked.connect(self.sawtooth_Click)

        self.whiteNoise = QPushButton('White Noise')
        self.whiteNoise.setMaximumWidth(100)
        self.LayoutWaveforms.addWidget(self.whiteNoise)
        self.whiteNoise.clicked.connect(self.whiteNoise_Click)

        self.radio1 = QRadioButton('Waveform')
        self.radio1.setChecked(True)
        self.radio2 = QRadioButton('Fourier Transform')
        self.LayoutGraphType.addWidget(self.radio1)
        self.LayoutGraphType.addWidget(self.radio2)


        self.tocsvButton = QPushButton("Save to .CSV")
        self.LayoutFile.addWidget(self.tocsvButton)
        self.tocsvButton.clicked.connect(self.save)
        self.towavButton = QPushButton("Save to .WAV")

        self.LayoutFile.addWidget(self.towavButton)
        self.fourierToCsvButton = QPushButton("Save Fourier Transform to .CSV")
        self.LayoutFile.addWidget(self.fourierToCsvButton)
        self.fourierToCsvButton.clicked.connect(self.saveFFT)
        self.clearr = QPushButton('Clear')
        self.LayoutFile.addWidget(self.clearr)
        self.clearr.clicked.connect(self.clear)

        self.graph = pg.PlotWidget()

        self.buttonLabel1 = QLabel(self)
        self.buttonLabel1.setText('Length[s]:')
        self.buttonLabel1.setStyleSheet("QLabel{font-size: 10pt; font-weight: bold;}")
        self.buttonLabel2 = QLabel(self)
        self.buttonLabel2.setText("Sample rate:")
        self.buttonLabel2.setStyleSheet("QLabel{font-size: 10pt; font-weight: bold;}")
        self.buttonLabel3 = QLabel(self)
        self.buttonLabel3.setText('Amplitude:')
        self.buttonLabel3.setStyleSheet("QLabel{font-size: 10pt; font-weight: bold;}")
        self.buttonLabel4 = QLabel(self)
        self.buttonLabel4.setText('Frequency[Hz]:')
        self.buttonLabel4.setStyleSheet("QLabel{font-size: 10pt; font-weight: bold;}")

        self.table = QTableWidget(self)
        self.table.resize(250, 350)
        self.table.setColumnCount(2)

        self.LayoutGraph = QHBoxLayout()
        self.LayoutGraph.addWidget(self.graph)


        self.LayoutButtons = QVBoxLayout()
        self.LayoutButtons.addWidget(self.buttonLabel1)
        self.LayoutButtons.addWidget(self.box1)
        self.LayoutButtons.addWidget(self.buttonLabel2)
        self.LayoutButtons.addWidget(self.box2)
        self.LayoutButtons.addWidget(self.buttonLabel3)
        self.LayoutButtons.addWidget(self.box3)
        self.LayoutButtons.addWidget(self.buttonLabel4)
        self.LayoutButtons.addWidget(self.box4)


        self.LayoutTable = QVBoxLayout()
        self.LayoutTable.addWidget(self.table)

        self.title = QLabel(self)
        self.title.setText("    ......./|QT WAVFROM|\.......")
        self.title.setStyleSheet("QLabel{font-size: 19pt; font-weight: bold; color: blue}")

        self.blank2 = QLabel(self)
        self.blank2.setText("")
        self.b1 = QLabel(self)
        self.b1.setText("      ")
        self.b2 = QLabel(self)
        self.b2.setText("      ")
        self.b3 = QLabel(self)
        self.b3.setText("      ")

        self.LayoutTitle = QHBoxLayout()
        self.LayoutTitle.addWidget(self.blank1)
        self.LayoutTitle.addWidget(self.title)
        self.LayoutTitle.addWidget(self.blank2)

        self.LayoutMain.addLayout(self.LayoutButtons)
        self.LayoutMain.addWidget(self.b1)
        self.LayoutMain.addLayout(self.LayoutGraph)
        self.LayoutMain.addWidget(self.b2)
        self.LayoutMain.addLayout(self.LayoutTable)

        self.LayoutFunctions = QHBoxLayout()
        self.LayoutFunctions.addWidget(self.blank1)
        self.LayoutFunctions.addLayout(self.LayoutWaveforms)
        self.LayoutFunctions.addLayout(self.LayoutGraphType)
        self.LayoutFunctions.addLayout(self.LayoutFile)

        self.Layout0.addLayout(self.LayoutTitle)
        self.Layout0.addLayout(self.LayoutMain)
        self.Layout0.addLayout(self.LayoutFunctions)
        self.setLayout(self.Layout0)
        self.show()
        #self.body()




    def sine_Click(self):
        self.graph.clear()
        self.f = float(self.box4.value())
        self.A = float(self.box3.value())
        self.steps = int(self.box2.value())
        self.table.setRowCount(int(self.steps)*44100)
        self.range = float(self.box1.value())

        t = np.linspace(0, self.range, self.steps*44100)
        y = gen.Sine(self.f, self.A, t)

        row1 = 0
        for i in t:
            self.table.setItem(row1, 0, QTableWidgetItem(str(i)))
            row1 = row1 + 1

        row2 = 0
        for i in y:
            self.table.setItem(row2, 1, QTableWidgetItem(str(i)))
            row2 = row2 + 1

        if self.radio1.isChecked():
            pen = pg.mkPen(color=(0, 0, 255), width=1)
            self.plot = self.graph.plot(t, y, pen=pen)
            self.graph.setLabel('left', text='<font size=10>Amplitude</font>')
            self.graph.setLabel('bottom', text='<font size=10>Time[s]</font>')
            self.graph.setTitle('<font size=20>Sine</font>')
        elif self.radio2.isChecked():

            xf, yf = gen.TransformataFouriera(y, t)

            for i in xf:
                self.table.setItem(row1, 0, QTableWidgetItem(str(i)))
                row1 = row1 + 1

            row2 = 0
            for i in yf:
                self.table.setItem(row2, 1, QTableWidgetItem(str(i)))
                row2 = row2 + 1

            pen = pg.mkPen(color=(0, 0, 255), width=1)
            self.plot = self.graph.plot(xf, yf, pen=pen)
            self.graph.setLabel('left', text='<font size=10>Value</font>')
            self.graph.setLabel('bottom', text='<font size=10>Frequency in Hz</font>')
            self.graph.setTitle('<font size=20> TF: Sine</font>')


        print('Waving...')

    def rectangle_Click(self):
        self.graph.clear()
        self.f = float(self.box4.value())
        self.A = float(self.box3.value())
        self.steps = int(self.box2.value())
        self.table.setRowCount(int(self.steps)*44100)
        self.range = float(self.box1.value())

        t = np.linspace(0, self.range, self.steps*44100)
        y = gen.Square(self.f, self.A,t)

        row1 = 0
        for i in t:
            self.table.setItem(row1, 0, QTableWidgetItem(str(i)))
            row1 = row1 + 1

        row2 = 0
        for i in y:
            self.table.setItem(row2, 1, QTableWidgetItem(str(i)))
            row2 = row2 + 1

        if self.radio1.isChecked():
            pen = pg.mkPen(color=(0, 0, 255), width=1)
            self.plot = self.graph.plot(t, y, pen=pen)
            self.graph.setLabel('left', text='<font size=10>Amplitude</font>')
            self.graph.setLabel('bottom', text='<font size=10>Time[s]</font>')
            self.graph.setTitle('<font size=20>Rectangle</font>')
        elif self.radio2.isChecked():
            xf, yf = gen.TransformataFouriera(y, t)

            for i in xf:
                self.table.setItem(row1, 0, QTableWidgetItem(str(i)))
                row1 = row1 + 1

            row2 = 0
            for i in yf:
                self.table.setItem(row2, 1, QTableWidgetItem(str(i)))
                row2 = row2 + 1

            pen = pg.mkPen(color=(0, 0, 255), width=1)
            self.plot = self.graph.plot(xf, yf, pen=pen)
            self.graph.setLabel('left', text='<font size=10>Value</font>')
            self.graph.setLabel('bottom', text='<font size=10>Frequency in Hz</font>')
            self.graph.setTitle('<font size=20> TF: Rectangle</font>')

        print('Waving...')

    def triangle_Click(self):
        self.graph.clear()
        self.f = float(self.box4.value())
        self.A = float(self.box3.value())
        self.steps = int(self.box2.value())
        self.table.setRowCount(int(self.steps)*44100)
        self.range = float(self.box1.value())

        t = np.linspace(0, self.range, self.steps*44100)
        y = gen.Triangle(self.f, self.A,t)

        row1 = 0
        for i in t:
            self.table.setItem(row1, 0, QTableWidgetItem(str(i)))
            row1 = row1 + 1

        row2 = 0
        for i in y:
            self.table.setItem(row2, 1, QTableWidgetItem(str(i)))
            row2 = row2 + 1

        if self.radio1.isChecked():
            pen = pg.mkPen(color=(0, 0, 255), width=1)
            self.plot = self.graph.plot(t, y, pen=pen)
            self.graph.setLabel('left', text='<font size=10>Amplitude</font>')
            self.graph.setLabel('bottom', text='<font size=10>Time[s]</font>')
            self.graph.setTitle('<font size=20>Triangle</font>')
        elif self.radio2.isChecked():

            xf, yf = gen.TransformataFouriera(y, t)

            for i in xf:
                self.table.setItem(row1, 0, QTableWidgetItem(str(i)))
                row1 = row1 + 1

            row2 = 0
            for i in yf:
                self.table.setItem(row2, 1, QTableWidgetItem(str(i)))
                row2 = row2 + 1

            pen = pg.mkPen(color=(0, 0, 255), width=1)
            self.plot = self.graph.plot(xf, yf, pen=pen)
            self.graph.setLabel('left', text='<font size=10>Value</font>')
            self.graph.setLabel('bottom', text='<font size=10>Frequency in Hz</font>')
            self.graph.setTitle('<font size=20> TF: Triangle</font>')

        print('Waving...')

    def sawtooth_Click(self):
        self.graph.clear()
        self.f = float(self.box4.value())
        self.A = float(self.box3.value())
        self.steps = int(self.box2.value())
        self.table.setRowCount(int(self.steps)*44100)
        self.range = float(self.box1.value())

        t = np.linspace(0, self.range, self.steps*44100)
        y = gen.Sawtooth(self.f, self.A,t)

        row1 = 0
        for i in t:
            self.table.setItem(row1, 0, QTableWidgetItem(str(i)))
            row1 = row1 + 1

        row2 = 0
        for i in y:
            self.table.setItem(row2, 1, QTableWidgetItem(str(i)))
            row2 = row2 + 1

        if self.radio1.isChecked():
            pen = pg.mkPen(color=(0, 0, 255), width=1)
            self.plot = self.graph.plot(t, y, pen=pen)
            self.graph.setLabel('left', text='<font size=10>Amplitude</font>')
            self.graph.setLabel('bottom', text='<font size=10>Time[s]</font>')
            self.graph.setTitle('<font size=20>Sawtooth</font>')
        elif self.radio2.isChecked():

            xf, yf = gen.TransformataFouriera(y, t)

            for i in xf:
                self.table.setItem(row1, 0, QTableWidgetItem(str(i)))
                row1 = row1 + 1

            row2 = 0
            for i in yf:
                self.table.setItem(row2, 1, QTableWidgetItem(str(i)))
                row2 = row2 + 1

            pen = pg.mkPen(color=(0, 0, 255), width=1)
            self.plot = self.graph.plot(xf, yf, pen=pen)
            self.graph.setLabel('left', text='<font size=10>Value</font>')
            self.graph.setLabel('bottom', text='<font size=10>Frequency in Hz</font>')
            self.graph.setTitle('<font size=20> TF: Sawtooth</font>')

        print('Waving...')

    def whiteNoise_Click(self):
        self.graph.clear()
        self.A = float(self.box3.value())
        self.steps = int(self.box2.value())
        self.table.setRowCount(int(self.steps)*44100)
        self.range = float(self.box1.value())

        t = np.linspace(0, self.range, self.steps*44100)

        y = gen.WhiteNoise(self.A, t)

        row1 = 0
        for i in t:
            self.table.setItem(row1, 0, QTableWidgetItem(str(i)))
            row1 = row1 + 1

        row2 = 0
        for i in y:
            self.table.setItem(row2, 1, QTableWidgetItem(str(i)))
            row2 = row2 + 1

        if self.radio1.isChecked():
            pen = pg.mkPen(color=(0, 0, 255), width=1)
            self.plot = self.graph.plot(t, y, pen=pen)
            self.graph.setLabel('left', text='<font size=10>Amplitude</font>')
            self.graph.setLabel('bottom', text='<font size=10>Time[s]</font>')
            self.graph.setTitle('<font size=20>White noise</font>')
        elif self.radio2.isChecked():

            xf, yf = gen.TransformataFouriera(y, t)

            for i in xf:
                self.table.setItem(row1, 0, QTableWidgetItem(str(i)))
                row1 = row1 + 1

            row2 = 0
            for i in yf:
                self.table.setItem(row2, 1, QTableWidgetItem(str(i)))
                row2 = row2 + 1

            pen = pg.mkPen(color=(0, 0, 255), width=1)
            self.plot = self.graph.plot(xf, yf, pen=pen)
            self.graph.setLabel('left', text='<font size=10>Value</font>')
            self.graph.setLabel('bottom', text='<font size=10>Frequency in Hz</font>')
            self.graph.setTitle('<font size=20> TF: White noise</font>')

        print('Waving...')

    def clear(self):
        self.graph.clear()
        self.box1.setValue(0)
        self.box2.setValue(0)
        self.box3.setValue(0)
        self.box4.setValue(0)
        self.table.clear()

    def save(self):
        print('Zapisuje wynik działania do pliku')
        self.steps = int(self.box2.value())
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getOpenFileName()", ".csv", options=options)

        t = []
        y = []

        for i in range(0, (int(self.steps) - 1) * 44100):
            t.append(self.table.item(i, 0).text())

        for i in range(0, (int(self.steps) - 1) * 44100):
            y.append(self.table.item(i, 1).text())

        data = {"t": t, "y": y}
        file = open(fileName, 'w')

        text = json.dumps(data)
        file.write(text)
        file.close()

    def saveFFT(self):
        print('Zapisuje wynik działania do pliku')
        self.steps = int(self.box2.value())
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getOpenFileName()", ".csv", options=options)

        t = []
        y = []

        for i in range(0, (int(self.steps)-1)*44100):
            t.append(self.table.item(i, 0).text())

        for i in range(0, (int(self.steps)-1)*44100):
            y.append(self.table.item(i, 1).text())

        data = {"t": t, "y": y}
        file = open(fileName, 'w')

        text = json.dumps(data)
        file.write(text)
        file.close()

    def SaveToWav(self, y, name):
        audio_data = np.int16(y * 2**15)
        write('%s.wav'%name, 44100, audio_data)


app = QApplication(sys.argv)

ex = App()
app.exec_()