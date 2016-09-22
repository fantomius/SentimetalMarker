u"""Класс для работы с базой размеченных текстов"""

from sentimental_estimator import EstimatorResult

class TextsCorpus:
	u'''Формат файла - строка текста табуляция оценка'''
	def __init__( self, base_file ):
		self.base = []
		self.positive = []
		self.neutral = []
		self.negative = []

		f = open( base_file, "r", encoding='utf-8' )
		
		problem_texts = 0

		scored_array = {
			-1: self.negative,
			0: self.neutral,
			1: self.positive
		}

		for line in f:
			if len(line) == 0:
				continue
			try:
				parts = line.split( "\t" )
				score_value = int( parts[1] )
				score_value = max( -1, min( 1, score_value ) )

				to_add = {"text": parts[0], "value": EstimatorResult( score_value ) }
				scored_array[score_value].append( to_add )
				self.base.append( to_add )
			except:
				# Не удалось спарсить - ничего страшного
				problem_texts = problem_texts + 1

		f.close()

		print( "PROBLEM TEXTS COUNT: " + str( problem_texts ) )
		print( "POSITIVE: " + str( len ( self.positive ) ) )
		print( "NEGATIVE: " + str( len ( self.negative ) ) )
		print( "NEUTRAL: " + str( len ( self.neutral ) ) )

	def get_base( self ):
		return self.base

	def get_positive( self ):
		return self.positive

	def get_neutral( self ):
		return self.neutral

	def get_negative( self ):
		return self.negative

# Вспомогательные функции
def get_sentences_quality( sentences, estimator ):
	correct = 0
	total = 0
	# False positive, negative, neutral
	fpos = 0
	fneg = 0
	fnet = 0
	for sentence in sentences:
		result = estimator.process_sentence( sentence["text"] )
		if result == sentence["value"]:
			correct = correct + 1
		else:
			if result == EstimatorResult.positive:
				fpos = fpos + 1
			elif result == EstimatorResult.neutral:
				fnet = fnet + 1
			else:
				fneg = fneg + 1

		total = total + 1

	return (correct, total, fpos, fnet, fneg)

#main
def main():
	import dictionaries
	import sentimental_estimator as se

	data_path = "data"
	dictionaries_with_weights = [
		{ "dict": dictionaries.WobotDictionary( data_path ), "weight": 4.98448263 },
		{ "dict": dictionaries.WNAffectDictionary( data_path ), "weight": 7.59540434 },
		{ "dict": dictionaries.LinisDictionary( data_path ), "weight": 3.71671178 }
	]
	neutral_treshold = 1.21818111

	estimator = se.SentimentalEstimator( dictionaries_with_weights, neutral_treshold )
	base = TextsCorpus( "base/texts.txt" )
	print(get_sentences_quality(base.get_negative()[0:100], estimator))
	print(get_sentences_quality(base.get_positive()[0:100], estimator))
	print(get_sentences_quality(base.get_neutral()[0:100], estimator))


if __name__ == "__main__":
	main()