u"""Основной класс, оценивающий предложение и фабричный метод для его создания"""

import dictionaries
from enum import Enum
import morpho_utils as mu
from debug_log import LOG

class EstimatorResult(Enum):
	negative = -1
	neutral = 0
	positive = 1

class SentimentalEstimator:
	def __init__( self, dictionaries_with_weights, neutral_treshold ):
		u"""dictionaries_with_weights - словарь с двумя ключами "dict", который хранит класс, реализующий
			SentimentalDictionary и "weight", который хранит вес, с которым учитывается словарь
			neutral_treshold - порог, начиная с которого отношение между положительной и отрицательной
			оценкой начинает считаться значимым (чтобы не считать предложений нейтральным)"""
		self.dictionaries = dictionaries_with_weights
		self.neutral_treshold = neutral_treshold

	def process_sentence( self, sentence ):
		u"""Обрабатываем предложение. Возвращает EstimatorResult"""
		LOG.write( "START", sentence )
		words = mu.split_sentece( sentence )

		LOG.write( "SPLITTED", str( words ) )
		total_positive = 0
		total_negative = 0

		for dict in self.dictionaries:
			LOG.write("START DICTIONARY", dict["dict"].__class__.__name__)
			scores = self.__scores_by_dictionary( dict["dict"], words )
			total_positive = total_positive + dict["weight"] * scores["positive"]
			total_negative = total_negative + dict["weight"] * scores["negative"]
			LOG.write("END DICTIONARY", "p: %f, n: %f" % ( scores["positive"], scores["negative"] ) )

		LOG.write( "TOTAL POSITIVE", str( total_positive ) )
		LOG.write( "TOTAL NEGATIVE", str( total_negative ) )

		if total_negative == 0:
			if total_positive > 0:
				return EstimatorResult.positive
			else:
				return EstimatorResult.neutral
		else:
			ratio = total_positive / total_negative
			if ratio > self.neutral_treshold:
				return EstimatorResult.positive
			elif ratio < 1 / self.neutral_treshold:
				return EstimatorResult.negative
			else:
				return EstimatorResult.neutral

	def __scores_by_dictionary( self, dict, words ):
		u"""Вычисляет оценки предложения по словарю"""
		result = {"positive": 0, "negative": 0}

		if len( words ) == 0:
			return result

		for w in words:
			positive_score = dict.positive_score( w )
			negative_score = dict.negative_score( w )
			result["positive"] = result["positive"] + positive_score
			result["negative"] = result["negative"] + negative_score
			LOG.write( w + " RESULT", "p: %d, n: %d" % ( positive_score, negative_score ) )

		result["positive"] = result["positive"] / len( words )
		result["negative"] = result["negative"] / len( words )

		return result

def create_estimator(data_path):
	u"""Создает экземпляр sentimental_estimator с правильными настройками"""

	# Веса словарей получены на основе дифф эволюции по корпусу + эвристических соображений
	dictionaries_with_weights = [
		{ "dict": dictionaries.WobotDictionary( data_path ), "weight": 1.98448263 },
		{ "dict": dictionaries.WNAffectDictionary( data_path ), "weight": 7.59540434 },
		{ "dict": dictionaries.LinisDictionary( data_path ), "weight": 3.71671178 }
	]
	neutral_treshold = 1.21818111

	estimator = SentimentalEstimator( dictionaries_with_weights, neutral_treshold )

	return estimator