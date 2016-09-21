import sys
from PyQt4 import QtGui

import dictionaries
import sentimental_estimator as se
from debug_log import LOG

ELEMENT_MARGIN = 10

class GuiDebugHandler(QtGui.QTextEdit):
	def __init__(self):
		super(GuiDebugHandler, self).__init__()
		self.resize( 480, 480 )

	def on_new_message( self, title, message ):
		self.append( title )
		self.append( message )
		self.append( "" )

	def clear( self ):
		self.setText( "" )

class MainWindow(QtGui.QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		self._init_GUI()
		self._init_estimator()

	def _init_GUI( self ):
		self.setWindowTitle("Sentimental Estimator")

		vbox = QtGui.QVBoxLayout()
		self.setLayout( vbox )

		sentence_label = QtGui.QLabel( self )
		sentence_label.setText( "Please, enter a sentence:" )
		vbox.addWidget( sentence_label )

		self.sentece_text = QtGui.QLineEdit( self )
		vbox.addWidget( self.sentece_text )

		process_button = QtGui.QPushButton( self )
		process_button.setText( "PROCESS" )
		process_button.clicked.connect(self._onProcess) 
		vbox.addWidget( process_button )

		result_label = QtGui.QLabel( self )
		result_label.setText( "Result:" )
		vbox.addWidget( result_label )

		self.result_text = QtGui.QLineEdit( self )
		vbox.addWidget( self.result_text )

		log_label = QtGui.QLabel( self )
		log_label.setText( "Log:" )
		vbox.addWidget( log_label )

		debug_log = GuiDebugHandler()
		vbox.addWidget( debug_log )
		LOG.set_handler( debug_log )
		LOG.set_enabled( True )

	def _init_estimator(self):
		data_path = "data"
		dictionaries_with_weights = [
			{ "dict": dictionaries.WobotDictionary( data_path ), "weight": 1 },
			{ "dict": dictionaries.WNAffectDictionary( data_path ), "weight": 1 },
			{ "dict": dictionaries.LinisDictionary( data_path ), "weight": 1 }
		]
		neutral_treshold = 0.1

		self.estimator = se.SentimentalEstimator( dictionaries_with_weights, neutral_treshold )

	def _onProcess( self ):
		LOG.clear()
		sentence = self.sentece_text.text()
		result = self.estimator.process_sentence( sentence )
		self.result_text.setText( str( result ) )

def main():
    
    app = QtGui.QApplication(sys.argv)

    w = MainWindow()
    w.move(300, 300)
    w.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()