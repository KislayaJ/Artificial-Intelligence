import inspect
import sys
import numpy as np
import math


# Log Array for our Prior probabilities
prior_p = np.zeros(10) 

#Log Array for Conditional Probabilities
conditional_p = np.zeros((10,784))
border_p = np.zeros((10,784))
body_p = np.zeros((10,784))
whitespace_p = np.zeros((10,784)) 

def _raise_not_defined():
    print "Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)

'''
Extract 'basic' features, i.e., whether a pixel is background or
forground (part of the digit) 
'''
def extract_basic_features(digit_data, width, height):
    features=[]
    for row in range(len(digit_data)):
        for col in range(len(digit_data[0])):
            if digit_data[row][col] == 0:
                features.append(False)
            else:
                features.append(True)
    #_raise_not_defined()

    #print "extract basic features completed"
    return features

'''
Extract advanced features that you will come up with 
'''
def extract_advanced_features(digit_data, width, height):
    features=[]
    feature_border=[]
    feature_body=[]
    feature_ws = []
    
    for row in range(len(digit_data)):
        for col in range(len(digit_data[0])):
            if digit_data[row][col] == 2:
                feature_border.append(True)
                feature_body.append(False)
                feature_ws.append(False)
            elif digit_data[row][col] == 1:
                feature_border.append(False)
                feature_body.append(True)
                feature_ws.append(False)
            else:
                feature_ws.append(True)
                feature_border.append(False)
                feature_body.append(False)


    features.append(feature_border)
    features.append(feature_body)
    features.append(feature_ws)

    return features

'''
Extract the final features that you would like to use
'''
def extract_final_features(digit_data, width, height):
    features = []

    basicFt = extract_basic_features(digit_data, width, height)
    advancedFt = extract_advanced_features(digit_data, width, height)

    features.append(basicFt)
    features.append(advancedFt)

    return basicFt




'''
Compupte the parameters including the prior and and all the P(x_i|y). Note
that the features to be used must be computed using the passed in method
feature_extractor, which takes in a single digit data along with the width
and height of the image. For example, the method extract_basic_features
defined above is a function than be passed in as a feature_extractor
implementation.

The percentage parameter controls what percentage of the example data
should be used for training. 
'''

def compute_statistics(data, label, width, height, feature_extractor, percentage=20.0):

    num_tests = int ((percentage/100) * len(label))

    frequencies = np.zeros(10) #Contains the frequencies of all digits

    num_pixels = np.zeros((10,784)) #2D array to store number of pixels of a digit

    k = 0.0001 # Smoothing Parameter

    #############################################################################################
                                # BASIC FEATURE IMPLEMENTATION
    #############################################################################################
    if feature_extractor == extract_basic_features or feature_extractor == extract_final_features: 

        for i in range(num_tests):
            currlabel = label[i]
            frequencies[currlabel]+=1

            features = feature_extractor(data[i], width, height)

            for j in range(len(features)):
                if features[j] == True:
                    num_pixels[currlabel][j]+=1

        for i in range(10): 
            prior_p[i] = float(frequencies[i]/num_tests)

        for i in range(len(num_pixels)):
            for j in range(len(num_pixels[i])):
                numerator = num_pixels[i][j]+k
                denominator = frequencies[i] + 2*k 
                conditional_p[i][j] = numerator/denominator
    #############################################################################################
                                # ADVANCED FEATURE IMPLEMENTATION
    #############################################################################################
    elif feature_extractor == extract_advanced_features:
        borderFt = np.zeros((10,784)) 
        bodyFt = np.zeros((10,784))
        whitespaceFt = np.zeros((10,784)) 

        for i in range(num_tests): 
            currlabel = label[i]
            frequencies[currlabel] += 1
            features = feature_extractor(data[i], width, height)
            feature_border = features[0]
            feature_body = features[1]
            feature_ws = features[2]   

            for j in range(len(feature_border)):
                if feature_border[j]==True:
                    borderFt[currlabel][j] += 1
                if feature_body[j]==True:
                    bodyFt[currlabel][j] += 1
                if feature_ws[j]==True:
                    whitespaceFt[currlabel][j] += 1
        
        for i in range(10):
            prior_p[i] = float (frequencies[i]/num_tests)


        for i in range(len(borderFt)):
            for j in range(len(borderFt[0])):
                numerator = borderFt[i][j] + k
                denominator = frequencies[i] + (2*k)
                border_p[i][j] = numerator/denominator

                numerator_2 = bodyFt[i][j] + k
                denominator_2 = frequencies[i] + (2*k)
                body_p[i][j] = numerator_2/denominator_2

                numerator_3 = whitespaceFt[i][j] + k 
                denominator_3 = frequencies[i] + (2*k)
                whitespace_p[i][j] = numerator_3/denominator_3

    elif feature_extractor == extract_final_features:
        basicFt = np.zeros((10,784))
        borderFt = np.zeros((10,784)) 
        bodyFt = np.zeros((10,784))
        whitespaceFt = np.zeros((10,784))

        for i in range(num_tests): 
            currlabel = label[i]
            frequencies[currlabel] += 1
            features = feature_extractor(data[i], width, height)

            feature_basic = features[0]
            feature_border = features[1]
            feature_body = features[2]
            feature_ws = features[3]

            for j in range(len(feature_basic)):
                if feature_basic[j]==True:
                    basicFt[currlabel][j] +=1
                if feature_border[j]==True:
                    borderFt[currlabel][j]+=1
                if feature_body[j]==True:
                    bodyFt[currlabel][j]+=1
                if feature_ws[j] ==True:
                    whitespaceFt[currlabel][j]+=1

        for i in range(10):
            prior_p[i] = float(frequencies[i]/num_tests)

        for i in range(len(borderFt)):
            for j in range(len(borderFt[0])):
                numerator = basicFt[i][j] + k
                denominator = frequencies[i] + (2*k)
                conditional_p[i][j] = numerator/denominator

                numerator_1 = borderFt[i][j] + k
                denominator_1 = frequencies[i] + (2*k)
                border_p[i][j] = numerator_1/denominator_1

                numerator_2 = bodyFt[i][j] + k
                denominator_2 = frequencies[i] + (2*k)
                body_p[i][j] = numerator_2/denominator_2

                numerator_3 = whitespaceFt[i][j] + k 
                denominator_3 = frequencies[i] + (2*k)
                whitespace_p[i][j] = numerator_3/denominator_3


