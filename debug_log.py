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
	u"""Handler должен содержать метод on_new_message(title, message) и метод clear()"""
	def __init__(self):
		self.enabled = False
		self.handler = None

	def is_enabled( self ):
		return self.enabled and self.handler != None

	def set_enabled( self, enabled ):
		self.enabled = enabled

		if self.enabled:
			assert self.handler != None, "Can't enable log with empty handler"

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
