from dateutil.parser import parse
def read_file(filename,start_date,end_date):
    '''
    input: * filename of csv data file
           * starting date of data to read in
           * ending date of date to read in 
    output: a dictionary with keys 'dates' and 'values'. Dates are python datetime objects
            and values are floats (tempertures)
    '''
    fileobj=open(filename,'rt')
    data={'dates':[], 'values':[]}
    dates=[]
    flag=False
    for i,line in enumerate(fileobj):
        if flag==True:
            words=line.split(',')
            try:
                # catch error then values in list cannont be parsed by dateutil module
                date=parse(words[0])
                # only save data collected between start and end dates
                if date<parse(end_date) and date>parse(start_date):
                    tmpt=float(words[1])
                    data['dates'].append(date)
                    data['values'].append(tmpt)
            except ValueError:
                pass
        elif 'TimeStamp,Temperature' in line:
            # find line when header ends and data begins
            flag=True
    return data