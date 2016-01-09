import json
import os, sys, re, operator
import pandas as pd
from pprint import pprint
from collections import Counter
import numpy as np
from datetime import datetime
import jieba
from collections import Counter


#convert json objects in statuses to python objects
root = '/Users/Chris/Downloads/weibo/comments/'
total_comments = []
for path, subdirs, files in os.walk(root):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(path, file)
            with open(file_path) as f:
                data = json.load(f)
                #pprint(data)

                #only select the features which are useful for our analysis
                comment = data['text']
                total_comments.append(comment)
                #pprint(data)

#convert data into pandas dataframe structure
array = np.array(total_comments)

#remove white space, convert to lower letters and remove nonalpha characters
comments = []
for comment in array:
    lower = comment.lower()
    comments.append(''.join([i for i in lower if i.isalpha()]))

#retrieve mentioned Chinese terms associated with each brand from all texts
mk = ['michaelkors', 'mk']
ks = ['katespade', 'ks']
mk_dict = {}
ks_dict = {}
#tokenize text in each weibo post
for sentence in comments:
    #create a counter object to count the occurrence of each term in texts
    c = Counter()
    result = jieba.tokenize(sentence)
    #create a list to store tokenized terms and their frequencies
    word = []
    for tk in result:
        #print "word %s\t\t start: %d \t\t end:%d" % (tk[0], tk[1], tk[2])
        word.append(tk[0])
    #update the counter object with new terms
    c.update(word)

    #find the number of co-occurrences with mk or ks for every token in all texts
    for key in c.keys():
        for word, count in c.most_common(10):
            if any(brand in key for brand in mk):
                mk_dict[word] =  count
            elif any(brand in key for brand in ks):
                ks_dict[word] = count
            else:
                continue

#output the top 10 most frequent co-occurrence word with each brand
sorted_mk = sorted(mk_dict.items(), key=operator.itemgetter(1), reverse=True)
sorted_ks = sorted(ks_dict.items(), key=operator.itemgetter(1), reverse=True)

print sorted_mk[:12]
print '\n'
print sorted_ks[:10]



