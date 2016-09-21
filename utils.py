u"""Разные вспомогательные утилиты"""

import json
import sys

def json_content_from_file( file_name ):
	u"""Возвращает распарсенное json'ом содержимое файла"""
	f = open( file_name, "r", encoding="utf-8" )
	content = f.read()
	f.close()

	return json.loads( content )