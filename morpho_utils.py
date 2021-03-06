u"""Вспомогательные функции для работы с морфологией."""

import pymorphy2
import nltk
import string
from nltk.corpus import stopwords
import re
from debug_log import LOG

__morph = pymorphy2.MorphAnalyzer()

def normalize_word( word ):
	u"""Нормализует слово. Для существительного - единственное число, мужской род и т.п."""
	parsing_results = __morph.parse( word )
	if len( parsing_results ) == 0:
		return word

	return parsing_results[0].normal_form

def normalize_words( words ):
	u"""Нормализует массив слов."""
	result = []
	for word in words:
		normalized = normalize_word( word )
		if normalized not in result:
			result.append( normalized )
	return result

def split_sentece( sentece ):
	u"""Разделяет предложение на слова, удаляет стоп-слова, знаки препинания и цифры"""
	clear_string_translation = str.maketrans('', '', string.digits + R"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""")
	clear_string = sentece.translate(clear_string_translation)
	LOG.write( "CLEARED", clear_string )
	words = nltk.word_tokenize( clear_string )
	LOG.write( "TOKENIZED", str( words ) )
	words = normalize_words( words )
	LOG.write( "NORMALIZED", str( words ) )
	return [w for w in words if w not in stopwords.words('russian')]

