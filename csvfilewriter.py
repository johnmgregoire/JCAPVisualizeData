import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def createcsvfilstr(datadlist, fomkeys, fmt='%.5e'):#for each sample, if fom not available inserts NaN
    smparr=[d['sample_no'] for d in datadlist]
    fomarr_smps=numpy.array([[(k in d['fomd'].keys() and (d['fomd'][k],) or (numpy.nan,))[0] for k in fomkeys] for d in datadlist]) 
    lines=[','.join(['sample_no']+fomkeys)]
    for smp, fomarr in zip(smparr, fomarr_smps):
        lines+=[','.join(['%d' %smp]+[fmt %n for n in fomarr])]
    s='\n'.join(lines)
    return s



class selectexportfom(QDialog):
    def __init__(self, parent, fomkeys, title='select FOMs to export. sample_no will be automatically included'):
        super(selectexportfom, self).__init__(parent)
        self.setWindowTitle(title)
        self.parent=parent
        self.fomkeys=fomkeys
        vlayouts=[]
        self.checkboxes=[]
        for count, k in enumerate(fomkeys):
            if count%10==0:
                vlayout=QVBoxLayout()
                vlayouts+=[vlayout]
            cb=QCheckBox()
            cb.setText(k)
            if len(k)>2 and not ('ample' in k or 'x(mm)' in k or 'y(mm)' in k):
                cb.setChecked(True)
            vlayout.addWidget(cb)
            self.checkboxes+=[cb]
        
        
        mainlayout=QGridLayout()
        for count, l in enumerate(vlayouts):
            mainlayout.addLayout(l, 0, count)
        
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox, min(10, len(self.checkboxes)), 0)
    
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        #QObject.connect(self.buttonBox,SIGNAL("rejected()"),self.ExitRoutineCancel)
        
        self.setLayout(mainlayout)

        #self.resize(300, 250)
        self.selectkeys=[]
    
    def ExitRoutine(self):
        for cb, k in zip(self.checkboxes, self.fomkeys):
            if cb.isChecked():
                self.selectkeys+=[k]
