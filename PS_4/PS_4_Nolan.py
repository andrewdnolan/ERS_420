import os
import numpy as np
import datetime
import matplotlib.pylab as pl
from read_ifile import read_file
import calendar

Blue_data=[]
dircty='sample_files/'
csv_files=[]
all_files=os.listdir(dircty)
#seperates out the all the csv files in the directory
for f in all_files:
	if f.endswith('.csv'):
		csv_files.append(f)
'''
Extracting the data at the Blue depth based on a start and end time to be
used to interpolate from for the model
'''
for fn in csv_files:
	fullname=os.path.join(dircty,fn)
	CB_data=fn.split('_')
	loc=CB_data[1]
	depth=CB_data[3]
	data=read_file(fullname,'2017-06-02T15:15:00','2017-06-15T14:00:00')
	if CB_data[1]=='Yellow'and CB_data[3]=='Blue':
		Blue_data.extend(data['values'])
y1=data['dates']
#converts the datestrings into timestamps so they can be interpolated from
def toTimestamp(d):
	return calendar.timegm(d.timetuple())
d=data['dates']
date_time=[]
for d in data['dates']:
	z=toTimestamp(d)
	date_time.append(z)
#Constants
rho=1100.
heat_cap=4000.
kond=1.1
T_top = 14
T_bot =8

len_model=-5.

time_interval=1864

del_t=100
ncells=251
del_x=len_model/(ncells-1)

D=kond*del_t/(heat_cap*rho*del_x**2)
#creates an empty matrix of zeros which will later be populated with the heat flux equation
A=np.zeros([ncells,ncells])
#creates an evenly spaced vector of the same number of values as the time interval spanning the range of the timestamps
timespan=np.linspace(date_time[0],date_time[-1],time_interval)
'''
creates an evenly spaced vector of 251 cells, the number within the model
ranging from the start temp of 14 to the specified 8 a the bottom
'''
Tmpt=np.linspace(T_top,T_bot,ncells)
#populating the diagonal of the matrix with the heat flux equation
for cell in range(ncells):
    if (cell==ncells-1)or(cell==0):
        A[cell,cell]=1
    else:
        A[cell,cell]=-2*D+1
        A[cell,cell-1]=D
        A[cell,cell+1]=D
x=np.arange(ncells)*del_x
'''
dictionaries for each of the depths of the loggers, sepeate list are created for the model output data
versus the data recorded by the loggers
'''
model_output={'Model8':[],'Model16':[],'Model40':[]}
depth8={'Model8':[],'Green':[]}
depth16={'Model16':[],'White':[]}
depth40={'Model40':[],'Red':[]}

fig1=pl.figure(1)
#model calculations, data is extracted at the corresponding depths as the loggers
for i,time in enumerate(timespan):
	surf_temp=np.interp(time,date_time,Blue_data)
	Tmpt_old=Tmpt.copy()
	Tmpt_old[0]=surf_temp
	Tmpt=np.dot(A,Tmpt_old)
	if x[4]==-.08:
		depth8['Model8'].append(Tmpt[4])
	if x[8]==-.16:
		depth16['Model16'].append(Tmpt[8])
	if x[20]==-.4:
		depth40['Model40'].append(Tmpt[19])
	if i%600==0:
		pl.xlabel('Temperature (C)')
		pl.ylabel('Depth (M)')
		pl.plot(Tmpt,x)
fig1.show()
#fig1.savefig('Model_Output_1.jpg')

dircty='sample_files/'
csv_files=[]
all_files=os.listdir(dircty)
for f in all_files:
	if f.endswith('.csv'):
		csv_files.append(f)
'''
list of just csv files is created by sorting through all files in directory
values for each of the depths are appended to lists to be plotted verus the model output
'''
for fn in csv_files:
	fullname=os.path.join(dircty,fn)
	CB_data=fn.split('_')
	loc=CB_data[1]
	depth=CB_data[3]
	data=read_file(fullname,'2017-06-02T15:15:00','2017-06-15T14:00:00')
	if CB_data[1]=='Yellow'and CB_data[3]=='Green':
		depth8['Green'].extend(data['values'])
	elif CB_data[1]=='Yellow'and CB_data[3]=='White':
		depth16['White'].extend(data['values'])
	elif CB_data[1]=='Yellow'and CB_data[3]=='Red':
		depth40['Red'].extend(data['values'])
#plot format to help create the legend for the sublpots
plot_fmt={'1Green':{'color':'green','depth':'8cm'},
          '2White':{'color':'black','depth':'16cm'},
          '3Red':{'color':'red','depth':'40cm'},
          '1Model8':{'color':'olive','depth':'Model-8cm'},
          '2Model16':{'color':'grey','depth':'Model-16cm'},
          '3Model40':{'color':'maroon','depth':'Model-40cm'}}
x=data['dates']

fig2,(ax1, ax2, ax3)=pl.subplots(3, sharex=True, sharey=True)
#creating each of the individual subplots with the same formatting through a for loop
for color in sorted(plot_fmt):
	if color[1:] in depth8:
		y1=depth8[color[1:]]
		ax1.plot_date(x,y1,color=plot_fmt[color]['color'],markersize=.75,label=plot_fmt[color]['depth'], marker='*')
		ax1.legend(title='8 cm Depth',ncol=2)
	if color[1:] in depth16:
		y2=depth16[color[1:]]
		ax2.plot_date(x,y2,color=plot_fmt[color]['color'],markersize=.75,label=plot_fmt[color]['depth'], marker='*')
		ax2.legend(title='16 cm Depth',ncol=2)
	if color[1:] in depth40:
		y3=depth40[color[1:]]
		ax3.plot_date(x,y3,color=plot_fmt[color]['color'],markersize=.75,label=plot_fmt[color]['depth'], marker='*')
		ax3.legend(title='40 cm Depth',ncol=2)

fig2.subplots_adjust(hspace=0)
pl.xlabel('Date (YYYY/MM/DD)')
pl.ylabel('Temperature (C)')
#centering the y axis label
ax3.yaxis.set_label_coords(-.075,1.5)
pl.legend(title='Depth of Data Loggers',ncol=4,labelspacing=.25)
fig2.show()
#fig2.savefig('Model_vs_Observed_1.jpg')
