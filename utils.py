u"""Разные вспомогательные утилиты"""

import json
import sys

def json_content_from_file( file_name ):
	u"""Возвращает распарсенное json'ом содержимое файла"""
	f = open( file_name, "r", encoding="utf-8" )
	content = f.read()
	f.close()

	return json.loads( content )

def try_load_corpus( corpus_class, DATA_PATH ):
	u"""Создание корпуса с обработкой ошибок"""
	try:
		return corpus_class( DATA_PATH )
	except Exception as e:
		print( "FAILED LOAD CORPUS " + corpus_name + " IN CASE OF EXCEPTION: ")
		print( str( e ) )
		sys.exit( -1 )
