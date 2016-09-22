u"""Фабрика для создания sentimental_estimator"""

import dictionaries
import sentimental_estimator as se

def create_estimator(data_path):
	u"""Создает экземпляр sentimental_estimator с правильными настройками"""

	# Веса словарей получены на основе дифф эволюции по корпусу + эвристических соображений
	dictionaries_with_weights = [
		{ "dict": dictionaries.WobotDictionary( data_path ), "weight": 1.98448263 },
		{ "dict": dictionaries.WNAffectDictionary( data_path ), "weight": 7.59540434 },
		{ "dict": dictionaries.LinisDictionary( data_path ), "weight": 3.71671178 }
	]
	neutral_treshold = 1.21818111

	estimator = se.SentimentalEstimator( dictionaries_with_weights, neutral_treshold )

	return estimator