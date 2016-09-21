import corpus
import utils
import morpho_utils as mu
#import nltk

#nltk.download()

class SentimetalMarker:
	def __init__(self, data_path, corpuses):
		self.corpuses = []
		for corp in corpuses:
			self.corpuses.append( utils.try_load_corpus( corp, data_path ) )

	def mark_sentece(self, sentece):
		u"""Оценивает предложение"""
		words = mu.split_sentece( sentece )
		raitings = []
		for corpus in self.corpuses:
			raitings.append( self.__calculate_corpus_raiting( words, corpus ) )
		return raitings

	def __calculate_corpus_raiting(self, words, corpus):
		u"""Вычисляет оценки предложения по корпусу"""
		result = {"positive": 0, "negative": 0}
		for w in words:
			result["positive"] = result["positive"] + corpus.positive_score( w )
			result["negative"] = result["negative"] + corpus.negative_score( w )

		result["positive"] = result["positive"] / len( words )
		result["negative"] = result["negative"] / len( words )

		return result

def main():
	sentece = "!!!Сегодня на удивление хорошая погода, хотя вчера шёл мерзкий дождь!!!!!"
	data_path = "data"
	corpuses = [corpus.WobotCorpus, corpus.WNAffectCorpus, corpus.LinisCorpus]

	marker = SentimetalMarker( data_path, corpuses )
	print( marker.mark_sentece( sentece ) )


if __name__ == "__main__":
	main()