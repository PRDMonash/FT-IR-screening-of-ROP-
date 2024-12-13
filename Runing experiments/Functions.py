import numpy as np


def CalConcentration(peakarea)->float:
    '''
    Explanation: this function is used to convert the peak area of monomer into its concentration
    peakarea = 3.6721*concentration + 1.2993, R^2 = 0.998
    '''
    x = (float(peakarea)-1.2993)/3.6721
    return(x)

def CalConversion(x:float, y:float)->float:
    '''
    Explanation: This function is used to calculate the conversion of monomer:
    x: the real time concentration of Monomer  
    y: the initial concentration of Monomer
    '''
    Conversion = (1 - (x/y))*100
    return(Conversion)



def integrate(x, y):
    area = np.trapz(y=y, x=x)
    return area
