import GetOldTweets3 as got
import csv
import operator
import sys

#Encoding in utf8 since tweets can contain characters other than ASCII
csv_file = open('tweets.csv', 'w', newline='', encoding='utf8')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['username', 'date', 'text', 'number of likes', 'number of retweets', 'number of discussions'])

tweetCriteria = got.manager.TweetCriteria().setQuerySearch('request for startup').setSince(sys.argv[1]).setUntil(sys.argv[2]).setMaxTweets(int(sys.argv[3]))
#Setting a tweet searching criteria for finding tweets containing 'requests for startup' between the dates user entered in the amount of wanted
#The more amount specified the more time needed to find tweets, may take unexpected length of time if the amount of tweets are too big 

tweets = got.manager.TweetManager.getTweets(tweetCriteria)
tweetsList = []
for tweet in tweets:
    tweetsList.append([tweet.username, tweet.date, tweet.text, tweet.favorites, tweet.retweets, tweet.replies])

tweetsList.sort(key=operator.itemgetter(4, 3, 5, 1))
#Sorts the tweets in order of (number of retweets)/(number of likes)/(number of discussions)/(date)
tweetsList.reverse()
#To make it in the descending order

#Finishing and writing it to a csv file
for tweet in tweetsList:
    csv_writer.writerow([tweet[0], tweet[1], tweet[2], tweet[3], tweet[4], tweet[5]])
csv_file.close()
