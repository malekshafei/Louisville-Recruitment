import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# pos_mapping = {
#         "Goalkeeper": "GK",
#         "Left Back": "LB",
#         "Left Wing Back": "LWB",
#         "Right Back": "RB",
#         "Right Wing Back": "RWB",
#         "Center Back": "CB",
#         "Centre Back": "CB",
#         "Right Center Back": "RCB",
#         "Right Centre Back": "RCB",
#         "Left Center Back": "LCB",
#         "Left Centre Back": "LCB",
#         "Center Defensive Midfield": "CDM",
#         "Centre Defensive Midfielder": "CDM",
#         "Left Defensive Midfield": "LDM",
#         "Left Defensive Midfielder": "LDM",
#         "Right Defensive Midfield": "RDM",
#         "Right Defensive Midfielder": "RDM",
#         "Left Center Midfield": "LCM",
#         "Left Centre Midfielder": "LCM",
#         "Right Center Midfield": "RCM",
#         "Right Centre Midfielder": "RCM",
#         "Left Midfield": "LM",
#         "Left Midfielder": "LM",
#         "Left Attacking Midfield": "LAM",
#         "Left Attacking Midfielder": "LAM",
#         "Left Wing": "LW",
#         "Right Midfield": "RM",
#         "Right Midfielder": "RM",
#         "Right Attacking Midfield": "RAM",
#         "Right Attacking Midfielder": "RAM",
#         "Right Wing": "RW",
#         "Center Attacking Midfield": "CAM",
#         "Centre Attacking Midfielder": "CAM",
#         "Center Forward": "CF",
#         "Centre Forward": "CF",
#         "Left Center Forward": "LCF",
#         "Left Centre Forward": "LCF",
#         "Right Center Forward": "RCF",
#         "Right Centre Forward": "RCF",
#         "CF": "CF",
#         "Striker": "CF"
#     }

# pos_map_2 = {
#     'CBs': 4,
#     'WBs': 3,
#     'CMs': 6,
#     'AMs': 10,
#     'Ws': 7,
#     'STs': 9
# }
# sb_only_cols = ['pctDefensive Third Tackles Won','pctDefensiveThirdTackle%', 'pctPressures', 'pctCounterpressures','pctAttacking Third Pressures', 'pctAttacking Third Counterpressures', 'pctFinal Third Receptions', 'pctBig Chance Conversion', 'pctBig Chances', 'pctBig Chances Created']

# CB_def_cols = ['pctTackle %', 'pctTackles Won', 'pctInterceptions', 'pctBlocks','pctAerial Wins', 'pctAerial %', 'pctDefensiveThirdTackle%']
# CB_att_cols = ['pctProgressive Passes', 'pctLong Passes Completed', 'pctLong Pass %', 'pctProgressive Carries', f"pct% of Passes Forward", 'pctPasses into Final Third', 'pctShort Pass %']

# wb_def_cols = ['pctTackles Won', 'pctTackle %', 'pctDefensive Third Tackles Won', 'pctDefensiveThirdTackle%', 'pctInterceptions', 'pctPressures','pctAttacking Third Pressures']
# wb_att_cols = ['pctKey Passes', 'pctCrosses Completed into Box', 'pctPasses into Box', 'pctxA', 'pctAssists', 'pctFinal Third Receptions', 'pctTake Ons']

# cm_def_cols = ['pctTackles Won', 'pctTackle %', 'pctInterceptions', 'pctPressures','pctCounterpressures','pctAttacking Third Pressures', 'pctAerial Wins']
# cm_passing_cols = ['pctProgressive Passes', 'pctPasses into Final Third', 'pctKey Passes', 'pctPasses into Box','pctShort Pass %', 'pctAssists', 'pctTake Ons']
# cm_box_cols = ['pctFinal Third Receptions', 'pctBox Receptions', 'pctGoals', 'pctShots', 'pctxG', 'pctxG/Shot', 'pctBig Chances']
                   
# am_def_cols = ['pctTackles Won', 'pctTackle %', 'pctInterceptions', 'pctPressures','pctCounterpressures','pctAttacking Third Pressures', 'pctAttacking Third Counterpressures']
# am_passing_cols = ['pctKey Passes', 'pctPasses into Box','pctShort Pass %', 'pctAssists', 'pctBig Chances Created', 'pctTake Ons', 'pctProgressive Carries']
# am_box_cols = ['pctBox Receptions', 'pctGoals', 'pctShots', 'pctxG', 'pctxG/Shot', 'pctBig Chances', 'pctBig Chance Conversion']


# pos_list = ['CBs', 'WBs', 'CMs', 'AMs', 'Ws', 'STs']



# NWSL2024 = pd.read_excel('NWSLPlayerSeasonDataPercentiles.xlsx')
# NWSL2024['Competition'] = 'NWSL'
# NWSL2024['Season'] = '2024'

# NWSL2023 = pd.read_excel('NWSL2023PlayerSeasonDataPercentiles.xlsx')
# NWSL2023['Competition'] = 'NWSL'
# NWSL2023['Season'] = '2023'

# USL2024 = pd.read_excel('USLPlayerSeasonDataPercentiles.xlsx')
# USL2024['Competition'] = 'USL'
# USL2024['Season'] = '2024'

