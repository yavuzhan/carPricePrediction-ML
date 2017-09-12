# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 10:21:56 2017

@author: han
"""
# -*- coding: utf-8 -*-
# Price prediction with regression method
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from math import isnan # Nan checker function import statement

# Part 1: Load the data from file
data = pd.read_csv('manipulated_sahibinden.csv')  #  index    year     km     cc  fuel  price
x = data.iloc[:,1:5]
#x1 = data.iloc[:,1] # year
#x2 = data.iloc[:,2] # km
#x3 = data.iloc[:,3] # cc
#x4 = data.iloc[:,4] # fuel
y = data.iloc[:,5] # price

# Part 2: Implement the gradient step calculation for theta
def computeStep(X,y,theta):
# Creation the hypothesis
    hypothesis = X.dot(theta).flatten() # >>> a = np.array([[1,2], [3,4]])  a.flatten() -> array([1, 2, 3, 4])
    return hypothesis

# Part 3: Implement the cost function calculation
def computeCost(X,y,theta):
    error = (computeStep(X,y,theta)-y)**2 # Distance of h(x)(i) and y(i)
    cost = (1.0 / (2 * len(X))) * error.sum()
    return cost

# Part 4: Prepare the data so that the input X has 5 columns: first a column of ones
X = np.empty(shape=(len(x),5)) # Firstly creating an empty matrix
X.fill(1)                      # Then it is filled by 1
X[:,1:5] = x                   # 2nd,3rd,4th,5th columns filled by x
XT = X.transpose()

# Part 5: Apply linear regression with gradient descent
num_iter = 1500
#alpha_line = [[0.1, '-b'], [0.03, '-r'], [0.01, '-g'], [0.003, ':b'], [0.001, ':r'], [0.0003, ':g']]
alpha_line = [[0.0001, ':r'], [0.0003, ':g'],[0.001, '-b'], [0.003, '-r'], [0.01, '-g'], [0.03, ':b'], [0.1, '-r'], [0.3, '-g'], [1, 'b']]
theta = np.array([0,0,0,0,0])
init_cost = computeCost(X,y,theta)  #initial cost
print('The initial cost is %f.' %init_cost)
plt.figure()
plt.ylim(0,20)
plt.xlim(0,10)
final_theta = []
cost_values = []  # Adding a new array for catching the cost values
for alpha, line in alpha_line:
    J_history = []
    theta = np.array([0,0,0,0,0])
    for i in range(num_iter):
        derivative_of_j0 = (computeStep(X,y,theta) - y) # Derivative of J(Theta 0)
        derivative_of_j1 = (computeStep(X,y,theta) - y) * X[:,1] # Derivative of J(Theta 1)
        derivative_of_j2 = (computeStep(X,y,theta) - y) * X[:,2] # Derivative of J(Theta 2)
        derivative_of_j3 = (computeStep(X,y,theta) - y) * X[:,3] # Derivative of J(Theta 3)
        derivative_of_j4 = (computeStep(X,y,theta) - y) * X[:,4] # Derivative of J(Theta 4)
        temp0 = theta[0] - ( alpha * (derivative_of_j0).sum() * (1.0 / len(X)))
        temp1 = theta[1] - ( alpha * (derivative_of_j1).sum() * (1.0 / len(X)))
        temp2 = theta[2] - ( alpha * (derivative_of_j2).sum() * (1.0 / len(X)))
        temp3 = theta[3] - ( alpha * (derivative_of_j3).sum() * (1.0 / len(X)))
        temp4 = theta[4] - ( alpha * (derivative_of_j4).sum() * (1.0 / len(X)))
        theta = [temp0,temp1,temp2,temp3,temp4]
        J_history.append(computeCost(X,y,theta))
    plt.plot(J_history, line, linewidth=3, label='alpha:%5.4f'%alpha)
    print(theta)
    final_theta.append(theta)
    print ('Final cost after %d iterations is %f' %(num_iter, J_history[-1]))
    cost_values.append(J_history[-1])  # Each cost value adding into the array after each iteration is finished

min_cost = min(i for i in cost_values if not isnan(i))
print("min cost is = "+str(min_cost))  # Checking min cost
index_of_min_cost = cost_values.index(min_cost)  # Finding index of min cost

plt.legend(fontsize=12)
plt.show()
# Part 6: Plot the resulting line and make predictions with the best performing theta
plt.figure(1)
best_theta = final_theta[index_of_min_cost]
plt.plot(x,y, '.', color="red")
plt.plot(X[:,1:5],np.dot(X,best_theta),'-', label='Linear regression with gradient descent')
plt.show()

#plt.plot(x1,x2,x3,x4,y, '.', color="blue")
plt.plot(x,y, '.', color="blue")
plt.xlabel('DATAs in 1000s')
plt.ylabel('Price in 1000s')
# If you like, you can see this plot by calling plt.show() at this line. However, in order to be able to plot the estimated lines on top of the same figure in Parts 7 and 9 (that's why an ID (1) is given), it is not be plotted here.)
plt.show()


# Part 7 : Test
print("---------------------------")
print("best theta is" + str(best_theta)+":/n")
y1 = (np.array([1,0.192,-0.085,-0.397,0.5]).dot(best_theta).flatten())
print ('Estimated price for a car of year :2012 ,km:51.000 ,cc:1.0 ,fuel:1 is %f' %y1) # ((y1*18.5)+25.29)
y2 = (np.array([1,-0.030,0.171,0.136,-0.5]).dot(best_theta).flatten())
print ('Estimated price for a car of year :2008 ,km:190000 ,cc:1.8 ,fuel:-1 is %f' %y2) #((y2*18.5)+25.29)


# Part 8: Calculate optimal theta values using normal equation and then compute the corresponding cost value
theta_normal = (np.linalg.pinv(X).dot(y))  # Calculating (Moore-Penrose) pseudo-inverse of X matrix.
print ('Theta parameters obtained by solving the normal equation are  %f,%f,%f,%f and %f.' %(theta_normal[0],theta_normal[1],theta_normal[2],theta_normal[3],theta_normal[4]))
cost_normal = computeCost(X,y,theta_normal) # Computing cost according to theta_normal
print ('Final cost after solving the normal equation is  %f.' %cost_normal)
plt.figure(1)
plt.plot(np.dot(X,theta_normal),'-r', label='Linear regression with normal equation')
plt.plot(np.dot(X,best_theta),'-b', label='Linear regression with gradient descent')
plt.legend(fontsize=12)
plt.show()
