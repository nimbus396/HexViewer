from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QStandardItem


class HexViewerTableViewModel(QAbstractTableModel):


    def __init__(self, byteArray=None, asciiArray=None):
        QAbstractTableModel.__init__(self)
        self.byteArray = byteArray
        self.asciiArray = asciiArray
        self.load_data()

    def load_data(self):
        self.column_count = 18
        self.row_count = (len(self.byteArray)/16)+1

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Offset", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "0D", "0E", "0F", "Data")[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                return "{:015x}".format(row)
            elif column > 0 and column < 17:
                try:
                    retData = self.byteArray[(row*16)+(column-1)]
                    return retData
                except IndexError:
                    return
            elif column == 17:
                retData = self.asciiArray[row]
                return retData
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.ForegroundRole and column == 0:
            return QColor(Qt.blue)

        return None