# USL2023 = pd.read_excel('USL2023PlayerSeasonDataPercentiles.xlsx')
# USL2023['Competition'] = 'USL'
# USL2023['Season'] = '2023'

# Mexico2024 = pd.read_excel('Mexico2024PlayerSeasonDataPercentiles.xlsx')
# Mexico2024['Competition'] = 'Mexico'
# Mexico2024['Season'] = '2023/24'

# Mexico2023 = pd.read_excel('Mexico2023PlayerSeasonDataPercentiles.xlsx')
# Mexico2023['Competition'] = 'Mexico'
# Mexico2023['Season'] = '2022/23'

# Spain2024 = pd.read_excel('Spain2024PlayerSeasonDataPercentiles.xlsx')
# Spain2024['Competition'] = 'Spain'
# Spain2024['Season'] = '2023/24'

# Spain2023 = pd.read_excel('Spain2023PlayerSeasonDataPercentiles.xlsx')
# Spain2023['Competition'] = 'Spain'
# Spain2023['Season'] = '2022/23'

# Germany2024 = pd.read_excel('Germany2024PlayerSeasonDataPercentiles.xlsx')
# Germany2024['Competition'] = 'Germany'
# Germany2024['Season'] = '2023/24'

# Germany2023 = pd.read_excel('Germany2023PlayerSeasonDataPercentiles.xlsx')
# Germany2023['Competition'] = 'Germany'
# Germany2023['Season'] = '2022/23'

# England2024 = pd.read_excel('England2024PlayerSeasonDataPercentiles.xlsx')
# England2024['Competition'] = 'England'
# England2024['Season'] = '2023/24'

# England2023 = pd.read_excel('England2023PlayerSeasonDataPercentiles.xlsx')
# England2023['Competition'] = 'England'
# England2023['Season'] = '2022/23'

# Brazil2024 = pd.read_excel('Brazil2024PlayerSeasonDataPercentiles.xlsx')
# Brazil2024['Competition'] = 'Brazil'
# Brazil2024['Season'] = '2024'

# Brazil2023 = pd.read_excel('Brazil2023PlayerSeasonDataPercentiles.xlsx')
# Brazil2023['Competition'] = 'Brazil'
# Brazil2023['Season'] = '2023'

# Sweden2024 = pd.read_excel('Sweden2024PlayerSeasonDataPercentiles.xlsx')
# Sweden2024['Competition'] = 'Sweden'
# Sweden2024['Season'] = '2024'

# Sweden2023 = pd.read_excel('Sweden2023PlayerSeasonDataPercentiles.xlsx')
# Sweden2023['Competition'] = 'Sweden'
# Sweden2023['Season'] = '2023'


# MLSNext2024 = pd.read_excel('MLS Next Pro2024PlayerSeasonDataPercentiles.xlsx')
# MLSNext2024['Competition'] = 'MLS Next Pro'
# MLSNext2024['Season'] = '2024'

# MLSNext2023 = pd.read_excel('MLS Next Pro2023PlayerSeasonDataPercentiles.xlsx')
# MLSNext2023['Competition'] = 'MLS Next Pro'
# MLSNext2023['Season'] = '2023'

# sb = pd.concat([NWSL2024, NWSL2023, USL2024, USL2023, Mexico2024, Mexico2023, Spain2024, Spain2023, Germany2024, Germany2023, England2024, England2023, Brazil2024, Brazil2023, Sweden2024, Sweden2023, MLSNext2024, MLSNext2023], ignore_index = True)


# ws = pd.DataFrame()
# for pos in pos_list:
#     data = pd.read_excel("July8WyscoutWomen.xlsx", sheet_name=pos)
#     data['pos_group'] = pos
#     data['pos_group'] = data['pos_group'].map(pos_map_2)
#     if pos == 'CMs': data.replace("Receiving", "Receiving Forward", inplace=True)
#     ws = pd.concat([ws,data], ignore_index = True)

# ws = ws[~(ws['league_name'].isin(['Sweden', 'England', 'Brazil', 'Mexico', 'Mexico23', 'Germany', 'USA']))]


# sb['Detailed Position'] = sb['Detailed Position'].map(pos_mapping)

# ### removed team from this list
# ws = ws.drop(['pos_3', 'grouped_position_1','grouped_position_2','grouped_position_3', 'Deep Completion Frequency',
#     'Long Pass Reception Frequency',
   
#     'zSuccessful defensive actions per 90',
#     'zDefensive duels per 90',
#     'zDefensive duels won, %',
#     'zAerial duels per 90',
#     'zAerial duels won, %',
#     'zShots blocked per 90',
#     'zInterceptions per 90',
#     'zPAdj Interceptions',
#     'zFouls per 90',
#     'zSuccessful attacking actions per 90',
#     'zGoals per 90',
#     'zNon-penalty goals per 90',
#     'zxG per 90',
#     'zHead goals per 90',
#     'zShots per 90',
#     'zGoal conversion, %',
#     'zAssists per 90',
#     'zCrosses per 90',
#     'zAccurate crosses, %',
#     'zDribbles per 90',
#     'zSuccessful dribbles, %',
#     'zOffensive duels per 90',
#     'zOffensive duels won, %',
#     'zTouches in box per 90',
#     'zProgressive runs per 90',
#     'zAccelerations per 90',
#     'zReceived passes per 90',
#     'zReceived long passes per 90',
#     'zFouls suffered per 90',
#     'zPasses per 90',
#     'zAccurate passes, %',
#     'zForward passes per 90',
#     'zAccurate forward passes, %',
#     'zAccurate short / medium passes, %',
#     'zLong passes per 90',
#     'zAccurate long passes, %',
#     'zxA per 90',
#     'zShot assists per 90',
#     'zSecond assists per 90',
#     'zThird assists per 90',
#     'zSmart passes per 90',
#     'zKey passes per 90',
#     'zPasses to final third per 90',
#     'zAccurate passes to final third, %',
#     'zPasses to penalty area per 90',
#     'zAccurate passes to penalty area, %',
#     'zThrough passes per 90',
#     'zAccurate through passes, %',
#     'zDeep completions per 90',
#     'zDeep completed crosses per 90',
#     'zProgressive passes per 90',
#     'zAccurate progressive passes, %',
#     'zFree kicks per 90',
   
