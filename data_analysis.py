import json
import os, sys, re, operator
import pandas as pd
from pprint import pprint
from collections import Counter
from nltk.tokenize import word_tokenize
import numpy as np
from datetime import datetime
import jieba
from collections import Counter


#convert json objects in statuses to python objects
root = '/Users/Chris/Downloads/weibo/statuses/'
total_post = []
for path, subdirs, files in os.walk(root):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(path, file)
            with open(file_path) as f:
                data = json.load(f)
                #only select the features which are useful for our analysis
                post = [data['user']['id'], data['user']['screen_name'], data['user']['location'], data['created_at'], data['text']]
                total_post.append(post)
                #pprint(data)

#convert data into pandas dataframe structure
array = np.array(total_post)
df = pd.DataFrame(array, columns=['userid', 'username', 'location', 'datetime', 'text'])
#print df

#remove white space, convert to lower letters and remove nonalpha characters
words = []
for desc in df['text']:
    lower = desc.lower()
    words.append(''.join([i for i in lower if i.isalpha()]))
df['words'] = words

#convert datetime to two new columns, date and hour
date = []
hour = []
for time in df['datetime']:
    date.append(time[4:10])
    hour.append(time[11:13])
df['date'] = date
df['hour'] = hour

#count the number of posts mentioned for each brand as well as the users who mentioned them
mk_count = 0
mk_id = []
ks_count = 0
ks_id = []
non_count = 0
mk = 'michaelkors'
ks = 'katespade'
#df['mention'] = pd.Series()
for word in df['words']:
    if mk in word:
        mk_count += 1
        mk_id.append(df['userid'])
    elif ks in word:
        ks_count += 1
        ks_id.append(df['userid'])
    else:
        non_count += 1

print mk_count, len(np.unique(mk_id))
print '\n'
print ks_count, len(np.unique(ks_id))
print '\n'


#find the top 10 users and locations (as province level in China and nation level worldwide) for total posts.
by_user = df.groupby('datetime').size().order(ascending=False)[:10]
by_location = df.groupby('location').size().order(ascending=False)[:10]

#Find the date that has the highest number of posts mentioning each of the brands
by_date = df.groupby('date').size().order(ascending=False)[0]
#Find the peak hour with the most posts
by_hour = df.groupby('hour').size().order(ascending=False)[0]




