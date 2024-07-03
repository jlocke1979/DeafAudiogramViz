
# Import libraries

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict # for dictionary usage)

### Turn Excel File into a Usable Data frame
# Retrieve current working directory (`cwd`)
cwd = os.getcwd()
#print (cwd)
# Change working directory
path = "C:\\Users\\justi\\Desktop\\Deaf Ed Viz\\python_scripts\\DeafDataViz\\data"
os.chdir(path)
# Assign spreadsheet filename to `file`
file = 'JRL_Data_Format_v2.0.xlsx'
# Load spreadsheet
xl = pd.ExcelFile(file)
# Load a sheet into a DataFrame by name: df
df = xl.parse('data')
# Print basics on dataframe
df.head()
   
### Create Dictionary for Sounds  
# dictionary is required because of Many to 1 relationship of Frequency to Sounds.   
sounds = {}

### Create dictionary for colors to use.  
#To be updated later with better color pallette
#Option for new pallet  Table20 = [(174,199,232)]   
colors_old = {1:'b', 2:'b',3:'b',4:'b',5:'b',6:'r',7:'b',8:'b',9:'b',10:'b',11:'b',12:'b',13:'b',14:'b',15:'b',16:'b',17:'b',18:'b',19:'b',20:'b',21:'b',22:'b',23:'b',24:'m',25:'b',26:'b',27:'b',28:'b',29:'b',30:'b',31:'b',32:'b',33:'b'}
colors = {6:'#1F77B4',9:'#AEC7E8',11:'#FF7F0E',23:'#FFBB78',26:'#2CA02C',29:'#98DF8A',32:'#D62728',33:'#FF9896'}
# switching to Hex as RGB seems to have problems. 
#
#for i in colors:    
#    #print (i)
#    r, g, b = colors[i]    
#    colors[i] = (r / 255., g / 255., b / 255.)    

    ################## COLORS AREN" BEHAVING ###################

# print (colors)

### Color Help
##Source: http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/

#### These are the "Tableau 20" colors as RGB.    
##colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
#             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
#             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
#             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
#             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
## Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
#for i in range(len(colors)):    
#    r, g, b = colors[i]    
#    colors[i] = (r / 255., g / 255., b / 255.)    
## These ae the same value as RBG,...just Hex format,...only did the first 8
colors_hex = ['#1F77B4', '#AEC7E8','#FF7F0E','#FFBB78',
              '#2CA02C','#98DF8A','#D62728','#FF9896']


### Cycle through DataFrame and Build the Sound Dictionary

for index, row in df.iterrows():
        sound_id= row['Sound_ID']
        if sound_id in sounds and not (sounds[sound_id] is None):   # Checks if Segment already exists, if so then go into this branch....(append additional line segment...leave the rest the same)
            ## Help from this link: https://stackoverflow.com/questions/473099/check-if-a-given-key-already-exists-in-a-dictionary-and-increment-it/7924128
            #current_line_segment = sounds[sound_id]['Segment']
            #additional_line_segment = [[row['StartFreqX1'], row['EndFreqX2']],[row['Power'],row['Power']]]
            #final_line = current_line_segment.append(additional_line_segment)
            sounds[sound_id]['Segment'].append([[row['StartFreqX1'], row['EndFreqX2']],[row['Power'],row['Power']]])
        else:  # If Segment doesn't exist...then store the key info on the first go around
            sounds[row['Sound_ID']] = {'Segment':[[[row['StartFreqX1'], row['EndFreqX2']],[row['Power'],row['Power']]]],'Sound': row['Sound'].encode('utf-8'), 'Manner': row['Manner'],'Formant':row['Formant']}


### Cycle through the Sound Dictionary and populat Matplot Lib Chart 

legend_dict = {}
for s in sounds:
    # store line segment as a variable
    segment = sounds[s]['Segment']
    # store manner as a variable
    manner = sounds[s]['Manner']
    # store formant as a variable
    formant = sounds[s]['Formant']
    #store sound as a variable
    sound = sounds[s]['Sound']

    if manner == "Fricative":  # Isolate this chart to only this specific Manner 
        # get and store color (by crossing referencing sound id to color dictionary) 
        col = colors.get(s,'k')
        legend_dict[sound] = col
        for sub_segment in segment:
            plt.plot(sub_segment[0],sub_segment[1],col,label=sounds[s]['Sound'].decode('utf-8'))