'''
For the given features for a single digit image, compute the class 
'''
def compute_class(features):
    predicted_prob = float('-inf')
    predicted_ans = -1

    if len(features) == 3:
        borderFt = features[0]
        prob1 = float('-inf')
        bodyFt = features[1]
        prob2 = float('-inf')
        whitespaceFt = features[2]

        for i in range(10):
            prob = math.log(prior_p[i])

            for j in range(len(features[0])):
                if borderFt[j] == True:
                    prob+=math.log(border_p[i][j])
                    prob+=math.log(1 - body_p[i][j])
                    prob+=math.log(1 - whitespace_p[i][j])

                elif bodyFt[j] == True:
                    prob+=math.log(body_p[i][j])
                    prob+=math.log(1 - border_p[i][j])
                    prob+=math.log(1 - whitespace_p[i][j])

                elif whitespaceFt == True:
                    prob+=math.log(whitespace_p[i][j])
                    prob+=math.log(1 - border_p[i][j])
                    prob+=math.log(1 - body_p[i][j])

            if prob>predicted_prob:
                predicted_ans = i
                predicted_prob = prob

    elif len(features) == 4:

        basicFt = features[0]
        borderFt = features[1]
        bodyFt = features[2]
        whitespaceFt = features[3]

        for i in range(10):
            prob = math.log(prior_p[i])
            for j in range(len(features[0])):
                if basicFt[j] == True:
                    prob+=math.log(conditional_p[i][j])
                    prob+=math.log(1 - body_p[i][j])
                    prob+=math.log(1 - whitespace_p[i][j])
                    prob+=math.log(1 - border_p[i][j])

                if borderFt[j] == True:
                    prob+=math.log(border_p[i][j])
                    prob+=math.log(1 - body_p[i][j])
                    prob+=math.log(1 - whitespace_p[i][j])
                    prob+=math.log(1 - conditional_p[i][j])

                elif bodyFt[j] == True:
                    prob+=math.log(body_p[i][j])
                    prob+=math.log(1 - border_p[i][j])
                    prob+=math.log(1 - whitespace_p[i][j])
                    prob+=math.log(1 - conditional_p[i][j])

                elif whitespaceFt == True:
                    prob+=math.log(whitespace_p[i][j])
                    prob+=math.log(1 - border_p[i][j])
                    prob+=math.log(1 - body_p[i][j])
                    prob+=math.log(1 - conditional_p[i][j])

            if prob>predicted_prob:
                predicted_ans = i
                predicted_prob = prob

    else:
        for i in range(10):
            prob = math.log(prior_p[i])
            for j in range(len(features)):
                if features[j] == True:
                    prob += math.log(conditional_p[i][j])
                else:
                    prob += math.log(1 - conditional_p[i][j])
                
            if prob>predicted_prob:
                predicted_ans = i
                predicted_prob = prob

    return predicted_ans

'''
Compute joint probaility for all the classes and make predictions for a list
of data
'''
def classify(data, width, height, feature_extractor):
    predicted=[]

    # Your code starts here 
    # You should remove _raise_not_defined() after you complete your code
    for i in data:
        features = feature_extractor(i,width,height)
        label = compute_class(features)
        predicted.append(label)

    return predicted







        
    
