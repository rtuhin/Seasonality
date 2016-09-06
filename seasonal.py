# -*- coding: utf-8 -*-
"""
Created on Fri Apr 08 10:03:14 2016

@author: tuhin
"""
import pandas as pd
import pandas.io.data as web
import numpy as np
#from pandas.tseries.offsets import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
#The RulesSeptember
#*On the last trading day of January buy Energies (FSESX)
#*On the 1st trading day of May sell Energies
#*On the 7th trading day of August buy Biotech (FBIOX)
#*On the 9th trading day of  sell Biotech
#*On the 19th trading day of October buy Retail (FSRPX)
#*On the 20th trading day of November sell Retail

#Strat 2
#Hold FRESX Jan (held over from previous Dec. , sell on last Trading day of January)
#Hold FSESX Feb, March April (Buy on last trading day of January, sell on last Trading day of April)
#Hold FRESX May June July (Buy on last trading day of April , sell on last Trading day of July)
#Hold FBIOX August September (Buy on last trading day of July, sell on last Trading day of Sep.)
#Hold FSRPX Oct Nov (Buy on last trading day of Sep, sell on last Trading day of Nov)
#Hold FRESX Dec (Buy on last trading day of Nov, hold thru Jan next year) 

def myFunc(x, ret, yearEnds):
    #print x
    #print ret
    x = x.multiply(1.0 + ret)
    #if (x.index.isin(yearEnds)):
    #    print 
    #print x
    #if (x.index.to_series().dt.isin(yearEnds.values)):
    #    print x.index.to_series().dt
    return x
    #return


 
def rand_date(duration_years):
    year = np.random.randint(1995, 2015)
    month = np.random.randint(1, 12)
    day = np.random.randint(3, 28)
    dt = datetime(year, month, day)
    #print dt.strftime('%Y-%m-%d')
    dt1 = datetime(2015, 12, 31)

    if (dt < dt1 - relativedelta(years=duration_years)):
        dt = dt - relativedelta(years=duration_years)
    
    #print dt.strftime('%m-%d-%Y')
    return dt

#######################################################
#
#  Main program
#
#######################################################

if __name__ == "__main__":
    #start_date = rand_date(duration_years)
        #print start_date.strftime('%m-%d-%Y')
    #end_date = start_date + relativedelta(years=duration_years)
    outlay = 1000.0
    each = outlay/4
    daily_interest_ret = (1.01)**(1.0/365) - 1.0
   #print each
    duration_years = 5
    N = 1
    
    for i in xrange(N):
        
        start_date = pd.datetime(1988, 12, 31)
        end_date = pd.datetime(2015, 12, 31)
        #    pd.bdate_range(start_date, end_date)
