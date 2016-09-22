import sys
from PyQt4 import QtGui

from estimator import create_estimator
from debug_log import LOG

ELEMENT_MARGIN = 10

class GuiDebugHandler(QtGui.QTextEdit):
	u"""Debug Handler, реализованный в виде окна QT"""
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
	u"""Главное окно приложения. Позволяет вводить текст,
	показывать результат, устанавливает глобальный debug handler в GuiDebugHandler,
	выводит информацию если где-то в estimator'е вылетело исключение"""
	def __init__(self):
		super(MainWindow, self).__init__()
		self._init_GUI()

		try:
			self.estimator = create_estimator( "data" )
		except Exception as e:
			self._handleException( e )

	def _init_GUI( self ):
		u"""Создаем GUI, располагая все в вертикальный стек"""
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

	def _onProcess( self ):
		u"""Реакция на кнопку process. Запускаем estimator для введеного приложения"""
		if self.estimator == None:
			return

		LOG.clear()
		try:
			sentence = self.sentece_text.text()
			result = self.estimator.process_sentence( sentence )
			self.result_text.setText( str( result ) )
		except Exception as e:
			self._handleException( e )

	def _handleException(self, e):
		u"""Реакция на исключение. Сбрасываем estimator в None (не пытаемся для простоты ничего реанимировать)
		устанавливаем информацию об ошибке в GUI"""
		self.estimator = None
		self.result_text.setText( "APPLICATION CRASHED" )
		LOG.clear()
		LOG.write( "EXCEPTION OCCURED", str( e ) )