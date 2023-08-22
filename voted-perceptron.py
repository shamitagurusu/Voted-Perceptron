# -*- coding: utf-8 -*-
"""Perceptron.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_N8bE40M4Zj774BYhtWW-unD9JClfCmG
"""

import numpy as np
import pandas as pd

def pandas_reader(fname):
    df = pd.read_csv(fname)
    #df = df.set_index("id")
    return df

def voted_perceptron_train(features, labels, num_epochs):
    num_instances, num_features = features.shape
    weights = np.zeros(num_features)
    weight_list = [weights.copy()]
    labels[labels == 0] = -1
    vote_list = []
    
    for _ in range(num_epochs):
        for i in range(num_instances):
            x_i = features[i]
            y_i = labels[i]
            prediction = np.dot(weights, x_i)
            
            if prediction * y_i <=0:
                weight_list.append(weights)
                vote_list.append(1)
                weights += y_i * x_i
            else:
                vote_list[-1] += 1
    
    return weight_list, vote_list

def voted_perceptron_predict(features, weight_list, vote_list):
    num_instances, num_features = features.shape
    num_votes = len(vote_list)
    predictions = np.zeros(num_instances)
    
    for i in range(num_instances):
        instance_prediction = 0
        for j in range(num_votes):
            weight = weight_list[j]
            instance_prediction += vote_list[j] * np.sign(np.dot(features[i], weight))
        
        predictions[i] = np.sign(instance_prediction)
    
    # Apply sign function to convert predictions to 0 or 1
    predictions = np.where(predictions < 0, 0, 1)
    # print(predictions)
    
    return predictions



def main():
  train = pandas_reader('/content/train.csv')
  test = pandas_reader('/content/test_noans.csv')

  #labels
  train_labels = train["label"].to_numpy()
  train_features = train[list(train.keys())[1:-1]].to_numpy()

  #training
  num_epochs = 3
  weight_list, vote_list = voted_perceptron_train(train_features, train_labels, num_epochs)
  print(weight_list)
  print(vote_list)

  #test feat
  test_features = test.iloc[:, 1:].to_numpy()

  #predictions
  predictions = voted_perceptron_predict(test_features, weight_list, vote_list)
  # print(predictions)

  #write to csv
  test = test.set_index("id")
  test["label"] = predictions

  test_ans = test["label"]
  test_ans.to_csv("test_ans.csv")

if __name__ == "__main__":
  main()