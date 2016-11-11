
# coding: utf-8

# In[48]:

import pandas as pd
import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC #support vector machine classification
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
in_file = ['18','24','55','60','97','177','185']
dfs= []
for i in in_file:    
    elem = pd.read_csv('FullOct2007'+i+'.csv')    
    dfs.append(elem)
    result = pd.concat(dfs)


# In[49]:

labels=['Family & Relationships', 'Entertainment & Music','Society & Culture', 'Computers & Internet']
def data_prepare(file_df,label_list):    
    df = file_df.loc[file_df['maincat'].isin(label_list)][['subject','content','maincat']]
    df = df.replace(np.nan, '', regex=True)    
    df['X'] = df['subject'].map(str) + ' ' +  df["content"].map(str)    
    df['X'].replace(' ', np.nan, inplace=True)    
    df.dropna(subset=['X'], inplace=True)
    initial_y = df['maincat']    
    le = preprocessing.LabelEncoder()    
    le.fit(initial_y)    
    y = le.transform(initial_y)    
    return df.X, y, df
X,y,df = data_prepare(result,labels)


# In[50]:

#split train,test
from sklearn.cross_validation import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(df['X'], y, train_size=.75)


# In[51]:

#Y_train[6]


# In[52]:

from sklearn.feature_extraction.text import CountVectorizer


# In[53]:

from sklearn.feature_extraction.text import TfidfTransformer


# In[54]:

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
text_clf_NB = Pipeline([('vect', CountVectorizer(stop_words= 'english')),('tfidf', TfidfTransformer()),('clf', MultinomialNB()),])


# In[55]:

text_clf_NB = text_clf_NB.fit(X_train, Y_train)


# In[56]:

# NB
predicted_NB = text_clf_NB.predict(X_test)
np.mean(predicted_NB == Y_test)


# In[57]:

#grid search for NB
from sklearn.grid_search import GridSearchCV
parameters = {'vect__ngram_range': [(1, 1), (1, 2)],'tfidf__use_idf': (True, False),'clf__alpha': (1,1e-1,1e-2, 1e-3,1e-4),}


# In[58]:

gs_clf = GridSearchCV(text_clf_NB, parameters, n_jobs=-1,verbose=10, scoring='log_loss')


# In[59]:

gs_clf = gs_clf.fit(X_train, Y_train)


# In[60]:

best_parameters, score, _ = max(gs_clf.grid_scores_, key=lambda x: x[1])
for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, best_parameters[param_name]))


# In[61]:

new_model = gs_clf.best_estimator_


# In[62]:

predicted_gs = new_model.predict(X_test)
np.mean(predicted_gs == Y_test)


# In[66]:

predicted_gs


# In[76]:

Y_test


# In[63]:

from sklearn.ensemble import RandomForestClassifier
rf = Pipeline([('vect', CountVectorizer(stop_words= 'english')),('tfidf', TfidfTransformer()),('clf', RandomForestClassifier()),])
rf= rf.fit(X_train, Y_train)


# In[64]:

predicted_rf = rf.predict(X_test)
np.mean(predicted_rf == Y_test)

