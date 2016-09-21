u"""Класс для работы с базой размеченных текстов"""

from sentimental_estimator import EstimatorResult

class TextsCorpus:
	u'''Формат файла - строка текста табуляция оценка'''
	def __init__( self, base_file ):
		self.base = []
		f = open( base_file, "r", encoding='utf-8' )
		
		problem_texts = 0

		for line in f:
			if len(line) == 0:
				continue
			try:
				parts = line.split( "\t" )
				score_value = int( parts[1] )
				score_value = max( -1, min( 1, score_value ) )

				self.base.append( {"text": parts[0], "value": EstimatorResult( score_value ) } )
			except:
				# Не удалось спарсить - ничего страшного
				problem_texts = problem_texts + 1

		print( "PROBLEM TEXTS COUNT: " + str( problem_texts ) )

		f.close()

	def get_base( self ):
		return self.base

# Вспомогательные функции
def get_sentences_quality( sentences, estimator ):
	correct = 0
	total = 0
	for sentence in sentences:
		result = estimator.process_sentence( sentence["text"] )
		if result == sentence["value"]:
			correct = correct + 1

		total = total + 1

	return (correct, total)

#main
def main():
	import dictionaries
	import sentimental_estimator as se

	data_path = "data"
	dictionaries_with_weights = [
		{ "dict": dictionaries.WobotDictionary( data_path ), "weight": 1 },
		{ "dict": dictionaries.WNAffectDictionary( data_path ), "weight": 1 },
		{ "dict": dictionaries.LinisDictionary( data_path ), "weight": 1 }
	]
	neutral_treshold = 0.1

	estimator = se.SentimentalEstimator( dictionaries_with_weights, neutral_treshold )
	base = TextsCorpus( "base/texts.txt" )
	print(get_sentences_quality(base.get_base()[0:100], estimator))


if __name__ == "__main__":
	main()