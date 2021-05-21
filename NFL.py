import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

cities.rename(columns={"Population (2016 est.)[8]": "Population"},
              inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "")
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "")
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "")
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "")

Big4 = "NFL"

def nfl_correlation(): 
    team = cities[Big4].str.extract("([A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*)")
    team["Metropolitan area"] = cities["Metropolitan area"]
    team = pd.melt(team,id_vars = ["Metropolitan area"]).drop(columns = ["variable"]).replace("", np.nan).replace("—", np.nan).dropna().reset_index().drop(columns = ["index"]).rename(columns = {"value":"team"})
    team = pd.merge(team, cities, how="left", on = "Metropolitan area").iloc[:,0:3]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    
    df = nfl_df[nfl_df["year"]==2018] 
    df['team'] = df['team'].str.replace(r'\*',"")
    df['team'] = df['team'].str.replace(r'\+',"")
    df['team'] = df['team'].str.replace(r'[\xa0]',"")
    df.rename(columns={"W-L%":"W/L%"}, inplace = True)
    df = df[['team','W/L%']]
    dropList=[]
    for i in range(df.shape[0]):
        row=df.iloc[i]
        if row['team']==row['W/L%']:
            dropList.append(i)
    df = df.drop(dropList)
    df = df.reset_index().drop(columns = ["index"])
    df['team'] = df['team'].str.replace('[\w.]* ','') 
    df = df.astype({"team": str, "W/L%": float})
    
    merge = pd.merge(team, df, how="outer", on = "team")
    merge = merge.groupby("Metropolitan area").agg({"W/L%": np.nanmean, "Population": np.nanmean})
    
    population_by_region = merge["Population"] # pass in metropolitan area population from cities
    win_loss_by_region = merge["W/L%"] # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
