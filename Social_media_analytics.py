"""
15-110 Hw6 - Social Media Analytics Project
Name:
AndrewID:
"""

import hw6_social_tests as test

project = "Social" # don't edit this

### WEEK 1 ###

import pandas as pd
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]

'''
makeDataFrame(filename)
#3 [Check6-1]
Parameters: str
Returns: dataframe
'''
import csv

def makeDataFrame(filename):
    df=pd.read_csv(filename)
    return df

'''
parseName(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseName(fromString):

    # Splitting the string by '(' and taking the first part
    name_part = fromString.split('(')[0].strip()
    #print(name_part)
    # Removing 'From:' and stripping any extra whitespace
    name = name_part.replace('From:', '').strip()
    #print(name)
    return name

'''
parsePosition(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parsePosition(fromString):

    # Step 1: Split the string by '('
    parts = fromString.split('(')
    # Step 2: Select the second part (index 1)
    position_part = parts[1]
    # Step 3: Split the selected part into words
    words = position_part.split()
    # Step 4: Select the first word (index 0)
    position = words[0]
    # Return the extracted position
    return position

'''
parseState(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseState(fromString):
    parts = fromString.split('(')
    state = parts[1].split(')')[0].split('from ')[-1]
    return state
'''
findHashtags(message)
#5 [Check6-1]
Parameters: str
Returns: list of strs
'''
def findHashtags(message):
    hashtags = []
    i = 0
    while i < len(message):
        if message[i] == '#':
            start = i
            end = i + 1
            while end < len(message) and message[end] not in endChars:
                end += 1
            hashtag = message[start:end]
            hashtags.append(hashtag)
            i = end
        else:
            i += 1
    return hashtags

'''
getRegionFromState(stateDf, state)
#6 [Check6-1]
Parameters: dataframe ; str
Returns: str
'''
def getRegionFromState(stateDf, state):
    row = stateDf.loc[stateDf['state'] == state]
    region = row['region'].values[0]
    return region

'''
addColumns(data, stateDf)
#7 [Check6-1]
Parameters: dataframe ; dataframe
Returns: None
'''
def addColumns(data, stateDf):
    # Create empty lists for the new columns
    names = []
    positions = []
    states = []
    regions = []
    hashtags = []

    # Iterate through each row in the dataframe
    for index, row in data.iterrows():
        # Parse name, position, and state from the label column
        name = parseName(row['label'])
        position = parsePosition(row['label'])
        state = parseState(row['label'])
        
        # Get region from state using stateDf
        region = getRegionFromState(stateDf, state)
        
        # Parse hashtags from the text column
        text = row['text']
        hashtag_list = findHashtags(text)
        
        # Append values to respective lists
        names.append(name)
        positions.append(position)
        states.append(state)
        regions.append(region)
        hashtags.append(hashtag_list)

    # Add new columns to the dataframe
    data['name'] = names
    data['position'] = positions
    data['state'] = states
    data['region'] = regions
    data['hashtags'] = hashtags

    # Return None
    return None


### WEEK 2 ###

'''
findSentiment(classifier, message)
#1 [Check6-2]
Parameters: SentimentIntensityAnalyzer ; str
Returns: str
'''
def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']

    if score<-0.1:
        return "negative"
    elif score>0.1:
        return "positive"
    else:
        return "neutral"


'''
addSentimentColumn(data)
#2 [Check6-2]
Parameters: dataframe
Returns: None
'''
def addSentimentColumn(data):
    classifier = SentimentIntensityAnalyzer()
    sentiments=[]
    for index, row in data.iterrows():
        message=row["text"]
        sentiment=findSentiment(classifier, message)
        sentiments.append(sentiment)
    data["sentiment"]=sentiments
    return


'''
getDataCountByState(data, colName, dataToCount)
#3 [Check6-2]
Parameters: dataframe ; str ; str
Returns: dict mapping strs to ints
'''
def getDataCountByState(data, colName, dataToCount):
    # Initialize an empty dictionary to store counts by state
    state_counts = {}

    # Iterate through each row in the data DataFrame using iterrows()
    for index, row in data.iterrows():
        # Check if both colName and dataToCount are empty strings
        if colName == "" and dataToCount == "":
            state = row['state']
            # Increment the count for the state in the dictionary
            if state in state_counts:
                state_counts[state] += 1
            else:
                state_counts[state] = 1
        else:
            # Check if the specified condition is met in the row
            if row[colName] == dataToCount:
                state = row['state']
                # Increment the count for the state in the dictionary
                if state in state_counts:
                    state_counts[state] += 1
                else:
                    state_counts[state] = 1
                    
   
    return state_counts


'''
getDataForRegion(data, colName)
#4 [Check6-2]
Parameters: dataframe ; str
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def getDataForRegion(data, colName):
    # Initialize an empty dictionary to store data for each region
    region_data = {}

    # Iterate through each row in the data DataFrame using iterrows()
    for index, row in data.iterrows():
        region = row['region']
        value = row[colName]

        # If the region is not already in the outer dictionary, add it with an empty inner dictionary
        if region not in region_data:
            region_data[region] = {}

        # If the value is not already in the inner dictionary for the region, add it with a count of 1
        if value not in region_data[region]:
            region_data[region][value] = 1
        else:
        # If the value is already in the inner dictionary, increment the count
            region_data[region][value] += 1

    return region_data
    


'''
getHashtagRates(data)
#5 [Check6-2]
Parameters: dataframe
Returns: dict mapping strs to ints
'''
def getHashtagRates(data):
    hashtag_counts = {}

    # Iterate through each row in the data DataFrame using iterrows()
    for index, row in data.iterrows():
        hashtags_list = row['hashtags']

        # Check if the 'hashtags' column has any entries
        if len(hashtags_list)>0:
            # Iterate through each hashtag in the list
            for hashtag in hashtags_list:
                # Update the count in the dictionary
                # hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
                if hashtag in hashtag_counts:
                    hashtag_counts[hashtag]+=1
                else:
                    hashtag_counts[hashtag]=1

    return hashtag_counts
    


'''
mostCommonHashtags(hashtags, count)
#6 [Check6-2]
Parameters: dict mapping strs to ints ; int
Returns: dict mapping strs to ints
'''
def mostCommonHashtags(hashtags, count):
    most_pop_hash={}
    
    while len(most_pop_hash)<count:
        max_value=0
        max_key=None

        for i in hashtags:
            if i not in most_pop_hash:
                if hashtags[i] > max_value:
                    max_value=hashtags[i]
                    max_key=i
        most_pop_hash[max_key]=max_value

    return most_pop_hash
    


'''
getHashtagSentiment(data, hashtag)
#7 [Check6-2]
Parameters: dataframe ; str
Returns: float
'''
def getHashtagSentiment(data, hashtag):
    lst = []
    for index, row in data.iterrows():
        text = row['text']
        hashtags = findHashtags(text)
        if hashtag in hashtags:
            sentiment = row['sentiment']
            if sentiment == 'positive':
                score = 1
            elif sentiment == 'negative':
                score = -1
            else:
                score = 0
            lst.append(score)
    return sum(lst)/len(lst)
    


### WEEK 3 ###

'''
graphStateCounts(stateCounts, title)
#2 [Hw6]
Parameters: dict mapping strs to ints ; str
Returns: None
'''
def graphStateCounts(stateCounts, title):
    import matplotlib.pyplot as plt
     # Create lists of keys (states) and values (counts)
    states = list(stateCounts.keys())
    counts = list(stateCounts.values())

    # Create a bar chart
    plt.bar(states, counts)

    # Set plot title and labels
    plt.title(title)
    plt.xlabel('States')
    plt.ylabel('Count')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation='vertical')

    # Display the plot
    plt.show()
    return 
    