#     'zCorners per 90',
#     'zPenalties taken',
#     'zAssists',
#     'zxA',
#     'zYellow cards per 90',
#     'zBack passes per 90',
#     'zAccurate back passes, %',
#     'zLateral passes per 90',
#     'zAccurate lateral passes, %',
#     'zShort / medium passes per 90',
#     'zAverage pass length, m',
#     'zAverage long pass length, m',
#     'zAccurate smart passes, %',
#     'zAvg Possession %',
#     'zOffensive Duels Won',
#     'zpAdj Offensive Duels Won',
#     'zTackles Won',
#     'zpAdj Tackles Won',
#     'zHeaders Won',
#     'znpxG',
#     'zpAdj Goals',
#     'zpAdj xG',
#     'zpAdj Shots',
#     'zpAdj Headed Goals',
#     'zxG per Shot',
#     'zGoals per xG',
#     'zPct of Goals Headed',
#     'zpAdj Assists',
#     'zpAdj xA',
#     'zpAdj Key Passes',
#     'zCrosses Completed',
#     'zpAdj Crosses Completed',
#     'zTake Ons Completed',
#     'zpAdj Take Ons Completed',
#     'zpAdj Progressive Carries',
#     'zPasses Completed',
#     'zLong Passes Completed',
#     'zPasses to Final Third',
#     'zPasses to Box',
#     'zpAdj Passes to Final Third',
#     'zThrough Passes Completed',
#     'zProgressive Passes Completed',
#     'zpAdj Through Passes',
#     'zpAdj Progressive Passes',
#     'zpAdj Touches',
#     'zpAdj Att Box Touches',
#     'zProgressive Pass Frequency',
#     'zProgressive Carry Frequency',
#     'zProgressive Action Frequency',
#     'zTake On Frequency',
#     'zPct of Passes Forward',
#     'zKey Pass Frequency',
#     'zAssist Frequency',
#     'zDeep Completion Frequency',
#     'zLong Pass Reception Frequency',
#     ], axis=1)


# sb = sb.drop(['pctTackle %'], axis = 1)

# ws = ws.rename(columns={'pos_1': 'Detailed Position',
#                         'pos_2': 'Secondary Position',
#                         'league_name': 'Competition',
#                         #'Team within selected timeframe': 'Team',
#                         'Minutes played': 'Minutes',
#                         'Matches played': 'Appearances',
#                         'pctDefensive duels won, %': 'pctTackle %',
#                         'pctpAdj Tackles Won': 'pctTackles Won',
#                         'pctHeaders Won': 'pctAerial Wins',
#                         'pctAerial duels won, %': 'pctAerial %',
#                         'pctShots blocked per 90': 'pctBlocks',
#                         'pctPAdj Interceptions': 'pctInterceptions',
#                         'pctProgressive passes per 90': 'pctProgressive Passes',
#                         'pctAccurate long passes, %': 'pctLong Pass %',
#                         'pctProgressive runs per 90': 'pctProgressive Carries',
#                         'pctPct of Passes Forward': f"pct% of Passes Forward",
#                         'pctProgressive Pass Frequency':f"pct% of Passes Progressive",
#                         'pctPasses to final third per 90': 'pctPasses into Final Third',
#                         "pctKey passes per 90": "pctKey Passes",
#                         "pctDeep completed crosses per 90": "pctCrosses Completed into Box",
#                         "pctPasses to Box":"pctPasses into Box",
#                         'pctTake Ons Completed': 'pctTake Ons',
#                         'pctTouches in box per 90':'pctBox Receptions',
#                         'pctShots per 90': 'pctShots',
#                         'pctnpxG':'pctxG',
#                         'pctNon-penalty goals per 90':'pctGoals',
#                         'pctxG per Shot':'pctxG/Shot',
#                         'pctAccurate short / medium passes, %': 'pctShort Pass %'
                    
#                         })


# sb = sb.rename(columns={'pctTackle to Dribbled Past Ratio': 'pctTackle %',
#                         'pctDefensive Third Tackle to Dribbled Past Ratio': 'pctDefensiveThirdTackle%'

# })

# sb2 = pd.DataFrame()

# for pos in pos_list:
#     data = pd.read_excel("July16NWSLPlayers-Cleaned.xlsx", sheet_name=pos)
#     data['pos_group'] = data['Primary Position'].mode()
#     data['Position Group'] = pos

