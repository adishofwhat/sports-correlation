import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

cities.rename(columns={"Population (2016 est.)[8]": "Population"},
              inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "")
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "")
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "")
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "")

Big4 = "MLB"

def mlb_correlation(): 
    team3 = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team3['Metropolitan area']=cities['Metropolitan area']
    team3 = pd.melt(team3, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().reset_index().rename(columns = {"value":"team"})
    team3=pd.merge(team3,cities,how='left',on = 'Metropolitan area').iloc[:,1:4]
    team3 = team3.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    
    df = mlb_df[nba_df["year"]==2018] 
    df['team'] = df['team'].str.replace(r'[\xa0]',"")
    df["team"] = df["team"].str.replace("Boston Red Sox", "RedSox")
    df["team"] = df["team"].str.replace("Chicago White Sox", "WhiteSox")
    df.rename(columns={"W-L%":"W/L%"}, inplace = True)
    df = df[['team','W/L%']]
    df['team'] = df['team'].str.replace('[\w.]* ','')
    df["team"] = df["team"].str.replace("Jays", "Blue Jays")
    df["team"] = df["team"].str.replace("WhiteSox", "White Sox")
    df["team"] = df["team"].str.replace("RedSox", "Red Sox")
    df = df.astype({"team": str, "W/L%": float})
    
    merge=pd.merge(team3,df,'outer', on = 'team')  
    merge = merge.groupby("Metropolitan area").agg({"W/L%": np.nanmean, "Population":np.nanmean})
    
    population_by_region = merge["Population"] # pass in metropolitan area population from cities
    win_loss_by_region = merge["W/L%"] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
