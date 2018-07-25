import os
import matplotlib.pyplot as pl
from read_ifile import read_file

blue_loc={'Blue':[],'Green':[],'Red':[],'White':[]}
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
	if CB_data[1]=='Blue':
		blue_loc[depth].extend(data['values'])
    
y=blue_loc['Blue']
y2=blue_loc['Green']
y3=blue_loc['Red']
y4=blue_loc['White']
x=data['dates']

pl.plot_date(x,y,color='blue',markersize=1,label='0 cm', marker='*')
pl.plot_date(x,y2,color='green',markersize=1,label='8 cm', marker='*')
pl.plot_date(x,y3,color='red',markersize=1,label='16 cm', marker='*')
pl.plot_date(x,y4,color='black',markersize=1,label='40 cm', marker='*')
pl.xlabel('Date (YYYY/MM/DD)')
pl.ylabel('Temperature (C)')
pl.legend(title='Depth of Data Loggers',ncol=2)
pl.show()