import pandas as pd
import numpy
import matplotlib as mp
from matplotlib import pyplot as plt
# ERROR in reading data when there's an empty val 
df = pd.read_csv("pinches_11-2.csv").fillna(0)
time = df['Time(ms)']
# citation: https://stackoverflow.com/questions/24342047/count-consecutive-occurences-of-values-varying-in-length-in-a-numpy-array
    

TF_array = numpy.array(time)
# only care about cap0-cap4 (wrapped around beads)
for i in range(1, 6):
    # use second val as threshold
    threshold = df.iloc[3,i] #could also use .mean()
    og_stringCol = (df.loc[:,'Cap'+str(i-1)]).to_numpy()
    print('****Cap'+str(i-1))
    # val = true if under threshold
    maskOfCol = og_stringCol < threshold -2
    TF_array = numpy.vstack((TF_array, maskOfCol))
    
    # want to find chunks of true for each string
    condition = maskOfCol
    # this finds the size of the true chunks
    print(numpy.diff(numpy.where(numpy.concatenate(([condition[0]],
                                     condition[:-1] != condition[1:],
                                     [True])))
                                     [0])[::2])
    # this finds the indexes of switch T/F
    whereArr = numpy.where(numpy.concatenate(([condition[0]],
                                     condition[:-1] != condition[1:],
                                     [True])))[0]
    # had to take out last val since it was OOB
    whereArr = whereArr[:-1]
    # these are the chunks of time of true (printed just to see)
    print(TF_array[:,whereArr])
numpy.savetxt('TF_array.csv',TF_array,fmt="%d", delimiter=',')