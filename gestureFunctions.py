
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
        
        
def slideDet(data):
    prev_avg = -1
    inc = 0
    for row in data:
        row = np.asarray(row)
        true_idx = np.where(row)
        #print(true_idx)
        if np.size(true_idx):
            true_idx = np.amax(true_idx) + 1 #bc 0 idx
            avg = np.sum(true_idx) / 9
            #print(avg)
            # check to see if increasing from last
            if avg >= prev_avg:
                inc += 1
                slide = True
                prev_avg = avg
            else: # decreasing so start new window
                slide = False
                inc = 0
                prev_avg = -1
        if inc >= 5: # hit end of window
            slide = True
            #print(inc)
            #print(slide)
            inc = 0
            #return slide
    slide = False
    #print(inc)
    #print(slide)
    return slide  

#testData = np.loadtxt('twistExampleForDevelopment.csv', delimiter = ",")
#testData = np.loadtxt('dev_3twist_3pinch_format.csv', delimiter = ",")

#baselines = np.array([0, 0, 0, 0, 0, 0, 129, 137, 148])
#twistDetect(testData[300:340], baselines, twistWindow = 40)



#### This pinch code (commented out) doesn't run in real time yet. Replaced with pinchDetect()
# def pinch():
#     # ERROR in reading data when there's an empty val 
#     df = pd.read_csv("pinches_11-2.csv").fillna(0)
#     time = df['Time(ms)']
#     # citation: https://stackoverflow.com/questions/24342047/count-consecutive-occurences-of-values-varying-in-length-in-a-numpy-array
        

#     TF_array = np.array(time)
#     # only care about cap0-cap4 (wrapped around beads)
#     for i in range(1, 6):
#         # use second val as threshold
#         threshold = df.iloc[3,i] #could also use .mean()
#         og_stringCol = (df.loc[:,'Cap'+str(i-1)]).to_numpy()
#         print('****Cap'+str(i-1))
#         # val = true if under threshold
#         maskOfCol = og_stringCol < threshold -2
#         TF_array = np.vstack((TF_array, maskOfCol))
        
#         # want to find chunks of true for each string
#         condition = maskOfCol
#         # this finds the size of the true chunks
#         print(np.diff(np.where(np.concatenate(([condition[0]],
#                                         condition[:-1] != condition[1:],
#                                         [True])))
#                                         [0])[::2])
#         # this finds the indexes of switch T/F
#         whereArr = np.where(np.concatenate(([condition[0]],
#                                         condition[:-1] != condition[1:],
#                                         [True])))[0]
#         # had to take out last val since it was OOB
#         whereArr = whereArr[:-1]
#         # these are the chunks of time of true (printed just to see)
#     numpy.savetxt('TF_array.csv',TF_array,fmt="%d", delimiter=',')
#     return(TF_array[:,whereArr])

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


# takes in data, 1d arr of baselines for each bead, and window start value
def slideDetect(data, baselines, w):
    smoothSlide = smooth(data, 3)
    smoothSlide = (np.rint(smoothSlide)).astype(int)
    # FOUR SUCESSIVE STRANDS
    #window = slidedata[-1*5:, [1,2,3,4,5]]
    # transition this to live --> -1*window +3,6,9,12 & window param will be the start of bead1
    bead1 = np.array(smoothSlide[w:w+10, :][:,1])
    bead2 = np.array(smoothSlide[w+3:w+13, :][:,2])
    bead3 = np.array(smoothSlide[w+6:w+16, :][:,3])
    bead4 = np.array(smoothSlide[w+9:w+19, :][:,4])
    bead5 = np.array(smoothSlide[w+12:w+22, :][:,5])

    bead_arr = np.column_stack((bead1,bead2, bead3, bead4, bead5))
    amp = bead_arr - baselines
    amt_below = np.cumsum(amp,axis=0)[-1]
    print(amt_below)
    # can edit this for slide up (pos) or slide down (neg)
    state = amt_below <= -10 # also i originally had this at -15 but missed some
    if len(np.where(state)[0]) >=3: # majority are bc depending on how person is sliding
        return True
    else:
        return False

#slidedata = np.loadtxt('slides_11-14.csv', delimiter = ",", skiprows=1)
#baselines = (np.mean(slidedata, axis = 0, dtype=int))[1:6]
#print(slideDetect(slidedata,baselines, 185))
#print(slideDetect(slidedata,baselines, 127))
#print(slideDetect(slidedata,baselines, 453))
#print(slideDetect(slidedata,baselines, 500))
#print(slideDetect(slidedata,baselines, 5)) #random one
