u"""Запись отладочной информации"""

class PrintDebugHandler:
	u"""DebugHandler, реализованный через print"""
	def on_new_message( self, title, message ):
		print( title )
		print( message )
		print()

	def clear( self ):
		print( "CLEAR" )

class DebugLog:
	u"""DebugLog создается как глобал
	ьная пемеренная Log ниже
	Позволяет ото всюду писать в него. Для работы требуется установить handler (через set_handler),
	после чего включить лог(через set_enabled( true ))
	Handler отвечает за непосредственно вывод сообщений пользователю
	Handler должен содержать методы on_new_message(title, message) и clear()"""
	def __init__(self):
		self.enabled = False
		self.handler = None

	def is_enabled( self ):
		return self.enabled and self.handler != None

	def set_enabled( self, enabled ):
		if enabled:
			assert self.handler != None, "Can't enable log with empty handler"
		self.enabled = enabled

	def set_handler( self, handler ):
		self.handler = handler

	def write( self, title, message ):
		if not self.is_enabled():
			return

		self.handler.on_new_message( title, message )

	def clear( self ):
		if not self.is_enabled():
			return

		self.handler.clear()

LOG = DebugLog()
