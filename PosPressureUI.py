import sys
import cv2
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication
from PyQt5.QtGui import QIcon
from os import system
import os
from configurator import getCfg
import numpy as np
import pickle
import PosPressure as pp

cwd = os.getcwd()
qtCreatorFile = cwd+"/PosPressure.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Block(object):
    def __init__(self, duration, lightConfig, flowRate, flowDir, flowGas):
        self.duration = duration
        self.lightConfig = lightConfig
        self.flowRate = flowRate
        self.flowDir = flowDir
        self.flowGas = flowGas

class ErrorMsg(QtWidgets.QMessageBox):
    def __init__(self, msg, parent=None):
        super(ErrorMsg, self).__init__(parent)
        self.setIcon(QtWidgets.QMessageBox.Critical)
        self.setText(msg)
        self.setWindowTitle('Error')

class WarningMsg(QtWidgets.QMessageBox):
    def __init__(self, msg, parent=None):
        super(WarningMsg, self).__init__(parent)
        self.setText(msg)
        self.setWindowTitle('Warning')


class PosPressure(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Positive Pressure System')
        self.setFixedSize(self.size())
        self.addBlockPB.clicked.connect(self.addBlock)
        self.addDupBlocksPB.clicked.connect(self.addDupBlocks)
        self.runPB.clicked.connect(self.run)
        self.deleteBlockPB.clicked.connect(self.deleteBlock)
        self.pickSaveFolderPB.clicked.connect(self.pickSaveFolder)
        self.saveProgramPB.clicked.connect(self.saveProgram)
        self.loadProgramPB.clicked.connect(self.loadProgram)
        self.blockList = []
        dString = "{},     {} \t{}\t{}  {}       {}".format('#', 'Dur (s)', 'Light', 'Gas', 'mL/s', 'Flow Dir')
        lString = "---------------------------------------------------------------"
        self.programList.addItems([dString, lString])

    def addBlock(self):
        # Configs: GreenLow = 1, GreenHigh = 2, RedLow = 3, RedHigh = 4, None=0
        # Air = 1, Odor = 2, None = 0
        if self.addGreenRadioButton.isChecked() and self.addDimRadioButton.isChecked():
            lightCfg = 1
            lightDspTxt = "Lo Green"
        elif self.addGreenRadioButton.isChecked() and self.addBrightRadioButton.isChecked():
            lightCfg = 2
            lightDspTxt = "Hi Green"
        elif self.addRedRadioButton.isChecked() and self.addDimRadioButton.isChecked():
            lightCfg = 3
            lightDspTxt = "Lo Red"
        elif self.addRedRadioButton.isChecked() and self.addBrightRadioButton.isChecked():
            lightCfg = 4
            lightDspTxt = "Hi Red"
        else:
            lightCfg = 0
            lightDspTxt = "No Light"
        if self.addFlowDir1RadioButton.isChecked():
            flowDir = 1
        if self.addFlowDir2RadioButton.isChecked():
            flowDir = 2
        else:
            #Error Pick Flow Dir
            flowDir = 0
        dur = float(self.addTimeSpinBox.value())
        flowRate = float(self.addFlowRateSpinBox.value())
        if self.addAirRadioButton.isChecked():
            flowGas = 1
            fgString = 'Air'
        elif self.addOdorRadioButton.isChecked():
            flowGas = 2
            fgString = 'Odor'
        else:
            flowGas = 0
            fgString = 'No Flow'
            flowRate = 0
            self.addFlowRateSpinBox.clear()
            flowRate = 0
        newBlock = Block(dur, lightCfg, flowRate, flowDir, flowGas)
        self.blockList.append(newBlock)
        listPos = len(self.blockList)
        dispString = "{},     {} \t{}\t{}  {}       {}".format(listPos, str(dur), lightDspTxt, fgString, str(flowRate), str(flowDir))
        self.programList.addItems([dispString])
        return None

    def deleteBlock(self):
        d = self.programList.currentRow() - 2
        item = self.programList.takeItem(self.programList.currentRow())
        item = None
        del self.blockList[d]
        entries = [self.programList.item(i).text() for i in range(self.programList.count())]
        reindexed = []
        for idx, entry in enumerate(entries[2:]):
            listOfInfos = entry.split(",")
            listOfInfos[0] = idx+1
            reconstructed = '{},{}'.format(listOfInfos[0], listOfInfos[1])
            reindexed.append(reconstructed)
        self.programList.clear()
        dString = "{},     {} \t{}\t{}  {}       {}".format('#', 'Dur (s)', 'Light', 'Gas', 'mL/s', 'Flow Dir')
        lString = "---------------------------------------------------------------"
        self.programList.addItems([dString, lString])
        for reindex in reindexed:
            self.programList.addItems([reindex])
        return None

    def addDupBlocks(self):



        single = False
        multi = False
        if self.dupBlockText.toPlainText() != '':
            single = True
            idx = int(self.dupBlockText.toPlainText()) -1
            entries = [self.programList.item(i).text() for i in range(self.programList.count())]
            toAdd = entries[idx+2]
            blockToAdd = self.blockList[idx]
            self.blockList.append(blockToAdd)
            self.dupBlockText.clear()
            listOfInfos = toAdd.split(",")
            listOfInfos[0] = str(len(self.blockList))
            reconstructed = '{},{}'.format(listOfInfos[0], listOfInfos[1])
            self.programList.addItems([reconstructed])

        else:
            if (self.dupBlocksFirstText.toPlainText() != "") and (self.dupBlocksLastText.toPlainText() != ""):
                if single == True:

                    msg = 'Cannot add single block and range in same operation'
                    self.warning = WarningMsg(msg)
                    self.warning.show()

                    self.dupBlocksFirstText.clear()
                    self.dupBlocksLastText.clear()
                else:
                    multi = True
                    idxLo = int(self.dupBlocksFirstText.toPlainText())
                    idxHi = int(self.dupBlocksLastText.toPlainText())

                    if idxLo >= idxHi:
                        msg = 'Last entry in range must be larger than first'
                        self.error = ErrorMsg(msg)
                        self.error.show()


                    copyBlocks = list(np.arange(idxLo, (idxHi+1), 1))
                    for i in range(self.programList.count()):
                        if i in copyBlocks:
                            blockToAdd = self.blockList[i]
                            self.blockList.append(blockToAdd)
                            index = str(len(self.blockList))
                            toAdd = self.programList.item(i+1).text()
                            listOfInfos = toAdd.split(",")
                            listOfInfos[0] = index
                            reconstructed = '{},{}'.format(listOfInfos[0], listOfInfos[1])
                            self.programList.addItems([reconstructed])
                        else:
                            pass
                self.dupBlocksFirstText.clear()
                self.dupBlocksLastText.clear()
            return None


    def pickSaveFolder(self):
        fname = QFileDialog.getExistingDirectory(self, 'Select Save Directory')
        self.savePath = str(fname)
        self.savePathLabel.setText(self.savePath)
        return None

    def saveProgram(self):
        self.programSavePath = QFileDialog.getSaveFileName(self, 'Select Save Directory', os.getcwd())
        self.programSavePath = self.programSavePath[0]+".pkl"
        entries = [self.programList.item(i).text() for i in range(self.programList.count())]
        savePack = {'dispList':entries,
                    'blockList':self.blockList}
        pickle_out = open(self.programSavePath,"wb")
        pickle.dump(savePack, pickle_out)
        pickle_out.close()
        return None

    def loadProgram(self):
        fname = QFileDialog.getOpenFileName(self, 'Select Program to Open', os.getcwd())
        self.openProgramPath = str(fname[0])
        pickle_in = open(self.openProgramPath, "rb")
        savePack = pickle.load(pickle_in)
        self.programList.clear()
        self.blockList = savePack['blockList']
        for entry in savePack['dispList']:
            self.programList.addItems([entry])
        return None

    def run(self):
        try:
            self.comm = self.arduinoCommText.toPlainText()
            self.baud = int(self.arduinoBaudText.toPlainText())
            self.nTrials = self.programCylceSpinBox.value()
        except ValueError:
            msg = 'Make sure all configuration fields are entered with valid entries'
            self.error = ErrorMsg(msg)
            self.error.show()


        pp.run(self.comm, self.baud, self.blockList, self.nTrials, self.savePath)
        return None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = PosPressure()
    window.show()
    sys.exit(app.exec_())