#     if pos == 'GKs':
#         data['pos_group'] = 1
#     if pos == 'CBs':
#         data['pos_group'] = 4
#     if pos == 'WBs':
#         data['pos_group'] = 3
#         data = data.rename(columns = {'WB_Defending_High': 'Defending High'})
#     if pos == 'CMs':
#         data['pos_group'] = 6
#     if pos == 'AMs':
#         data['pos_group'] = 10
#     if pos == 'Ws':
#         data['pos_group'] = 7
#     if pos == 'STs':
#         data['pos_group'] = 9
        

#     sb2 = pd.concat([sb2,data],ignore_index= True, sort=False)


# sb2 = sb2.rename(columns = {'Name': 'Player',
#                            #'Primary Position': 'pos_group',
#                            'Minutes Played': 'Minutes',
#                            'pctNon-Penalty Goals': 'pctGoals',
#                            'pctOP Passes Into Box': 'pctPasses into Box',
#                            'pctCounterpressures in Opposing Half': 'pctAttacking Third Counterpressures',
#                            'pctTack/Dribbled Past%': 'pctTackle %',
#                            'pctpAdj xA': 'pctxA',
#                            'pctDeep Progressions': 'pctProgressive Passes',
#                            'pctLong Balls': 'pctLong Passes Completed',
#                            'pctPressures in Opposing Half': 'pctAttacking Third Pressures',
#                            'pctTouches In Box': 'pctBox Receptions',
#                            'pctCarries': 'pctProgressive Carries',
#                            'pctpAdj Key Passes': 'pctKey Passes',
#                            'pctLong Ball%': 'pctLong Pass %',
#                            'pctTake Ons Completed': 'pctTake Ons',
#                            'pctAerial Win%': 'pctAerial %',
#                            'pctPassing%': 'pctShort Pass %',
#                            'pctSuccessful Crosses': 'pctCrosses Completed into Box',
#                            'pctpAdj Assists': 'pctAssists',
#                            'pctpAdj Tackles Won': 'pctTackles Won',
#                            'pctDeep Progressions': 'pctPasses into Final Third'





                           

# })
# sb2 = sb2.drop(['Primary Position','Secondary Position', 'Appearances', 'Starting Appearances',
#                'Crossing', 'Height',
#                 'Open Play Assists',
#                 'Open Play Key Passes',
#                 'Set Piece Assists',
#                 'Set Piece Key Passes',
#                 'Set-Piece xG Assisted',
#                 'xG Assisted',
#                 'Dribble%',
#                 'Dribbles',
#                 'Fouls Won',
#                 'Successful Dribbles',
#                 'Turnovers',
#                 'Non-Penalty Goals',
#                 'Post Shot xG',
#                 'Shots',
#                 'Shot Touch%',
#                 'xG',
#                 'xG/Shot',
#                 'Aggressive Actions',
#                 'Average Defensive Action Distance',
#                 'Ball Recoveries',
#                 'Defensive Action Regains',
#                 'Defensive Actions',
#                 'Interceptions',
#                 'Opposition Half Ball Recoveries',
#                 'PAdj Clearances',
#                 'PAdj Interceptions',
#                 'Aerial Win%',
#                 'Aerial Wins',
#                 'Errors',
#                 'Tack/Dribbled Past%',
#                 'Tackles',
#                 'Average Pressure Distance',
#                 'Counterpressure Regains',
#                 'Counterpressures',
#                 'Counterpressures in Opposing Half',
#                 'Counterpressures in Opposing Half%',
#                 'PAdj Pressures',
#                 'Pressure Regains',
#                 'Pressures',
#                 'Pressures in Opposing Half',
#                 'Pressures in Opposing Half%',
#                 'Crossing%',
#                 'Deep Completions',
#                 'Open Play Final Third Passes',
#                 'OP Passes Into Box',
#                 'Passes + Touches In Box',
#                 'Successful Box Cross%',
#                 'Successful Crosses',
#                 'Throughballs',
#                 'Touches In Box',
#                 'Carries',
#                 'Carry%',
#                 'Carry Length',
#                 'Deep Progressions',
#                 'xGBuildup',
#                 'xGChain',
#                 'Final Third Pass Forward%',
#                 'Pass Forward%',
#                 'Long Ball%',
#                 'Long Balls',
#                 'Open Play Passes',
#                 'Passes Being Pressured%',
#                 'Passing%',
#                 'Pressured Pass%',
#                 'Defensive Action OBV',
#                 'Dribble & Carry OBV',
#                 'OBV',
#                 'Pass OBV',
#                 'Shot OBV',
#                 'Avg Possession %',
#                 'pAdj Def OBV',
#                 'pAdj Pass OBV',
#                 'pAdj Dribble OBV',
#                 'pAdj Tackles Won',
#                 'pAdj Aggressive Actions',
#                 'pAdj Ball Recoveries',
#                 'pAdj Ball Recoveries in Att Half',
#                 'pAdj Errors',
#                 'pct of Ball Recoveries in Att Half',
#                 'pAdj Pressures',
#                 'pAdj Pressure Regains',
#                 'pAdj Pressures in Att Half',
#                 'pct of Pressures Succ',
#                 'Goals per xG',
#                 'psxG per xG',
#                 'pAdj Goals',
#                 'pAdj xG',
#                 'pAdj Shots',
#                 'pAdj psxG',
#                 'Goal Conversion',
#                 'pAdj xGChain',
#                 'pAdj xA',
#                 'pAdj Key Passes',
#                 'pAdj Assists',
#                 'pAdj Deep Completions',
#                 'pAdj Crosses',
#                 'Take Ons Completed',
#                 'pAdj Take Ons Completed',
#                 'pAdj Carries',
#                 'pAdj Passes into Box',
#                 'pAdj Deep Progressions',
#                 'pAdj Att Box Touches',
#                 'pctHeight'], axis = 1)
# sb2.to_excel("sb2test.xlsx", index = False)