'''
graphTopNStates(stateCounts, stateFeatureCounts, n, title)
#3 [Hw6]
Parameters: dict mapping strs to ints ; dict mapping strs to ints ; int ; str
Returns: None
'''
def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
     # print(stateFeatureCounts)
    d={}
    for i in stateFeatureCounts:
        d[i]=stateFeatureCounts[i]/stateCounts[i]
    b=mostCommonHashtags(d, n)
    graphStateCounts(b,title)
    
    return


'''
graphRegionComparison(regionDicts, title)
#4 [Hw6]
Parameters: dict mapping strs to (dicts mapping strs to ints) ; str
Returns: None
'''
def graphRegionComparison(regionDicts, title):
    feature_names=[]
    region_names=[]
    region_feature=[]
    for regions in regionDicts:
        region_names.append(regions)
        for features in regionDicts[regions]:
            if features not in feature_names:
                feature_names.append(features)
    for regions in region_names:
        tmp=[]
        for features in feature_names:
            if features in regionDicts[regions]:
                tmp.append(regionDicts[regions][features])
            else:
                tmp.append(0)
        region_feature.append(tmp)
    sideBySideBarPlots(feature_names,region_names,region_feature,title)
    return None
    


'''
graphHashtagSentimentByFrequency(data)
#4 [Hw6]
Parameters: dataframe
Returns: None
'''
def graphHashtagSentimentByFrequency(data):
    dict={}
    a= getHashtagRates(data)
    b= mostCommonHashtags(a, 50)

    hashtags=[]
    ferquencies=[]
    sentiment_scores=[]

    for i in b:
        hashtags.append(i)
        ferquencies.append(b[i])
        sentiment=getHashtagSentiment(data, i)
        sentiment_scores.append(sentiment)

    scatterPlot(ferquencies,sentiment_scores , hashtags,"Hashtag Sentiment ByFrequency") 
    return



#### WEEK 3 PROVIDED CODE ####
"""
Expects 3 lists - one of x labels, one of data labels, and one of data values - and a title.
You can use it to graph any number of datasets side-by-side to compare and contrast.
"""
def sideBySideBarPlots(xLabels, labelList, valueLists, title):
    import matplotlib.pyplot as plt

    w = 0.8 / len(labelList)  # the width of the bars
    xPositions = []
    for dataset in range(len(labelList)):
        xValues = []
        for i in range(len(xLabels)):
            xValues.append(i - 0.4 + w * (dataset + 0.5))
        xPositions.append(xValues)

    for index in range(len(valueLists)):
        plt.bar(xPositions[index], valueLists[index], width=w, label=labelList[index])

    plt.xticks(ticks=list(range(len(xLabels))), labels=xLabels, rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Expects that the y axis will be from -1 to 1. If you want a different y axis, change plt.ylim
"""
def scatterPlot(xValues, yValues, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xValues, yValues)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xValues[i], yValues[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.ylim(-1, 1)

    # a bit of advanced code to draw a line on y=0
    ax.plot([0, 1], [0.5, 0.5], color='black', transform=ax.transAxes)

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