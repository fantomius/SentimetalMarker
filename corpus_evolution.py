u"""Дифф эволюция параметров Estimator'а на основе корпуса"""

import scipy as sp
import numpy as np

import dictionaries
import textscorpus as txts
import estimator as se

#Константы
# Столько предложений мы просматриваем за одну итерацию дифф эволюции
CHUNK_SIZE = 300
CORPUS = txts.TextsCorpus( "base/texts.txt" )
DATA_PATH = "data"
DICTIONARIES = [
	dictionaries.WobotDictionary( DATA_PATH ),
	dictionaries.WNAffectDictionary( DATA_PATH ),
	dictionaries.LinisDictionary( DATA_PATH )
]
ITERATION = 0

def MinimizationFunc( x ):
	u"""Миниизационная функция для эволюции"""
	assert len( x ) == 4, "INVALID PARAMS PASSED"

	dictionaries_with_weights = [
		{ "dict": DICTIONARIES[0], "weight": x[0] },
		{ "dict": DICTIONARIES[1], "weight": x[1] },
		{ "dict": DICTIONARIES[2], "weight": x[2] }
	]

	estimator = se.SentimentalEstimator( dictionaries_with_weights, x[3] )

	# Строим сбалансированную выборку
	sentences = np.random.choice( CORPUS.get_positive(), int( CHUNK_SIZE / 3 ), replace=False ).tolist()
	sentences.extend( np.random.choice( CORPUS.get_negative(), int( CHUNK_SIZE / 3 ), replace=False ).tolist() )
	sentences.extend( np.random.choice( CORPUS.get_neutral(), int( CHUNK_SIZE / 3 ), replace=False ).tolist() )

	correct, total, _, _, _ = txts.get_sentences_quality( sentences, estimator )

	quality = ( total - correct ) / total
	global ITERATION
	ITERATION = ITERATION + 1
	print( "ITERATION: " + str( ITERATION ) )
	print( "quality: " + str( quality ) )
	print( "params: " + str( x ) )
	print()

	return quality


EVO_BOUNDS = [(0, 10), (0, 10), (0, 10), (1, 2)]
result = sp.optimize.differential_evolution( MinimizationFunc, EVO_BOUNDS )

print( result.x )
print( result.fun )