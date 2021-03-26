import pandas as pd 
from bs4 import BeautifulSoup as bs
import requests

#create a dictionary so the url for shooting stats match logs for each team can be easily accessed
shooting_dict = {'ARS_PL_21_Shooting' : 'https://fbref.com/en/squads/18bb7c10/2020-2021/matchlogs/s10728/shooting/Arsenal-Match-Logs-Premier-League',
                 'AVL_PL_21_Shooting' : 'https://fbref.com/en/squads/8602292d/2020-2021/matchlogs/s10728/shooting/Aston-Villa-Match-Logs-Premier-League',
                 'BHA_PL_21_Shooting' : 'https://fbref.com/en/squads/d07537b9/2020-2021/matchlogs/s10728/shooting/Brighton-and-Hove-Albion-Match-Logs-Premier-League',
                 'BUR_PL_21_Shooting' : 'https://fbref.com/en/squads/943e8050/2020-2021/matchlogs/s10728/shooting/Burnley-Match-Logs-Premier-League',
                 'CHE_PL_21_Shooting' : 'https://fbref.com/en/squads/cff3d9bb/2020-2021/matchlogs/s10728/shooting/Chelsea-Match-Logs-Premier-League',
                 'CPA_PL_21_Shooting' : 'https://fbref.com/en/squads/47c64c55/2020-2021/matchlogs/s10728/shooting/Crystal-Palace-Match-Logs-Premier-League',
                 'EVE_PL_21_Shooting' : 'https://fbref.com/en/squads/d3fd31cc/2020-2021/matchlogs/s10728/shooting/Everton-Match-Logs-Premier-League',
                 'FUL_PL_21_Shooting' : 'https://fbref.com/en/squads/fd962109/2020-2021/matchlogs/s10728/shooting/Fulham-Match-Logs-Premier-League',
                 'LEE_PL_21_Shooting' : 'https://fbref.com/en/squads/5bfb9659/2020-2021/matchlogs/s10728/shooting/Leeds-United-Match-Logs-Premier-League',
                 'LEI_PL_21_Shooting' : 'https://fbref.com/en/squads/a2d435b3/2020-2021/matchlogs/s10728/shooting/Leicester-City-Match-Logs-Premier-League',
                 'LVP_PL_21_Shooting' : 'https://fbref.com/en/squads/822bd0ba/2020-2021/matchlogs/s10728/shooting/Liverpool-Match-Logs-Premier-League',
                 'MNC_PL_21_Shooting' : 'https://fbref.com/en/squads/b8fd03ef/2020-2021/matchlogs/s10728/shooting/Manchester-City-Match-Logs-Premier-League',
                 'MNU_PL_21_Shooting' : 'https://fbref.com/en/squads/19538871/2020-2021/matchlogs/s10728/shooting/Manchester-United-Match-Logs-Premier-League',
                 'NEW_PL_21_Shooting' : 'https://fbref.com/en/squads/b2b47a98/2020-2021/matchlogs/s10728/shooting/Newcastle-United-Match-Logs-Premier-League',
                 'SHE_PL_21_Shooting' : 'https://fbref.com/en/squads/1df6b87e/2020-2021/matchlogs/s10728/shooting/Sheffield-United-Match-Logs-Premier-League',
                 'SOU_PL_21_Shooting' : 'https://fbref.com/en/squads/33c895d4/2020-2021/matchlogs/s10728/shooting/Southampton-Match-Logs-Premier-League',
                 'TOT_PL_21_Shooting' : 'https://fbref.com/en/squads/361ca564/2020-2021/matchlogs/s10728/shooting/Tottenham-Hotspur-Match-Logs-Premier-League',
                 'WBA_PL_21_Shooting' : 'https://fbref.com/en/squads/60c6b05f/2020-2021/matchlogs/s10728/shooting/West-Bromwich-Albion-Match-Logs-Premier-League',
                 'WHA_PL_21_Shooting' : 'https://fbref.com/en/squads/7c21e445/2020-2021/matchlogs/s10728/shooting/West-Ham-United-Match-Logs-Premier-Leaguee',
                 'WOL_PL_21_Shooting' : 'https://fbref.com/en/squads/8cec06e1/2020-2021/matchlogs/s10728/shooting/Wolverhampton-Wanderers-Match-Logs-Premier-League'}


def shooting_func(team, url):
    """
    This function handles taking the url for a specific team's match logs and converting into a dataframe
    
    Arguments used in the function: team, url
    team: uses the team key in the shooting_dic dictionary to assign the team name to the dataframe
    url: uses the value pair to the team key from the shooting_dict dictionary  
    
    """
    html = requests.get(url).text
    data = bs(html, 'html5')
    table = data.find('table')
    columns = []

    for header in table.find_all('th'):
        columns.append(header.string)
    columns = columns[5:29] #gets necessary column headers


    #display(columns)
    rows = [] #initliaze list to store all rows of data
    for rownum, row in enumerate(table.find_all('tr')): #find all rows in table
        if len(row.find_all('td')) > 0: 
            #if rownum % 2 == 0: #uses every other row, there is an unxplained extra row for each match
            rowdata = [] #initiliaze list of row data
            for i in range(len(row.find_all('td'))): #get all column values for row
                rowdata.append(row.find_all('td')[i].text)
            rows.append(rowdata)

    df = pd.DataFrame(rows, columns=columns)
    df = df[:-1]
    df.drop('Match Report', axis=1, inplace=True)
    df['Team'] = team[:3] 
    return df


#create dictionary of all dataframes
shooting_dfs = {}
for i in shooting_dict:
    df_var = i + '_df'
    shooting_dfs[df_var] = shooting_func(i, shooting_dict[i])

#initialize match log dataframe
shooting_columns = shooting_dfs['LVP_PL_21_Shooting_df'].columns
match_logs = pd.DataFrame(columns=list(shooting_columns))

#append all data frames
for i in shooting_dfs:
    match_logs = match_logs.append(shooting_dfs[i])

rounds = []
print(type(rounds))
for round in match_logs['Round']:
    rounds.append(int(round.split(" ")[1]))
match_logs['Round'] = rounds


match_logs.to_csv('adv_shooting_PL_21.csv')