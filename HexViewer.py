import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
from PySide6.QtCore import QFile, QIODevice, Slot, Qt
from PySide6.QtGui import QFont
from HexViewerTableViewModel import HexViewerTableViewModel

"""
Stylesheet for table
"""
hexTableViewStyle = """
QHeaderView::section {
    color: blue;
}
"""

"""
For every possible byte, convert printable characters to their string representation.
For all other, just put '.'
"""
def createConvertTable():
    convertTable=[]
    for i in range(0, 256):
        convertTable.append('.')
    for i in range(32, 127):
        convertTable[i] = chr(i)
    for i in range(161, 156):
        convertTable[i] = chr(i)
    return convertTable

"""
Select a file and load the tables
"""
def selectFile():

    byteArray = []
    asciiArray = []
    convertTable = []
    convertedArray = []


    dialog = QFileDialog(None)
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setViewMode(QFileDialog.Detail)

    if dialog.exec():
        fileName = dialog.selectedFiles()
    else:
        return

    """
    Build some tables.
    byteArray: hex representation from file byte
    asciiArray: string representation from file byte
    convertTable: table used to convert byte to ascii
    """
    convertTable = createConvertTable()

    """
    Open the file
    """
    try:
        with open(fileName[0], "rb") as binFile:
            # Read the first byte
            byte = binFile.read(1)
            # Add it to the hex and ascii lists
            while byte:
                byteArray.append(("{:02x}".format(ord(byte))))
                asciiArray.append(convertTable[ord(byte)])
                byte = binFile.read(1)
    except IOError:
        print('Error while opening file')
        byteArray.append('00')
        asciiArray.append('00')
        convertedArray.append('Error')

    for i in range(0, len(asciiArray), 16):
        convertedArray.append(''.join(asciiArray[i:i+16]))

    hexGUI.hexTableView.setFont(QFont("Courier New",11))
    hexModel = HexViewerTableViewModel(byteArray, convertedArray)
    hexGUI.hexTableView.setModel(hexModel)
    hexGUI.hexTableView.setStyleSheet(hexTableViewStyle)
    hexGUI.hexTableView.setShowGrid(False)
    hexGUI.hexTableView.setVisible(False)
    hexGUI.hexTableView.resizeColumnsToContents()
    hexGUI.hexTableView.setVisible(True)
    return

"""
This where it all starts
"""
if __name__ == '__main__':
    # Setup an application object
    app = QApplication(sys.argv)

    # UI file created with pyside6-designer found in venv Scripts
    ui_file_name = "HexViewer.ui"
    ui_file = QFile(ui_file_name)

    # Open the UI file
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {uifile.errorString()}")
        sys.exit(-1)

    # Load the UI file
    loader = QUiLoader()
    hexGUI = loader.load(ui_file)
    ui_file.close()

    if not hexGUI:
        print(loader.errorString())
        sys.exit(-1)
    hexGUI.show()

    # Connect Menu Options
    hexGUI.actionOpen.triggered.connect(selectFile)
    hexGUI.actionQuit.triggered.connect(hexGUI.close)

    # Wait for the app to close and then exit
    sys.exit(app.exec())
