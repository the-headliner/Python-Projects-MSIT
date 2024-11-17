"""
15-110 Hw6 - Language Modeling Project
Name: Laxmikant Vishwakarma
AndrewID:
"""

import hw6_language_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):
    corpus= []
    with open(filename, "r") as file:
        for x in file:
            words = x.split()
            if words:  # Check if the list is not empty
                corpus.append(words)      
    return corpus
'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus):   #Returns Unigrams!
    corpuslen=0
    for i in corpus:
        for j in i:
            corpuslen+=1
    return corpuslen
'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus):   #This corpus is a 2D List
    vocabulary = []       #List initialised to store the ditinct Unigrams in this and this will be returned
    for i in corpus:    #Iterate thru the corpus(2D list) 
        for j in i:     #iterate through the each element inside each element of corpus
            if j not in vocabulary:   #check if that element is already there in vocabulary list.
                vocabulary.append(j)   # If that word is not there append that word in the Vocabulary list
    return vocabulary   #Returns a 1D list

#Sample Output:: 1
# corpus = [ ["hello", "world"],["hello", "world", "again"] ]
# build_vocabulary(corpus) -> ["hello", "world", "again"]

#Sample Output:: 2
# corpus = [ ["hello","and","welcome","to","15-110","."],["we're","happy","to","have","you","."] ]
# build_vocabulary(corpus) -> ["hello", "and", "welcome", "to","15-110", ".", "we're", "happy", "have", "you"]


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):
    Frequency_of_words={}  #Frequency of words needs to be stored in a dictionary as it will contain the word and its count
    for i in corpus:       #For every element in the 2D list ---->[[X]]
        for j in i:        #for every key inside the element ---->[[X[i]]]
            if j in Frequency_of_words:      #if that exists in the dictionary
                Frequency_of_words[j] += 1   #Increment the count od that key word with 1.
            else:
                Frequency_of_words[j] = 1  #Set the count of that key word to 1.
    
    return Frequency_of_words              #Return that dictionary.



