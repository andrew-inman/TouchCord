import serial
import time
import csv
import multiprocessing
import pandas as pd
import numpy as np
from gestureFunctions import *
from BlitManager import *
from sys import stdout
from animateBeads import *

# Read serial data from the Arduino.
# Put the read data (one row at a time) into a pipe for the processData
def getData(pipeConnection):
    # Set up arduino
    arduinoSerialObject = serial.Serial(port = 'COM11', baudrate = 9600, timeout = 1)
    
    while True:
        try:
            line = arduinoSerialObject.readline().decode()
            line = line.strip()
            line = line[0:-1]
            lineList = line.split(',')
            # Put in the pipe
            pipeConnection.send(lineList)

        except:
            # If the Arduino has been disconnected, the try block will error.
            arduinoSerialObject.close()

            # Send the END signal
            pipeConnection.send("END")
            pipeConnection.close() # Close the communication
            break


def processData(pipeConnection, fileName):
    dataArray = []
    numpyArray = []
    headers = []
    columns = 0

    # Data processing parameters:
    timeForBaseline = 5000 # Milliseconds from beginning of program to average over to get baselines
    baselines = [] # Baseline values for each capacitor
    baselinesSet = False
    numpyArrayStarted = False
    currentTime = 0 # Timestamp of current datapoint
    touchedState = []
    twistState = False
    grabState = False

    prevGestureState = {
        "touchState": [False, False, False, False, False, False, False, False, False],
        "slide": 0,
        "twist": False,
        "grab": False
    }

    beadCount = 9
    prev_slide_avg = -1
    inc_slide = 0

    # Initialize Display:
    window = createWindow()
    canvas = createCanvas(window)
    
    # fig, ax = plt.subplots()
    # (rects,) = ax.bar(range(beadCount), [5,5,5,5,5,5,5,5,5], animated = True)
    # plt.show(block=False)
    while True:
        newData = pipeConnection.recv()
        if newData == "END" or len(newData) < columns:
            # If the newData is less than the length of the rest of the data, it means the device was unplugged part way through reading the capacitors
            print("Unplugged")

            with open(fileName + '.csv', 'w', newline = '') as f:
                # create the csv writer
                writer = csv.writer(f)

                # write a row to the csv file
                writer.writerows(dataArray[1:])
                break

        else:
            dataArray.append(newData) # Keep this. It is what the csv writer uses.

            # The Pandas tail function could be useful
            #print("inside else")

            if headers: # Only do the following after the headers row has been read
                # Make/add to numeric numpy array
                numericData = [int(x) for x in newData]
                columns = len(numericData)
                numericData = np.array(numericData)
                numericData = np.reshape(numericData, (1, columns))
                if not numpyArrayStarted: # If it is empty (not made yet)
                    numpyArray = numericData
                    numpyArrayStarted = True
                else:
                    numpyArray = np.append(numpyArray, numericData, axis = 0)
                ####################################################
                ### Data processing code goes below this line. ###
                # This will run once for every sensor readout (of all capacitors)
                
                # Get current time:
                currentTime = int(newData[0])

                # Get initial baselines:
                if currentTime >= timeForBaseline and not baselinesSet: # If baselines have not been set yet
                    baselines = np.mean(numpyArray, axis = 0)
                        # Do dataArray[1:] to exclude headers
                    baselinesSet = True
                    print("Ready")

                
                if baselinesSet:
                    # Check for pinches:
                    touchedState = pinchDetect(numpyArray, baselines, beadCount)

                    # Check for grabs:
                    grabState = grab(numpyArray, baselines, beadCount)

                    # Check for slides:
                    slideState = slideDetect(numpyArray, baselines, beadCount, window = 20, beadsPerSlide = 4, compliance = 0.6)

                    # Check for twists:
                    twistState = twistDetect(numpyArray, baselines, twistWindow = 20)

                    gestureState = {
                        "touchState": touchedState,
                        "slide": slideState,
                        "twist": twistState,
                        "grab": grabState
                    }

                    #if gestureState != prevGestureState:
                    drawBeads(window, canvas, gestureState)
                    time.sleep(0.01)
                    #    prevGestureState = gestureState
                    
                    
                    # Uncomment for command-line display
                    # print("\r" + str(touchedState) + " Grabbed: " + str(grabState) + " Slide: " + str(slideState) + " Twist: " + str(twistState), end = "")
                    # stdout.flush()
                    # stdout.write("\n")

                    # reset the background back in the canvas state, screen unchanged
                    # fig.canvas.restore_region(bg)
                    # update the artist, neither the canvas state nor the screen have changed
                    # for i in range(len(rects)):
                    #     if (touchedState[i]==True):
                    #         rects[i].set_height(50)
                    #     else:
                    #         rects[i].set_height(5)
                    # ax.draw_artist(rects)
                    # # copy the image to the GUI state, but screen might not be changed yet
                    # fig.canvas.blit(fig.bbox)
                    # # flush any pending GUI events, re-painting the screen if needed
                    # fig.canvas.flush_events()
                    # # you can put a pause in if you want to slow things down
                    # # plt.pause(.1)
     

            # Establish headers
            if newData[0] == 'Time(ms)': # Check that newData is the headers row
                headers = newData



            


if __name__ == "__main__": # This is the main process.

    # Read in the first line of the arduino input, including the column headers:
    #line = arduino.readline().decode()
    #line = line.strip()
    #rawDataList = [line.split(',')] # This is the global "buffer" holding the data
    #print(rawDataList)

    print("Enter filename: ")
    fileName = input()

    # Create pipe to communicate between processes:
    connection_getData, connection_processData = multiprocessing.Pipe()

    # Create processes:
    process_getData = multiprocessing.Process(target=getData, args=(connection_getData,))
    process_processData = multiprocessing.Process(target=processData, args=(connection_processData,fileName))
    # Start processes:
    process_getData.start()
    process_processData.start()

    # Wait for processes to end:
    process_processData.join() # This one should terminate first because getData requests user input
    process_getData.join()