# sb2 = pd.read_excel("sb2test.xlsx")
# sb2['Detailed Position'] = sb2['Detailed Position'].map(pos_mapping)

# sb2 = sb2.replace("USL Championship", "USL")
# sb2 = sb2.replace(2020, "2020")
# sb2 = sb2.replace(2021, "2021")
# sb2 = sb2.replace(2022, "2022")
# sb2 = sb2.replace(2023, "2023")
# sb2 = sb2.replace(2024, "2024")




# USL2022 = sb2[(sb2['Competition'] == 'USL') & (sb2['Season'] == '2022')]

# USL2021 = sb2[(sb2['Competition'] == 'USL') & (sb2['Season'] == '2021')]
# USL2020 = sb2[(sb2['Competition'] == 'USL') & (sb2['Season'] == '2020')]

# NWSL2022 = sb2[(sb2['Competition'] == 'NWSL') & (sb2['Season'] == '2022')]
# NWSL2021 = sb2[(sb2['Competition'] == 'NWSL') & (sb2['Season'] == '2021')]
# NWSL2020 = sb2[(sb2['Competition'] == 'NWSL') & (sb2['Season'] == '2020')]

# # MLSNext2024 = sb2[(sb2['Competition'] == 'MLS Next Pro') & (sb2['Season'] == '2024')]
# # MLSNext2023 = sb2[(sb2['Competition'] == 'MLS Next Pro') & (sb2['Season'] == '2023')]
# # MLSNext2022 = sb2[(sb2['Competition'] == 'MLS Next Pro') & (sb2['Season'] == '2022')]


# Sweden2022 = sb2[(sb2['Competition'] == 'Damallsvenskan') & (sb2['Season'] == '2022')]
# Sweden2022['Competition'] = 'Sweden'
# Sweden2021 = sb2[(sb2['Competition'] == 'Damallsvenskan') & (sb2['Season'] == '2021')]
# Sweden2021['Competition'] = 'Sweden'

# Germany2022 = sb2[(sb2['Competition'] == 'Frauen Bundesliga') & (sb2['Season'] == '2021/2022')]
# Germany2022['Season'] = '2021/22'

# Germany2021 = sb2[(sb2['Competition'] == 'Frauen Bundesliga') & (sb2['Season'] == '2020/2021')]
# Germany2021['Season'] = '2020/21'

# Spain2022 = sb2[(sb2['Competition'] == 'Liga F') & (sb2['Season'] == '2021/2022')]
# Spain2022['Season'] = '2021/22'

# Spain2021 = sb2[(sb2['Competition'] == 'Liga F') & (sb2['Season'] == '2020/2021')]
# Spain2021['Season'] = '2020/21'

# England2022 = sb2[(sb2['Competition'] == "FAWSL (FA Women's Super League)") & (sb2['Season'] == '2021/2022')]
# England2022['Season'] = '2021/22'

# England2021 = sb2[(sb2['Competition'] == "FAWSL (FA Women's Super League)") & (sb2['Season'] == '2020/2021')]
# England2021['Season'] = '2020/21'





# sb2.reset_index(drop=True, inplace=True)

# sb.reset_index(drop=True, inplace=True)
# ws.reset_index(drop=True, inplace=True)

# # sb_columns_without_name = [col for col in sb.columns if col is None or col == '']
# # sb.drop(columns=sb_columns_without_name, inplace=True)

# # ws_columns_without_name = [col for col in ws.columns if col is None or col == '']
# # ws.drop(columns=ws_columns_without_name, inplace=True)


# # # print(ws.head())
# # # print(sb.head())

# sb.to_excel("sbtest.xlsx", index=False)
# ws.to_excel("wstest.xlsx", index = False)

# sb = pd.read_excel("sbtest.xlsx")
# ws = pd.read_excel("wstest.xlsx")

# #combined = pd.concat([sb, ws], ignore_index= True, sort=False)
# combined = pd.concat([sb, ws, USL2020, USL2021, USL2022, NWSL2020, NWSL2021, NWSL2022, Sweden2022, Sweden2021, Germany2022, Germany2021, Spain2022, Spain2021, England2022, England2021], ignore_index= True, sort=False)


# nn_cols = ['Player', 'Team', 'Competition', 'Season', 'pos_group','Detailed Position', 'Minutes','Age', 'Tackle Accuracy', 'Defensive Output', 'Defending High', 'Heading', 'Progressive Passing', 'Carrying', 'Ball Retention', 'Chance Creation', 'Progression', 'Pressing', 'Dribbling', 'Poaching', 'Finishing']

# sb_only_cols = ['pctDefensive Third Tackles Won','pctDefensiveThirdTackle%', 'pctPressures', 'pctCounterpressures','pctAttacking Third Pressures', 'pctAttacking Third Counterpressures', 'pctFinal Third Receptions', 'pctBig Chance Conversion', 'pctBig Chances', 'pctBig Chances Created']

