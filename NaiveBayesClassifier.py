import numpy as np
import pandas as pd
import scipy
from scipy.stats import norm
import argparse
import math

# Create the parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument("first_arg", help="The first argument", type=str)
parser.add_argument("second_arg", help="The second argument", type=str)

# Parse the arguments
args = parser.parse_args()

#Naive network...
# Output P(W| A,B,C,...Z) > P(L| A,B,C,....Z)

# P(W| A,B,C,...Z) = P(W, A, B, C, ... Z | W)P(W) 

#P(W, A, B, C, ... Z | W) = P(A|W)P(B|W)P(C|W)...P(C|Z)P(W)
# P(A,B,C,...,Z) = P(A)P(B)P(C)...P(Z) 

# Have win statistics seperate - find, mean, variance, use to calculate prob of certain input stat val given win


class stats:
    def __init__(self,df):
        self.dataBase = df  # 0 is discrete, 1 is continuous, -3 is label, -1 is discrete ignored, -2 is continuous ignored
        self.size = self.dataBase.shape[0]
        self.meanData = {}
        self.stdData = {}
        

        self.categories = [ 
    ('team_abbreviation_home', 0),
    ('team_abbreviation_away', 0),
    ('season_type', -1),#no
    ('min_avg5', -1), 
    ('fg_pct_home_avg5', 1),
    ('fg3_pct_home_avg5', -1),
    ('ft_pct_home_avg5', 1),
    ('oreb_home_avg5', -1),# w .69 ********
    ('dreb_home_avg5', 1),# w out .67
    ('reb_home_avg5', 1), # w out .688
    ('ast_home_avg5', -1), # w .679
    ('stl_home_avg5', 1), #w o .673
    ('blk_home_avg5', 1), # w o .681
    ('tov_home_avg5',1),# w o .673
    ('pf_home_avg5', 1),# w o .683
    ('pts_home_avg5', 1),
    ('home_wl_pre5', -1),
    ('fg_pct_away_avg5', 1),# w o .683
    ('fg3_pct_away_avg5', 1),# w o .684
    ('ft_pct_away_avg5', -1),# w .690*****
    ('oreb_away_avg5', -1),# w .69 *******
    ('dreb_away_avg5', 1),# w o .685
    ('reb_away_avg5', -1),# w .684
    ('ast_away_avg5', 1),# w o .688
    ('stl_away_avg5', 1),# w o  .688
    ('blk_away_avg5', -1),# w .689*******
    ('tov_away_avg5', 1),# w o .687
    ('pf_away_avg5', 1),# w o .68
    ('pts_away_avg5', 1),
    ('away_wl_pre5', -1)

]
     

    def getdf(self):
        return self.dataBase
    
    def statProb(self,val, category):
        if category in self.meanData:
            meanOverall = self.meanData[category]
            std = self.stdData[category]
        else:
            data_col = self.dataBase[category].to_numpy()
            meanOverall = np.mean(data_col)
            std = np.std(data_col)
        
            self.meanData[category] = meanOverall
            self.stdData[category] = std

    
        data_col = self.dataBase[category].to_numpy()

        z_score = (np.float64(val) - np.float64(meanOverall)) / std

        return norm.pdf(z_score)
        
    

    def discreteProb(self,val,category):
        column_data = self.dataBase[category].to_numpy()
        numOccurrences = np.sum(column_data == val)
        return numOccurrences/  self.size
        

    def calcProb(self,arr): # arr will hold all input params
        
        product = 1

        for i in range(len(arr)):
            stat = 0
            if(self.categories[i][1] == 1):
                stat = self.statProb(arr[i], self.categories[i][0])
            elif self.categories[i][1] == 0:
                stat = self.discreteProb(arr[i],self.categories[i][0])
            else:
                stat = 1

            if(stat == 0): #smoothing
                stat = 1/1000000

            product*= stat

        return product*(self.size)#percentage of winning/losing

def dataRead():
    data = pd.read_csv(args.first_arg)

    dfw = data[data['label'] == 1]
    dfl = data[data['label'] == 0]

    # dfw['away_wl_pre5'] = dfw['away_wl_pre5'].apply(lambda x: x.count('W'))
    # dfl['away_wl_pre5'] = dfl['away_wl_pre5'].apply(lambda x: x.count('W'))

    # dfw['home_wl_pre5'] = dfw['home_wl_pre5'].apply(lambda x: x.count('W'))
    # dfl['home_wl_pre5'] = dfl['home_wl_pre5'].apply(lambda x: x.count('W'))

    w = stats(dfw)  # DataFrame for wins
    l = stats(dfl) # DataFrame for losses

    return w,l


w,l = dataRead()
df = pd.read_csv(args.second_arg).to_numpy()


correct= 0
for i in range(len(df)):

              
    winProb = w.calcProb(df[i])
    lossProb = l.calcProb(df[i])

    choice = 0
    if(winProb > lossProb):
        print(1)
        choice = 1
    else:
        print(0)
        
        


    







    




        
