u"""Классы корпусов с оценками слова."""

import os.path
import morpho_utils as mu
import utils

class SentimentalCorpus:
	u'''Базовый класс для унификации интерфейса'''

	def __init__(self, data_path):
		u"""Тут происходит загрузка корпуса"""
		self.data_path = data_path

	def positive_score(word):
		u"""Поиск слова в позитивных словах и возвращение веса"""
		return 0

	def negative_score(word):
		u"""Поиск слова в негативных слова и возвращение веса"""
		return 0

class WobotCorpus(SentimentalCorpus):
	u'''Корпус на основе слов отсюда: https://github.com/Wobot/Sentimental'''

	def __init__(self, data_path):
		super(WobotCorpus, self).__init__( data_path )
		
		file_name = os.path.join( self.data_path, "wobot.data" )
		data = utils.json_content_from_file( file_name )
		
		self.positive = self._normalize( data["positive"] )
		self.negative = self._normalize( data["negative"] )

	def positive_score(self, word):
		return self._mark( word, self.positive )

	def negative_score(self, word):
		return self._mark( word, self.negative )

	def _normalize( self, container ):
		new_container = []
		for words in container:
			new_container.append( mu.normalize_words( words ) )
		return new_container

	def _mark( self, word, container ):
		for i, words_list in enumerate( container ):
			if word in words_list:
				return i + 1

		return 0

class WNAffectCorpus(SentimentalCorpus):
	u'''Корпус на основе слов отсюда: http://lilu.fcim.utm.md/resourcesRoRuWNA.html'''

	def __init__(self, data_path):
		super(WNAffectCorpus, self).__init__( data_path )

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


class LinisCorpus(SentimentalCorpus):
	u'''Корпус на основе слов отсюда: http://linis-crowd.org/'''

	def __init__(self, data_path):
		super(LinisCorpus, self).__init__( data_path )

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