import os 
rod_loc={'Blue':[],'Green':[],'Orange':[],'Red':[],'Yellow':[]}
rod_depth={'Blue':[],'Green':[],'Red':[],'White':[]}
#empty strings for the depth and location are created to input the parsed values into
from read_ifile import read_file
import statistics
dircty='sample_files/'
csv_files=[]
station_dictionary={}
all_files=os.listdir(dircty)
for f in all_files:
	if f.endswith('.csv'):
		csv_files.append(f)
#list of just csv files is created by sorting through all files in directory 
station_dictionary={}
for fn in csv_files:
	fullname=os.path.join(dircty,fn)
	CB_data=fn.split('_')
	loc=CB_data[1]
	depth=CB_data[3]
	data=read_file(fullname,'2017-06-02T15:15:00','2017-06-15T14:00:00')
	rod_loc[loc].extend(data['values'])
	rod_depth[depth].extend(data['values'])
#csvfiles are split, and parsed based off function from part 1. the parsed values are added to the previously created empty dictionaries 
file_output1=open('rod_depth.txt','w')
file_output1.write('{0:.6s}\t{1:.6s}\t{2:.6s}\t{3:.6s}\t{4:.6s}''\n'.format('Color','Mean','Sttdev','Min','Max'))
#file for depth is written and header is added 
for fn in rod_depth:
	color=fn
	mean=statistics.mean(rod_depth[fn])
	sttdev=statistics.stdev(rod_depth[fn])
	Min=min(rod_depth[fn])
	Max=max(rod_depth[fn])
	file_output1.write('{0:.6s}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4:.2f}''\n'.format(color,mean,sttdev,Min,Max))
#statistical opperations for depth are done for each of the keywrods inside the dictionary 
file_output1.close()
file_output2=open('rod_location.txt','w')
file_output2.write('{0:.6s}\t{1:.6s}\t{2:.6s}\t{3:.6s}\t{4:.6s}''\n'.format('Color','Mean','Sttdev','Min','Max'))
for fn in rod_loc:
	color=fn
	mean=statistics.mean(rod_loc[fn])
	sttdev=statistics.stdev(rod_loc[fn])
	Min=min(rod_loc[fn])
	Max=max(rod_loc[fn])
	file_output2.write('{0:.6s}\t{1:.2f}\t{2:.2f}\t{3:.2f}\t{4:.2f}''\n'.format(color,mean,sttdev,Min,Max))
#statistical opperations for location are done for each of the keywrods inside the dictionary 
file_output2.close()