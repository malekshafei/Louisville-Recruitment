import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import io
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta

# if 'last_change_time' not in st.session_state:
#     st.session_state.last_change_time = datetime.min
# if 'last_league' not in st.session_state:
#     st.session_state.last_league = ''
# if 'last_name' not in st.session_state:
#     st.session_state.last_name = ''
# # if 'last_season' not in st.session_state:
# #     st.session_state.last_season = ''


# if 'position_group1' not in st.session_state:
#     st.session_state.position_group1 = 'CBs'
# if 'league1' not in st.session_state:
#     st.session_state.league1 = 'NWSL'
# if 'name1' not in st.session_state:
#     st.session_state.name1 = 'Abby Erceg'
# if 'season1' not in st.session_state:
#     st.session_state.season1 = '2024'





file_name = 'InternationalWomensData.parquet'
df = pd.read_parquet(file_name)
print('reading file')
st.set_page_config( 
    page_title="Racing Recruitment",
    page_icon=":checkered_flag:",
    layout="centered",
    initial_sidebar_state="expanded"   
    
)
df.fillna(0, inplace=True)

mins = 0

regular_font_path = '/Users/malekshafei/Downloads/Montserrat/static/Montserrat-Regular.ttf'
bold_font_path = '/Users/malekshafei/Downloads/Montserrat/static/Montserrat-Bold.ttf'

