import inspect
import sys
import numpy as np 
from numpy import transpose 
import matplotlib.pyplot as plt



#Global vars to hold state's
estimated_ghost_position = [[0,0]]
estimated_errors = [2*np.identity(2)]


def _raise_not_defined():
    print "Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)



def kf_time_update(A, X_prev, B, U, P_prev, Q):
    predicted_x = A*X_prev + B*U 
    predicted_p = A*P_prev*transpose(A) + Q

    return (predicted_x, predicted_p)



def kf_measurement_update(H, P, X, R, z):
    kalman_gain = P*transpose(H)/(H*P*transpose(H) + R)
    x_updated = X + kalman_gain*(z - H*X)
    p_updated = (np.identity(2) - kalman_gain*H)*P 

    return (x_updated, p_updated)


'''
Kalman 2D
'''
def kalman2d(data):
    print "updated"
    estimated = []
    A = np.identity(2)
    B = np.identity(2)
    H = np.identity(2)
    Q = np.matrix([[0.0001, 0.00002], [ 0.00002,0.0001]])
    R = np.matrix([[0.01, 0.005], [0.005, 0.02]])

    lambda_scaling = 1

    prev_P = lambda_scaling * np.identity(2)
    X = transpose(np.matrix([0, 0])) # 0,0 is first position assumed
    estimated.append(X)
    prev_counter = 0
    for d in data:
        U = transpose(np.matrix([d[0], d[1]]))
        z = transpose(np.matrix([d[2], d[3]]))
        x = estimated[prev_counter]
        P = prev_P
        (x_time_update, p_time_update) = kf_time_update(A, x, B, U, P, Q)
        (x_updated, p_updated) = kf_measurement_update(H, p_time_update, x_time_update, R, z)
        estimated.append(x_updated)
        prev_P = p_updated
        prev_counter += 1

    return estimated

'''
Plotting
'''
def plot(data, output):

    observed_x = []
    observed_y = []
    for d in data:
        observed_x.append(d[2])
        observed_y.append(d[3])

    estimated_x = []
    estimated_y = []
    for o in output:
        estimated_x.append(float(o[0]))
        estimated_y.append(float(o[1]))
    
    d1 = plt.plot(observed_x, observed_y, 'o')
    l1 = plt.plot(observed_x, observed_y, label="Observations")
    l2 = plt.plot(estimated_x, estimated_y, label="Estimated Position")
    d2 = plt.plot(estimated_x,estimated_y, 'o')
    plt.setp(d1, color='Blue')
    plt.setp(l1, color='Blue')
    plt.setp(l2, color='Red')
    plt.setp(d2, color='Red')

    plt.legend()
    plt.show()
    
    return

'''
Kalman 2D 
'''

def kalman2d_shoot(ux, uy, ox, oy, reset=False):
    global estimated_ghost_position
    global estimated_errors

    lambda_scaling = 2

    if reset == True:
        estimated_ghost_position = [[0,0]]
        estimated_errors = [lambda_scaling*np.identity(2)]

    A = np.identity(2)
    B = np.identity(2)
    H = np.identity(2)
    Q = np.matrix([[0.0001, 0.00002], [ 0.00002,0.0001]])    
    R = np.matrix([[0.01, 0.05], [0.05, 0.02]])
    z = transpose([ox, oy])
    u = transpose([ux, uy])
    
    (x_time_update, p_time_update) = kf_time_update(A, estimated_ghost_position.pop(), B, u, estimated_errors.pop(), Q)

    (x_updated, p_updated) = kf_measurement_update(H, p_time_update, x_time_update, R, z)

    if p_updated.item(0) < .0015 and p_updated.item(2) < 0.014:
        return ((x_updated.item(0), x_updated.item(1), True))
    
    estimated_ghost_position.append(x_updated)
    estimated_errors.append(p_updated)

    return ((x_updated.item(0), x_updated.item(1), False))

    

'''
Kalman 2D 
'''
def kalman2d_adv_shoot(ux, uy, ox, oy, reset=False):
    decision = (0, 0, False)
    # Your code starts here 
    # Your code ends here 
    _raise_not_defined()
    return decision

