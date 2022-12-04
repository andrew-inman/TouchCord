
import pandas as pd
import numpy as np
import matplotlib as mp
from matplotlib import pyplot as plt

def smooth (data, window):
    cols = data.shape[1]
    output = []
    convolutionWindow = np.ones(window) / window
    for c in range(cols):
        thisColSmoothed = np.convolve(convolutionWindow, data[:, c], mode = 'same')
        output.append(thisColSmoothed)
    return np.array(output).T

def twistDetect (data, baselines, twistWindow = 10, twistThreads = [10, 11, 12], verbose = False):
        # twistThreads is the capacitor channel (number on the MPR121) + 1
    # Hyperparameters:
    smoothingWindow = 3 # How many samples for the moving average
    twistThreshold = 0.4 # Threshold RMSSD required for twist detection
    movingBaselineWindow = 6 # How many samples for the moving baseline
        # Working combinations:
            # In general, the closer the movingBaselineWindow to the smoothingWindow, the lower the difference (smoothedData - movingBaseline) would be (at the extreme, having these equal would reduce every point to 0 (because subtracting the same value)). This is why a larger threshold can be used with a larger movingBaselineWindow
            # smootingWindow = 3, twistThreshold = 0.7, movingBaselineWindow = 5
            # smootingWindow = 3, twistThreshold = 0.9, movingBaselineWindow = 6
    
    
    window = data[-1*twistWindow:, twistThreads]
    baseline = baselines[twistThreads] # 1 by 3 numpy array
    amplitudes = window - baseline # Difference between each channel and its baseline (3 column numpy array)
    amplitudeDifferences = np.array([
        amplitudes[:,0] - amplitudes[:,1],
        amplitudes[:,1] - amplitudes[:,2],
        amplitudes[:,0] - amplitudes[:,2]
        ]).T
    smoothedAmplitudeDifferences = smooth(amplitudeDifferences, window = smoothingWindow)
    #movingBaseline = np.average(amplitudeDifferences)
    movingBaseline = smooth(amplitudeDifferences, window = movingBaselineWindow) # Smooth over a large window in order to get a moving baseline for the amplitude differences. This will help to distinguish between twists and static grabs.

    squares = np.square(smoothedAmplitudeDifferences - movingBaseline)
    sumOfSquares = np.sum(squares, axis=0)
    meanOfSquares = sumOfSquares / twistWindow # Divide sum of squares by number of elements
    rootMeanSquare = meanOfSquares ** (1/2)
    #print(rootMeanSquare)
    if verbose:
        print(rootMeanSquare)
        #plt.plot(data[(-1*twistWindow):,0], smoothedAmplitudeDifferences)
        #plt.plot(data[(-1*twistWindow):,0], movingBaseline)
        plt.plot(data[(-1*twistWindow):,0], smoothedAmplitudeDifferences - movingBaseline)
        plt.show()

    if np.average(rootMeanSquare) > twistThreshold:
        return True
    else:
        return False
        
        
def slideDet(data, prev_slide_avg, inc_slide, baselines, beadCount):
    data = pinchDetect(data, baselines, beadCount)
    if (inc_slide == 0):
        prev_slide_avg = -1
    x = np.where(data==True)
    for val in x:
        true_idx = np.array(val)
    if np.size(true_idx):
        true_idx = np.amax(true_idx) + 1 #bc 0 idx
        avg = true_idx*9 / 9
        # check to see if increasing from last
        if avg == 0:
            return
        if avg >= prev_slide_avg:
            inc_slide += 1
            prev_slide_avg = avg
            return inc_slide
        else: # decreasing so start new window
            inc_slide = 0
            prev_slide_avg = -1
            return inc_slide
    return inc_slide



def pinchDetect(data, baseline, beadCount = 5):
    touchedState = data[-1, 1:beadCount + 1] < (baseline[1:beadCount + 1] - 2)
    return touchedState

def grab(data, baseline, beadCount =5):
    #get true false array created in pinch
    tf_array = pinchDetect(data, baseline, beadCount)
    search_val = [True, True, True] #search for atleast 3 beads being touched
    #print(tf_array[0])
    for i in range(len(tf_array)-3):
        if ((tf_array[i] and tf_array[i+1] and tf_array[i+2]) == True):
            return True
    return False

