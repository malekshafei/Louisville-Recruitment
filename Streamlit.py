import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import io
import warnings
warnings.filterwarnings('ignore')



st.set_page_config( 
    page_title="Racing Recruitment",
    page_icon=":checkered_flag:",
    layout="centered",
    initial_sidebar_state="expanded",
   
    
)
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

#st.title(f"Racing Recruitment")

#st.dataframe(df)




file_name = 'InternationalWomensData.xlsx'
df = pd.read_excel(file_name)
pos_list = ['CBs', 'WBs', 'CMs', 'AMs', 'Ws', 'STs']
#df['Position Group'] = df['pos_group']




position_group1 = st.selectbox("Select Position Group", options=pos_list)
df = df[df['Position Group'] == position_group1]


# for pos in pos_list:
#     new_data = pd.read_excel(file_name, sheet_name=pos)
#     new_data['Position Group'] = pos
#     #df = pd.concat([df,new_data], ignore_index = True)

compare = "No"
league1 = st.selectbox("Select League", options=['NWSL', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL' ])
name1 = st.selectbox("Select Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique())
season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True))

if position_group1 == 'CMs': mode1 = st.selectbox("Select Mode", options=["Basic", 'Defending', 'Buildup & Chance Creation', 'Box Threat'])

elif position_group1 == 'CBs': mode1 = st.selectbox("Select Mode", options=["Basic", 'In Possession', 'Defending'])
elif position_group1 in ['AMs', 'Ws', 'STs']: mode1 = st.selectbox("Select Mode", options=["Basic", 'Threat Creation', 'Shooting', 'Out of Possession'])

else: mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Attacking', 'Defending'])
compare = st.selectbox("Compare with another player?", options=["No", 'Yes'])

if compare == 'Yes':
    league2 = st.selectbox("Select other League", options=['NWSL', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL' ])
    name2 = st.selectbox("Select other Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league2)]['Player'].unique())
    season2 = st.selectbox("Select other season", options=sorted(df[(df['Competition'] == league2) & (df['Position Group'] == position_group1) & (df['Player'] == name2)]['Season'].unique(), reverse=True))


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




if position_group1 == 'CBs' and mode1 == 'Defending':
        
    TacklePct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctTackle %']
    Tackles = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctTackles Won']
    Interceptions = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctInterceptions']
    Blocks = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctBlocks']
    Headers = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAerial Wins']
    AerialPct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAerial %']
    DefThirdTacklePct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctDefensiveThirdTackle%']


    data1 = [TacklePct, Tackles, Interceptions, Blocks, Headers, AerialPct, DefThirdTacklePct]
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


if position_group1 == 'WBs' and mode1 == 'Defending':
        
    TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackles Won']) 
    TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackle %'])
    DefThirdTackles = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctDefensive Third Tackles Won'])
    DefThirdTacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctDefensiveThirdTackle%'])
    Intercepts = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctInterceptions'])
    Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPressures'])
    AttThirdPressures = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAttacking Third Pressures']
    
    data1 = [TacklesWon, TacklePct, DefThirdTackles, DefThirdTacklePct, Intercepts, Pressures,AttThirdPressures]
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


if position_group1 == 'WBs' and mode1 == 'Attacking':
        
    KeyPasses = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctKey Passes']) 
    Crosses = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctCrosses Completed into Box'])
    PassesIntoBox = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPasses into Box'])
    xA = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctxA'])
    Assists = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAssists'])
    FinalThirdTouches = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctFinal Third Receptions'])
    TakeOns = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'1v1 Dribbles Completed']
    
    data1 = [KeyPasses, Crosses, PassesIntoBox, xA, Assists, FinalThirdTouches,TakeOns]
    metrics = ['pctKey Passes', 'pctCrosses Completed into Box', 'pctPasses into Box', 'pctxA', 'pctAssists', 'pctFinal Third Receptions', 'pctTake Ons']
    metric_names = ['Key Passes', 'Completed Crosses', 'Passes into Box', 'xA', 'Assists', 'Final Third Touches', 'Take Ons Completed']

    if compare == 'True':
        KeyPasses2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctKey Passes']) 
        Crosses2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctCrosses Completed into Box'])
        PassesIntoBox2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPasses into Box'])
        xA2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctxA'])
        Assists2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAssists'])
        FinalThirdTouches2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctFinal Third Receptions'])
        TakeOns2 = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'1v1 Dribbles Completed']
        
        data2 = [KeyPasses, Crosses, PassesIntoBox, xA, Assists, FinalThirdTouches,TakeOns]

 


#streamlit run streamlit.py



if position_group1 == 'CMs' and mode1 == 'Basic':
        
    Creating = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Chance Creation']) 
    Carrying = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Carrying'])
    Technical = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Ball Retention'])
    BoxThreat = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Receiving Forward'])
    DefAccuracy = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Tackle Accuracy'])
    DefEngage = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defensive Output'])
    Pressing = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Pressing'])

    DefendingHigh = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defending High']
    Heading = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Heading'])

    data1 = [BoxThreat, Creating, Technical, Carrying, DefAccuracy, DefEngage,Heading]
    metrics = ['Receiving', 'Chance Creation', 'Ball Retention', 'Tackle Accuracy', 'Defensive Output', 'Pressing','Heading']
    metric_names = ['Receiving', 'Chance Creation', 'Ball Retention', 'Tackle\nAccuracy', 'Defensive Output', 'Pressing','Heading']

    if compare == 'Yes':
        Creating2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Chance Creation']) 
        Carrying2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Carrying'])
        Technical2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Ball Retention'])
        BoxThreat2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Receiving Forward'])
        DefAccuracy2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Tackle Accuracy'])
        DefEngage2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defensive Output'])
        Pressing2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Pressing'])

        DefendingHigh = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defending High']
        Heading = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Heading'])

        data2 = [BoxThreat2, Creating2, Technical2, Carrying2, DefAccuracy2, DefEngage2,Heading2]


if position_group1 == 'CMs' and mode1 == 'Defending':
        
    TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackles Won']) 
    TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackle %'])
    Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctInterceptions'])
    Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPressures'])
    CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctCounterpressures'])
    AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAttacking Third Pressures'])
    AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAerial Wins'])

    data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
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
    metric_names = ['Progressive Passes', 'Passes into Final Third', 'Key Passes', 'Passes into Box','Short Pass %', 'Assists', '1v1 Dribbles Completed']

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

    data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
    metrics = ['Final Third Touches', 'Box Touches', 'Goals', 'Shots', 'xG', 'xG/Shot', 'Big Chances']
    metric_names = ['Final Third Touches', 'Box Touches', 'Goals', 'Shots', 'xG', 'xG/Shot', 'Big Chances']

    if compare == 'Yes':

        TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctFinal Third Receptions']) 
        TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctBox Receptions'])
        Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctGoals'])
        Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctShots'])
        CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctxG'])
        AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctxG/Shot'])
        AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctBig Chances'])

        data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]



              
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

if (position_group1 == 'Ws' or position_group1 == 'AMs' or position_group1 == 'STs') and mode1 == "Shooting":
    TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctBox Receptions']) 
    TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctGoals'])
    Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctShots'])
    Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctxG'])
    CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctxG/Shot'])
    AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctBig Chances'])
    AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctBig Chance Conversion'])

    data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
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



if (position_group1 == 'Ws' or position_group1 == 'AMs' or position_group1 == 'STs') and mode1 == "Out of Possession":
    TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackles Won']) 
    TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackle %'])
    Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctInterceptions'])
    Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctPressures'])
    CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctCounterpressures'])
    AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAttacking Third Pressures'])
    AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAttacking Third Counterpressures'])

    data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
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

x_list = [1150,830,730,450,515,800,1090]
y_list = [460,185,185,460,770,885,770]
orient_list = ['left', 'left', 'right', 'right', 'right','center', 'left']

for i in range(7):
    plt.text(x_list[i], y_list[i], metric_names[i], ha = orient_list[i], fontsize=30, color = 'white',fontname='Avenir')



club = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Team']
mins = int(df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Minutes'])
detailed_pos = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Detailed Position']



if compare == 'No':
    plt.text(800,70,f"{name1}",ha = 'center', fontsize=45, color = 'white', fontweight = 'bold')
    plt.text(800,120,f"{club} - {season1} {league1} - {mins} Minutes - {detailed_pos}",ha = 'center', fontsize=30, color = 'white', fontname='Avenir')
    plt.text(30,880,f"Data compared to {league1} {position_group1} in {season1}",ha = 'left', fontsize=21.5, color = 'white', fontname='Avenir')


if compare == 'Yes':
    club2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Team']
    mins2 = int(df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Minutes'])
    detailed_pos2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Detailed Position']

    plt.text(40,65,f"{name1}",ha = 'left', fontsize=35, color = 'green', fontweight = 'bold')
    plt.text(40,110,f"{club} - {season1} {league1}",ha = 'left', fontsize=30, color = 'green', fontname='Avenir')
    plt.text(40,150,f"{mins} Minutes - {detailed_pos}",ha = 'left', fontsize=30, color = 'green', fontname='Avenir')
    
    plt.text(1560,65,f"{name2}",ha = 'right', fontsize=35, color = 'red', fontweight = 'bold')
    plt.text(1560,110,f"{club2} - {season2} {league2}",ha = 'right', fontsize=30, color = 'red', fontname='Avenir')
    plt.text(1560,150,f"{mins2} Minutes - {detailed_pos2}",ha = 'right', fontsize=30, color = 'red', fontname='Avenir')
    plt.text(30,880,f"Data compared to {position_group1} in player's league",ha = 'left', fontsize=17, color = 'white', fontname='Avenir')

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

