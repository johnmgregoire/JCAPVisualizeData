import os.path, numpy
#sample number can be provided as "Sample####_*"  in filename or in header
def smp_dict_generaltxt(path): # can have raw data files with UV-vis or ECHE styles or a fom file with column headings as first line, in which case smp=None
    smp=None
    fn=os.path.split(path)[1]
    if fn.startswith('Sample'):
        s=fn.partition('Sample')[2].partition('_')[0]
        try:
            smp=eval(s)
        except:
            smp=None
    if smp is None:
        smp=getsamplefromheader(path)
#    if smp is None:
#        return None, {}
    
    f=open(path, mode='r')
    lines=f.readlines()
    f.close()
    if lines[0].startswith('%'):
        for count, l in enumerate(lines):
            if l.startswith('%column_headings='):
                chs=l.partition('%column_headings=')[2]
                firstdatalineind=count+1
                break
    elif lines[0][0].isdigit():
        numheadlines=lines[0].rpartition('\t')[2].strip()
        try:
            numheadlines=eval(numheadlines)
        except:
            return None, {}
        chs=lines[numheadlines+1].strip()
        firstdatalineind=numheadlines+2
    elif lines[1][0].isdigit():
        chs=lines[0].strip()
        firstdatalineind=1
    else:
        return None, {}
    
    
    d={}
    z=[]
    column_headings=chs.split('\t')
    column_headings=[s.strip() for s in column_headings]
    z=[map(float, l.split('\t')) for l in lines[firstdatalineind:]]
    for k, arr in zip(column_headings, numpy.float32(z).T):
        d[k]=arr
    return smp, d
    

    
def getsamplefromheader(path):
    trylist=getheadattrs(path, searchstrs=['Sample', 'Sample No', 'sample_no'])
    for v in trylist:
        if not v is None:
            return v
    return None
    
def getheadattrs(path, searchstrs=['Sample', 'Sample No', 'sample_no'], readbytes=1000):
    f=open(path, mode='r')
    s=f.read(readbytes)
    f.close()
    ret=[]
    for ss in searchstrs:
        if not ss in s:
            ret+=[None]
            continue
        vs=s.partition(ss)[2].partition('\n')[0].strip().strip(':').strip('=').strip()
        try:
            ret+=[eval(vs)]
        except:
            ret+=[None]
    return ret
