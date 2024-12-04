# Import python packages
import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data

# Sidebar
st.set_page_config(layout = "wide", initial_sidebar_state='collapsed')
st.sidebar.subheader("Navigation")

# Initalizes the current page in the session state if it does not exist
if "current_page" not in st.session_state:
    st.session_state.current_page = "home_page"

#Create Sidebar Buttons Action
def switch_page(page: str):
    st.session_state.current_page = page

#Create Sidebar Buttons
home_page_button = st.sidebar.button(
    "Home".upper(), on_click=switch_page, args=["home_page"]
)

player_page_button = st.sidebar.button(
    "Player Performance".upper(), on_click=switch_page, args=["player_page"]
)

#Import Players Data
players = pd.read_csv('skaters 23-24.csv')
carolina_players = players[players['team'] == 'CAR']
carolina_players_all_situations = carolina_players[carolina_players['situation'] == 'all']
# carolina_players = carolina_players.rename(columns={'name': 'Name'}, inplace=True)

# Create Home Page
def home_page():
    st.title(':red[Carolina Hurricanes] Shooting Efficiency')
    st.header('2023/2024 Season')
    # Create Columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Season in Review', divider="red")
        st.write('The Carolina Hurricanes had a impressive 52 win, 111 point season that ended leaving fans feeling like they deserved more. The playoffs obruptly ended in the second round against the New York Rangers after dominating the New York Islanders in the first round. The series loss seemed to be attributed to a lack of goalscoring and miscues in the defensive zone. The defensive issues were surprising as the Hurricanes are known to have one of the toughest defenses due to man-on-man defense they play but the know issue going into the post-season was the weakness of finishing opportunities. The Hurricanes consistantly out-shoot their opponents but will lose a game they dominated on paper and I believe that is due to the opportunities we struggle to captialize. Don Waddle, the GM, made a transfer deadline trade for Jake Guentzel to help with our offense but it did not solve all the teams issues. This dashboard reviews the shooting/scoring opportunities at the team and individual player level.')

    with col2:
        st.subheader(" ")
        st.image('Team Photo.jpg')
    st.subheader("Key Defintions", divider="red")
    st.write('**Expected Goals:** :gray[The sum of the probabilities of unblocked shot attempts being goals. For example, a rebound shot in the slot may be worth 0.5 expected goals, while a shot from the blueline while short handed may be worth 0.01 expected goals. The expected value of each shot attempt is calculated by the MoneyPuck Expected Goals model. Expected goals is commonly abbreviated as "xGoals". Blocked shot attempts are valued at 0 xGoals.]')
    st.write('**Actual vs Expected:** :gray[The Actual amount of goals scored divided by the Expected Goals scored.]')
    st.write("**Shot on Goal:** :gray[A shot that would have gone into the net if the goaltender hadn't stopped it.]")
    st.write('**High Danger Shot:** :gray[Unblocked Shot attempts  with >= 20% probability of being a goal. High danger shots account for ~5% of shots and ~33% of goals.]')
    st.write('**Points:** :gray[A goal is worth 1 point and an assist is worth 1 point.]')
    st.write('**+/-:** :gray[The goal differential when a player is on the Ice.]')

# Create Second Page
def player_page():
    st.title('Individual Player Performance')

    # total_goals_assists = carolina_players.groupby(['name']).agg({'I_F_goals': ['sum'],'I_F_primaryAssists': ['sum'],'I_F_secondaryAssists': ['sum']}).reset_index()
    # total_goals_assists = total_goals_assists.assign(Assists = total_goals_assists['I_F_primaryAssists'] + total_goals_assists['I_F_secondaryAssists'])
    # total_goals_assists.columns = ['Goals', 'Primary Assists', 'Secondary Assists', 'Total Assists']
    # st.dataframe(data=carolina_players_all_situations)

    total_goals_assists = carolina_players_all_situations[['name', 'position', 'I_F_goals', 'I_F_primaryAssists', 'I_F_secondaryAssists']] 
    total_goals_assists = total_goals_assists.assign(Assists = total_goals_assists['I_F_primaryAssists'] + total_goals_assists['I_F_secondaryAssists'])
    total_goals_assists.columns = ['Name', 'Position', 'Goals', 'Primary Assists', 'Secondary Assists', 'Total Assists']

    # create scatter plot of goals vs assists
    # goals_assists_scatterplot = alt.Chart(total_goals_assists).mark_point().encode(
    #     x='Total Assists',
    #     y='Goals',
    #     color='Position'
    # ) 
    # data_labels1 = goals_assists_scatterplot.mark_text(
    #     align='left',
    #     baseline='middle',
    #     dx=7
    # ).encode(
    #     text='Name'
    # )
    # scatterplot1 = goals_assists_scatterplot + data_labels1
    # st.altair_chart(scatterplot1, use_container_width=True)

    goals_assists_scatterplot = alt.Chart(total_goals_assists).mark_text().encode(
        x="Total Assists",
        y="Goals",
        color="Position",
        text="Name",
    )
    st.altair_chart(goals_assists_scatterplot, use_container_width=True)
    

# Page Navigation
fn_map = {
    "home_page": home_page,
    "second_page": player_page
}
main_window = st.container()
main_workflow = fn_map.get(st.session_state.current_page, home_page)
main_workflow()