# CB_def_cols = ['pctTackle %', 'pctTackles Won', 'pctInterceptions', 'pctBlocks','pctAerial Wins', 'pctAerial %', 'pctDefensiveThirdTackle%']
# CB_att_cols = ['pctProgressive Passes', 'pctLong Passes Completed', 'pctLong Pass %', 'pctProgressive Carries', f"pct% of Passes Forward", 'pctPasses into Final Third', 'pctShort Pass %']

# wb_def_cols = ['pctTackles Won', 'pctTackle %', 'pctDefensive Third Tackles Won', 'pctDefensiveThirdTackle%', 'pctInterceptions', 'pctPressures','pctAttacking Third Pressures']
# wb_att_cols = ['pctKey Passes', 'pctCrosses Completed into Box', 'pctPasses into Box', 'pctxA', 'pctAssists', 'pctFinal Third Receptions', 'pctTake Ons']

# cm_def_cols = ['pctTackles Won', 'pctTackle %', 'pctInterceptions', 'pctPressures','pctCounterpressures','pctAttacking Third Pressures', 'pctAerial Wins']
# cm_passing_cols = ['pctProgressive Passes', 'pctPasses into Final Third', 'pctKey Passes', 'pctPasses into Box','pctShort Pass %', 'pctAssists', 'pctTake Ons']
# cm_box_cols = ['pctFinal Third Receptions', 'pctBox Receptions', 'pctGoals', 'pctShots', 'pctxG', 'pctxG/Shot', 'pctBig Chances']
                   
# am_def_cols = ['pctTackles Won', 'pctTackle %', 'pctInterceptions', 'pctPressures','pctCounterpressures','pctAttacking Third Pressures', 'pctAttacking Third Counterpressures']
# am_passing_cols = ['pctKey Passes', 'pctPasses into Box','pctShort Pass %', 'pctAssists', 'pctBig Chances Created', 'pctTake Ons', 'pctProgressive Carries']
# am_box_cols = ['pctBox Receptions', 'pctGoals', 'pctShots', 'pctxG', 'pctxG/Shot', 'pctBig Chances', 'pctBig Chance Conversion']

# sb_cb_cols = ['Heading', 'Carrying', 'Ball Retention', 'Progressive Passing', 'Tackle Accuracy', 'Defensive Output', 'Defending High']
# sb_wb_cols = ['Receiving Forward', 'Ball Retention', 'Chance Creation', 'Tackle Accuracy', 'Defensive Output', 'Defending High', 'Heading']
# sb_cm_cols = ['Receiving Forward', 'Chance Creation', 'Ball Retention', 'Tackle Accuracy', 'Defensive Output', 'Pressing', 'Heading']
# sb_am_cols = ['Chance Creation', 'Dribbling', 'Poaching', 'Finishing', 'Heading', 'Defensive Output', 'Progression']
# sb_st_cols = ['Chance Creation', 'Dribbling', 'Poaching', 'Finishing', 'Heading', 'Defensive Output', 'Ball Retention']

# keep_cols = nn_cols + sb_cb_cols + sb_wb_cols + sb_cm_cols + sb_am_cols + sb_st_cols + CB_def_cols + CB_att_cols + wb_def_cols + wb_att_cols + cm_def_cols + cm_passing_cols + cm_box_cols + am_def_cols + am_passing_cols + am_box_cols
# keep_cols = list(set(keep_cols))

# combined_cols = [col for col in keep_cols]
# combined = combined[combined_cols]
# new_col_order = nn_cols + [col for col in combined.columns if col not in nn_cols]


# combined = combined[new_col_order]

# pos_map3 = {
#     1: 'GKs',
#     4: 'CBs',
#     3: 'WBs',
#     6: 'CMs',
#     10: 'AMs',
#     7: 'Ws',
#     9: 'STs'
# }

# combined['Position Group'] = combined['pos_group'].map(pos_map3)




# # sb_cb_cols = ['Heading', 'Carrying', 'Ball Retention', 'Progressive Passing', 'Tackle Accuracy', 'Defensive Output', 'Defending High']
# # sb_wb_cols = ['Receiving Forward', 'Ball Retention', 'Chance Creation', 'Tackle Accuracy', 'Defensive Output', 'Defending High', 'Heading']
# # sb_cm_cols = ['Receiving Forward', 'Chance Creation', 'Ball Retention', 'Tackle Accuracy', 'Defensive Output', 'Pressing', 'Heading']
# # sb_am_cols = ['Chance Creation', 'Dribbling', 'Poaching', 'Finishing', 'Heading', 'Defensive Output', 'Progression']
# # sb_st_cols = ['Chance Creation', 'Dribbling', 'Poaching', 'Finishing', 'Heading', 'Defensive Output', 'Ball Retention']


# import glob
# import os
# folder_path = f"/Users/malekshafei/Desktop/Louisville/Player Mapping"

# csv_files = glob.glob(os.path.join(folder_path, "*.json"))
# dataframes = [pd.read_json(file) for file in csv_files]
# full_df = pd.concat(dataframes, ignore_index=True)
# full_df = full_df.drop_duplicates(subset = ['player_name', 'player_nickname'])
# full_df = full_df[['player_name', 'player_nickname']]
# combined = pd.merge(combined, full_df, left_on = 'Player', right_on = 'player_name', how = 'left')
# combined['Player'] = np.where(combined['player_nickname'].notna(), combined['player_nickname'], combined['Player'])

