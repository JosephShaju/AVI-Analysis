import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import math 
from scipy import signal,fft



def split_video_channels(mirror=False):
 

    file = "filename.avi"
    #gets file to be analyzed
    Bvalues = []
    Gvalues = []
    Rvalues = []
    #count = []
    cap = cv2.VideoCapture(file)
    #cap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
    #count = cap.get(cv2.CAP_PROP_POS_MSEC)
    
    fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('fps = ' + str(fps))
    print('number of frames = ' + str(frameCount))
    duration = 4.0


    print('duration (S) = ' + str(duration))
    seconds = duration%60
    dummylist = []

    #cv2.namedWindow('Video',cv2.WINDOW_NORMAL)
    while True:
        ret_val, frame = cap.read()
 
        if ret_val == True:
            #if mirror:
                #flip the image
             #   frame = cv2.flip(frame, 1)
 
            # split the image into its RGB channels

            height, width, layers = frame.shape
            tot_pix = height*width
            
            # The OpenCV image sequence is Blue(B),Green(G) and Red(R)
            dummylist.append(tot_pix)
            (B, G, R) = cv2.split(frame)
            avg_color_per_row = np.average(R, axis=0)
            avg_colorR = np.average(avg_color_per_row, axis=0)     
            avg_color_per_row = np.average(G, axis=0)
            avg_colorG = np.average(avg_color_per_row, axis=0) 
            avg_color_per_row = np.average(B, axis=0)
            avg_colorB = np.average(avg_color_per_row, axis=0) 
            
            Rvalues.append(avg_colorR)
            Gvalues.append(avg_colorG)
            Bvalues.append(avg_colorB)



        else:
            break
 
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # if 'q' is pressed then quit
            break
    cap.release()
    return (Rvalues,Gvalues,Bvalues,duration,frameCount,dummylist)
    
def write_file(value1,value2,value3,value4):   # writes data values into text files 
    
    file1 = open("fileR.txt",'w+')
    file2 = open("fileG.txt",'w+')
    file3 = open("fileB.txt",'w+')
    file4 = open("fileGR.txt",'w+')
    delete_file(file1,file2,file3,file4)
    for value in value1:
        file1.write(str(value) + "\n")
    for value in value2:
        file2.write(str(value) + "\n")
    for value in value3:
        file3.write(str(value) + "\n")
    for value in value4:
        file4.write(str(value) + "\n")
        
    return (file1,file2,file3,file4)
    
def delete_file(file1,file2,file3,file4):
    file1.seek(0)
    file1.truncate()
    file2.seek(0)
    file2.truncate()
    file3.seek(0)
    file3.truncate()
    file4.seek(0)
    file4.truncate()

def avgGR(value1,value2):# function to get the normalized G/R values and stored in list gr
    gr = []
    val = 0.00
    for i in range(0,len(value1)):
        val = (value2[i])/(value1[i])
        gr.append(val)
    return (gr)

def list_duplicates(seq):
  seen = set()
  seen_add = seen.add
  # adds all elements it doesn't know yet to seen and all other to seen_twice
  seen_twice = set( x for x in seq if x in seen or seen_add(x) )
  # turn the set into a list (as requested)
  return list( seen_twice )



def plot_graph(value1,value2,value3,value4):
    count = []

    time = 0
    
    for i in range(1,4001):#frameCount
        count.append(time)
        time += 1

    #used seaborn to plot the graphs
    sns.lineplot(x = count ,y = value1,color="red", label="trendforRed")
    plt.figure()
    sns.lineplot(x = count,y = value2,color="green", label="trendforGreen")
    plt.figure()
    sns.lineplot(x = count,y = value3,color="blue", label="trendforBlue")
    plt.figure()
    sns.lineplot(x = count,y = value4,color="coral", label="trendforGR")
    plt.figure()

    

    
def main():
    value1,value2,value3,duration,frameCount,dummylist = split_video_channels(mirror=True)
    value4 = avgGR(value1,value2) # normalization
    val_4 = list_duplicates(value4) # remove duplicates in list
    #file1,file2,file3,file4 = write_file(value1,value2,value3,val_4)
    print (len(value1),len(value2),len(value3),len(val_4)) # just for clarification

    plot_graph(value1,value2,value3,val_4)  #plots the graphs
 
if __name__ == '__main__':
    main()
