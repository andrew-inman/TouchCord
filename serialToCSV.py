from tkinter import W
import serial
import time
import csv

arduino = serial.Serial(port = 'COM4', baudrate = 9600, timeout = 1)

i = 0
line = arduino.readline().decode()
line = line.strip()
rawDataList = [line.split(',')]

while True:
    try:
        line = arduino.readline().decode()
        line = line.strip()
        line = line[0:-1]
        lineList = line.split(',')
        rawDataList.append(lineList)
    except:
        print("Unplugged")
        
        arduino.close()
        #print(rawDataList[1:])
        
        print("Enter filename: ")      
        fileName = input()
        with open(fileName + '.csv', 'w', newline = '') as f:
            # create the csv writer
            writer = csv.writer(f)

            # write a row to the csv file
            writer.writerows(rawDataList[1:])
            break