# combined.to_excel("InternationalWomensData.xlsx",index=False)


NWSL2024 = pd.read_excel("NWSLPlayerMatchDataPercentiles.xlsx")
NWSL2024['Competition'] = 'NWSL'
NWSL2024['Season'] = '2024'

NWSL2023 = pd.read_excel("NWSL2023PlayerMatchDataPercentiles.xlsx")
NWSL2023['Competition'] = 'NWSL'
NWSL2023['Season'] = '2023'

USL2024 = pd.read_excel("USLPlayerMatchDataPercentiles.xlsx")
USL2024['Competition'] = 'USL'
USL2024['Season'] = '2024'

USL2023 = pd.read_excel("USL2023PlayerMatchDataPercentiles.xlsx")
USL2023['Competition'] = 'USL'
USL2023['Season'] = '2023'

Mexico2024 = pd.read_excel("MexicoPlayerMatchDataPercentiles.xlsx")
Mexico2024['Competition'] = 'Mexico'
Mexico2024['Season'] = '2023/24'

Mexico2023 = pd.read_excel("Mexico2023PlayerMatchDataPercentiles.xlsx")
Mexico2023['Competition'] = 'Mexico'
Mexico2023['Season'] = '2022/23'

Spain2023 = pd.read_excel("Spain2023PlayerMatchDataPercentiles.xlsx")
Spain2023['Competition'] = 'Spain'
Spain2023['Season'] = '2022/23'

Spain2024 = pd.read_excel("Spain2024PlayerMatchDataPercentiles.xlsx")
Spain2024['Competition'] = 'Spain'
Spain2024['Season'] = '2023/24'


Germany2023 = pd.read_excel("Germany2023PlayerMatchDataPercentiles.xlsx")
Germany2023['Competition'] = 'Germany'
Germany2023['Season'] = '2022/23'

Germany2024 = pd.read_excel("Germany2024PlayerMatchDataPercentiles.xlsx")
Germany2024['Competition'] = 'Germany'
Germany2024['Season'] = '2023/24'

England2023 = pd.read_excel("England2023PlayerMatchDataPercentiles.xlsx")
England2023['Competition'] = 'England'
England2023['Season'] = '2022/23'

England2024 = pd.read_excel("England2024PlayerMatchDataPercentiles.xlsx")
England2024['Competition'] = 'England'
England2024['Season'] = '2023/24'

Brazil2024 = pd.read_excel("Brazil2024PlayerMatchDataPercentiles.xlsx")
Brazil2024['Competition'] = 'Brazil'
Brazil2024['Season'] = '2024'

Brazil2023 = pd.read_excel("Brazil2023PlayerMatchDataPercentiles.xlsx")
Brazil2023['Competition'] = 'Brazil'
Brazil2023['Season'] = '2023'

Sweden2024 = pd.read_excel("Sweden2024PlayerMatchDataPercentiles.xlsx")
Sweden2024['Competition'] = 'Sweden'
Sweden2024['Season'] = '2024'

Sweden2023 = pd.read_excel("Sweden2023PlayerMatchDataPercentiles.xlsx")
Sweden2023['Competition'] = 'Sweden'
Sweden2023['Season'] = '2023'

MLSNext2024 = pd.read_excel("MLS Next Pro2024PlayerMatchDataPercentiles.xlsx")
MLSNext2024['Competition'] = 'MLS Next Pro'
MLSNext2024['Season'] = '2024'

MLSNext2023 = pd.read_excel("MLS Next Pro2024PlayerMatchDataPercentiles.xlsx")
MLSNext2023['Competition'] = 'MLS Next Pro'
MLSNext2023['Season'] = '2023'



match_level = pd.concat([NWSL2024, NWSL2023, USL2024, USL2023, Mexico2024, Mexico2023, Spain2024, Spain2023, Germany2024, Germany2023, England2024, England2023, Brazil2024, Brazil2023, Sweden2024, Sweden2023,  MLSNext2024, MLSNext2023], ignore_index= True, sort=False)
#match_level = pd.concat([NWSL2024, NWSL2023, USL2024, USL2023, Mexico2024, Spain2024, Germany2024, England2024, Brazil2024, Sweden2024, MLSNext2024, MLSNext2023], ignore_index= True, sort=False)
match_level.to_parquet("InternationalWomensMatchLevelData.parquet",index=False)





NWSL2024 = pd.read_excel("NWSLLeagueData.xlsx")
NWSL2024['Competition'] = 'NWSL'
NWSL2024['Season'] = '2024'

NWSL2023 = pd.read_excel("NWSL2023LeagueData.xlsx")
NWSL2023['Competition'] = 'NWSL'
NWSL2023['Season'] = '2023'

USL2024 = pd.read_excel("USLLeagueData.xlsx")
USL2024['Competition'] = 'USL'
USL2024['Season'] = '2024'

USL2023 = pd.read_excel("USL2023LeagueData.xlsx")
USL2023['Competition'] = 'USL'
USL2023['Season'] = '2023'

