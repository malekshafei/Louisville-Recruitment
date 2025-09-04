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


def get_original_team_name(short_name):
        team_replacements_reverse = {
            "El Paso": "El Paso Locomotive",
            "San Diego": "San Diego Wave",  # Note: this will be the last one due to duplicate
            'Tampa Bay': 'Tampa Bay Rowdies',
            'Sporting KC II': 'Sporting Kansas City II',
            'Loudoun': 'Loudoun United',
            'Memphis': 'Memphis 901',
            'Tacoma': 'Tacoma Defiance',
            'Hartford': 'Hartford Athletic',
            'Birmingham': 'Birmingham Legion',
            'Pittsburgh': 'Pittsburgh Riverhounds',
            'Atlanta II': 'Atlanta United II',
            'Orange County': 'Orange County SC',
            'LouCity': 'Louisville City',
            'NYRB II': 'New York RB II',
            'Union II': 'Philadelphia Union II',
            'Phoenix': 'Phoenix Rising',
            'RGV': 'Rio Grande Valley',
            'LV Lights': 'Las Vegas Lights',
            'New Mexico': 'New Mexico United',
            'Portland II': 'Portland Timbers II',
            'Charlotte Ind.': 'Charlotte Independence',
            'Sacramento': 'Sacramento Republic',
            'Charleston': 'Charleston Battery',
            'Wolfsburg': 'VfL Wolfsburg WFC',
            'Hoffenheim': 'TSG 1899 Hoffenheim',
            'Frankfurt': 'Eintracht Frankfurt',
            'Bayer 04': 'TSV Bayer 04 Leverkusen',
            'Gotham': 'NJ NY Gotham FC',
            'NC Courage': 'North Carolina Courage',
            'Seattle': 'Seattle Reign',
            'Orlando': 'Orlando Pride',
            'Washington': 'Washington Spirit',
            'Chicago': 'Chicago Red Stars',
            'Portland': 'Portland Thorns',  # Note: this will overwrite Portland II
            'Racing': 'Racing Louisville FC',
            'Utah': 'Utah Royals'
        }
        
        return team_replacements_reverse.get(short_name, short_name)


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

regular_font_path = 'Montserrat-Regular.ttf'
bold_font_path = 'Montserrat-Bold.ttf'

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
pos_list = ['CBs', 'WBs', 'CMs', 'AMs', 'Ws', 'STs', 'GKs']

#st.title(f"Racing Recruitment")

#st.dataframe(df)




mode = st.selectbox("Select Mode", options=['Player Overview', 'Multi Player Dot Graph', 'Player Rankings',  'Team Style'])

