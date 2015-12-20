#!/usr/bin/env python

#TODO: NORMALIZE, UNNORMALIZE

#read csv file
import numpy as np
from sklearn.linear_model.coordinate_descent import ElasticNetCV

positions = {1:'PG.csv', 2:'SG.csv', 3:'SF.csv', 4:'PF.csv', 5:'C.csv'}
#open csv
b = open('models', 'w')
for pos in range(1, 6):
    filename = positions[pos]
    a = open('../data/cleaned/'+filename, 'r')
    #read in csv into lines
    lines = []
    counter = 0
    for line in a:
        print counter
        counter += 1
        line = line.split(',')
        if len(line) < 2:
            continue
        for i in range(0, len(line) - 1):
            line[i] = line[i].strip()
            line[i] = float(line[i])
        lines.append(line)

    #conver lines to numpy array
    num_data = len(lines)
    num_features = len(lines[0]) - 2

    X = np.zeros((num_data,num_features))
    Y = np.zeros((num_data))

    for i in range(num_data):
        for ii in range(num_features):
            X[i][ii] = lines[i][ii]
        Y[i] = lines[i][-2] #last one is name

    
    #create an instance of elasticnet
    net = ElasticNetCV(alphas=[0.01, 0.05, 0.1], eps=2e-3,
                       l1_ratio=[0.5, 0.7, 1], cv=3, normalize=True)
    
    #create a model based on our data
    fit = net.fit(X, Y)
    for i in net.coef_:
        b.write(str(i) + ",")
    b.write('\n')

    #get the residuals
    resid = X.dot(net.coef_) - Y
    c = open("resid"+filename,'w')
    for i in range(len(resid)):
        c.write(lines[i][-1].strip()+","+str(resid[i])+'\n')
    
    print sum(resid)
        




    
