# Objective
Build a Spam Classifier using Machine Learning and Elasticsearch.

# Data
1. Obtain a collection of e-mail from http://plg.uwaterloo.ca/~gvcormac/treccorpus07/
2. Use a library (```email``` if you're using Python) to parse e-mail content, then use Elasticsearch to do indexing (or you can write your 
own program to clean the text content to "unigram").
3. Construct a feature matrix.
4. Partition the data into 80% training data set and 20% test data set.

# Manual Spam Features
1. Manually create a list of words that you think are related to spam. For example, "free", "win", "porn", etc.
2. Instead of using your own list, use the words from the given list.
3. The term frequency of these spam words will be the features of the e-mails.
    * You can use a full matrix here since the matrix size won't be too large.
4. Train/test 3 models:
    * Decision tree based
    * Regression based
    * Naive-Bayes
    
# All Unigrams as Features
1. The term frequency of all the words will be the features of the e-mails.
2. A sparse feature matrix is required in this part, otherwise the size will be too large.
3. ```sklearn.feature_extraction.text``` is very helpful here (if you're using Python) to extract text content and statistic info.
4. Train/test the same 3 models and compare the results.