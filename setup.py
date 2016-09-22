u"""Скрипт для установки всех необходимых библиотек"""

import pip
import sys
import importlib

def install(package):
	try:
		pip.main(['install', package])
	except Exception as e:
		print( "Failed to install package " + package + "in case of exception " + str( e ) )
		sys.exit( -1 )

# Проверяем, что установлены numpy, scipy и PyQt4
try:
    import numpy
    import scipy
    import PyQt4
    print('numpy, scipy and PyQt4 installed!')
except ImportError:
    print('No numpy, scipy and PyQt4 modules!\nPlease, visit https://www.continuum.io/downloads')
    sys.exit( -1 )

# Устанавливаем пакеты
install( "pymorphy2" )
install( "pymorphy2-dicts-ru" )
install( "nltk" )
globals()["nltk"] = importlib.import_module( "nltk" )

# Устанавливаем необходимые пакеты nltk
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_ru")

