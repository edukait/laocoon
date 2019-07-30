#!/usr/bin/env python

import pandas as pd
import sys
import glob
from laocoon import equalization as eq
from laocoon.dapi_pipeline import *
from laocoon.edu_pipeline import *
from laocoon.gfp_pipeline import *
from laocoon.rfp_pipeline import *
import numpy as np
import os


COLUMNS = ['filename','DAPI','EdU','RFP','GFP','EdU/DAPI','G1/DAPI','Green/DAPI','Green-EdU/DAPI']
COLUMNS_EXTRA = ['filename','DAPI','EdU','RFP','GFP','EdU/DAPI','G1/DAPI','Green/DAPI','Green-EdU/DAPI','uncolored cells','colorless/DAPI']


if __name__=='__main__':
    abspath = sys.argv[1]
    filetype = sys.argv[2]
    savepath = sys.argv[3]
    images = glob.glob(abspath+'/*.'+filetype)
    images.sort()
    Hist_Eps = pd.DataFrame(0,index=np.arange(len(images)/4),columns=COLUMNS_EXTRA)
    Hist = pd.DataFrame(0,index=np.arange(len(images)/4),columns=COLUMNS)
    Eps = pd.DataFrame(0,index=np.arange(len(images)/4),columns=COLUMNS_EXTRA)
    Neither = pd.DataFrame(0,index=np.arange(len(images)/4),columns=COLUMNS)

    index = 0
    for i in range(0,len(images),4):
        subset = [images[i+1].lower(),images[i+2].lower(),images[i+3].lower()]
        name = os.path.basename(os.path.normpath(images[i]))
        Hist_Eps.loc[index,'filename'] = name[:name.find('_')]
        Hist.loc[index,'filename'] = name[:name.find('_')]
        Eps.loc[index,'filename'] = name[:name.find('_')]
        Neither.loc[index,'filename'] = name[:name.find('_')]
        print('analyzing',name[:name.find('_')],'images')

        # images[i] will always be dapi
        dapi_hist = DAPI_Pipeline(images[i])

        Hist_Eps.loc[index,'DAPI'] = dapi_hist.count
        Hist.loc[index,'DAPI'] = dapi_hist.count
        Eps.loc[index,'DAPI'] = dapi_hist.count
        Neither.loc[index,'DAPI'] = dapi_hist.count
        dapi_coords = dapi_hist.coords

        Hist_Eps_Checked = [0]*len(dapi_coords)
        Eps_Checked = [0]*len(dapi_coords)

        for sub in subset:
            if 'edu' in sub:
                edu_hist_eps = EdU_Pipeline(sub,Hist_Eps_Checked,dapi_coords)
                edu_hist = EdU_Pipeline(sub,Hist_Eps_Checked,dapi_coords,epsilon=False)
                edu_eps = EdU_Pipeline(sub,Eps_Checked,dapi_coords,hist=False)
                edu_none = EdU_Pipeline(sub,Eps_Checked,dapi_coords,hist=False,epsilon=False)

                Hist_Eps.loc[index,'EdU'] = edu_hist_eps.count
                Hist_Eps_Checked = edu_hist_eps.checked
                Hist.loc[index,'EdU'] = edu_hist.count
                Eps.loc[index,'EdU'] = edu_eps.count
                Eps_Checked = edu_eps.checked
                Neither.loc[index,'EdU'] = edu_none.count

            elif 'rfp' in sub:
                rfp_hist_eps = RFP_Pipeline(sub,Hist_Eps_Checked,dapi_coords)
                rfp_hist = RFP_Pipeline(sub,Hist_Eps_Checked,dapi_coords,epsilon=False)
                rfp_eps = RFP_Pipeline(sub,Eps_Checked,dapi_coords,hist=False)
                rfp_none = RFP_Pipeline(sub,Eps_Checked,dapi_coords,hist=False,epsilon=False)

                Hist_Eps.loc[index,'RFP'] = rfp_hist_eps.count
                Hist_Eps_Checked = rfp_hist_eps.checked
                Hist.loc[index,'RFP'] = rfp_hist.count
                Eps.loc[index,'RFP'] = rfp_eps.count
                Eps_Checked = rfp_eps.checked
                Neither.loc[index,'RFP'] = rfp_none.count

            else:
                gfp_hist_eps = GFP_Pipeline(sub,Hist_Eps_Checked,dapi_coords)
                gfp_hist = GFP_Pipeline(sub,Hist_Eps_Checked,dapi_coords,epsilon=False)
                gfp_eps = GFP_Pipeline(sub,Eps_Checked,dapi_coords,hist=False)
                gfp_none = GFP_Pipeline(sub,Eps_Checked,dapi_coords,hist=False,epsilon=False)

                Hist_Eps.loc[index,'GFP'] = gfp_hist_eps.count
                Hist_Eps_Checked = gfp_hist_eps.checked
                Hist.loc[index,'GFP'] = gfp_hist.count
                Eps.loc[index,'GFP'] = gfp_eps.count
                Eps_Checked = gfp_eps.checked
                Neither.loc[index,'GFP'] = gfp_none.count

        # calculate ratios
        Hist_Eps.loc[index,'EdU/DAPI'] = Hist_Eps.iloc[index]['EdU']/Hist_Eps.iloc[index]['DAPI']
        Hist_Eps.loc[index,'G1/DAPI'] = Hist_Eps.iloc[index]['RFP']/Hist_Eps.iloc[index]['DAPI']
        Hist_Eps.loc[index,'Green/DAPI'] = Hist_Eps.iloc[index]['GFP']/Hist_Eps.iloc[index]['DAPI']
        Hist_Eps.loc[index,'Green-EdU/DAPI'] = (Hist_Eps.iloc[index]['GFP']-Hist_Eps.iloc[index]['EdU'])/Hist_Eps.iloc[index]['DAPI']
        Hist_Eps.loc[index,'uncolored cells'] = len([val for val in Hist_Eps_Checked if val == 0])
        Hist_Eps.loc[index,'colorless/DAPI']= Hist_Eps.iloc[index]['uncolored cells']/Hist_Eps.iloc[index]['DAPI']

        Hist.loc[index,'EdU/DAPI'] = Hist.iloc[index]['EdU']/Hist.iloc[index]['DAPI']
        Hist.loc[index,'G1/DAPI'] = Hist.iloc[index]['RFP']/Hist.iloc[index]['DAPI']
        Hist.loc[index,'Green/DAPI'] = Hist.iloc[index]['GFP']/Hist.iloc[index]['DAPI']
        Hist.loc[index,'Green-EdU/DAPI'] = (Hist.iloc[index]['GFP']-Hist.iloc[index]['EdU'])/Hist.iloc[index]['DAPI']

        Eps.loc[index,'EdU/DAPI'] = Eps.iloc[index]['EdU']/Eps.iloc[index]['DAPI']
        Eps.loc[index,'G1/DAPI'] = Eps.iloc[index]['RFP']/Eps.iloc[index]['DAPI']
        Eps.loc[index,'Green/DAPI'] = Eps.iloc[index]['GFP']/Eps.iloc[index]['DAPI']
        Eps.loc[index,'Green-EdU/DAPI'] = (Eps.iloc[index]['GFP']-Eps.iloc[index]['EdU'])/Eps.iloc[index]['DAPI']
        Eps.loc[index,'uncolored cells'] = len([val for val in Eps_Checked if val == 0])
        Eps.loc[index,'colorless/DAPI']= Eps.iloc[index]['uncolored cells']/Eps.iloc[index]['DAPI']

        Neither.loc[index,'EdU/DAPI'] = Neither.iloc[index]['EdU']/Neither.iloc[index]['DAPI']
        Neither.loc[index,'G1/DAPI'] = Neither.iloc[index]['RFP']/Neither.iloc[index]['DAPI']
        Neither.loc[index,'Green/DAPI'] = Neither.iloc[index]['GFP']/Neither.iloc[index]['DAPI']
        Neither.loc[index,'Green-EdU/DAPI'] = (Neither.iloc[index]['GFP']-Neither.iloc[index]['EdU'])/Neither.iloc[index]['DAPI']

        index += 1

    print('saving files.')
    Hist_Eps.to_csv(savepath+'/hist_eps.csv')
    Hist.to_csv(savepath+'/hist.csv')
    Eps.to_csv(savepath+'/eps.csv')
    Neither.to_csv(savepath+'/neither.csv')
