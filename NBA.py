import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nba_df=pd.read_csv("assets/nba.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

cities.rename(columns={"Population (2016 est.)[8]": "Population"},
              inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "")
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "")
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "")
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "")

Big4='NBA'

def nba_correlation():
    
    team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team['Metropolitan area']=cities['Metropolitan area']
    team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().reset_index().rename(columns = {"value":"team"})
    team=pd.merge(team,cities,how='left',on = 'Metropolitan area').iloc[:,1:4]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    team['team']=team['team'].str.replace('[\w.]*\ ','')
    
    df = nba_df[nba_df["year"]==2018]
    df['team'] = df['team'].str.replace(r'\*',"")
    df['team'] = df['team'].str.replace(r'\(\d*\)',"")
    df['team'] = df['team'].str.replace(r'[\xa0]',"")
    df = df[['team','W/L%']]
    df['team'] = df['team'].str.replace('[\w.]* ','')
    df = df.astype({"team": str, "W/L%": float})
    
    merge=pd.merge(team,df,'inner', on = 'team')
    merge = merge.groupby("Metropolitan area").agg({"W/L%" : np.nanmean, "Population": np.nanmean})
    
    population_by_region = merge["Population"] # pass in metropolitan area population from cities
    win_loss_by_region = merge["W/L%"] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
