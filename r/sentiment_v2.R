library(plyr)
library(stringr)

score.sentiment = function(sentences, pos.words, neg.words, .progress='none')
{
    require(plyr)
    require(stringr)
     
    # we got a vector of sentences. plyr will handle a list
    # or a vector as an "l" for us
    # we want a simple array ("a") of scores back, so we use 
    # "l" + "a" + "ply" = "laply":
    scores = laply(sentences, function(sentence, pos.words, neg.words) {
         
        # clean up sentence with R's regex-driven global substitute, gsub():
        sentence = gsub('[[:punct:]]', '', sentence)
        sentence = gsub('[[:cntrl:]]', '', sentence)
        sentence = gsub('\\d+', '', sentence)
        # and convert to lower case and ASCII:

  sentence = iconv(sentence, 'UTF-8', 'ASCII')
        sentence = tolower(sentence)
 
        # split into words. str_split is in the stringr package
        word.list = str_split(sentence, '\\s+')
        # sometimes a list() is one level of hierarchy too much
        words = unlist(word.list)


        # compare and match our words to the dictionaries of positive & negative terms
        pos.matches = which(!is.na(match(words, pos.words)))
        neg.matches = which(!is.na(match(words, neg.words)))
	versterkers.matches = match(words, versterkers.words)
	ontkenners.matches = which(!is.na(match(words, ontkenners.words)))
     
	# kijk naar de polek direct voor de positieve maches voor een potentiele ontkenning
	pos.ontkenners_place = pos.matches - 1
	neg.ontkenners_place = neg.matches - 1

	# welke hebben dezelfde positie als de ontkenners ?
	pos.ontkenners = which(pos.ontkenners_place %in% ontkenners.matches)
	neg.ontkenners = which(neg.ontkenners_place %in% ontkenners.matches)

	# tel het aantal matches, en tel de ontkenningen dubbel  
	score = length(pos.matches) + length(neg.ontkenners)*2 - length(neg.matches) - length(pos.ontkenners) *2

 
        return(score)
    }, pos.words, neg.words, .progress=.progress )
 
    scores.df = data.frame(score=scores, text=sentences)
    return(scores.df)
}

sample <- c('not bad', 'really stupid', 'wonderful')

pos.words = scan('z:/doc/datamining/sentiment/positive-words.txt', what='character', comment=';')
neg.words = scan('z:/doc/datamining/sentiment/negative-words.txt', what='character', comment=';')

result = score.sentiment(sample, pos.words, neg.words, .progress='text')
class(result)
result$score
