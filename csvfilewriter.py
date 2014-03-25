import numpy

def createcsvfilstr(datadlist, fomkeys, fmt='%.5e'):
    smparr=[d['sample_no'] for d in datadlist]
    fomarr_smps=numpy.array([[(k in d['fomd'].keys() and (d['fomd'][k],) or (numpy.nan,))[0] for k in fomkeys] for d in datadlist]) 
    lines=[','.join(['sample_no']+fomkeys)]
    for smp, fomarr in zip(smparr, fomarr_smps):
        lines+=[','.join(['%d' %smp]+[fmt %n for n in fomarr])]
    s='\n'.join(lines)
    return s
    