#        start_date = rand_date(duration_years)
#            #print start_date.strftime('%m-%d-%Y')
#        end_date = start_date + relativedelta(years=duration_years)
        real_estate_Df = web.DataReader('FRESX', data_source='yahoo',start=start_date, end=end_date)
        energyDf = web.DataReader('FSESX', data_source='yahoo',start=start_date, end=end_date)
        bioDf = web.DataReader('FBIOX', data_source='yahoo',start=start_date, end=end_date)
        retailDf = web.DataReader('FSRPX', data_source='yahoo',start=start_date, end=end_date)
        #print energyDf.head()  
        
        #ax1 = energyDf['Close'].plot(grid=True, figsize=(8, 5))
        #ax2 = bioDf['Close'].plot(grid=True, figsize=(8, 5))
        #ax3 = retailDf['Close'].plot(grid=True, figsize=(8, 5))
    #    start_date = pd.to_datetime('12/31/1988')
        #df = pd.DataFrame(pd.bdate_range(start_date, end_date), energyDf['Close'], bioDf['Close'], retailDf['Close'])
        #print energyDf.info()
        #print bioDf.info()
        #print retailDf.info()
        #print energyDf.index
        #print bioDf.index
        #print retailDf.index
        df = pd.DataFrame(index=energyDf.index, columns=['real_estate', 'energy', 'bio', 'retail'])
        df['real_estate'] = real_estate_Df['Adj Close']
        df['energy'] = energyDf['Adj Close']
        df['bio'] = bioDf['Adj Close']
        df['retail'] = retailDf['Adj Close']
    
        df['real_estate_ret'] = df['real_estate']/df['real_estate'].shift(1) - 1.0
        df['energy_ret'] = df['energy']/df['energy'].shift(1) - 1.0
        df['bio_ret'] = df['bio']/df['bio'].shift(1) - 1.0
        df['retail_ret'] = df['retail']/df['retail'].shift(1) - 1.0
        # daily returns
        
        # log returns of each sector
        df['real_estate_cum_ret'] = (np.log(1.0 + df['real_estate_ret'])).cumsum().apply(np.exp)
        
        df['energy_cum_ret'] = (np.log(1.0 + df['energy_ret'])).cumsum().apply(np.exp)
        
        df['bio_cum_ret'] = (np.log(1.0 + df['bio_ret'])).cumsum().apply(np.exp)
        
        df['retail_cum_ret'] = (np.log(1.0 + df['retail_ret'])).cumsum().apply(np.exp)
    #    df.plot(grid=True, figsize=(8, 5))
          
        # passive return without rebalancing
        df['passive'] = 250*(df['real_estate_cum_ret'] + df['energy_cum_ret'] + df['bio_cum_ret'] + df['retail_cum_ret'])
        
        
        # get year end dates for rebalancing
        yearEnd_dates = (df.index.to_series()).asfreq('BA-DEC')
        #print type(yearEnd_dates)#[0]
        ##df.ix[yearEnd_dates, 'seasonal_return'] = 5.0
        df['real_estate_cum_ret_rebal'] = 1.0#df['real_estate_cum_ret']
        df['energy_cum_ret_rebal'] = 1.0#df['energy_cum_ret']
        df['bio_cum_ret_rebal'] = 1.0#df['bio_cum_ret'] 
        df['retail_cum_ret_rebal'] = 1.0#df['retail_cum_ret']
        
        #print df['real_estate_ret']
        #df[['real_estate_cum_ret_rebal']].apply(myFunc, args = (df[['real_estate_ret']], yearEnd_dates))
        #print type(df[['real_estate_ret']])
        #print df[['real_estate_cum_ret_rebal']]
        #df['real_estate_ret'].applymap(myFunc)
        #df['real_estate_cum_ret_rebal'] = df['real_estate_ret'].apply(myFunc)
        
        #rebalance at first year end 
        #df.ix[yearEnd_dates[0], 'real_estate_cum_ret_rebal'] = (df['real_estate_cum_ret'] + df['energy_cum_ret'] + df['bio_cum_ret'] + df['retail_cum_ret'])/4.0
        #df.ix[yearEnd_dates[0], 'energy_cum_ret_rebal'] = (df['real_estate_cum_ret'] + df['energy_cum_ret'] + df['bio_cum_ret'] + df['retail_cum_ret'])/4.0
        #df.ix[yearEnd_dates[0], 'bio_cum_ret_rebal'] = (df['real_estate_cum_ret'] + df['energy_cum_ret'] + df['bio_cum_ret'] + df['retail_cum_ret'])/4.0    
        #df.ix[yearEnd_dates[0], 'retail_cum_ret_rebal'] = (df['real_estate_cum_ret'] + df['energy_cum_ret'] + df['bio_cum_ret'] + df['retail_cum_ret'])/4.0
        last_real_estate = 1.0
        last_energy = 1.0
        last_bio = 1.0
        last_retail = 1.0
        #print type(df.index)
        for index, row in df.iterrows():
            if (~row.isnull().values.any()):
            #row['real_estate_ret'], row['energy_ret'], row['bio_ret'], row['retail_ret']
                real_estate = last_real_estate*(1.0 + row['real_estate_ret'])
                
                last_real_estate = real_estate
                energy = last_energy*(1.0 + row['energy_ret'])
                last_energy = energy
                bio = last_bio*(1.0 + row['bio_ret'])
                last_bio = bio
                retail = last_retail*(1.0 + row['retail_ret'])
                last_retail = retail
                #print pd.to_datetime(index), row['real_estate_cum_ret_rebal']
                #print real_estate, energy, bio, retail
                if (pd.to_datetime(index) in yearEnd_dates):
                    val = (real_estate + energy + bio + retail)/4.0      
                    real_estate = energy = bio = retail = val 
                    #print index, val
                    last_real_estate = last_energy = last_bio = last_retail = val
                
                # update dataframe values
                df.ix[pd.to_datetime([index]), 'real_estate_cum_ret_rebal'] = real_estate
                df.ix[pd.to_datetime([index]), 'energy_cum_ret_rebal'] = energy
                df.ix[pd.to_datetime([index]), 'bio_cum_ret_rebal'] = bio
                df.ix[pd.to_datetime([index]), 'retail_cum_ret_rebal'] = retail
                
        #    row['real_estate_cum_ret_rebal'] = row['real_estate_cum_ret_rebal'].shift(1)*(1.0 + row['real_estate_ret'])
        #    row['energy_cum_ret_rebal'] = row['energy_cum_ret_rebal'].shift(1)*(1.0 + row['energy_ret'])
        #    row['bio_cum_ret_rebal'] = row['bio_cum_ret_rebal'].shift(1)*(1.0 + row['bio_estate_ret']) 
        #    row['retail_cum_ret_rebal'] = row['retail_cum_ret_rebal'].shift(1)*(1.0 + row['retail_estate_ret'])
        #    if (index.isin(yearEnd_dates)):
        #        row['real_estate_cum_ret_rebal'] = (row['real_estate_cum_ret_rebal'] \
        #                                         + row['energy_cum_ret_rebal'] \
        #                                         + row['bio_cum_ret_rebal'] \
        #                                         + row['retail_cum_ret_rebal'])/4.0
    #    #df['passive_rebal_ret'] = (df['real_estate_cum_ret_rebal'] + df['energy_cum_ret_rebal'] + df['bio_cum_ret_rebal'] + df['retail_cum_ret_rebal'])
        df['passive_rebal'] = 250.0*(df['real_estate_cum_ret_rebal'] \
                                + df['energy_cum_ret_rebal'] \
                                + df['bio_cum_ret_rebal']\
                                + df['retail_cum_ret_rebal'])
    
        #all_months = np.arange(1,13)
        real_estate_hold_months =  [12] #all_months #[1, 2, 3, 4, 5, 12]
        energy_hold_months = [2, 4, 5] #all_months #[1, 2, 4, 5]
        bio_hold_months = [1, 6, 7, 8, 9] #all_months #[1, 2, 5, 6, 7, 9, 11, 12]
        retail_hold_months = [3, 10, 11] # all_months# [2, 3, 4, 5, 9, 11, 12]
    
        # daily interest return when cash is held
        df.ix[df.index.to_series().dt.month.isin(real_estate_hold_months), 'seasonal_ret'] = df['real_estate_ret']
        df.ix[df.index.to_series().dt.month.isin(energy_hold_months), 'seasonal_ret'] = df['energy_ret']
        df.ix[df.index.to_series().dt.month.isin(bio_hold_months), 'seasonal_ret'] = df['bio_ret']
        df.ix[df.index.to_series().dt.month.isin(retail_hold_months), 'seasonal_ret'] = df['retail_ret']
        
        # get the seasonal cumulative return
        df['strategy'] = 1000.0*(np.log(1.0 + df['seasonal_ret'])).cumsum().apply(np.exp)
    #    df['energy_seasonal_cum_ret'] = (np.log(1.0 + df['energy_seasonal_ret'])).cumsum().apply(np.exp)
    #    df['bio_seasonal_cum_ret'] = (np.log(1.0 + df['bio_seasonal_ret'])).cumsum().apply(np.exp)
    #    df['retail_seasonal_cum_ret'] = (np.log(1.0 + df['retail_seasonal_ret'])).cumsum().apply(np.exp)    
        
    
        #ax = df[['passive', 'passive_rebal', 'strategy']].plot(grid=True, figsize=(8, 5)) 
        #fig = ax.get_figure()
            #print cumRet[-1]
        #fig.savefig('growth')
        print df[['passive', 'passive_rebal', 'strategy']].ix[-1]    
        writer = pd.ExcelWriter('df.xls')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
    
        df_annual = df[['passive', 'passive_rebal', 'strategy']].asfreq('BA-DEC')
        #print df_annual
        #df_annual.ix[pd.to_datetime('12/31/1988')] = np.array([1000]*3)
        annual_returns = (df_annual/df_annual.shift(1) - 1.0)*100.0
        annual_returns.ix[0] = 100*(df_annual.ix[0]/1000.0 - 1.0)
        #print annual_returns
        #ax = annual_returns.plot(x=df_annual.index.to_series().dt.year, kind='bar', grid=True, \
        #                    title='Annual Returns', figsize=(9, 6))
        #fig = ax.get_figure()
            #print cumRet[-1]
        #fig.savefig('return')
        
        cagr = (df_annual['strategy'][-1]/1000.0)**(1.0/(end_date.year - start_date.year)) - 1.0
        cagr *= 100.0
        print start_date, end_date, 'CAGR:', cagr
        #print df_annual