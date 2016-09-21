u"""Классы словарей с оценками слова."""

import os.path
import morpho_utils as mu
import utils

class SentimentalDictionary:
	u'''Базовый класс для унификации интерфейса'''

	def __init__(self, data_path):
		u"""Тут происходит загрузка словаря"""
		self.data_path = data_path

	def positive_score(word):
		u"""Поиск слова в позитивных словах и возвращение веса"""
		return 0

	def negative_score(word):
		u"""Поиск слова в негативных слова и возвращение веса"""
		return 0

class WobotDictionary(SentimentalDictionary):
	u'''Словарь на основе слов отсюда: https://github.com/Wobot/Sentimental'''

	def __init__(self, data_path):
		super(WobotDictionary, self).__init__( data_path )
		
		file_name = os.path.join( self.data_path, "wobot.data" )
		data = utils.json_content_from_file( file_name )
		
		self.positive = self._normalize( data["positive"] )
		self.negative = self._normalize( data["negative"] )

	def positive_score(self, word):
		return self._get_score( word, self.positive )

	def negative_score(self, word):
		return self._get_score( word, self.negative )

	def _normalize( self, container ):
		new_container = []
		for words in container:
			new_container.append( mu.normalize_words( words ) )
		return new_container

	def _get_score( self, word, container ):
		for i, words_list in enumerate( container ):
			if word in words_list:
				return i + 1

		return 0

class WNAffectDictionary(SentimentalDictionary):
	u'''Словарь на основе слов отсюда: http://lilu.fcim.utm.md/resourcesRoRuWNA.html'''

	def __init__(self, data_path):
		super(WNAffectDictionary, self).__init__( data_path )

		file_name = os.path.join( self.data_path, "affect.data" )
		data = utils.json_content_from_file( file_name )
		
		self.positive = []
		self.negative = []

		self.negative.extend( mu.normalize_words( self._filter_words( data["anger"] ) ) )
		self.negative.extend( mu.normalize_words( self._filter_words( data["disgust"] ) ) )
		self.negative.extend( mu.normalize_words( self._filter_words( data["fear"] ) ) )
		self.negative.extend( mu.normalize_words( self._filter_words( data["sadness"] ) ) )

		self.positive.extend( mu.normalize_words( self._filter_words( data["joy"] ) ) )
		self.positive.extend( mu.normalize_words( self._filter_words( data["surprise"] ) ) )

	def positive_score(self, word):
		if word in self.positive:
			return 1

		return 0

	def negative_score(self, word):
		if word in self.negative:
			return 1

		return 0

	def _filter_words(self, words):
		u"""Убираем составные слова, которые встречаются в этом словаре"""
		result = []
		for word in words:
			if "_" in word:
				continue
			result.append( word )

		return result


class LinisDictionary(SentimentalDictionary):
	u'''Словарь на основе слов отсюда: http://linis-crowd.org/'''

	def __init__(self, data_path):
		super(LinisDictionary, self).__init__( data_path )

		file_name = os.path.join( self.data_path, "linis.data" )
		data = utils.json_content_from_file( file_name )
		
		self.super_positive = []
		self.positive = []
		self.negative = []
		self.super_negative = []

		data_to_array = {
			-2: self.super_negative,
			-1: self.negative,
			0: None,
			1: self.positive,
			2: self.super_positive
		}

		for key in data:
			target_array = data_to_array[data[key]]
			if target_array == None:
				continue

			target_array.append( mu.normalize_word( key ) )

	def positive_score(self, word):
		if word in self.super_positive:
			return 2

		if word in self.positive:
			return 1

		return 0

	def negative_score(self, word):
		if word in self.super_negative:
			return 2

		if word in self.negative:
			return 1

		return 0