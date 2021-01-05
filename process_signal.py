import csv
import re
import numpy as np
from scipy.interpolate import BSpline
from scipy.signal import find_peaks
from hrvanalysis import get_time_domain_features, plot_poincare

values = []
clip_threshold = 2

def rolling_avg(data, count):
    x = len(data)- count
    i=0
    new_array = []
    
    while i < x:
        temp_array = []
        y = 0
        for z in range(count):
            temp_array.append(data[i+y])
        new_array.append(sum(temp_array)/count)
        i += 1
    return new_array
    

with open('hrm_log.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        rawdata = re.sub('[^0-9-]', '', row[0])
        rawdata = float(rawdata)
        if(rawdata > 4.5):
            rawdata = 4.5
        values.append(rawdata)

    values = rolling_avg(values,5)
  
    file = open('rolling_average.csv', 'w')
    # writing the data into the file 
    with file:     
        write = csv.writer(file)
        for x in values:
            file.write(str(x) + '\n')

    x_axis = np.arange(len(values))
    #cs = CubicSpline(x_axis, values)
    cs = BSpline(x_axis, values, 4)

    upscaled = []
    x = len(values)
    i=0
    while i < x:
        upscaled.append(cs(i))
        upscaled.append(cs(i+0.25))
        upscaled.append(cs(i+0.5))
        upscaled.append(cs(i+0.75))
        i += 1

    file = open('B_spline.csv', 'w')
    with file:     
        write = csv.writer(file)
        i = 0
        for x in upscaled:
            if(x > 4.5):
                x = 4.5
                upscaled[i] = 4.5
            file.write(str(x) + '\n')
            i+=1

    peaks = find_peaks(upscaled, height=clip_threshold, distance=100)
    peaks = peaks[0]
    file = open('peaks.csv', 'w')
    write = csv.writer(file)
    for x in peaks:
        file.write(str(x) + '\n')

    RR_intervals = []
    x = len(peaks)-1
    i=0    
    while i < x:
        RR_intervals.append(peaks[i+1]-peaks[i])
        i+=1

    #filter any extremes
    RR_intervals = [x * 5 for x in RR_intervals if x < 300]

    average_size = sum(RR_intervals)/len(RR_intervals)
    RR_intervals = [x for x in RR_intervals if x > (average_size-(average_size*0.15)) and x < (average_size+(average_size*0.15))]
    
    file = open('RR.csv', 'w')
    write = csv.writer(file)
    for x in RR_intervals:
        file.write(str(x) + '\n')
        
    time_domain_features = get_time_domain_features(RR_intervals)
    print(time_domain_features)

    #plot_poincare(RR_intervals, plot_sd_features=True)
    
    file.close()