custom_css = f"""
<style>
@font-face {{
    font-family: 'Montserrat';
    src: url('file://{regular_font_path}') format('truetype');
    font-weight: normal;
}}
@font-face {{
    font-family: 'Montserrat';
    src: url('file://{bold_font_path}') format('truetype');
    font-weight: bold;
}}
html, body, [class*="css"] {{
    font-family: 'Montserrat', sans-serif;
    background-color: #400179;
    color: #ffffff;
}}
.sidebar .sidebar-content {{
    background-color: #400179;
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
pos_list = ['CBs', 'WBs', 'CMs', 'AMs', 'Ws', 'STs']

#st.title(f"Racing Recruitment")

#st.dataframe(df)




mode = st.selectbox("Select Mode", options=['Player Overview', 'Multi Player Dot Graph', 'Player Match by Match Performance', 'Team Style'])

if mode == 'Player Overview':


    # file_name = 'InternationalWomensData.xlsx'
    # df = pd.read_excel(file_name)
    df = df[df['Detailed Position'] != 'GK'].sort_values(by = ['Season Order', 'Minutes'], ascending=[False, False])

    
    #df['Position Group'] = df['pos_group']




    position_group1 = st.selectbox("Select Position Group", options=pos_list)
    #df = df[df['Position Group'] == position_group1]
    if position_group1 in ['AMs', 'Ws']: 
        df = df[(df['Position Group'] == 'AMs') | (df['Position Group'] == 'Ws')]
        df = df.sort_values(by = ['Season','Minutes'], ascending=[False,False])
        df = df.drop_duplicates(subset=['Player', 'Season'])
        
        #df = df.drop_duplicates(subset=['Player', 'Season'])

    else: df = df[df['Position Group'] == position_group1]


    # for pos in pos_list:
    #     new_data = pd.read_excel(file_name, sheet_name=pos)
    #     new_data['Position Group'] = pos
    #     #df = pd.concat([df,new_data], ignore_index = True)

    radar = True
    compare = "No"
    # league1 = st.selectbox("Select League", options=['NWSL', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL', 'MLS Next Pro', 'USL League One' ])
    # name1 = st.selectbox("Select Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique())
    # season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True))
    col1, col2, col3 = st.columns(3)
    with col1:
        league1 = st.selectbox(
            'Select League',
            ['NWSL', 'Olympics','NCAA Women','Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'CONCACAF W Champions League','USL', 'MLS Next Pro', 'USL League One' ]
        )

    # Place the second selectbox in the second column
    with col2:
        #player_options = df[df['Competition'] == st.session_state.league1]['Player'].unique()
        name1 = st.selectbox(
            'Select Player',
            #df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique(),
            df[(df['Competition'] == league1)]['Player'].unique(),
            #player_options
            
        )

    # Place the third selectbox in the third column
    with col3:
        #season_options = sorted(df[(df['Competition'] == st.session_state.league1) & (df['Player'] == st.session_state.name1)]['Season'].unique(), reverse=True)
        season1 = st.selectbox(
            'Select Season',
            #sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True),
            sorted(df[(df['Competition'] == league1)  & (df['Player'] == name1)]['Season'].unique(), reverse=True),
            #season_options
        )

    col1, col2 = st.columns(2)
    with col1:

        if position_group1 == 'CMs': mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Defending', 'Buildup & Chance Creation', 'Box Threat'])

        elif position_group1 == 'CBs': mode1 = st.selectbox("Select Radar Type", options=["Basic", 'In Possession', 'Defending'])
        elif position_group1 in ['AMs', 'Ws', 'STs']: mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Threat Creation', 'Shooting', 'Out of Possession'])

        else: mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Attacking', 'Defending'])

    
    if mode1 == 'Match by Match Overview': radar = False

 
    

    if radar == True:
        with col2:
            compare = st.selectbox("Compare with another player?", options=["No", 'Yes'])


        if compare == 'Yes':
            col1, col2, col3 = st.columns(3)
            with col1: league2 = st.selectbox("Select other League", options=['NWSL', 'Olympics', 'NCAA Women', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'CONCACAF W Champions League','USL', 'MLS Next Pro','USL League One' ])
            with col2: 
                #name2 = st.selectbox("Select other Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league2)]['Player'].unique())
                name2 = st.selectbox("Select other Player", options=df[(df['Competition'] == league2)]['Player'].unique())
            with col3: 
                #season2 = st.selectbox("Select other season", options=sorted(df[(df['Competition'] == league2) & (df['Position Group'] == position_group1) & (df['Player'] == name2)]['Season'].unique(), reverse=True))
                season2 = st.selectbox("Select other season", options=sorted(df[(df['Competition'] == league2)  & (df['Player'] == name2)]['Season'].unique(), reverse=True))

        ws_leagues = ['NCAA Women', 'CONCACAF W Champions League','France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL League One' ]

    # st.session_state['position_group1'] = position_group1
    # st.session_state['league1'] = league1
    # st.session_state['name1'] = name1
    # st.session_state['season1'] = season1
    # st.session_state['mode1'] = mode1
    # st.session_state['compare'] = compare
    # if compare == 'Yes':
    #     st.session_state['league2'] = league2
    #     st.session_state['name2'] = name2
    #     st.session_state['season2'] = season2

    # if st.button('Run Code'):
    #     # Retrieve selections from session state
    #     position_group1 = st.session_state['position_group1']
    #     league1 = st.session_state['league1']
    #     name1 = st.session_state['name1']
    #     season1 = st.session_state['season1']
    #     mode1 = st.session_state['mode1']
    #     compare = st.session_state['compare']
    #     if compare == 'Yes':
    #         league2 = st.session_state['league2']
    #         name2 = st.session_state['name2']
    #         season2 = st.session_state['season2']
    
        
        # Radar Chart Code
        if position_group1 == 'CBs' and mode1 == 'Basic':
                
            Heading = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Heading']
            Carrying = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Carrying']
            BallRetention = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Ball Retention']
            ProgressivePassing = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Progressive Passing']
            DefAccuracy = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Tackle Accuracy']
            DefEngage = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Defensive Output']
            DefHigh = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Defending High']


            data1 = [Heading, Carrying, BallRetention, ProgressivePassing, DefAccuracy, DefEngage, DefHigh]
            #if league1 in ws_leagues: data1 = [Heading, Carrying, BallRetention, ProgressivePassing, DefAccuracy, DefEngage, 0]
            metrics = ['Heading', 'Carrying', 'Ball Retention', 'Progressive Passing', 'Tackle Accuracy', 'Defensive Output', 'Defending High']
            metric_names = ['Heading', 'Carrying', 'Ball Retention', 'Progressive\nPassing', 'Tackle\nAccuracy', 'Defensive Output', 'Defending\nHigh']

            if compare == 'Yes':
                Heading2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Heading']
                Carrying2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Carrying']
                BallRetention2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Ball Retention']
                ProgressivePassing2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Progressive Passing']
                DefAccuracy2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Tackle Accuracy']
                DefEngage2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Defensive Output']
                DefHigh2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Defending High']


                data2 = [Heading2, Carrying2, BallRetention2, ProgressivePassing2, DefAccuracy2, DefEngage2, DefHigh2]
                #if league2 in ws_leagues: data2 = [Heading2, Carrying2, BallRetention2, ProgressivePassing2, DefAccuracy2, DefEngage2, 0]



        if position_group1 == 'CBs' and mode1 == 'Defending':
                
            TacklePct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctTackle %']
            Tackles = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctTackles Won']
            Interceptions = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctInterceptions']
            Blocks = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctBlocks']
            Headers = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAerial Wins']
            AerialPct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAerial %']
            DefThirdTacklePct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctDefensiveThirdTackle%']


            data1 = [TacklePct, Tackles, Interceptions, Blocks, Headers, AerialPct, DefThirdTacklePct]
            #if league1 in ws_leagues: data1 = [TacklePct, Tackles, Interceptions, Blocks, Headers, AerialPct, 0]
            metrics = ['pctTackle %', 'pctTackles Won', 'pctInterceptions', 'pctBlocks','pctAerial Wins', 'pctAerial %', 'pctDefensiveThirdTackle%']
            metric_names = ['Tackle %', 'Tackles', 'Interceptions', 'Blocks','Headers Won', 'Aerial %', 'Defensive Third\nTackle %']

            if compare == 'Yes':
                TacklePct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctTackle %']
                Tackles2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctTackles Won']
                Interceptions2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctInterceptions']
                Blocks2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctBlocks']
                Headers2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctAerial Wins']
                AerialPct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctAerial %']
                DefThirdTacklePct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctDefensiveThirdTackle%']


                data2 = [TacklePct2, Tackles2, Interceptions2, Blocks2, Headers2, AerialPct2, DefThirdTacklePct2]
                #if league2 in ws_leagues: data2 = [TacklePct2, Tackles2, Interceptions2, Blocks2, Headers2, AerialPct2, 0]


        if position_group1 == 'CBs' and mode1 == 'In Possession':
                
            TacklePct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctProgressive Passes']
            Tackles = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctLong Passes Completed']
            Interceptions = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctLong Pass %']
            Blocks = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctProgressive Carries']
            Headers = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], f"pct% of Passes Forward"]
            AerialPct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctPasses into Final Third']
            DefThirdTacklePct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctShort Pass %']


            data1 = [TacklePct, Tackles, Interceptions, Blocks, Headers, AerialPct, DefThirdTacklePct]
            metrics = ['pctProgressive Passes', 'pctLong Passes Completed', 'pctLong Pass %', 'pctProgressive Carries', f"pct% of Passes Forward", 'pctPasses into Final Third', 'pctShort Pass %']
            metric_names = ['Progressive\nPasses', 'Long Passes', 'Long Pass %', 'Progressive\nCarries',f'% of Passes\nForward', 'Passes into Final Third', 'Short Passing %']

            if compare == 'Yes':
                TacklePct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctProgressive Passes']
                Tackles2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctLong Passes Completed']
                Interceptions2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctLong Pass %']
                Blocks2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctProgressive Carries']
                Headers2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], f"pct% of Passes Forward"]
                AerialPct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctPasses into Final Third']
                DefThirdTacklePct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctShort Pass %']


                data2 = [TacklePct2, Tackles2, Interceptions2, Blocks2, Headers2, AerialPct2, DefThirdTacklePct2]




        if position_group1 == 'WBs' and mode1 == 'Basic':
                
            Creating = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Chance Creation']) 
            Carrying = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Carrying'])
            Technical = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Ball Retention'])
            ReceivingForward = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Receiving Forward'])
            DefAccuracy = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Tackle Accuracy'])
            DefEngage = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defensive Output'])
            DefendingHigh = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defending High']
            Heading = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Heading'])
            #data1 = [Creating, Carrying, Technical, BoxThreat, DefAccuracy, DefEngage, DefendingHigh, Heading]
            
            data1 = [ReceivingForward, Technical, Creating, DefAccuracy, DefEngage, DefendingHigh,Heading]
            #if league1 in ws_leagues: data1 = [ReceivingForward, Technical, Creating, DefAccuracy, DefEngage, 0,Heading]
            metrics = ['Receiving', 'Ball Retention', 'Chance Creation', 'Tackle Accuracy', 'Defenisve Output', 'Defending High', 'Heading']
            metric_names = ['Receiving', 'Ball Retention', 'Chance Creation', 'Tackle\nAccuracy', 'Defenisve\nOutput', 'Defending High', 'Heading']

            if compare == 'Yes':
                Creating2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Chance Creation']) 
                Carrying2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Carrying'])
                Technical2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Ball Retention'])
                ReceivingForward2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Receiving Forward'])
                DefAccuracy2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Tackle Accuracy'])
                DefEngage2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defensive Output'])
                DefendingHigh2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defending High']
                Heading2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Heading'])
                #data1 = [Creating, Carrying, Technical, BoxThreat, DefAccuracy, DefEngage, DefendingHigh, Heading]
                
                data2 = [ReceivingForward2, Technical2, Creating2, DefAccuracy2, DefEngage2, DefendingHigh2,Heading2]
                #if league2 in ws_leagues: data2 = [ReceivingForward2, Technical2, Creating2, DefAccuracy2, DefEngage2, 0,Heading2]

        if position_group1 == 'WBs' and mode1 == 'Defending':
                
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackles Won']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackle %'])
            DefThirdTackles = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctDefensive Third Tackles Won'])
            DefThirdTacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctDefensiveThirdTackle%'])
            Intercepts = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctInterceptions'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPressures'])
            AttThirdPressures = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAttacking Third Pressures']
            
            data1 = [TacklesWon, TacklePct, DefThirdTackles, DefThirdTacklePct, Intercepts, Pressures,AttThirdPressures]
            #if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, 0, 0, Intercepts, 0,0]
            metrics = ['Tackles Won', 'Tackle %', 'Def. Third Tackles Won', 'Def. Third Tackle %', 'Interceptions', 'Pressures','Att. Third Pressures']
            metric_names = ['Tackles Won', 'Tackle %', 'Def. Third Tackles Won', 'Def. Third Tackle %', 'Interceptions', 'Pressures','Att. Third Pressures']

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackles Won']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackle %'])
                DefThirdTackles2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctDefensive Third Tackles Won'])
                DefThirdTacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctDefensiveThirdTackle%'])
                Intercepts2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctInterceptions'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctPressures'])
                AttThirdPressures2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctAttacking Third Pressures']
                
                data2 = [TacklesWon2, TacklePct2, DefThirdTackles2, DefThirdTacklePct2, Intercepts2, Pressures2,AttThirdPressures2]
                #if league2 in ws_leagues: data2 = [TacklesWon2, TacklePct2, 0, 0, Intercepts2, 0,0]

        if position_group1 == 'WBs' and mode1 == 'Attacking':
                
            KeyPasses = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctKey Passes']) 
            Crosses = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctCrosses Completed into Box'])
            PassesIntoBox = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPasses into Box'])
            xA = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctxA'])
            Assists = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAssists'])
            FinalThirdTouches = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctFinal Third Receptions'])
            TakeOns = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTake Ons']
            
            data1 = [KeyPasses, Crosses, PassesIntoBox, xA, Assists, FinalThirdTouches,TakeOns]
            #if league1 in ws_leagues: data1 = [KeyPasses, Crosses, PassesIntoBox, xA, Assists, 0,TakeOns]
            metrics = ['pctKey Passes', 'pctCrosses Completed into Box', 'pctPasses into Box', 'pctxA', 'pctAssists', 'pctFinal Third Receptions', 'pctTake Ons']
            metric_names = ['Key Passes', 'Completed Crosses', 'Passes into Box', 'xA', 'Assists', 'Final Third Touches', 'Take Ons Completed']

            if compare == 'Yes':
                KeyPasses2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctKey Passes']) 
                Crosses2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctCrosses Completed into Box'])
                PassesIntoBox2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctPasses into Box'])
                xA2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctxA'])
                Assists2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctAssists'])
                FinalThirdTouches2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctFinal Third Receptions'])
                TakeOns2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTake Ons']
                
                data2 = [KeyPasses2, Crosses2, PassesIntoBox2, xA2, Assists2, FinalThirdTouches2,TakeOns2]
                #if league2 in ws_leagues: data2 = [KeyPasses2, Crosses2, PassesIntoBox2, xA2, Assists2, 0,TakeOns2]

        


        #streamlit run streamlit.py



        if position_group1 == 'CMs' and mode1 == 'Basic':
                
            Creating = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Chance Creation']) 
            Carrying = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Carrying'])
            Technical = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Ball Retention'])
            BoxThreat = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Progression'])
            DefAccuracy = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Tackle Accuracy'])
            DefEngage = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defensive Output'])
            Pressing = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Pressing'])

            DefendingHigh = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defending High']
            Heading = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Heading'])

            data1 = [BoxThreat, Creating, Technical, DefAccuracy, DefEngage, Pressing, Heading]
            #if league1 in ws_leagues: data1 = [BoxThreat, Creating, Technical, DefAccuracy, DefEngage, 0, Heading]
            metrics = ['Progression', 'Chance Creation', 'Ball Retention', 'Tackle Accuracy', 'Defensive Output', 'Pressing','Heading']
            metric_names = ['Progression', 'Chance Creation', 'Ball Retention', 'Tackle\nAccuracy', 'Defensive Output', 'Pressing','Heading']

            if compare == 'Yes':
                Creating2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Chance Creation']) 
                Carrying2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Carrying'])
                Technical2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Ball Retention'])
                BoxThreat2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Progression'])
                DefAccuracy2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Tackle Accuracy'])
                DefEngage2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defensive Output'])
                Pressing2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Pressing'])

                DefendingHigh2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defending High']
                Heading2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Heading'])

                data2 = [BoxThreat2, Creating2, Technical2, DefAccuracy2, DefEngage2, Pressing2, Heading2]
                #if league2 in ws_leagues: data2 = [BoxThreat2, Creating2, Technical2, DefAccuracy2, DefEngage2, 0, Heading2]

        if position_group1 == 'CMs' and mode1 == 'Defending':
                
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackles Won']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackle %'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctInterceptions'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPressures'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctCounterpressures'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAttacking Third Pressures'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAerial Wins'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            #if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, Interceptions, 0, 0, 0 ,AerialWins]
            metrics = ['Tackles Won', 'Tackle %', 'Interceptions', 'Pressures','Counterpressures','Att. Third Pressures', 'Headers Won']
            metric_names = ['Tackles Won', 'Tackle %', 'Interceptions', 'Pressures','Counterpressures','Att. Third Pressures', 'Headers Won']

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackles Won']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackle %'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctInterceptions'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctPressures'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctCounterpressures'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctAttacking Third Pressures'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctAerial Wins'])

                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]
                #if league2 in ws_leagues: data2 = [TacklesWon2, TacklePct2, Interceptions2, 0, 0, 0,AerialWins2]

        if position_group1 == 'CMs' and mode1 == 'Buildup & Chance Creation':
                
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctProgressive Passes']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPasses into Final Third'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctKey Passes'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctPasses into Box'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctShort Pass %'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAssists'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTake Ons'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            metrics = ['Progressive Passes', 'Passes into Final Third', 'Key Passes', 'Passes into Box','Short Pass %', 'Assists', '1v1 Dribbles Completed']
            metric_names = ['Progressive Passes', 'Passes into Final Third', 'Key Passes', 'Passes into Box','Short Pass %', 'Assists', '1v1 Dribbles\nCompleted']

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctProgressive Passes']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctPasses into Final Third'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctKey Passes'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctPasses into Box'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctShort Pass %'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctAssists'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTake Ons'])

                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]



        if position_group1 == 'CMs' and mode1 == 'Box Threat':
                
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctFinal Third Receptions']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctBox Receptions'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctGoals'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctShots'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctxG'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctxG/Shot'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctBig Chances'])

            data1 = [0, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            #if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,0]
            metrics = ['Final Third Touches', 'Box Touches', 'Goals', 'Shots', 'xG', 'xG/Shot', 'Big Chances']
            metric_names = ['Final Third\nTouches', 'Box Touches', 'Goals', 'Shots', 'xG', 'xG/Shot', 'Big Chances']

            if compare == 'Yes':

                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctFinal Third Receptions']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctBox Receptions'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctGoals'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctShots'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctxG'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctxG/Shot'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctBig Chances'])

                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]
                #if league2 in ws_leagues: data2 = [0, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,0]


                    
        if (position_group1 == 'Ws' or position_group1 == 'AMs') and mode1 == "Basic":
            #Goal_Contributions = df.loc[df.index[(df['Name'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'FW_Goal_Contribution']
            Creating = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Chance Creation'])
            Poaching = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Poaching'])
            Finishing = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Finishing'])
            Technical = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Ball Retention'])
            Dribbling = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Dribbling'])
            DefOutput = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defensive Output'])
            Progression = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Progression'])
            Heading = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Heading'])

            data1 = [Creating, Dribbling, Poaching, Finishing, Heading, DefOutput, Progression]
            metrics = ['Chance Creation', 'Dribbling Threat', 'Poaching', 'Finishing', 'Heading','Defensive Output','Progression']
            metric_names = ['Chance\nCreation', 'Dribbling Threat', 'Poaching', 'Finishing', 'Heading', 'Defensive Output', 'Progression']

            if compare == 'Yes':

                Creating2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Chance Creation'])
                Poaching2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Poaching'])
                Finishing2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Finishing'])
                Technical2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Ball Retention'])
                Dribbling2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Dribbling'])
                DefOutput2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defensive Output'])
                Progression2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Progression'])
                Heading2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Heading'])

                data2 = [Creating2, Dribbling2, Poaching2, Finishing2, Heading2, DefOutput2, Progression2]



        if (position_group1 == 'Ws' or position_group1 == 'AMs' or position_group1 == 'STs') and mode1 == "Threat Creation":
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctKey Passes']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPasses into Box'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctShort Pass %'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAssists'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctBig Chances Created'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctTake Ons'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctProgressive Carries'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            #if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, Interceptions, Pressures, 0, AttThirdPressures,AerialWins]
            metrics = ['Key Passes', 'Passes into Box','Short Pass %', 'Assists', 'Big Chances Created', '1v1 Dribbles', 'Progressive Carries']
            metric_names = ['Key Passes', 'Passes into Box','Short Pass %', 'Assists', 'Big Chances Created', '1v1 Dribbles', 'Progressive Carries']

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctKey Passes']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctPasses into Box'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctShort Pass %'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctAssists'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctBig Chances Created'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctTake Ons'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctProgressive Carries'])

                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]
                #if league2 in ws_leagues: data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, 0, AttThirdPressures2,AerialWins2]

        if (position_group1 == 'Ws' or position_group1 == 'AMs' or position_group1 == 'STs') and mode1 == "Shooting":
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctBox Receptions']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctGoals'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctShots'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctxG'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctxG/Shot'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctBig Chances'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctBig Chance Conversion'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            #if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, 0,0]
            metrics = ['Touches in Box', 'Goals', 'Shots', 'xG', 'xG/Shot', 'Big Chances', 'Big Chance Conversion']
            metric_names = ['Touches in Box', 'Goals', 'Shots', 'xG', 'xG/Shot', 'Big Chances', 'Big Chance Conversion']

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctBox Receptions']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctGoals'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctShots'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctxG'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctxG/Shot'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctBig Chances'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctBig Chance Conversion'])

                
                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]
                #if league2 in ws_leagues: data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, 0,0]


        if (position_group1 == 'Ws' or position_group1 == 'AMs' or position_group1 == 'STs') and mode1 == "Out of Possession":
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackles Won']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackle %'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctInterceptions'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctPressures'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctCounterpressures'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAttacking Third Pressures'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAttacking Third Counterpressures'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            #if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, Interceptions, 0, 0, 0,0]
            metrics = ['Tackles Won', 'Tackle %', 'Interceptions', 'Pressures','Counterpressures','Att. Third Pressures', 'Att. Third Counterpressures']
            metric_names = ['Tackles Won', 'Tackle %', 'Interceptions', 'Pressures','Counterpressures','Att. Third Pressures', 'Att. Third\nCounterpressures']

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackles Won']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackle %'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctInterceptions'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctPressures'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctCounterpressures'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctAttacking Third Pressures'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctAttacking Third Counterpressures'])


                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]
                #if league2 in ws_leagues: data2 = [TacklesWon2, TacklePct2, Interceptions2, 0, 0, 0,0]



        if position_group1 == 'STs' and mode1 == "Basic":
            #Goal_Contributions = df.loc[df.index[(df['Name'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'FW_Goal_Contribution']
            Creating = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Chance Creation'])
            Poaching = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Poaching'])
            Finishing = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Finishing'])
            Technical = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Ball Retention'])
            Dribbling = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Dribbling'])
            DefOutput = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defensive Output'])
            Heading = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Heading'])

            data1 = [Creating, Dribbling, Poaching, Finishing, Heading, DefOutput, Technical]
            metrics = ['Chance Creation', 'Dribbling Threat', 'Poaching', 'Finishing', 'Heading','Defensive Output','Ball Retention']
            metric_names = ['Chance\nCreation', 'Dribbling Threat', 'Poaching', 'Finishing', 'Heading', 'Defensive Output', 'Ball\nRetention']

            if compare == 'Yes':
                Creating2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Chance Creation'])
                Poaching2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Poaching'])
                Finishing2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Finishing'])
                Technical2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Ball Retention'])
                Dribbling2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Dribbling'])
                DefOutput2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defensive Output'])
                Heading2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Heading'])

                data2 = [Creating2, Dribbling2, Poaching2, Finishing2, Heading2, DefOutput2, Technical2]
                        

        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        data1 += data1[:1]  # Repeat the first value to close the polygon
        angles += angles[:1]  # Repeat the first angle to close the polygon

        if compare == 'Yes':
            data2 += data2[:1]

        fig, ax = plt.subplots(figsize=(16, 9), subplot_kw=dict(polar=True, facecolor='#400179'))
        fig.patch.set_facecolor('#400179')
        fig.set_facecolor('#400179')

        ax.set_facecolor('#400179')


        ax.spines['polar'].set_visible(False)

        ax.plot(angles, [100] * len(angles), color='white', linewidth=2.25, linestyle='-')
        ax.plot(angles, [75] * len(angles), color='white', linewidth=0.7, linestyle='-')
        ax.plot(angles, [50] * len(angles), color='white', linewidth=0.7, linestyle='-')
        ax.plot(angles, [25] * len(angles), color='white', linewidth=0.7, linestyle='-')

        if compare == 'No':
            ax.plot(angles, data1, color='green', linewidth=0.4, linestyle='-', marker='o', markersize=3)
            ax.fill(angles, data1, color='green', alpha=0.95)

        if compare == 'Yes':
            ax.plot(angles, data1, color='green', linewidth=2.5, linestyle='-', marker='o', markersize=3)
            ax.fill(angles, data1, color='green', alpha=0.7)

            ax.plot(angles, data2, color='red', linewidth=2.5, linestyle='-', marker='o', markersize=3)
            ax.fill(angles, data2, color='red', alpha=0.55)



        ax.set_xticks(angles[:-1])
        metrics = ["" for i in range(len(metrics))]
        ax.set_xticklabels(metrics)

        ax.set_yticks([])
        ax.set_ylim(0, 100)

        ax.plot(0, 0, 'ko', markersize=4, color='#400179')
        #fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        #fig.subplots_adjust(left=0.25, right=0.75, top=0.75, bottom=0.25)
        fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)



        #ax.set_xticklabels(metrics, color='white', size=12)


        #plt.savefig(save_path + file_name + '.png')
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0,facecolor=fig.get_facecolor())
        #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

        buf.seek(0)

        # # Open the image using PIL
        # image = Image.open(buf)

        # # Create a new canvas with desired dimensions and background color
        # final_canvas = Image.new('RGB', (1600, 900), (64, 1, 121))

        image = Image.open(buf).convert("RGBA")

        # Create a new canvas with desired dimensions and background color
        final_canvas = Image.new('RGBA', (1600, 900), (64, 1, 121, 255))


        resize_factor = 1.07
        new_size = (int(image.size[0] * resize_factor), int(image.size[1] * resize_factor))
        image = image.resize(new_size)
        image = image.rotate(13, expand=True)
        #image = image.rotate(13)


        # Calculate the position to paste, centering the image
        x = (final_canvas.width - image.width) // 2
        y = (final_canvas.height - image.height) // 2

        # Paste the matplotlib generated image onto the canvas
        final_canvas.paste(image, (x, y+65), image)

        final_canvas = final_canvas.convert("RGB")

        # plt.figure(figsize=(16, 9))  # Adjust figure size as needed
        # plt.imshow(final_canvas)
        # plt.axis('off')  # Turns off axes.


        fig_canvas, ax_canvas = plt.subplots(figsize=(16, 9))
        ax_canvas.imshow(final_canvas)

        ax_canvas.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.tight_layout(pad=0)
        plt.margins(0, 0)

        x_list = [1150,820,770,450,515,800,1090]
        y_list = [460,190,190,460,770,885,770]
        orient_list = ['left', 'left', 'right', 'right', 'right','center', 'left']

        for i in range(7):
            plt.text(x_list[i], y_list[i], metric_names[i], ha = orient_list[i], fontsize=30, color = 'white')#,fontname='Avenir')



        club = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Team']
        mins = int(df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Minutes'])
        detailed_pos = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Detailed Position']



        if compare == 'No':
            plt.text(800,70,f"{name1}",ha = 'center', fontsize=45, color = 'white', fontweight = 'bold')
            plt.text(800,120,f"{club} - {season1} {league1} - {mins} Minutes - {detailed_pos}",ha = 'center', fontsize=30, color = 'white')#, fontname='Avenir')
            plt.text(30,880,f"Data compared to {league1} {position_group1} in {season1}",ha = 'left', fontsize=16, color = 'white')#, fontname='Avenir')

            if league1 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            if league1 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')

        if compare == 'Yes':
            club2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Team']
            mins2 = int(df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Minutes'])
            detailed_pos2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Detailed Position']

            plt.text(40,65,f"{name1}",ha = 'left', fontsize=35, color = 'green', fontweight = 'bold')
            #plt.text(40,110,f"{club} - {season1} {league1}",ha = 'left', fontsize=30, color = 'green', fontname='Avenir')
            #plt.text(40,150,f"{mins} Minutes - {detailed_pos}",ha = 'left', fontsize=30, color = 'green', fontname='Avenir')
            plt.text(40,110,f"{club}",ha = 'left', fontsize=30, color = 'green')#, fontname='Avenir')
            plt.text(40,150,f"{season1} {league1}",ha = 'left', fontsize=30, color = 'green')#, fontname='Avenir')
            plt.text(40,190,f"{mins} Minutes - {detailed_pos}",ha = 'left', fontsize=30, color = 'green')#, fontname='Avenir')
        
            plt.text(1560,65,f"{name2}",ha = 'right', fontsize=35, color = 'red', fontweight = 'bold')
            #plt.text(1560,110,f"{club2} - {season2} {league2}",ha = 'right', fontsize=30, color = 'red', fontname='Avenir')
            #plt.text(1560,150,f"{mins2} Minutes - {detailed_pos2}",ha = 'right', fontsize=30, color = 'red', fontname='Avenir')
            plt.text(1560,110,f"{club2}",ha = 'right', fontsize=30, color = 'red')#, fontname='Avenir')
            plt.text(1560,150,f"{season2} {league2}",ha = 'right', fontsize=30, color = 'red')#, fontname='Avenir')
            plt.text(1560,190,f"{mins2} Minutes - {detailed_pos2}",ha = 'right', fontsize=30, color = 'red')#, fontname='Avenir')
            plt.text(30,880,f"Data compared to {position_group1} in player's league",ha = 'left', fontsize=15, color = 'white')#, fontname='Avenir')


            if league1 in ws_leagues and league2 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            elif league1 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            elif league2 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league2}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            
            if league1 in ws_leagues and league2 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            elif league1 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')

            elif league2 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable for {league2}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')


        #streamlit run streamlit.py


        # plt.subplots_adjust(left=0, right=1, top=1, bottom=0) 
        # plt.margins(0,0) 

        # plt.tight_layout(pad=0)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

        buf.seek(0)


        # plt.savefig("PIctestjuly3.png")

        #st.pyplot(plt)

            
        st.image(buf, use_column_width=True)


    
if mode == 'Team Style':
    file_name = 'InternationalWomensTeamLevelData.xlsx'
    df = pd.read_excel(file_name)
    position_group1 = 'NA'


    radar = True
    compare = "No"
    league1 = st.selectbox("Select League", options=['NWSL', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'USL', 'MLS Next Pro'])
    name1 = st.selectbox("Select Team", options=df[(df['Competition'] == league1)]['Team'].unique())
    season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition'] == league1) & (df['Team'] == name1)]['Season'].unique(), reverse=True))

    if radar == True:
        compare = st.selectbox("Compare with another Team?", options=["No", 'Yes'])

        if compare == 'Yes':
            league2 = st.selectbox("Select other League", options=['NWSL', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'USL'])
            name2 = st.selectbox("Select other Team", options=df[(df['Competition'] == league2)]['Team'].unique())
            season2 = st.selectbox("Select other season", options=sorted(df[(df['Competition'] == league2) & (df['Team'] == name2)]['Season'].unique(), reverse=True))
            
    Possession = df.loc[df.index[(df['Team'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Possession']
    Progression = df.loc[df.index[(df['Team'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Progression']
    ChanceCreation = df.loc[df.index[(df['Team'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Chance Creation']
    CounterAttacking = df.loc[df.index[(df['Team'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Counter Attacking']
    DefSolidity = df.loc[df.index[(df['Team'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Defensive Solidity']
    DefIntensity = df.loc[df.index[(df['Team'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Defensive Intensity']
    DefHigh = df.loc[df.index[(df['Team'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Defending High']


    data1 = [Possession, Progression, ChanceCreation, CounterAttacking, DefSolidity, DefIntensity, DefHigh]
    
    metrics = ['Possession', 'Progression', 'Chance Creation', 'Counter Attacking', 'Defensive Solidity', 'Defensive Intensity', 'High Pressing']
    metric_names = ['Possession', 'Progression', 'Chance Creation', 'Counter\nAttacking', 'Defensive Solidity', 'Defensive Intensity', 'High Pressing']

    if compare == 'Yes':
        Possession2 = df.loc[df.index[(df['Team'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Possession']
        Progression2 = df.loc[df.index[(df['Team'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Progression']
        ChanceCreation2 = df.loc[df.index[(df['Team'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Chance Creation']
        CounterAttacking2 = df.loc[df.index[(df['Team'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Counter Attacking']
        DefSolidity2 = df.loc[df.index[(df['Team'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Defensive Solidity']
        DefIntensity2 = df.loc[df.index[(df['Team'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Defensive Intensity']
        DefHigh2 = df.loc[df.index[(df['Team'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Defending High']


        data2 = [Possession2, Progression2, ChanceCreation2, CounterAttacking2, DefSolidity2, DefIntensity2, DefHigh2]
        
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    data1 += data1[:1]  # Repeat the first value to close the polygon
    angles += angles[:1]  # Repeat the first angle to close the polygon

    if compare == 'Yes':
        data2 += data2[:1]

    fig, ax = plt.subplots(figsize=(16, 9), subplot_kw=dict(polar=True, facecolor='#400179'))
    fig.patch.set_facecolor('#400179')
    fig.set_facecolor('#400179')

    ax.set_facecolor('#400179')


    ax.spines['polar'].set_visible(False)

    ax.plot(angles, [100] * len(angles), color='white', linewidth=2.25, linestyle='-')
    ax.plot(angles, [75] * len(angles), color='white', linewidth=0.7, linestyle='-')
    ax.plot(angles, [50] * len(angles), color='white', linewidth=0.7, linestyle='-')
    ax.plot(angles, [25] * len(angles), color='white', linewidth=0.7, linestyle='-')

    if compare == 'No':
        ax.plot(angles, data1, color='green', linewidth=0.4, linestyle='-', marker='o', markersize=3)
        ax.fill(angles, data1, color='green', alpha=0.95)

    if compare == 'Yes':
        ax.plot(angles, data1, color='green', linewidth=2.5, linestyle='-', marker='o', markersize=3)
        ax.fill(angles, data1, color='green', alpha=0.7)

        ax.plot(angles, data2, color='red', linewidth=2.5, linestyle='-', marker='o', markersize=3)
        ax.fill(angles, data2, color='red', alpha=0.55)



    ax.set_xticks(angles[:-1])
    metrics = ["" for i in range(len(metrics))]
    ax.set_xticklabels(metrics)

    ax.set_yticks([])
    ax.set_ylim(0, 100)

    ax.plot(0, 0, 'ko', markersize=4, color='#400179')
    #fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    #fig.subplots_adjust(left=0.25, right=0.75, top=0.75, bottom=0.25)
    fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)



    #ax.set_xticklabels(metrics, color='white', size=12)


    #plt.savefig(save_path + file_name + '.png')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0,facecolor=fig.get_facecolor())
    #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

    buf.seek(0)

    # # Open the image using PIL
    # image = Image.open(buf)

    # # Create a new canvas with desired dimensions and background color
    # final_canvas = Image.new('RGB', (1600, 900), (64, 1, 121))

    image = Image.open(buf).convert("RGBA")

    # Create a new canvas with desired dimensions and background color
    final_canvas = Image.new('RGBA', (1600, 900), (64, 1, 121, 255))


    resize_factor = 1.07
    new_size = (int(image.size[0] * resize_factor), int(image.size[1] * resize_factor))
    image = image.resize(new_size)
    image = image.rotate(13, expand=True)
    #image = image.rotate(13)


    # Calculate the position to paste, centering the image
    x = (final_canvas.width - image.width) // 2
    y = (final_canvas.height - image.height) // 2

    # Paste the matplotlib generated image onto the canvas
    final_canvas.paste(image, (x, y+65), image)

    final_canvas = final_canvas.convert("RGB")

    # plt.figure(figsize=(16, 9))  # Adjust figure size as needed
    # plt.imshow(final_canvas)
    # plt.axis('off')  # Turns off axes.


    fig_canvas, ax_canvas = plt.subplots(figsize=(16, 9))
    ax_canvas.imshow(final_canvas)

    ax_canvas.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.tight_layout(pad=0)
    plt.margins(0, 0)

    x_list = [1150,830,730,450,515,800,1090]
    y_list = [460,190,190,460,770,885,770]
    orient_list = ['left', 'left', 'right', 'right', 'right','center', 'left']

    for i in range(7):
        plt.text(x_list[i], y_list[i], metric_names[i], ha = orient_list[i], fontsize=30, color = 'white')#,fontname='Avenir')



    # club = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Team']
    # mins = int(df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Minutes'])
    # detailed_pos = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Detailed Position']



    if compare == 'No':
        plt.text(800,70,f"{name1}",ha = 'center', fontsize=45, color = 'white', fontweight = 'bold')
        plt.text(800,120,f"{season1} {league1}",ha = 'center', fontsize=30, color = 'white')#, fontname='Avenir')
        plt.text(30,880,f"Data compared to {league1} teams in {season1}",ha = 'left', fontsize=16, color = 'white')#, fontname='Avenir')

    if compare == 'Yes':

        plt.text(40,65,f"{name1}",ha = 'left', fontsize=35, color = 'green', fontweight = 'bold')
        #plt.text(40,110,f"{club} - {season1} {league1}",ha = 'left', fontsize=30, color = 'green', fontname='Avenir')
        #plt.text(40,150,f"{mins} Minutes - {detailed_pos}",ha = 'left', fontsize=30, color = 'green', fontname='Avenir')
        plt.text(40,110,f"{season1} {league1}",ha = 'left', fontsize=30, color = 'green')#, fontname='Avenir')
    
        plt.text(1560,65,f"{name2}",ha = 'right', fontsize=35, color = 'red', fontweight = 'bold')
        #plt.text(1560,110,f"{club2} - {season2} {league2}",ha = 'right', fontsize=30, color = 'red', fontname='Avenir')
        #plt.text(1560,150,f"{mins2} Minutes - {detailed_pos2}",ha = 'right', fontsize=30, color = 'red', fontname='Avenir')
        plt.text(1560,110,f"{season2} {league2}",ha = 'right', fontsize=30, color = 'red')#, fontname='Avenir')
        plt.text(30,880,f"Data compared to teams in their league",ha = 'left', fontsize=15, color = 'white')#, fontname='Avenir')


    #streamlit run streamlit.py


    # plt.subplots_adjust(left=0, right=1, top=1, bottom=0) 
    # plt.margins(0,0) 

    # plt.tight_layout(pad=0)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

    buf.seek(0)


    # plt.savefig("PIctestjuly3.png")

    #st.pyplot(plt)

        
    st.image(buf, use_column_width=True)





if  mode == 'Multi Player Dot Graph':
    pos_list = ['CBs', 'WBs', 'CMs', 'AMs', 'Ws', 'STs']
    #df['Position Group'] = df['pos_group']




    position_group1 = st.selectbox("Select Position Group", options=pos_list)
    if position_group1 in ['AMs', 'Ws']: 
        df = df[(df['Position Group'] == 'AMs') | (df['Position Group'] == 'Ws')]
        df = df.sort_values(by = ['Season','Minutes'], ascending=[False,False])
        df = df.drop_duplicates(subset=['Player', 'Season'])
    else: df = df[df['Position Group'] == position_group1]

    # st.session_state['league2'] = ''
    # st.session_state['name2'] = ''
    # st.session_state['season2'] = ''

    # st.session_state['league3'] = ''
    # st.session_state['name3'] = ''
    # st.session_state['season3'] = ''
    # league1 = 'NA'
    # player1 = 'NA'
    # season1 = 'NA'

    # league2 = 'NA'
    # player2 = 'NA'
    # season2 = 'NA'

    # league3 = 'NA'
    # player3 = 'NA'
    # season3 = 'NA'

    # league4 = 'NA'
    # player4 = 'NA'
    # season4 = 'NA'

    # league5 = 'NA'
    # player5 = 'NA'
    # season5 = 'NA'

    if 'league2' not in st.session_state:
        st.session_state.league2 = ''
    if 'name2' not in st.session_state:
        st.session_state.name2 = ''
    if 'season2' not in st.session_state:
        st.session_state.season2 = ''

    
    

    # league1 = st.selectbox("Select League", options=['NWSL', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL', 'MLS Next Pro', 'USL League One' ])
    # name1 = st.selectbox("Select Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique())
    # season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True))

    col1, col2, col3 = st.columns(3)
    with col1:
        league1 = st.selectbox(
            'Select League #1',
            ['NWSL',  'Olympics', 'NCAA Women','Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'CONCACAF W Champions League','USL', 'MLS Next Pro', 'USL League One' ]
        )

    # Place the second selectbox in the second column
    with col2:
        name1 = st.selectbox(
            'Select Player #1',
            #df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique()
            df[(df['Competition'] == league1)]['Player'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season1 = st.selectbox(
            'Select Season #1',
            #sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True)
            sorted(df[(df['Competition'] == league1) & (df['Player'] == name1)]['Season'].unique(), reverse=True)
        )


    col1, col2, col3 = st.columns(3)
    with col1:
        league2 = st.selectbox(
            'Select League #2',
            ['NWSL',  'Olympics','NCAA Women','Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'CONCACAF W Champions League','USL', 'MLS Next Pro', 'USL League One' ]
        )

    # Place the second selectbox in the second column
    with col2:
        name2 = st.selectbox(
            'Select Player #2',
            #df[(df['Position Group'] == position_group1) & (df['Competition'] == league2)]['Player'].unique()
            df[(df['Competition'] == league2)]['Player'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season2 = st.selectbox(
            'Select Season #2',
            #sorted(df[(df['Competition'] == league2) & (df['Position Group'] == position_group1) & (df['Player'] == name2)]['Season'].unique(), reverse=True)
            sorted(df[(df['Competition'] == league2) & (df['Player'] == name2)]['Season'].unique(), reverse=True)
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        league3 = st.selectbox(
            'Select League #3',
            ['NWSL',  'Olympics','NCAA Women','Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'CONCACAF W Champions League','USL', 'MLS Next Pro', 'USL League One' ]
        )

    # Place the second selectbox in the second column
    with col2:
        name3 = st.selectbox(
            'Select Player #3',
            #df[(df['Position Group'] == position_group1) & (df['Competition'] == league3)]['Player'].unique()
            df[(df['Competition'] == league3)]['Player'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season3 = st.selectbox(
            'Select Season #3',
            #sorted(df[(df['Competition'] == league3) & (df['Position Group'] == position_group1) & (df['Player'] == name3)]['Season'].unique(), reverse=True)
            sorted(df[(df['Competition'] == league3) & (df['Player'] == name3)]['Season'].unique(), reverse=True)
        )
    
    
    col1, col2, col3 = st.columns(3)
    with col1:
        league4 = st.selectbox(
            'Select League #4',
            ['NWSL', 'Olympics', 'NCAA Women','Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'CONCACAF W Champions League','USL', 'MLS Next Pro', 'USL League One' ]
        )

    # Place the second selectbox in the second column
    with col2:
        name4 = st.selectbox(
            'Select Player #4',
            #df[(df['Position Group'] == position_group1) & (df['Competition'] == league4)]['Player'].unique()
            df[(df['Competition'] == league4)]['Player'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season4 = st.selectbox(
            'Select Season #4',
            #sorted(df[(df['Competition'] == league4) & (df['Position Group'] == position_group1) & (df['Player'] == name4)]['Season'].unique(), reverse=True)
            sorted(df[(df['Competition'] == league4) & (df['Player'] == name4)]['Season'].unique(), reverse=True)
        )

    # data = {
    #     'Player': ['Turner', 'Silva', 'Jheniffer', 'Tanaka', 'Ludmila'],
    #     'League': ['NWSL', 'Portugal', 'NWSL', 'Greece', 'NWSL'],
    #     'Season': ['2024', '2023/24', '2023/24', '2023/24', '2023/24'],
    #     'Poaching': [70, 90, 80, 50, 85],
    #     'Finishing': [60, 75, 85, 70, 90],
    #     'Defensive Output 1': [50, 55, 40, 65, 70],
    #     'Chance Creation': [45, 60, 80, 85, 70],
    #     'Defensive Output 2': [5, 50, 45, 70, 80]
    # }


    # df = pd.DataFrame(data)




    df = df[((df['Competition'] == league1) & (df['Player'] == name1) & (df['Season'] == season1)) | 
            ((df['Competition'] == league2) & (df['Player'] == name2) & (df['Season'] == season2)) | 
            ((df['Competition'] == league3) & (df['Player'] == name3) & (df['Season'] == season3)) | 
            ((df['Competition'] == league4) & (df['Player'] == name4) & (df['Season'] == season4))]# |
            #((df['Competition'] == league5) & (df['Player'] == name5) & (df['Season'] == season5))]
                
    #print(df)
    # Plotting
    df['unique_label'] = df.apply(lambda row: f"{row['Player']}\n{row['Competition']} - {row['Season']}", axis=1)

    if position_group1 == 'CBs': metrics = ['Ball Retention', 'Progressive Passing', 'Heading', 'Defensive Output', 'Tackle Accuracy']
    if position_group1 == 'WBs': metrics = ['Ball Retention', 'Chance Creation', 'Receiving Forward', 'Defensive Output', 'Tackle Accuracy']
    if position_group1 == 'CMs': metrics = ['Heading','Defensive Output', 'Tackle Accuracy','Pressing','Chance Creation','Progression' ]
    if position_group1 in ['Ws', 'AMs']: metrics = ['Defensive Output', 'Finishing', 'Poaching', 'Dribbling', 'Chance Creation']
    if position_group1 == 'STs': metrics = ['Chance Creation', 'Heading','Defensive Output', 'Finishing', 'Poaching']


    #metrics = metrics[::-1]

    #players = [player1, player2, player3, player4, player5 ]
    #players = df['Player']
    players = df['unique_label']
    colors = ['purple', 'red', 'green', 'orange', 'black']
    #fig, ax = plt.subplots(figsize=(10, 6))
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('#400179')
    fig.set_facecolor('#400179')

    ax.set_facecolor('#400179')
    #fig, ax = plt.subplots(figsize=(16, 9))


    # Plot lines for each metric
    for i in range(len(metrics)):
        y = len(metrics) - i
        metric = metrics[i]

        ax.plot([0, 100], [y, y], color='white', linewidth=0.8)



        for x in np.arange(0, 101, 10):
            #ax.axvline(x, ymin=y - 0.05, ymax=y + 0.05, color='black', linewidth=0.5)
            ax.vlines(x, ymin=y-0.1, ymax=y+0.1, color='white', linewidth=0.6, zorder= 1)

        for j in range(len(players)):
            row = df.iloc[j]
            unique_label = row['unique_label']
            player = row['Player']
            league = row['Competition']
            season = row['Season']

            #x = df.loc[j, metric]
            x = row[metric]
            print(player, season, metric, x)
            ax.scatter(x, i+1, s = 950, color=colors[j], label=unique_label if i == 0 else "", zorder = 3)



    # Customizing the plot

    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_xticklabels(np.arange(0, 101, 10), size = 22, color = 'white')#,fontname='Avenir',
    ax.set_xlabel(f'Rankings vs {position_group1} in their League', size = 20,  color = 'white')#,fontname='Avenir',
    ax.set_title('Player Comparison\n ', size = 30, color = 'white')#fontname='Avenir'

    # for label in ax.get_yticklabels():
    #     label.set_x(-0.05)  # Adjust the value as needed to create more space

    #ax.yaxis.set_tick_params(pad=60)

    for label in ax.get_yticklabels():
        label.set_bbox(dict(facecolor='#400179', edgecolor='None', alpha=0.65, pad=5))

    ax.set_yticks(np.arange(1, len(metrics) + 1))
    ax.set_yticklabels(metrics, size = 23, ha='right', color = 'white')#, fontname='Avenir')




    # Adding legend
    # handles, labels = ax.get_legend_handles_labels()
    # by_label = dict(zip(labels, handles))
    # ax.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize='large', ncol=5)
    # handles, labels = ax.get_legend_handles_labels()
    # legend_labels = [f'{label}\n{df.loc[df["Player"] == label, "Competition"].iloc[0]} - {df.loc[df["Player"] == label, "Season"].iloc[0]}\n{int(df.loc[df["Player"] == label, "Minutes"].iloc[0])} Minutes' for label in labels]
    # by_label = dict(zip(labels, handles))
    # legend = ax.legend(by_label.values(), legend_labels, facecolor = '#400179', loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize=16, ncol=len(players))
     
    handles, labels = ax.get_legend_handles_labels()
    #legend_labels = [f'{label}\n{df.loc[df["Player"] == label, "Competition"].iloc[0]} - {df.loc[df["Player"] == label, "Season"].iloc[0]}\n{int(df.loc[df["Player"] == label, "Minutes"].iloc[0])} Minutes' for label in labels]
    legend_labels = [f'{label}\n{int(df.loc[df["unique_label"] == label, "Minutes"].iloc[0])} Minutes' for label in labels]

    by_label = dict(zip(labels, handles))
    legend = ax.legend(by_label.values(), legend_labels, facecolor = '#400179', loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize=16, ncol=len(players))
     
    for text in legend.get_texts():
        text.set_color('white')
    # from matplotlib import font_manager as fm

    # for text in legend.get_texts():
    #     text.set_color('white')
    #     lines = text.get_text().split('\n')
    #     text.set_text('')  # Clear the current text

    # # Create Text objects with different font sizes
    #     for i, line in enumerate(lines):
    #         if i == 0:
    #             font_properties = fm.FontProperties(size=20)  # Larger font for the first line
    #         else:
    #             font_properties = fm.FontProperties(size=16)  # Normal font for other lines
    #         text_line = plt.Text(0, 0, line, fontproperties=font_properties)
    #         text_line.set_fontproperties(font_properties)

    #         # Append each line with appropriate font size to the text
    #         text._text += text_line.get_text() + '\n'




        
    

    #plt.subplots_adjust(left=0.3, right=0.95, top=0.9, bottom=0.1)
    #plt.axis('off')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2)
    #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

    buf.seek(0)


    # plt.savefig("PIctestjuly3.png")

    #st.pyplot(plt)

        
    st.image(buf, use_column_width=True)
    radar = True
    position_group1 = 'NA'
        
if mode == 'Player Match by Match Performance':
    mode1 = 'NA'
    position_group1 = 'CBs'
    df = pd.read_parquet("InternationalWomensMatchLevelData.parquet")

    pos_map_2 = {
    4: 'CBs',
    3: 'WBs',
    6: 'CMs',
    10: 'AMs',
    7: 'Ws',
    9: 'STs'
    }
    
    df['Position Group'] = df['pos_group'].map(pos_map_2)
    position_group1 = st.selectbox("Select Position Group", options=pos_list)
    df = df[df['Position Group'] == position_group1]

    radar = True
    compare = "No"
   
   
    col1, col2, col3 = st.columns(3)
    with col1:
        league1 = st.selectbox(
            'Select League',
            ['NWSL', 'Olympics', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'USL', 'MLS Next Pro']
        )

    # Place the second selectbox in the second column
    with col2:
        #player_options = df[df['Competition'] == st.session_state.league1]['Player'].unique()
        name1 = st.selectbox(
            'Select Player',
            df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique(),
            #player_options
            
        )

    # Place the third selectbox in the third column
    with col3:
        #season_options = sorted(df[(df['Competition'] == st.session_state.league1) & (df['Player'] == st.session_state.name1)]['Season'].unique(), reverse=True)
        season1 = st.selectbox(
            'Select Season',
            sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True),
            #season_options
        )
   
    df = df[(df['Competition'] == league1) & (df['Season'] == season1)]

    df.sort_values(by=['match_date'], ascending=[True], inplace=True)

    pos_map3 = {
        1: 'GKs',
        4: 'CBs',
        3: 'WBs',
        6: 'CMs',
        10: 'AMs',
        7: 'Ws',
        9: 'STs'
    }

    df['Position Group'] = df['pos_group'].map(pos_map3)

    pos_mapping = {
            "Goalkeeper": "GK",
            "Left Back": "LB",
            "Left Wing Back": "LWB",
            "Right Back": "RB",
            "Right Wing Back": "RWB",
            "Center Back": "CB",
            "Right Center Back": "RCB",
            "Left Center Back": "LCB",
            "Center Defensive Midfield": "CDM",
            "Left Defensive Midfield": "LDM",
            "Right Defensive Midfield": "RDM",
            "Left Center Midfield": "LCM",
            "Right Center Midfield": "RCM",
            "Left Midfield": "LM",
            "Left Attacking Midfield": "LAM",
            "Left Wing": "LW",
            "Right Midfield": "RM",
            "Right Attacking Midfield": "RAM",
            "Right Wing": "RW",
            "Center Attacking Midfield": "CAM",
            "Center Forward": "CF",
            "Left Center Forward": "LCF",
            "Right Center Forward": "RCF",
            "CF": "CF",
            "Striker": "CF"
        }

    df['Short Position'] = df['Position'].map(pos_mapping)

    selected_player = name1
    df = df[(df['Player']==selected_player) & (df['Position Group'] == position_group1) & (df['Minutes'] >= 30)]
    # fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(18, 10))  # Adjust size as needed
    # metrics = ['Poaching', 'Finishing', 'Chance Creation', 'Dribbling', 'Defensive Output']
    # colors = ['orange', 'green', 'blue', 'cyan', 'red']
    # positions = df['Position'].unique()

    # # Plot each metric in a separate subplot
    # for ax, metric, color in zip(axes, metrics, colors):
    #     for pos in positions:
    #         subset = df[df['Position'] == pos]
    #         ax.barh(subset['match_date'] + " " + subset['Opponent'], subset[metric], label=pos, color=color)
    #     ax.set_title(metric)
    #     ax.set_xlabel('Value')
    #     ax.invert_yaxis()  # Invert y axis to match your example
    import matplotlib.cm as cm
    import matplotlib.colors as mcolors
    from datetime import datetime


    if position_group1 == 'CBs': metrics = ['Tackle Accuracy', 'Defensive Output', 'Heading','Ball Retention', 'Progressive Passing']
    elif position_group1 == 'WBs': metrics = ['Receiving Forward', 'Chance Creation', 'Ball Retention', 'Tackle Accuracy', 'Defensive Output']
    elif position_group1 == 'CMs':metrics = ['Defensive Output', 'Tackle Accuracy','Pressing','Chance Creation','Progression' ]#metrics = ['Box Threat', 'Chance Creation', 'Tackle Accuracy', 'Defensive Output','Pressing']
    else: metrics = ['Poaching', 'Finishing', 'Chance Creation', 'Dribbling', 'Defensive Output']

    # print(metrics)

    cmap = cm.get_cmap('RdYlGn')
    norm = mcolors.Normalize(0, 100)  # Normalize from 0 to 100
    df = df.reset_index(drop=True)
    # Create subplots
    fig, axes = plt.subplots(nrows=len(df), ncols=9, figsize=(16, 9), gridspec_kw={'width_ratios': [0.1, 0.65, 0.1, 0.1] + [1]*5})
    # fig, axes = plt.subplots(nrows=len(df), ncols=9, figsize=(16, 9), 
    #                      gridspec_kw={'width_ratios': [0.1, 0.65, 0.1, 0.1] + [1]*5,
    #                                   'height_ratios': [0.05]*len(df)})  # Adjust the height as needed


    fig.patch.set_facecolor('#400179')
    fig.set_facecolor('#400179')
 
    #axes.set_facecolor('#400179')
    plt.subplots_adjust(hspace=0.5)

    # Add column headers
    # fig.add_subplot(111, frame_on=False)
    # plt.tick_params(labelcolor="none", bottom=False, left=False)
    # plt.grid(False)
    # plt.xlabel("Date       |      Opponent      |      Mins       |       Position", fontsize=12)


    #fig.text(0.5, 0.98, f"{selected_player}", fontsize=15,fontweight= 'bold', ha='center', va='top')
    fig.suptitle(f"{selected_player} Performance over {season1} Season", fontsize=18, fontweight='bold', color = 'white',y=0.92)

    #fig.text(0.01, 0.91, " Date   |   Opponent    |  Position |  Mins", fontsize=12,fontweight= 'bold', ha='left', va='bottom',color = 'white')

            
    # Plot each row
    for i, row in df.iterrows():
        # Set match date
        match_date = datetime.strptime(row['match_date'], '%Y-%m-%d').strftime('%m/%d')

        axes[i, 0].text(0.2, 0.5, f"  {match_date}", ha='center', va='center', fontsize=14,fontweight= 'bold', color = 'white')
        axes[i, 0].axis('off')  

        # Set opponent
        if row['Opponent'] == 'North Carolina Courage':
            opp = 'North Carolina'
        elif row['Opponent'] == 'Racing Louisville FC':
            opp = 'Racing'
        elif row['Opponent'] == 'Pittsburgh Riverhounds':
            opp = 'Pittsburgh'
        elif row['Opponent'] == 'Sacramento Republic':
            opp = 'Sacramento'
        elif row['Opponent'] == 'Birmingham Legion':
            opp = 'Birmingham'
        elif row['Opponent'] == 'Charleston Battery':
            opp = 'Charleston'
        else:
            opp = row['Opponent']

        axes[i, 1].text(0, 0.5, opp, ha='left', va='center', fontsize=11.5,fontweight= 'bold', color = 'white')
        axes[i, 1].axis('off')

        # Set position
        axes[i, 2].text(0, 0.5, row['Short Position'], ha='left', va='center', fontsize=11.5,fontweight= 'bold', color = 'white')
        axes[i, 2].axis('off')

        # Set minutes
        axes[i, 3].text(0, 0.5, f"{row['Minutes']}", ha='left', va='center', fontsize=11.5,fontweight= 'bold', color = 'white')
        axes[i, 3].axis('off')

        # Plot metrics
        for j, metric in enumerate(metrics):
            axes[i, j+4].barh(row['match_date'], row[metric], color=cmap(norm(row[metric])), edgecolor='none', height = 0.05, linewidth=0)
            #print(row[metric])
            axes[i, j+4].set_xlim(0, 100)
            axes[i, j+4].invert_yaxis()
            #axes[i, j+4].set_yticks([])
            axes[i, j+4].set_facecolor('#400179')

            # axes[i, j+4].spines['top'].set_visible(False)
            # axes[i, j+4].spines['right'].set_visible(False)
            # axes[i, j+4].spines['bottom'].set_visible(False)
            # axes[i, j+4].spines['left'].set_visible(False)
            axes[i, j+4].spines['top'].set_color('white')
            axes[i, j+4].spines['right'].set_color('white')
            axes[i, j+4].spines['bottom'].set_color('white')
            axes[i, j+4].spines['left'].set_color('white')
            


            if i == 0:
                axes[i, j+4].set_title(metric, fontweight = 'bold', color = 'white')
            if i == len(df)-1:
                axes[i, j+4].tick_params(axis='x', colors='white')
            else:
                axes[i, j+4].tick_params(axis='x', colors='#400179')
                axes[i, j+4].tick_params(axis='y', colors='#400179')

        axes[0, 0].set_title('Date', fontweight = 'bold', color = 'white')
        axes[0, 1].set_title('Opponent', fontweight = 'bold', color = 'white')
        axes[0, 2].set_title('Position', fontweight = 'bold', color = 'white')
        axes[0, 3].set_title(' Mins', fontweight = 'bold', color = 'white')

    # Remove y-axis ticks from the entire plot except the first column
    for ax in axes.flat:
        ax.label_outer()
    # fig.patch.set_facecolor('#400179')


    # Add your plotting code here

    # for i in range(1, len(df)):
    #     plt.hline(y=i*1000, color='white', linestyle='-', linewidth=0.5)

    #plt.tight_layout()
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    #plt.show()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

    buf.seek(0)


    # plt.savefig("PIctestjuly3.png")

    #st.pyplot(plt)

        
    st.image(buf, use_column_width=True)

def get_columns_to_compare(row):
    if row['pos_group'] == 4:
        columns = ['Tackle Accuracy', 'Defensive Output', 'Heading', 'Progressive Passing', 'Ball Retention']
        if pd.notna(row['Defending High']):
            columns.append('Defending High')
    elif row['pos_group'] == 3:
        columns = ['Tackle Accuracy', 'Defensive Output', 'Ball Retention', 'Crossing', 'Chance Creation', 'Progression', 'Receiving Forward', 'Heading', 'Carrying']
        if pd.notna(row['Defending High']):
            columns.extend(['Defending High', 'Pressing'])
    elif row['pos_group'] == 6:
        columns = ['Tackle Accuracy', 'Defensive Output', 'Ball Retention', 'Chance Creation', 'Progression', 'Receiving Forward', 'Heading', 'Carrying']
        if pd.notna(row['Defending High']):
            columns.extend(['Defending High', 'Pressing'])
    elif row['pos_group'] in [7, 10]:
        columns = ['Defensive Output', 'Ball Retention', 'Chance Creation', 'Progression', 'Dribbling', 'Poaching', 'Finishing']
    elif row['pos_group'] == 9:
        columns = ['Defensive Output', 'Ball Retention', 'Chance Creation', 'Dribbling', 'Poaching', 'Finishing', 'Heading']
    else:
        columns = ['Ovr']
    return columns

def normalize(series):
    min_val = series.min()
    max_val = series.max()
    if min_val == max_val:
        return pd.Series(1, index=series.index)  # All values are the same
    return (series - min_val) / (max_val - min_val)

def cosine_sim(a, b):
    a = np.array(a).reshape(1, -1)
    b = np.array(b).reshape(1, -1)
    return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))




if mode == 'Player Overview':
    med_mins = 0
    col1, col2 = st.columns(2)
    with col1:
        BestPlayers = df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]

        BestPlayers['Season'] = BestPlayers['Season'].astype(str)
        #filtered_seasons = BestPlayers['Season'][BestPlayers['Season'].str.len() < 8]
        max_season_order = BestPlayers['Season Order'].max()
        BestPlayers = BestPlayers[(BestPlayers['Season Order'] == max_season_order) & (BestPlayers['Season'].str.len() < 8)]
        max_season = BestPlayers['Season'].values[0]



        st.write(f"Best {position_group1} in {max_season} {league1}")
                
        med_mins = np.median(BestPlayers['Minutes'])
        BestPlayers = BestPlayers[BestPlayers['Minutes'] > med_mins].sort_values(by = 'Ovr', ascending=False)[:10]
        i = 1
        for _, row in BestPlayers.iterrows():
            st.write(f"{i}. {row['Player']}  \n({row['Team']} - {row['Age']} - {row['Detailed Position']} - {int(row['Minutes'])} mins)")
            i += 1
    
    
    with col2:
        #print('hiii')
        # Assuming you have position_group2 and league2 defined similarly to col1
        AllPlayers = df[(df['Position Group'] == position_group1) & (df['Competition'] == league1) & (df['Minutes'] > med_mins)]
        #print(len(AllPlayers))

        # Filter for the most recent season
        AllPlayers['Season'] = AllPlayers['Season'].astype(str)
        max_season_order = AllPlayers['Season Order'].max()
        AllPlayers = AllPlayers[(AllPlayers['Season Order'] == max_season_order) & (AllPlayers['Season'].str.len() < 8)]
        max_season = AllPlayers['Season'].values[0]
        # print(len(AllPlayers))
        # print(max_season)

        st.write(f"Most Similar {position_group1} to {name1} in {max_season} {league1}")

        AllPlayers['columns_to_compare'] = AllPlayers.apply(get_columns_to_compare, axis=1)

        def calculate_similarity(player1, player2):
            columns = set(player1['columns_to_compare']) & set(player2['columns_to_compare'])
            st.write(f"Comparing columns: {columns}")
            if not columns:
                return 0
            values1 = player1[columns].values
            values2 = player2[columns].values
            values1_norm = normalize(pd.Series(values1))
            values2_norm = normalize(pd.Series(values2))
            
            return cosine_sim(values1_norm, values2_norm)[0][0]

        
        
        def get_most_similar_players(player_name, n=10):
            player = AllPlayers[AllPlayers['Player'] == player_name].iloc[0]
            similarities = AllPlayers.apply(lambda x: calculate_similarity(player, x), axis=1)
            similar_indices = similarities.sort_values(ascending=False).index[1:n+1]  # Exclude the player itself
            similar_players = AllPlayers.loc[similar_indices]
            return pd.DataFrame({
                'Player': similar_players['Player'],
                'Similarity': similarities[similar_indices],
                'Team': similar_players['Team'],
                'Age': similar_players['Age'],
                'Detailed Position': similar_players['Detailed Position'],
                'Minutes': similar_players['Minutes']
            })
        

       
        similar_players = get_most_similar_players(name1)
        
        for i, (_, row) in enumerate(similar_players.iterrows(), 1):
            similarity_percentage = round(row['Similarity'] * 100, 2)
            st.write(f"{i}. {row['Player']} (Similarity: {similarity_percentage}%)  \n"
                    f"({row['Team']} - {row['Age']} - {row['Detailed Position']} - {int(row['Minutes'])} mins)")
            
        player = AllPlayers[AllPlayers['Player'] == name1].iloc[0] 
    



        




        
        

    

        

        



if mode == 'Team Style':
    st.write("Metric Definitions:")
    st.write("High Pressing: How often they press, counterpress and regain possession in the attacking half, third")
    st.write("Defensive Intensity: How quickly they win the ball back")
    st.write("Defensive Solidity: How few goals, shots, xG, Final Third & Box Entries they concede")
    st.write("Progression: How often they advance the ball to the Final Third")
    st.write("Chance Creation: How often they generate goals, shots, xG")
    st.write("Counter Attacking: Goal and shot creation from counter attacks")
    

if position_group1 == 'CBs' and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Progressive Passing: How often and how accurate the player is at making progressive, long, and final third entry passes")
    st.write("Ball Retention: A measure of how good they are at keeping the ball and not turning it over (passing and dribbling accuracies)")
    st.write("Carrying: Threat added from ball carries")
    st.write("Heading: How often the player wins aerial duels and how accurate they are in them")
    st.write("Defending High: How often the player makes defensive actions in the attacking half [Only available for leagues with StatsBomb data]")
    st.write("Defensive Output: How often the player makes tackles, interceptions, blocks")
    st.write("Tackle Accuracy: Ratio of tackles won per attacker faced")

if position_group1 == 'WBs' and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Chance Creation: Assists, xA, Key Passes, Passes & Crosses Completed into Box")
    st.write("Ball Retention: A measure of how good they are at keeping the ball and not turning it over (passing and dribbling accuracies)")
    st.write("Receiving: How often the player receives the ball in advanced positions")
    st.write("Heading: How often the player wins aerial duels and how accurate they are in them")
    st.write("Defending High: How often the player makes defensive actions in the attacking half [Only available for leagues with StatsBomb data]")
    st.write("Defensive Output: How often the player makes tackles, interceptions, blocks")
    st.write("Tackle Accuracy: Ratio of tackles won per attacker faced")

if position_group1 == 'CMs' and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Ball Retention: A measure of how good they are at keeping the ball and not turning it over (passing and dribbling accuracies)")
    st.write("Chance Creation: Assists, xA, Key Passes, Passes & Crosses Completed into Box")
    st.write("Receiving: How often the player receives the ball in advanced positions")
    st.write("Heading: How often the player wins aerial duels and how accurate they are in them")
    st.write("Pressing: How often the player makes pressure & counterpressure actions, with an emphasis on attacking third pressures [Only available for leagues with StatsBomb data]")
    st.write("Defensive Output: How often the player makes tackles, interceptions, blocks")
    st.write("Tackle Accuracy: Ratio of tackles won per attacker faced")

if (position_group1 == 'AMs' or position_group1 == 'Ws') and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Finishing: Goal Conversion %, xG Over/Underperformance")
    st.write("Poaching: How often the player gets into goalscoring positons (xG, xG/Shot, Touches in Box)")
    st.write("Dribbling Threat: 1v1 Dribbles, Progressive Carries")
    st.write("Chance Creation: Assists, xA, Key Passes, Passes & Crosses Completed into Box")
    st.write("Progression: Player's involvement in moving the ball forward in the buildup via final third and box entry passes, dribbles")
    st.write("Defensive Output: How often the player makes pressures, counterpressures, tackles, interceptions")
    st.write("Heading: How often the player wins aerial duels and how accurate they are in them")

if position_group1 == 'STs' and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Finishing: Goal Conversion %, xG Over/Underperformance")
    st.write("Poaching: How often the player gets into goalscoring positons (xG, xG/Shot, Touches in Box)")
    st.write("Dribbling Threat: 1v1 Dribbles, Progressive Carries")
    st.write("Chance Creation: Assists, xA, Key Passes, Passes & Crosses Completed into Box")
    st.write("Ball Retention: A measure of how good they are at keeping the ball and not turning it over (passing and dribbling accuracies)")
    st.write("Defensive Output: How often the player makes pressures, counterpressures, tackles, interceptions")
    st.write("Heading: How often the player wins aerial duels and how accurate they are in them")
     

#streamlit run streamlit.py