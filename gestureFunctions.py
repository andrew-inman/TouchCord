import numpy as np
from matplotlib import pyplot as plt

def smooth (data, window):
    cols = data.shape[1]
    output = []
    convolutionWindow = np.ones(window) / window
    for c in range(cols):
        thisColSmoothed = np.convolve(convolutionWindow, data[:, c], mode = 'same')
        output.append(thisColSmoothed)
    return np.array(output).T

def twistDetect (data, baselines, twistWindow = 10, twistThreads = [6, 7, 8], verbose = False):
        # twistThreads is the capacitor channel (number on the MPR121) + 1
    # Hyperparameters:
    smoothingWindow = 3 # How many samples for the moving average
    twistThreshold = 0.9 # Threshold RMSSD required for twist detection
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
    movingBaseline = smooth(amplitudeDifferences, window = movingBaselineWindow) # Smooth over a large window in order to get a moving baseline for the amplitude differences. This will help to distinguish between twists and static grabs.

    squares = np.square(smoothedAmplitudeDifferences - movingBaseline)
    sumOfSquares = np.sum(squares, axis=0)
    meanOfSquares = sumOfSquares / twistWindow # Divide sum of squares by number of elements
    rootMeanSquare = meanOfSquares ** (1/2)
    #print(rootMeanSquare)
    if verbose:
        print(rootMeanSquare)
        plt.plot(data[(-1*twistWindow):,0], smoothedAmplitudeDifferences)
        plt.show()

    if np.average(rootMeanSquare) > twistThreshold:
        return True
    else:
        return False
        
    


#testData = np.loadtxt('twistExampleForDevelopment.csv', delimiter = ",")
testData = np.loadtxt('dev_3twist_3pinch_format.csv', delimiter = ",")

baselines = np.array([0, 0, 0, 0, 0, 0, 129, 137, 148])
twistDetect(testData[300:340], baselines, twistWindow = 40)