if mode == 'Player Overview':


    # file_name = 'InternationalWomensData.xlsx'
    # df = pd.read_excel(file_name)
    #df = df[df['Detailed Position'] != 'GK'].sort_values(by = ['Season Order', 'Minutes'], ascending=[False, False])
    df = df.sort_values(by = ['Season Order', 'Minutes'], ascending=[False, False])

    
    #df['Position Group'] = df['pos_group']




    position_group1 = st.selectbox("Select Position Group", options=pos_list)
    #df = df[df['Position Group'] == position_group1]
    # if position_group1 in ['AMs', 'Ws']: 
    #     df = df[(df['Position Group'] == 'AMs') | (df['Position Group'] == 'Ws')]
    #     df = df.sort_values(by = ['Season','Minutes'], ascending=[False,False])
    #     df = df.drop_duplicates(subset=['Player', 'Season'])
        
    #     #df = df.drop_duplicates(subset=['Player', 'Season'])

    # else: df = df[df['Position Group'] == position_group1]
    df = df[df['Position Group'] == position_group1]

    df = df.drop_duplicates(subset=['Player', 'Season', 'Position Group', 'Competition'])


    # for pos in pos_list:
    #     new_data = pd.read_excel(file_name, sheet_name=pos)
    #     new_data['Position Group'] = pos
    #     #df = pd.concat([df,new_data], ignore_index = True)

    radar = True
    compare = "No"
    # league1 = st.selectbox("Select League", options=['NWSL', 'Mexico', 'Brazil','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden', 'France', 'China', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL Super League', 'USL', 'MLS', 'MLS Next Pro', 'USL League One', 'NCAA Men', 'Canada' ])
    # name1 = st.selectbox("Select Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique())
    # season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True))
    col1, col2, col3 = st.columns(3)
    with col1:
        league1 = st.selectbox(
            'Select League',
            ['USL', 'NWSL', 'NCAA Women','Mexico', 'Brazil','France','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden', 'China', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL Super League', 'Olympics', 'U20 World Cup', 'U19Euros', 'CONCACAF W Champions League', 'CAF W Champions League', 'MLS', 'MLS Next Pro', 'USL League One', 'NCAA Men', 'Canada', 'ScotlandMen' ]
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
        
        if position_group1 == 'GKs': mode1 = st.selectbox("Select Radar Type", options=["Basic"])
        elif position_group1 == 'CMs': mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Defending', 'Buildup & Chance Creation', 'Box Threat', 'Physical'])

        elif position_group1 == 'CBs': mode1 = st.selectbox("Select Radar Type", options=["Basic", 'In Possession', 'Defending', 'Physical'])
        elif position_group1 in ['AMs', 'Ws', 'STs']: mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Threat Creation', 'Shooting', 'Out of Possession', 'Physical'])

        else: mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Attacking', 'Defending', 'Physical'])

    
    if mode1 == 'Match by Match Overview': radar = False

 
    

    if radar == True:
        with col2:
            compare = st.selectbox("Compare with another player?", options=["No", 'Yes'])


        if compare == 'Yes':
            col1, col2, col3 = st.columns(3)
            with col1: league2 = st.selectbox("Select other League", options=['USL', 'NWSL', 'NCAA Women','Mexico', 'Brazil','France','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden', 'China', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL Super League', 'Olympics', 'U20 World Cup', 'U19Euros', 'CONCACAF W Champions League', 'CAF W Champions League', 'MLS', 'MLS Next Pro', 'USL League One', 'NCAA Men', 'Canada', 'ScotlandMen' ])
            with col2: 
                #name2 = st.selectbox("Select other Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league2)]['Player'].unique())
                name2 = st.selectbox("Select other Player", options=df[(df['Competition'] == league2)]['Player'].unique())
            with col3: 
                #season2 = st.selectbox("Select other season", options=sorted(df[(df['Competition'] == league2) & (df['Position Group'] == position_group1) & (df['Player'] == name2)]['Season'].unique(), reverse=True))
                season2 = st.selectbox("Select other season", options=sorted(df[(df['Competition'] == league2)  & (df['Player'] == name2)]['Season'].unique(), reverse=True))

        ws_leagues = ['NCAA Women', 'U20 World Cup', 'U19Euros', 'CONCACAF W Champions League', 'CAF W Champions League','France', 'China', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL Super League', 'USL League One', 'NCAA Men', 'Canada' ]

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
        if position_group1 == 'GKs' and mode1 == 'Basic':
            GK_Chances_Faced = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'GK_Chances Faced']
            GK_Shot_Stopping = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'GK_Shot Stopping']
            GK_Short_Distribution = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'GK_Short Distribution']
            GK_Long_Distribution = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'GK_Long Distribution']
            GK_Defending_High = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'GK_Defending High']
            GK_Difficult_Shot_Stopping = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'GK_Difficult Shot Stopping']
            GK_1v1_Saves = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'GK_1v1 Saves']


            data1 = [GK_Chances_Faced, GK_Shot_Stopping, GK_Short_Distribution, GK_Long_Distribution, GK_Defending_High, GK_Difficult_Shot_Stopping, GK_1v1_Saves]
            #if league1 in ws_leagues: data1 = [Heading, Carrying, BallRetention, ProgressivePassing, DefAccuracy, DefEngage, 0]
            metrics = ['Chances Faced', 'Shot Stopping', 'Short Distribution', 'Long Distribution', 'Defending High', 'Difficult Shot Stopping', '1v1 Saving']
            metric_names = ['Chances Faced', 'Shot Stopping', 'Short Distribution', 'Long\nDistribution', 'Defending High', 'Difficult Shot Stopping', '1v1 Saving']

            if compare == 'Yes':
                GK_Chances_Faced2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'GK_Chances Faced']
                GK_Shot_Stopping2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'GK_Shot Stopping']
                GK_Short_Distribution2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'GK_Short Distribution']
                GK_Long_Distribution2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'GK_Long Distribution']
                GK_Defending_High2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'GK_Defending High']
                GK_Difficult_Shot_Stopping2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'GK_Difficult Shot Stopping']
                GK_1v1_Saves2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'GK_1v1 Saves']


                data2 = [GK_Chances_Faced2, GK_Shot_Stopping2, GK_Short_Distribution2, GK_Long_Distribution2, GK_Defending_High2, GK_Difficult_Shot_Stopping2, GK_1v1_Saves2]
                #if league2 in ws_leagues: data2 = [Heading2, Carrying2, BallRetention2, ProgressivePassing2, DefAccuracy2, DefEngage2, 0]

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
            #print(name1, Progression)
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


        if (position_group1 == 'CBs' or position_group1 == 'WBs' or position_group1 == 'CMs' or position_group1 == 'Ws' or position_group1 == 'AMs' or position_group1 == 'STs') and mode1 == "Physical":
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTop Speed']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctDistance'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctHI Distance'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctHI Count'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctSprinting Distance'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctSprint Count'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pct% of Distance HI'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            #if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, Interceptions, 0, 0, 0,0]
            metrics = ['Top Speed', 'Distance', 'HI Distance', 'HI Actions','Sprint Dist.','Sprints', '% of Dist. HI']
            metric_names = ['Top Speed', 'Distance', 'HI Distance', 'HI Actions','Sprint Dist.','Sprints', '% of Dist HI']

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTop Speed']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctDistance'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctHI Distance'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctHI Count'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctSprinting Distance'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctSprint Count'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pct% of Distance HI'])


                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]
                #if league2 in ws_leagues: data2 = [TacklesWon2, TacklePct2, Interceptions2, 0, 0, 0,0]
                
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


        df = df.reset_index()
        #print(name1)
        club = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Team']
        #print(club)
        mins = int(df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Minutes'])

       
            
        detailed_pos = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Detailed Position']
        


        if compare == 'No':
            plt.text(800,70,f"{name1}",ha = 'center', fontsize=45, color = 'white', fontweight = 'bold')
            plt.text(800,120,f"{club} - {season1} {league1} - {mins} Minutes - {detailed_pos}",ha = 'center', fontsize=30, color = 'white')#, fontname='Avenir')
            plt.text(30,880,f"Data compared to {league1} {position_group1} in {season1}",ha = 'left', fontsize=16, color = 'white')#, fontname='Avenir')

            if league1 in ws_leagues and mode1 == 'Basic' and position_group1 == 'GKs': plt.text(1570,880,f"Defending High, Difficult & 1v1 Shot Stopping\ndata unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
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
            if league1 in ws_leagues and league2 in ws_leagues and mode1 == 'Basic' and position_group1 == 'GKs': plt.text(1570,880,f"Defending High, Difficult & 1v1 Shot Stopping\ndata unavailable",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')

            elif league1 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            elif league2 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league2}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            elif league1 in ws_leagues and  mode1 == 'Basic' and position_group1 == 'GKs': plt.text(1570,880,f"Defending High, Difficult & 1v1 Shot Stopping\ndata unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            elif league2 in ws_leagues and  mode1 == 'Basic' and position_group1 == 'GKs': plt.text(1570,880,f"Defending High, Difficult & 1v1 Shot Stopping\ndata unavailable for {league2}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            
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

            
        st.image(buf, use_container_width=True)


    
if mode == 'Team Style':
    file_name = 'InternationalWomensTeamLevelData.xlsx'
    df = pd.read_excel(file_name)
    position_group1 = 'NA'


    radar = True
    compare = "No"
    league1 = st.selectbox("Select League", options=['USL', 'NWSL', 'Mexico', 'Brazil','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden',  'MLS', 'MLS Next Pro', 'ScotlandMen'])
    name1 = st.selectbox("Select Team", options=df[(df['Competition'] == league1)]['Team'].unique())
    season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition'] == league1) & (df['Team'] == name1)]['Season'].unique(), reverse=True))

    if radar == True:
        compare = st.selectbox("Compare with another Team?", options=["No", 'Yes'])

        if compare == 'Yes':
            league2 = st.selectbox("Select other League", options=['USL', 'NWSL', 'Mexico', 'Brazil','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden', 'ScotlandMen'])
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

        
    st.image(buf, use_container_width=True)





if  mode == 'Multi Player Dot Graph':
    pos_list = pos_list = ['CBs', 'WBs', 'CMs', 'AMs', 'Ws', 'STs', 'GKs']

    #df['Position Group'] = df['pos_group']




    position_group1 = st.selectbox("Select Position Group", options=pos_list)
    # if position_group1 in ['AMs', 'Ws']: 
    #     df = df[(df['Position Group'] == 'AMs') | (df['Position Group'] == 'Ws')]
    #     df = df.sort_values(by = ['Season','Minutes'], ascending=[False,False])
    #     df = df.drop_duplicates(subset=['Player', 'Season'])
    # else: df = df[df['Position Group'] == position_group1]
    df = df[df['Position Group'] == position_group1]
    df = df.drop_duplicates(subset=['Player', 'Season', 'Position Group', 'Competition'])

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

    
    

    # league1 = st.selectbox("Select League", options=['NWSL', 'Mexico', 'Brazil','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden', 'France', 'China', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL Super League', 'USL', 'MLS', 'MLS Next Pro', 'USL League One', 'NCAA Men', 'Canada' ])
    # name1 = st.selectbox("Select Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique())
    # season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True))

    col1, col2, col3 = st.columns(3)
    with col1:
        league1 = st.selectbox(
            'Select League #1',
            ['USL', 'NWSL', 'NCAA Women','Mexico', 'Brazil','France','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden', 'China', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL Super League', 'Olympics', 'U20 World Cup', 'U19Euros', 'CONCACAF W Champions League', 'CAF W Champions League', 'MLS', 'MLS Next Pro', 'USL League One', 'NCAA Men', 'Canada', 'ScotlandMen' ]
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
            ['USL', 'NWSL', 'NCAA Women','Mexico', 'Brazil','France','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden', 'China', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL Super League', 'Olympics', 'U20 World Cup', 'U19Euros', 'CONCACAF W Champions League', 'CAF W Champions League', 'MLS', 'MLS Next Pro', 'USL League One', 'NCAA Men', 'Canada', 'ScotlandMen' ]
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
            ['USL', 'NWSL', 'NCAA Women','Mexico', 'Brazil','France','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden', 'China', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL Super League', 'Olympics', 'U20 World Cup', 'U19Euros', 'CONCACAF W Champions League', 'CAF W Champions League', 'MLS', 'MLS Next Pro', 'USL League One', 'NCAA Men', 'Canada', 'ScotlandMen' ]
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
            ['USL', 'NWSL', 'NCAA Women','Mexico', 'Brazil','France','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden', 'China', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL Super League', 'Olympics', 'U20 World Cup', 'U19Euros', 'CONCACAF W Champions League', 'CAF W Champions League', 'MLS', 'MLS Next Pro', 'USL League One', 'NCAA Men', 'Canada', 'ScotlandMen' ]
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

    if position_group1 == 'GKs': metrics = ['GK_Chances Faced', 'GK_Shot Stopping','GK_Short Distribution', 'GK_Long Distribution','GK_Difficult Shot Stopping']
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

        
    st.image(buf, use_container_width=True)
    radar = True
    position_group1 = 'NA'

if mode == 'Player Rankings':
    import matplotlib.font_manager as font_manager
    from matplotlib import font_manager, rcParams

    font_manager.fontManager.addfont(regular_font_path)
    font_manager.fontManager.addfont(bold_font_path)
    rcParams['font.family'] = 'Montserrat'
    mode1 = 'Basic'

    file_name = 'InternationalWomensData.parquet'
    df = pd.read_parquet(file_name)
    
    
    df = df[df['Competition'].isin(['USL', 'NWSL'])].sort_values(by = 'Ovr', ascending=False)

    df['Top Speed'] = df['pctTop Speed']
    df['HI Distance'] = (0.3 * df['pctHI Count']) + (0.4 * df['pctDistance']) + (0.3 * df['pctHI Distance'])

    df = df.rename(columns={'GK_Chances Faced': 'Chances Faced',
                            'GK_Shot Stopping':'Shot Stopping',
                            'GK_Short Distribution':'Short Distribution',
                            'GK_Long Distribution':'Long Distribution',
                            'GK_Defending High':'Coming Off Line',
                            'GK_Difficult Shot Stopping':'Difficult Shot Stopping',
                            'GK_1v1 Saves':'1v1 Saves',
                            'Detailed Position': 'Position'
                        })


    value_cols = ['Ovr', 'Tackle Accuracy', 'Defensive Output', 'Defending High',
       'Heading', 'Receiving Forward', 'Crossing', 'Progressive Passing',
       'Carrying', 'Ball Retention', 'Chance Creation', 'Progression',
       'Pressing', 'Dribbling', 'Poaching', 'Finishing', 'Top Speed', 'HI Distance',
       'Chances Faced','Shot Stopping', 'Short Distribution', 'Long Distribution',
       'Coming Off Line', 'Difficult Shot Stopping', '1v1 Saves']
    
    all_cols = ['Player', 'Team', 'Competition', 'Age', 'Minutes', 'Position Group', 'Position', 'Season', 'Season Order'] + value_cols

    df = df[all_cols]

    for col in df.columns: print(col)

    for col in value_cols:
        
        if col == 'Ovr': df[col] = round(df[col],1)
        else:
            df=df.fillna(0) 
            df[col] = df[col].astype(int)




    df = df[pd.notna(df['Team']) & (df['Team'] != 0) & (df['Team'] != '0') ]
    col1, col2, col3 = st.columns(3)

    with col1: 
        leagues = st.segmented_control("League", ['NWSL', 'USL'], default='USL')
        df = df[(df['Competition'] == leagues)]

        age_range = st.slider("Age Range", 15, 40, (15,30))
        df = df[((df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])) | (pd.isna(df['Age']))]

        create_ratings = st.segmented_control("Customize Rating Weights?", ["Yes", "No"], default = "No")


    with col2: 
        position_group1 = st.selectbox("Select Position Group", options=pos_list)
        df = df[(df['Position Group'] == position_group1)]
        df = df[~df['Season'].str.contains('-', na=False)]
        df = df[df['Season Order'] == df.groupby('Competition')['Season Order'].transform('max')]

        
        minutes_range = st.slider("Minutes Played Range", 0, max(df['Minutes']), (800, max(df['Minutes'])))
        df = df[(df['Minutes'] >= minutes_range[0]) & (df['Minutes'] <= minutes_range[1])]
    
    with col3: 
        
        spec_position = st.pills("Select Primary Positions",sorted(df['Position'].unique()), selection_mode='multi',default = df['Position'].unique())

        num_shown = st.segmented_control("# Players to Show", ["10", "15", "25", "All"],default = "15" )
    
        
    
    if create_ratings == 'Yes':
        if position_group1 == 'GKs':
            ratings = ['Chances Faced','Shot Stopping', 'Short Distribution', 'Long Distribution',
                        'Coming Off Line', 'Difficult Shot Stopping', '1v1 Saves']
        if position_group1 == 'CBs':
            ratings = ['Tackle Accuracy', 'Defensive Output', 'Defending High',
                         'Progressive Passing', 'Carrying', 'Ball Retention', 'Heading',
                          'Top Speed', 'HI Distance']
            
        if position_group1 == 'WBs':
            ratings = ['Tackle Accuracy', 'Defensive Output', 'Defending High',
                       'Pressing', 'Heading', 
                       'Ball Retention', 'Progression', 'Carrying',
                       'Receiving Forward', 'Crossing', 'Chance Creation',
                        'Top Speed', 'HI Distance']
            
        if position_group1 == 'CMs':
            ratings = ['Tackle Accuracy', 'Defensive Output', 'Defending High',
                       'Pressing', 'Heading', 
                       'Ball Retention', 'Progression', 'Carrying',
                       'Receiving Forward', 'Chance Creation',
                        'Top Speed', 'HI Distance']
            
        if position_group1 in ['AMs', 'Ws']:
            ratings = ['Chance Creation', 'Dribbling', 'Progression',
                       'Poaching', 'Finishing', 'Ball Retention',
                       'Crossing','Heading',  'Defensive Output',
                        'Top Speed', 'HI Distance'
                      ]
        if position_group1 == 'STs':
            ratings = ['Poaching', 'Finishing', 'Heading',
                       'Chance Creation', 'Dribbling', 'Progression'
                       'Ball Retention', 'Defensive Output',
                       'Top Speed', 'HI Distance'
                       
                      ]

                         
            
                
            
        weights = {}
        col1, col2, col3 = st.columns(3)
        ind = 0
        with col1:
            for x in ratings[::3]:
                #xx = st.slider(x,0,100,value = 50, key=x)
                weights[x] = st.slider(x,0,100,value = 50)
                ind+=1
        with col2:
            for x in ratings[1::3]:
                #xx = st.slider(x,0,100,value = 50, key=x)
                weights[x] = st.slider(x,0,100,value = 50)
                ind+=1
        with col3:
            for x in ratings[2::3]:
                #xx = st.slider(x,0,100,value = 50, key=x)
                weights[x] = st.slider(x,0,100,value = 50)
                ind+=1


        print(weights)
        total = sum(weights.values())
        normalized = {k: v / total * 100 for k, v in weights.items()}
        df['Ovr'] = round(sum(df[col] * (normalized[col]*.01) for col in normalized),1)
        df = df.sort_values(by = 'Ovr', ascending=False)

    df.insert(0, "Rank", range(1, len(df) + 1))


    data_copy = df.copy(deep=True)


            
            
            
        
    

    

    

    if num_shown == "5": df = df.head(5)
    elif num_shown == "10": df = df.head(10)
    elif num_shown == "15": df = df.head(15)
    elif num_shown == "25": df = df.head(25)
    elif num_shown == "All": df = df.copy(deep=True)
    
    #st.write(df)


    columns = ["Rank","Player", "Position","Minutes", "Age", "Ovr"]

    

    def create_football_table(data, columns):
        # ---- Figure & layout (fixes: subtitle whitespace) ----
        fig, ax = plt.subplots(figsize=(14, 12))
        # We'll control margins explicitly; avoid tight_layout which can add unpredictable gaps with tables.
        fig.set_constrained_layout(False)
        fig.subplots_adjust(left=0.02, right=0.98, bottom=0.06, top=0.90)

        # Titles sit in the top figure margin; table lives entirely inside the axes.
        title = f'Top {position_group1} - Data Ranking'
        subtitle = f'{leagues} | Age: {age_range[0]}-{age_range[1]} | Minutes: {minutes_range[0]}-{minutes_range[1]}'
        fig.suptitle(title, fontsize=24, fontweight='bold', y=0.965)
        fig.text(0.5, 0.92, subtitle, ha='center', va='center', fontsize=14, color='black')

        ax.axis('off')

        data_df = pd.DataFrame(data, columns=columns)

        # ---- Table ----
        table = ax.table(
            cellText=data_df.values,
            colLabels=data_df.columns,
            cellLoc='center',
            loc='center',
            bbox=[0.00, 0.00, 1.00, 1.00]  # Fill the axes; margins come from subplots_adjust above
        )

        # Basic styling
        table.auto_set_font_size(False)
        table.set_fontsize(14)
        table.scale(1, 2)

        # Remove borders
        for _, cell in table.get_celld().items():
            cell.set_linewidth(0)
            cell.set_edgecolor('none')


        

        # Header styling
        ncols = len(data_df.columns)
        for j in range(ncols):
            cell = table[(0, j)]
            cell.set_facecolor('#E8E8E8')
            cell.set_text_props(weight='bold', color='black')
            cell.set_height(0.08)

        # Data rows
        nrows = len(data_df)
        for i in range(1, nrows + 1):
            for j in range(ncols):
                c = table[(i, j)]
                c.set_facecolor('white')
                if j == ncols - 1:
                    c.set_facecolor('#E6E1F0')  # last column
                if j == 1:
                    c.set_text_props(ha='left')
                    #c.get_text().set_x(0.15)  # space for logo

                    if nrows < 4:
                        table[(i, 1)].PAD = 0.45
                    elif nrows < 8:
                        table[(i, 1)].PAD = 0.35
                    elif nrows < 12:
                        table[(i, 1)].PAD = 0.3
                    else: table[(i, 1)].PAD = 0.25

                c.set_height(0.06)
                c.set_text_props(color='black')

        col_widths = {
            "Rank": 0.05,
            "Player": 0.25,
            "Position": 0.2,
            "Minutes": 0.10,
            "Age": 0.10,
            "Ovr": 0.12
        }

        # Apply widths to all cells in that column
        for j, col in enumerate(data_df.columns):
            for i in range(nrows + 1):  # +1 to include header row
                cell = table[(i, j)]
                cell.set_width(col_widths.get(col, 0.1))

        # Force draw to get real positions
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        # ---- Logos (fixes: y positioning) ----
        # Place logos using the *figure* coordinate system, derived from each first-column cell bbox.
        for i in range(1, nrows + 1):
            player_name = data_df.iloc[i - 1, 1]
            try:
                team_name = df.loc[df['Player'] == player_name, 'Team'].iloc[0]
                logo_path = f"Club Logos/{get_original_team_name(team_name)}.webp"
                img = plt.imread(logo_path)

                # Bbox of the (i, 0) cell in *figure* coordinates
                cell_disp = table[(i, 1)].get_window_extent(renderer)
                cell_fig = cell_disp.transformed(fig.transFigure.inverted())

                # Make a square logo that fits the cell height; small left padding
                
                pad = cell_fig.height * 0.10
                if nrows < 2: size = cell_fig.height * 0.2
                if nrows < 5: size = cell_fig.height * 0.40
                else: 
                    size = cell_fig.height * 0.80
                logo_left = cell_fig.x0 + pad
                logo_bottom = cell_fig.y0 + (cell_fig.height - size) / 2

                # Create an overlay axes exactly where we want the logo
                logo_ax = fig.add_axes([logo_left, logo_bottom, size, size])
                logo_ax.imshow(img)
                logo_ax.axis('off')
            except FileNotFoundError:
                print(f"Logo not found for {player_name}: {logo_path}")
            except Exception as e:
                print(f"Error loading logo for {player_name}: {e}")

        # ---- Row separators (fixes: incorrect placement/omissions) ----
        # Draw a thin line under every data row except the last, using each row's true bottom y.
        # We'll align lines to the full table width (from first to last column).
        first_left_disp = table[(1, 0)].get_window_extent(renderer).x0
        last_right_disp = table[(1, ncols - 1)].get_window_extent(renderer).x1
        left_fig = fig.transFigure.inverted().transform((first_left_disp, 0))[0]
        right_fig = fig.transFigure.inverted().transform((last_right_disp, 0))[0]

        for i in range(1, nrows):  # separators between data rows
            row_bottom_fig_y = table[(i, 0)].get_window_extent(renderer)
            row_bottom_fig_y = row_bottom_fig_y.transformed(fig.transFigure.inverted()).y0
            line = plt.Line2D([left_fig, right_fig],
                            [row_bottom_fig_y, row_bottom_fig_y],
                            color='#DDDDDD', linewidth=0.9, alpha=0.9,
                            transform=fig.transFigure, zorder=2)
            fig.add_artist(line)

        # ---- Footer ----
        # ax.text(0.98, 0.01, "Test", transform=ax.transAxes,
        #         ha='right', va='bottom', fontsize=10, color='gray')

        return fig, ax, table


    

    # Create the table
    fig, ax, table = create_football_table(df, columns)
    #plt.show()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2)
    #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

    buf.seek(0)
        
    st.image(buf, use_container_width=True)
    
    
    
    if position_group1 == 'GKs':
        ratings = ['Chances Faced','Shot Stopping', 'Short Distribution', 'Long Distribution',
                        'Coming Off Line', 'Difficult Shot Stopping', '1v1 Saves']
    if position_group1 == 'CBs':
        ratings = ['Tackle Accuracy', 'Defensive Output', 'Defending High',
                        'Progressive Passing', 'Carrying', 'Ball Retention', 'Heading',
                        'Top Speed', 'HI Distance']
        
    if position_group1 == 'WBs':
        ratings = ['Tackle Accuracy', 'Defensive Output', 'Defending High',
                    'Pressing', 'Heading', 
                    'Ball Retention', 'Progression', 'Carrying',
                    'Receiving Forward', 'Crossing', 'Chance Creation',
                    'Top Speed', 'HI Distance']
        
    if position_group1 == 'CMs':
        ratings = ['Tackle Accuracy', 'Defensive Output', 'Defending High',
                    'Pressing', 'Heading', 
                    'Ball Retention', 'Progression', 'Carrying',
                    'Receiving Forward', 'Chance Creation',
                    'Top Speed', 'HI Distance']
        
    if position_group1 in ['AMs', 'Ws']:
        ratings = ['Chance Creation', 'Dribbling', 'Progression',
                    'Poaching', 'Finishing', 'Ball Retention',
                    'Crossing','Heading',  'Defensive Output',
                    'Top Speed', 'HI Distance'
                    ]
    if position_group1 == 'STs':
        ratings = ['Poaching', 'Finishing', 'Heading',
                    'Chance Creation', 'Dribbling', 'Progression'
                    'Ball Retention', 'Defensive Output',
                    'Top Speed', 'HI Distance'
                    
                    ]
        
    selected_cols =  ["Rank","Player", "Team", "Position","Minutes", "Age", "Ovr"] + ratings
    data_copy = data_copy[selected_cols]
   # st.write(data_copy, ind)
    st.dataframe(data_copy, hide_index=True)
    # Example with custom data and columns
    

    # position_group1 = 'CBs'
    # mode1 = ''

    # # URL of your Tableau dashboard (can be from Tableau Public or Server)
    # import streamlit.components.v1 as components

    # # Replace this with your Tableau Public embed link (copied from the "Embed Code" section)
    # tableau_embed_code = """
    # <div class='tableauPlaceholder' id='viz1733282530187' style='position: relative'>
    #     <noscript>
    #         <a href='#'>
    #             <img alt='Dashboard 1' src='https://public.tableau.com/static/images/Lo/LouisvillePlayerData/Dashboard1/1_rss.png' style='border: none' />
    #         </a>
    #     </noscript>
    #     <object class='tableauViz' style='display:none;'>
    #         <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
    #         <param name='embed_code_version' value='3' />
    #         <param name='site_root' value='' />
    #         <param name='name' value='LouisvillePlayerData/Dashboard1' />
    #         <param name='tabs' value='no' />
    #         <param name='toolbar' value='yes' />
    #         <param name='static_image' value='https://public.tableau.com/static/images/Lo/LouisvillePlayerData/Dashboard1/1.png' />
    #         <param name='animate_transition' value='yes' />
    #         <param name='display_static_image' value='yes' />
    #         <param name='display_spinner' value='yes' />
    #         <param name='display_overlay' value='yes' />
    #         <param name='display_count' value='yes' />
    #         <param name='language' value='en-US' />
    #     </object>
    # </div>

    # <script type='text/javascript'>
    #     var divElement = document.getElementById('viz1733282530187');
    #     var vizElement = divElement.getElementsByTagName('object')[0];
    #     if ( divElement.offsetWidth > 800 ) {
    #         vizElement.style.width='1220px';
    #         vizElement.style.minHeight='587px';
    #         vizElement.style.maxHeight='887px';
    #         vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
    #     } else if ( divElement.offsetWidth > 500 ) {
    #         vizElement.style.width='1220px';
    #         vizElement.style.minHeight='587px';
    #         vizElement.style.maxHeight='887px';
    #         vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
    #     } else {
    #         vizElement.style.width='100%';
    #         vizElement.style.height='727px';
    #     }
    #     var scriptElement = document.createElement('script');
    #     scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
    #     vizElement.parentNode.insertBefore(scriptElement, vizElement);
    # </script>
    # """ 
    # tableau_embed_code = """
    # <div class='tableauPlaceholder' id='viz1733283562119' style='position: relative'><noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Lo&#47;LouisvillePlayerData&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='LouisvillePlayerData&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Lo&#47;LouisvillePlayerData&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1733283562119');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='504px';vizElement.style.maxWidth='774px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='504px';vizElement.style.maxWidth='774px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='887px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    # """
    # # Embed the Tableau dashboard using st.components.v1.html
    # components.html(tableau_embed_code, height=600)

    


if mode == 'Player Match by Match Performance':
    mode1 = 'NA'
    position_group1 = 'CBs'
    df = pd.read_parquet("InternationalWomensMatchLevelData.parquet")

    pos_map_2 = {
    1: 'GKs',
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
            ['NWSL', 'Olympics', 'Mexico', 'Brazil','England', 'England2', 'Germany2', 'Spain2', 'Spain', 'Germany', 'Sweden', 'USL', 'MLS', 'MLS Next Pro', 'ScotlandMen']
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

        
    st.image(buf, use_container_width=True)

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
    series = pd.to_numeric(series, errors='coerce')  # Convert to numeric, forcing non-numeric values to NaN
    min_val = series.min()
    max_val = series.max()
    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return pd.Series(1, index=series.index)  # All values are the same or all NaN
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
        player_row = df[(df['Season'] == season1) & (df['Position Group'] == position_group1) & (df['Competition'] == league1) & (df['Player'] == name1)]
        AllPlayers = df[(df['Position Group'] == position_group1) & (df['Competition'] == league1) & (df['Minutes'] > med_mins)]
        

        #print(len(AllPlayers))

        # Filter for the most recent season
        AllPlayers['Season'] = AllPlayers['Season'].astype(str)
        max_season_order = AllPlayers['Season Order'].max()
        AllPlayers = AllPlayers[(AllPlayers['Season Order'] == max_season_order) & (AllPlayers['Season'].str.len() < 8)]
        AllPlayers = pd.concat([AllPlayers, player_row]).drop_duplicates(subset=['Player', 'Season'])
        max_season = AllPlayers['Season'].values[0]
        # print(len(AllPlayers))
        # print(max_season)

        st.write(f"Most Similar {position_group1} to {name1} in {max_season} {league1}")

        AllPlayers['columns_to_compare'] = AllPlayers.apply(get_columns_to_compare, axis=1)

        def calculate_similarity(player1, player2):
            columns = list(set(player1['columns_to_compare']) & set(player2['columns_to_compare']))
            if not columns:
                return 0
            values1 = player1[columns].values
            values2 = player2[columns].values
            values1_norm = normalize(pd.Series(values1))
            values2_norm = normalize(pd.Series(values2))
            
            return cosine_sim(values1_norm, values2_norm)[0][0]

        
        
        def get_most_similar_players(player_name, n=10):
            player_rows = AllPlayers[AllPlayers['Player'] == player_name]
            if player_rows.empty:
                st.error(f"Player {player_name} not found in the dataset.")
                return pd.DataFrame()
            
            player = player_rows.iloc[0]
            
            # Check for NAs in the player's data
            na_columns = player[player['columns_to_compare']].isna().sum()
            if na_columns > 0:
                st.warning(f"Player {player_name} has {na_columns} NA values in their data.")
            
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
   
   

if position_group1 == 'GKs' and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Chances Faced: Measure of how often the goalkeeper is tested (and how high quality the chances are)")
    st.write("Shot Stopping: Measure of shot stopping quality (xG Faced - Goals Conceded, Save %, etc)")
    st.write("Short Distribution: How accurate the goalkeeper is in short passing and how often he is trusted to play out the back")
    st.write("Long Distribution: How accurate and (how frequently) the goalkeeper is in long/progressive passing")
    st.write("Defending High: How high up the field the goalkeeper makes defensive actions like rushes, pressures, saves on average")
    st.write("Difficult Shot Stopping: How well the goalkeeper does with facing high xG shots")
    st.write("1v1 Saving: RHow well the goalkeeper does with facing 1v1 opportounities")

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