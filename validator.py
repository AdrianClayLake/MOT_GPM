# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 10:24:49 2018

@author: Adrian
"""

from sklearn.model_selection import cross_validate
from sklearn.metrics import recall_score

scoring = ['precision_macro', 'recall_macro']
clf = svm.SVC(kernel='linear', C=1, random_state=0)
scores = cross_validate(clf, iris.data, iris.target, scoring=scoring,
                        cv=5, return_train_score=False)
sorted(scores.keys())

scores['test_recall_macro']      