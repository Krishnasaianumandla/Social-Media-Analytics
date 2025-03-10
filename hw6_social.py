"""
Social Media Analytics Project
Name:
Roll Number:
"""

import hw6_social_tests as test

project = "Social" # don't edit this

### PART 1 ###

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
def makeDataFrame(filename):
   return pd.read_csv(filename)

'''
parseName(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseName(fromString):
    start=fromString.find("From:")+len("From:")
    fromString=fromString[start:]
    end=fromString.find(" (")
    fromString=fromString[:end].strip()
    return fromString

'''
parsePosition(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parsePosition(fromString):
    start=fromString.find(" (")+len(" (")
    fromString=fromString[start:]
    end=fromString.find(" from")
    fromString=fromString[:end].strip()
    return fromString


'''
parseState(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseState(fromString):
    start=fromString.find(" from ")+len(" from ")
    fromString=fromString[start:]
    end=fromString.find(')")')
    fromString=fromString[:end].strip()
    return fromString


'''
findHashtags(message)
#5 [Check6-1]
Parameters: str
Returns: list of strs
'''
def findHashtags(message):              
    hashtags=[]
    m = message.split("#")
    for x in m[1:len(m)]: 
        string=""
        for y in x:
            if y not in endChars:
                string+=y
            else:
                break
        string="#"+string
        hashtags.append(string)
    return hashtags


'''
getRegionFromState(stateDf, state)
#6 [Check6-1]
Parameters: dataframe ; str
Returns: str
'''
def getRegionFromState(stateDf, state):
    # print(stateDf.loc[stateDf['state'] == state,'region'].values[0])
    return stateDf.loc[stateDf['state'] == state,'region'].values[0]


'''
addColumns(data, stateDf)
#7 [Check6-1]
Parameters: dataframe ; dataframe
Returns: None
'''
def addColumns(data, stateDf):
    names=[]
    positions=[]
    states=[]
    regions=[]
    hashtags=[]
    for index,row in data.iterrows():
        fromString=row['label']
        names.append(parseName(fromString))
        positions.append(parsePosition(fromString))
        states.append(parseState(fromString))
        regions.append(getRegionFromState(stateDf,parseState(fromString)))
        text=row['text']
        hashtags.append(findHashtags(text))
    data['name']=names
    data['position']=positions
    data['state']=states
    data['region']=regions
    data['hashtags']=hashtags
    return None


### PART 2 ###

'''
findSentiment(classifier, message)
#1 [Check6-2]
Parameters: SentimentIntensityAnalyzer ; str
Returns: str
'''
def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']
    if score>0.1:
        return "positive"
    if score<-0.1:
        return "negative"
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
    sentiment=[]
    for index,row in data.iterrows():
        text=row['text']
        sentiment.append(findSentiment(classifier,text))
    data['sentiment']=sentiment
    return None


'''
getDataCountByState(data, colName, dataToCount)
#3 [Check6-2]
Parameters: dataframe ; str ; str
Returns: dict mapping strs to ints
'''
def getDataCountByState(data, colName, dataToCount):
    count={}
    for index,row in data.iterrows():
        if colName=="" and dataToCount=="" or row[colName]==dataToCount:
            if row['state'] not in count:
                 count[row['state']]=0
            count[row['state']]+=1   
    return count
df = makeDataFrame("data/politicaldata.csv")
stateDf = makeDataFrame("data/statemappings.csv")
addColumns(df, stateDf)
addSentimentColumn(df)

'''
getDataForRegion(data, colName)
#4 [Check6-2]
Parameters: dataframe ; str
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def getDataForRegion(data, colName):
    d={}
    for index,row in data.iterrows():
        outer=row['region']
        inner=row[colName]
        if outer not in d:
            d[outer]={}                  
        if inner not in d[outer]:               
            d[outer][inner]=1
        else:
            d[outer][inner]+=1
    return d

'''
getHashtagRates(data)
#5 [Check6-2]
Parameters: dataframe
Returns: dict mapping strs to ints
'''
def getHashtagRates(data):
    d={}
    l=[]
    for index,row in data.iterrows():
        for i in row['hashtags']:
            l.append(i)
    for i in l:
        if i not in d:
            d[i]=0
        d[i]+=1
    return d 


'''
mostCommonHashtags(hashtags, count)
#6 [Check6-2]
Parameters: dict mapping strs to ints ; int
Returns: dict mapping strs to ints
'''
def mostCommonHashtags(hashtags, count):
    d={}
    orderedHashtags=sorted(hashtags.items(),key=lambda x:x[1],reverse=True)
    for i in orderedHashtags:
        if count!= len(d):
            d[i[0]]=i[1]
    return d


'''
getHashtagSentiment(data, hashtag)
#7 [Check6-2]
Parameters: dataframe ; str
Returns: float
'''
def getHashtagSentiment(data, hashtag):
    l=[]
    for index,row in data.iterrows():
        if hashtag in row['text']:
            if row['sentiment']=='positive':
                l.append(1)
            elif row['sentiment']=='negative':
                l.append(-1)
            else:
                l.append(0)
    return sum(l)/len(l)


### PART 3 ###

'''
graphStateCounts(stateCounts, title)
#2 [Hw6]
Parameters: dict mapping strs to ints ; str
Returns: None
'''
def graphStateCounts(stateCounts, title):
    import matplotlib.pyplot as plt
    x,y=list(stateCounts.keys()),list(stateCounts.values())
    w=0.75
    for i in range(len(x)):
        plt.bar(x[i],y[i],width=w)
    plt.xticks(ticks=list(range(len(x))),label=x,rotation="vertical")
    plt.title(title)
    plt.xlabel("State")
    plt.ylabel("Count")
    plt.show()
    return


'''
graphTopNStates(stateCounts, stateFeatureCounts, n, title)
#3 [Hw6]
Parameters: dict mapping strs to ints ; dict mapping strs to ints ; int ; str
Returns: None
'''
def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
    feature={}
    for i in stateFeatureCounts:
        feature[i]=(stateFeatureCounts[i]/stateCounts[i])
    topstates=dict(sorted(feature.items(),key=lambda x:x[1],reverse=True)[:n])
    graphStateCounts(topstates,title)
    return


'''
graphRegionComparison(regionDicts, title)
#4 [Hw6]
Parameters: dict mapping strs to (dicts mapping strs to ints) ; str
Returns: None
'''
def graphRegionComparison(regionDicts, title):
    region=[]
    feature=[]
    feature_region=[]
    for i in regionDicts:
        region.append(i)
        dummy=[]
        x=regionDicts[i]
        for j in x:
            dummy.append(x[j])
            if j not in feature:
                feature.append(j)
        feature_region.append(dummy)
    sideBySideBarPlots(feature,region,feature_region,title)
    return


'''
graphHashtagSentimentByFrequency(data)
#4 [Hw6]
Parameters: dataframe
Returns: None
'''
def graphHashtagSentimentByFrequency(data):
    hashtagCounts=getHashtagRates(data)
    topCommonHashtags=mostCommonHashtags(hashtagCounts,50)
    hashtags=[]
    hastagFreq=[]
    sentimentScores=[]
    for tag in topCommonHashtags:
        hashtags.append(tag)
        hastagFreq.append(topCommonHashtags[tag])
        sentimentScores.append(getHashtagSentiment(data,tag))
    scatterPlot(hastagFreq,sentimentScores,hashtags,"Hastag Frequencies VS Sentiment Scores")



#### PART 3 PROVIDED CODE ####
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
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()
    # test.testParseName()
    # test.testParsePosition()
    # test.testParseState()
    # test.testFindHashtags()
    # test.testGetRegionFromState()
    # test.testAddColumns()
    # test.testFindSentiment()
    # test.testAddSentimentColumn()
    # test.testGetDataCountByState(df)
    # test.testGetDataForRegion(df)
    # test.testGetHashtagRates(df)
    # test.testMostCommonHashtags(df)
    # test.testGetHashtagSentiment(df)
    # makeDataFrame("icecream.csv")
    ## Uncomment these for Week 2 ##
    """print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()"""

    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
