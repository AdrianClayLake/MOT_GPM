# -*- coding: utf-8 -*-
# title           :validator.py
# description     :Workspace for validating GPR Model
# author          :
# email           :
# date            :09.01.2018
# version         :1
# usage           :
# notes           :
# python_version  :
#==============================================================================


from sklearn.model_selection import cross_validate
from sklearn.metrics import recall_score

scoring = ['precision_macro', 'recall_macro']
clf = svm.SVC(kernel='linear', C=1, random_state=0)
scores = cross_validate(clf, iris.data, iris.target, scoring=scoring,
                        cv=5, return_train_score=False)
sorted(scores.keys())

scores['test_recall_macro']      