Mexico2024 = pd.read_excel("MexicoLeagueData.xlsx")
Mexico2024['Competition'] = 'Mexico'
Mexico2024['Season'] = '2023/24'

Mexico2023 = pd.read_excel("Mexico2023LeagueData.xlsx")
Mexico2023['Competition'] = 'Mexico'
Mexico2023['Season'] = '2022/23'

Spain2023 = pd.read_excel("Spain2023LeagueData.xlsx")
Spain2023['Competition'] = 'Spain'
Spain2023['Season'] = '2022/23'

Spain2024 = pd.read_excel("Spain2024LeagueData.xlsx")
Spain2024['Competition'] = 'Spain'
Spain2024['Season'] = '2023/24'


Germany2023 = pd.read_excel("Germany2023LeagueData.xlsx")
Germany2023['Competition'] = 'Germany'
Germany2023['Season'] = '2022/23'

Germany2024 = pd.read_excel("Germany2024LeagueData.xlsx")
Germany2024['Competition'] = 'Germany'
Germany2024['Season'] = '2023/24'

England2023 = pd.read_excel("England2023LeagueData.xlsx")
England2023['Competition'] = 'England'
England2023['Season'] = '2022/23'

England2024 = pd.read_excel("England2024LeagueData.xlsx")
England2024['Competition'] = 'England'
England2024['Season'] = '2023/24'

Brazil2024 = pd.read_excel("Brazil2024LeagueData.xlsx")
Brazil2024['Competition'] = 'Brazil'
Brazil2024['Season'] = '2024'

Brazil2023 = pd.read_excel("Brazil2023LeagueData.xlsx")
Brazil2023['Competition'] = 'Brazil'
Brazil2023['Season'] = '2023'

Sweden2024 = pd.read_excel("Sweden2024LeagueData.xlsx")
Sweden2024['Competition'] = 'Sweden'
Sweden2024['Season'] = '2024'

Sweden2023 = pd.read_excel("Sweden2023LeagueData.xlsx")
Sweden2023['Competition'] = 'Sweden'
Sweden2023['Season'] = '2023'

MLSNext2023 = pd.read_excel("MLS Next Pro2023LeagueData.xlsx")
MLSNext2023['Competition'] = 'MLS Next Pro'
MLSNext2023['Season'] = '2023'

MLSNext2024 = pd.read_excel("MLS Next Pro2024LeagueData.xlsx")
MLSNext2024['Competition'] = 'MLS Next Pro'
MLSNext2024['Season'] = '2024'




team_level = pd.concat([NWSL2024, NWSL2023, USL2024, USL2023, Mexico2024, Mexico2023, Spain2024, Spain2023, Germany2024, Germany2023, England2024, England2023, Brazil2024, Brazil2023, Sweden2024, Sweden2023, MLSNext2024, MLSNext2023], ignore_index= True, sort=False)

team_level['Possession'] = team_level['pctPossession %']
team_level['Progression'] = (0.1 * team_level['pctProgressive Passes']) + (0.55 * team_level['pctFinal Third Entries']) + (0.35 * team_level['pctBox Entries'])
team_level['Chance Creation'] = (0.35 * team_level['pctGoals']) + (0.35 * team_level['pctxG']) + (0.2 * team_level['pctBig Chances']) + (0.1 * team_level['pctShots on Target'])
team_level['Verticality'] = (0.2 * team_level[f"pct% of Passes Progressive"]) + (0.6 * team_level[f"pct% of Passes Forward"]) + (0.2 * (100 - team_level['pctPasses per Sequence']))

team_level['Counter Attacking'] = (0.3 * team_level['pctShots from Counters']) + (0.3 * team_level['pctCounter Attack Shots']) + (0.4 * team_level['pctShots from High Pressing 15s'])
team_level['Attacking Set Pieces'] = (0.4 * team_level['pctSP Goals']) + (0.2 * team_level['pctSP xG']) + (0.3 * team_level['pctxG/SP']) + (0.1 * team_level['pctSP Shots'])
team_level['Defending Set Pieces'] = (0.4 * (100 - team_level['pctSP Goals Conceded'])) + (0.2 * (100 - team_level['pctSP xG Conceded'])) + (0.3 * (100 - team_level['pctxG/SP Against'])) + (0.1 * (100 - team_level['pctSP Shots Conceded']))

team_level['Defensive Solidity'] = (0.2 * (100 - team_level['pctBox Entries Conceded'])) + (0.2 * (100 - team_level['pctFinal Third Entries Conceded'])) + (0.2 * (100 - team_level['pctGoals Conceded'])) + (0.3 * (100 - team_level['pctxG Conceded'])) + (0.1 * (100 - team_level['pctBig Chances Conceded']))
team_level['Defensive Intensity'] = (0.4 * (100 - team_level['pctOpponent Passes per Sequence'])) + (0.4 * (100 - team_level['pctOpponent Avg. Sequence Length'])) + (0.2 * team_level['pctCounter Pressures'])
team_level['Defending High'] = (0.3 * team_level['pctDefensive Line Height']) + (0.3 * team_level['pctAttacking Third Pressures']) + (0.2 * team_level['pctAttacking Third Ball Recoveries']) + (0.1 * team_level['pctHigh Regains']) + (0.1 * team_level['pctAttacking Half Pressures'])



team_level.to_excel("InternationalWomensTeamLevelData.xlsx",index=False)


