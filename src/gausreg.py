import numpy as np
import mahotas as mh
import pandas as pd
import os
import sys
import glob


# global variables
COLUMNS = ['filename','DAPI','EdU','RFP','GFP','EdU/DAPI','G1/DAPI','Green/DAPI','Green-EdU/DAPI']


def analyze_dapi(file):
    """Takes a DAPI file and returns the number of cells counted in the given
    image.

    Parameters
    ----------
    file : str
        The file name of the DAPI image. Must be in the user-specified folder.

    Returns
    -------
    int
        A count of cells in the image.
    """

    img = mh.imread(file)
    imgg = mh.colors.rgb2grey(img)
    imggf = mh.gaussian_filter(imgg,5).astype(np.uint8)
    rmax = mh.regmax(imggf)
    return mh.label(rmax)[1]


def analyze_edu(file):
    """Takes an EdU file and returns the number of cells counted in the given
    image.

    Parameters
    ----------
    file : str
        The file name of the DAPI image. Must be in the user-specified folder.

    Returns
    -------
    int
        A count of cells in the image.
    """

    img = mh.imread(file)
    imgg = mh.colors.rgb2grey(img)
    imggf = mh.gaussian_filter(imgg,11).astype(np.uint8)
    rmax = mh.regmax(imggf)
    return mh.label(rmax)[1]


def analyze_rfp(file):
    """Takes an RFP file and returns the number of cells counted in the given
    image.

    Parameters
    ----------
    file : str
        The file name of the DAPI image. Must be in the user-specified folder.

    Returns
    -------
    int
        A count of cells in the image.
    """

    img = mh.imread(file)
    imgg = mh.colors.rgb2grey(img)
    imggf = mh.gaussian_filter(imgg,14).astype(np.uint8)
    rmax = mh.regmax(imggf)
    return mh.label(rmax)[1]


def analyze_gfp(file):
    """Takes a GFP file and returns the number of cells counted in the given
    image.

    Parameters
    ----------
    file : str
        The file name of the DAPI image. Must be in the user-specified folder.

    Returns
    -------
    int
        A count of cells in the image.
    """

    img = mh.imread(file)
    imgg = mh.colors.rgb2grey(img)
    imggf = mh.gaussian_filter(imgg,11.5).astype(np.uint8)
    rmax = mh.regmax(imggf)
    return mh.label(rmax)[1]


if __name__=='__main__':
    print('using default gausreg pipeline.')
    path = sys.argv[1]
    filetype = sys.argv[2]
    images = glob.glob(path+'/*.'+filetype)
    images.sort()
    Data = pd.DataFrame(0,index=np.arange(len(images)/4),columns=COLUMNS)

    index = 0
    for i in range(0,len(images),4):
        name = os.path.basename(os.path.normpath(images[i]))
        Data.loc[index,'filename'] = name[:name.find('_')]

        # get counts
        Data.loc[index,'DAPI'] = analyze_dapi(images[i])
        Data.loc[index,'EdU'] = analyze_edu(images[i+1])
        Data.loc[index,'RFP'] = analyze_rfp(images[i+2])
        Data.loc[index,'GFP'] = analyze_gfp(images[i+3])

        # calculate ratios
        Data.loc[index,'EdU/DAPI'] = Data.iloc[index]['EdU']/Data.iloc[index]['DAPI']
        Data.loc[index,'G1/DAPI'] = Data.iloc[index]['RFP']/Data.iloc[index]['DAPI']
        Data.loc[index,'Green/DAPI'] = Data.iloc[index]['GFP']/Data.iloc[index]['DAPI']
        Data.loc[index,'Green-EdU/DAPI'] = (Data.iloc[index]['GFP']-Data.iloc[index]['EdU'])/Data.iloc[index]['DAPI']

        index += 1

    print('saving file.')
    Data.to_csv('gausreg_results.csv')
