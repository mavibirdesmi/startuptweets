from django.shortcuts import render
from django.http import HttpResponse
import csv 
import operator
import GetOldTweets3 as got

# Create your views here.
def homepage(request):
    return HttpResponse('<h1> Firstly navigate to /tweets to find 100 (default) tweets conatining "request for startup"</h1>')

def home(request):  
    findTweets()
    return HttpResponse('<p> 10 tweets found until 10.07.2020 (more can be find by using startuptweets.py by giving appropriate arguements) \n\
    and can be downloaded through tweets/download and can be displayed by tweets/display (highly recomended to download csv file) </p>')

def printTweets (request):
    response = '<table class = "table table-bordered table-hover table-condensed">\n'
    try:
        file = open('tweets.csv', 'r', encoding= 'utf8')
        reader = csv.reader(file)
        i = 0
        for tweet in reader:
            if i == 0:
                response += '<thead><tr>'
            else:
                response += '<tr>\n'
            for text in tweet:
                k = 1
                if i == 0:
                    response += '<th title="Field #"' + str(k) + '">' + text + '</th>\n'
                else:
                    response += '<td>' + text + '</td>\n'
                k+=1
            if i == 0:
                response += '</tr></thead>\n<tbody>\n'
            i += 1
        response += '</tbody></table>'
        return HttpResponse(response)
    except:
        return HttpResponse('<h1> Please just navigate to /tweets first </h1>')
    
def findTweets ():
    '''Finds tweets containing "request for startup" word series '''
    csv_file = open('tweets.csv', 'w', newline='', encoding='utf8')

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['username', 'date', 'text', 'number of likes', 'number of retweets', 'number of discussions'])

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('request for startup').setSince("2015-05-01").setUntil("2020-07-10").setMaxTweets(10)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    tweetsList = []
    for tweet in tweets:
        tweetsList.append([tweet.username, tweet.date, tweet.text, tweet.favorites, tweet.retweets, tweet.replies])

    tweetsList.sort(key=operator.itemgetter(4, 3, 5, 1))
    tweetsList.reverse()

    for tweet in tweetsList:
        csv_writer.writerow([tweet[0], tweet[1], tweet[2], tweet[3], tweet[4], tweet[5]])
    csv_file.close()

def returnCSV (request):
    '''Returns the data in a .csv file'''
    try:
        csv_file = open('tweets.csv', 'r', encoding='utf8')
        csv_reader = csv.reader(csv_file)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tweetsData.csv"'
        writer = csv.writer(response)
        for row in csv_reader:
            writer.writerow(row)
        return response
    except:
        return HttpResponse('<h1> Please just navigate to /tweets first </h1>')