'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
''' 
def getStartWords(corpus): #Takes in the corpus as input
    start_words = []       #empty 1D list to store all the start words that would be obtained as output.
    for i in corpus:
        if i[0] not in start_words: #If the element and the first key inside that element is not present in start words 1D list,then append.
            start_words.append(i[0]) #Append happens here
    return start_words   #Returns 1D list

'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):
    start_words_count_dict = {}
    for i in corpus:
        if i[0] in start_words_count_dict:
            start_words_count_dict[i[0]]+=1
        else:
            start_words_count_dict[i[0]]=1
    return start_words_count_dict

    
'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):
    bigram_count={}
    for content in corpus:
        for i in range(len(content)-1):
            curr_word=content[i]
            next_word=content[i+1]

            if curr_word not in bigram_count:
                bigram_count[curr_word]={}

            if next_word not in bigram_count[curr_word]:
                bigram_count[curr_word][next_word] = 1
            else:
                bigram_count[curr_word][next_word] += 1

    return bigram_count

    #print(bigram_count)


### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams):
    probability=1/len(unigrams) #Since every word has a probablity of 1/N , where N is the size oof the Vocabulary.
    UniformProbs= [probability]*len(unigrams) #The notation [probability] * len(unigrams) is using Python's list multiplication.
   
    return UniformProbs


'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    UnigramProbs = []

    # Iterate through the indexes of the unigram list
    for i in unigrams:
        # Check if the unigram is in the dictionary
        if i in unigramCounts:
            # Get the count of the corresponding unigram
            count = unigramCounts[i]
        else:
            # If the unigram is not in the dictionary, set count to 0
            count = 0

        # Calculate the probability and append to the list
        probability = count / totalCount
        UnigramProbs.append(probability)

    return UnigramProbs


'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts):

    bigramProbs = {}
    for prevWord in bigramCounts:
        wordList = []
        probList = []

        for word in bigramCounts[prevWord]:
            wordList.append(word)
            probability = bigramCounts[prevWord][word] / unigramCounts[prevWord]
            probList.append(probability)

        tempDict = {"words": wordList, "probs": probList}
        bigramProbs[prevWord] = tempDict

    return bigramProbs

'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
def getTopWords(count, words, probs, ignoreList):
    
    top_words = {}  # Dictionary to store the top words and their probabilities.

    while len(top_words) < count: 
        max_prob = 0
        max_word = None

        for i in range(len(words)):
            word = list(words)[i]
            prob = list(probs)[i]

            if word not in ignoreList and word not in top_words:
                # Update max_prob and max_word if the current probability is higher
                if prob > max_prob:
                    max_prob = prob
                    max_word = word

        # If a word meeting the criteria is found, add it to the top_words dictionary
        if max_word is not None:
            top_words[max_word] = max_prob

    return top_words

'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''

import random
from random import choices

def generateTextFromUnigrams(count, words, probs):
    cumulative_probs = [0] * len(probs)
    current_sum = 0
    for i in range(len(probs)):
        current_sum += probs[i]
        cumulative_probs[i] = current_sum

  
    generated_text = ""

    i = 0
    while i < count:
        # Use a random number to choose the word based on cumulative probabilities
        random_num = random.random()

        # Find the index where random_num is less than or equal to cumulative_prob
        chosen_index = 0
        cum_prob = 0
        while chosen_index < len(cumulative_probs) and random_num > cumulative_probs[chosen_index]:
            chosen_index += 1

        # Use the chosen index to get the corresponding word
        chosen_word = words[chosen_index]

        generated_text += chosen_word + " "  # Concatenate the chosen word to the generated_text string
        i += 1

    # Remove the trailing space and return the generated text
    return generated_text.rstrip()

'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
import random

def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    text = ""

    for _ in range(count):
        if not text or text.endswith("."):
            # Case 1: Start a new sentence
            new_word = random.choices(startWords, startWordProbs)[0]
        else:
            # Case 2: Continue the sentence based on the last word
            last_word = text.split()[-1]
            if last_word in bigramProbs:
                next_word = random.choices(bigramProbs[last_word]["words"], bigramProbs[last_word]["probs"])[0]
            else:
                # If last_word not found in bigramProbs, choose a random start word
                next_word = random.choices(startWords, startWordProbs)[0]

            new_word = next_word

        text += " " + new_word

    return text.strip()



### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]

'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
import numpy
import matplotlib


def graphTop50Words(corpus):
    # Call the function to get unigrams
    unigrams = buildVocabulary(corpus)
    # Call the function to count unigrams
    unigramCounts = countUnigrams(corpus)
    # Call the function to get the total count of words in the corpus
    totalCount = getCorpusLength(corpus)
    # Call the function to compute unigram probabilities
    probabilities = buildUnigramProbs(unigrams, unigramCounts, totalCount)
    # Get the top 50 words based on probabilities, excluding common words
    top_words = getTopWords(50, unigrams, probabilities, ignore)
    # Call the barPlot function to visualize the top 50 words
    title = "Top 50 Words in Corpus"

    barPlot(top_words,title)

    return
    


'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus):

    a=getStartWords(corpus)
    c=countStartWords(corpus)  
    d=getCorpusLength(a)   
    b=buildUnigramProbs(a, c, d)
    e=getTopWords(50, a, b, ignore)
    barPlot(e,"TOP Start Words")
    return
     


'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):

    bigramCounts = countBigrams(corpus)
    unigramCounts = countUnigrams(corpus)
    bigramProbs = buildBigramProbs(unigramCounts, bigramCounts)
    nextWords = list(bigramProbs.get(word, {}).get("words", []))
    
    nextWordProbs = {}
    for nextWord in nextWords:
        nextWordProbs[nextWord] = bigramProbs[word]["probs"][nextWords.index(nextWord)] 

    topWords = getTopWords(10, nextWords, nextWordProbs.values(), ignore)
    barPlot(topWords, f"Top Next Words for {word}")
    return
       
    
'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
import numpy 
import matplotlib


def setupChartData(corpus1, corpus2, topWordCount):
    unigram_1 = countUnigrams(corpus1)
    unigram_2 = countUnigrams(corpus2)

    unigram_Top_1 = getTopWords(topWordCount, unigram_1.keys(), unigram_1.values(), ignore)
    unigram_Top_2 = getTopWords(topWordCount, unigram_2.keys(), unigram_2.values(), ignore)
    Total_words = list(unigram_Top_1.keys())

    for i in list(unigram_Top_2.keys()):
        if i not in Total_words:
            Total_words.append(i)

    prob1 = []
    for word in Total_words:
        if word in unigram_Top_1:
            prob1.append(unigram_Top_1[word]/getCorpusLength(corpus1))
        else:
            prob1.append(0)

    prob2 = []
    for word1 in Total_words:
        if word1 in unigram_Top_2:
            prob2.append(unigram_Top_2[word1]/getCorpusLength(corpus2))
        else:
            prob2.append(0)

    dict = {"topWords" : Total_words, "corpus1Probs" : prob1, "corpus2Probs" : prob2}
    return dict


'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    #sideBySideBarPlots(xValues, values1, values2, category1, category2, title)
    a=  setupChartData(corpus1, corpus2, numWords)
    sideBySideBarPlots(a["topWords"], a["corpus1Probs"], a["corpus2Probs"], name1, name2, "TopWords SidebySide")
    return

'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    a = setupChartData(corpus1, corpus2, numWords)
    scatterPlot( a["corpus1Probs"], a["corpus2Probs"], a["topWords"], "Top words InScatterplot")
    return

### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.


"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    test.runWeek1()

    ## Uncomment these for Week 2 ##

    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()


    ## Uncomment these for Week 3 ##
    
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()