print (legend_dict)
patchList = []
for key in legend_dict:  
    data_key = mpatches.Patch(color=legend_dict[key], label=key.decode('utf-8'))
    patchList.append(data_key)

plt.legend(handles=patchList,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


    ###  Next Step  Update Legend and Colors
            
plt.title("Fricative Audiogram")
plt.ylabel('Power (db)')
plt.xlabel('Frequency (Hz)')
plt.axis([100, 7000, -25, 100])
#plt.figure(figsize=(10, 7.5))    # You typically want your plot to be ~1.33x wider than tall. # Common sizes: (10, 7.5) and (12, 9)    
# plt.legend()
## Remove the plot frame lines. They are unnecessary chartjunk.    
#ax = plt.subplot(111)    
#ax.spines["top"].set_visible(False)    
#ax.spines["bottom"].set_visible(False)    
#ax.spines["right"].set_visible(False)    
#ax.spines["left"].set_visible(False)    
## Ensure that the axis ticks only show up on the bottom and left of the plot.    
## Ticks on the right and top of the plot are generally unnecessary chartjunk.    
#ax.get_xaxis().tick_bottom()    
#ax.get_yaxis().tick_left()    
# # Always include your data source(s) and copyright notice! And for your    
#plt.text(1966, -8, "Data source: <INSERT TEXT>", fontsize=10)     
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()



###########################################   #Appendix n Use this for Reference when Building ##############################################################################################################################

#iterate through DF V1 
#for index, row in df.iterrows():
 #   print ([row['StartFreqX1'], row['StartPowerY1']])


# Chart version1.0
#plt.plot([1500, 2000], [37, 37],'r-',[4000, 5000], [37, 37],'r-')
#plt.ylabel('power (db)')
#plt.xlabel('frequency (hz)')
#plt.axis([100, 6000, -25, 100])
#plt.title("fricative")
#plt.show()

#### Chart Version 2
#### iterate through Dataframe
#color_dictionary = {}
#for index, row in df.iterrows():
#    if row['Manner']== 'Fricative':
#        #print ([row['StartFreqX1'], row['StartPowerY1']])
#        color_dictionary[row['Sound']] = 'red' 
#        plt.plot([row['StartFreqX1'], row['EndFreqX2']], [row['Power'], row['Power']],label=row['Sound'])
#plt.ylabel('Power (db)')
#plt.xlabel('Frequency (Hz)')
#plt.axis([100, 8000, -25, 100])
#plt.legend(loc='right')
#plt.show()

 # Chart Version 3 - THIS SEEMS LIKE IT HAS POTENTIAL FOR FINAL SOLUTION....NEED TO UPDATE USING DF.  Task = Take V2 (which iterates through DF and use it to build up the segments dictionary.  
# (also probably def a function)
# Also need to find a way to chart y axis (power).  current method uses 1 & 2 for vertical axis.  Probaby can't use power as the index in dictionary


#  Source: https://stackoverflow.com/questions/12290983/how-to-plot-interrupted-horizontal-lines-segments-in-matplotlib-in-a-cheap-wa

#segments = {1: [(0, 500),
#                (915, 1000)],
#            2: [(0, 250),
#                (500, 1000)]}

#colors = {1: 'b', 2: 'r'}

#for y in segments:
#    print (y)
#    col = colors.get(y, 'k')
#    for seg in segments[y]:
#        print (seg)
#        plt.plot(seg, [y, y], color=col)

#plt.ylabel('power (db)')
#plt.xlabel('frequency (hz)')
##plt.axis([100, 6000, -25, 100])
#plt.legend(loc='right')
#plt.show()


####  subplots REference

# fig, axs = plt.subplots(2, 2, figsize=(5, 5))


##  Help with getting single Legend entry (even thought I'm graphing 2-4 lines)
#https://stackoverflow.com/questions/39500265/manually-add-legend-items-python-matplotli
#
#import matplotlib.patches as mpatches
#import matplotlib.pyplot as plt

#red_patch = mpatches.Patch(color='red', label='The red data')
#plt.legend(handles=[red_patch])

#plt.show()


