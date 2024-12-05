# Import python packages
import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data
import string
import random

# Sidebar
st.set_page_config(layout = "wide", initial_sidebar_state='collapsed')
st.sidebar.subheader("Navigation")

# Initalizes the current page in the session state if it does not exist
if "current_page" not in st.session_state:
    st.session_state.current_page = "home_page"

# initialized the name filter selection in session state (chart 2 player page)
if "selected_name_var" not in st.session_state:
    st.session_state.selected_name_var = None

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

# Add Metrics to Carolina Players
carolina_players_all_situations['Expected Goal %'] = round(carolina_players_all_situations["I_F_goals"] / carolina_players_all_situations['I_F_xGoals'],3)
carolina_players_all_situations['Finishing Expected High Danger %'] = round(carolina_players_all_situations['I_F_highDangerGoals'] / carolina_players_all_situations['I_F_highDangerxGoals'],3)
carolina_players_all_situations['On Ice +/-'] = carolina_players_all_situations['OnIce_F_goals'] - carolina_players_all_situations['OnIce_A_goals']

#create photo list
photos = ["https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/KK.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Drury.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/DeAngelo.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Turbo.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Kuznetsov.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Staal.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Necas.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Noesen.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Martinook.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Ponomarev.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Burns.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Burke.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Coghlan.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Brady%20Skjei.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Guentzel.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Slavin.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Fast.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Nadeau.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Svech.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Morrow.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Jarvis.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Aho.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Orlov.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Blake.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Comtois.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Chatfield.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Lemieux.png",
        "https://raw.githubusercontent.com/hwillif/Visual_Analytics_Final/refs/heads/main/Player_Photos/Pesce.png"]

carolina_players_all_situations['photos'] = photos

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

    # Create GoalsxAssists Scatter Plot
    # Text Above Scatter Plot
    st.write(":red[Player Goals vs Assists]")
        
    # Create dataframe for the GoalsxAssists scatterplot
    total_goals_assists = carolina_players_all_situations[['name', 'position', 'I_F_goals', 'I_F_primaryAssists', 'I_F_secondaryAssists', 'photos']] 
    total_goals_assists = total_goals_assists.assign(Assists = total_goals_assists['I_F_primaryAssists'] + total_goals_assists['I_F_secondaryAssists'])
    total_goals_assists.columns = ['Name', 'Position', 'Goals', 'Primary Assists', 'Secondary Assists', 'Photos', 'Total Assists']

    # create scatter plot of goals vs assists
    goals_assists_scatterplot = alt.Chart(total_goals_assists).mark_point().encode(
        x='Total Assists',
        y='Goals',
        color='Position'
    ) 
    # create data labels for goals vs assists
    data_labels1 = goals_assists_scatterplot.mark_text(
        align='left',
        baseline='middle',
        dx=7
    ).encode(
        text='Name'
    )
    scatterplot1 = goals_assists_scatterplot + data_labels1
    # Print chart with names
    # st.altair_chart(scatterplot1, use_container_width=True)

    # Datalabels on ScatterPlot
    goals_assists_text = alt.Chart(total_goals_assists).mark_text(dy=45).encode(
        text="Name",
        x="Total Assists",
        y="Goals"
    )

    #Create Photo Chart
    photo_scatter = alt.Chart(total_goals_assists).mark_image(width=75, height=75).encode(
        x="Total Assists",
        y="Goals",
        url= 'Photos',
        tooltip= alt.Tooltip(field = "Name")
    )
    # Print Chart with Names and Photos
    st.altair_chart(photo_scatter + goals_assists_text, use_container_width=True)

    # Create Second Section
    st.subheader("Player Performance Comparisons", divider="red")
    
    #create multiselect drop down
    names = carolina_players_all_situations['name'].tolist()
    selected_name_var = st.multiselect(
        "**Select Players to Compare:**",
        names,
        # index=names.index(st.session_state.selected_name_var) if st.session_state.selected_name_var else 0
        max_selections=10,
        placeholder = 'Choose a Player',
        default = ['Sebastian Aho', 'Seth Jarvis', 'Andrei Svechnikov']     
    )
    length_selected_names = len(selected_name_var)
    # create loop for dynamic columns based on length of selected names list
    def autocolumn(i):
        temp1=[]
        for x in range(i):
            temp1.append(random.choice(string.ascii_uppercase)+str(length_selected_names))
        if i == 1:
            loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[0])]
            st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
                        
        if i == 2:
            temp1[0:1]=st.columns(2)
            with temp1[0]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[0])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[1]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[1])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)

        elif i == 3:
            temp1[0:2]=st.columns(3)
            with temp1[0]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[0])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[1]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[1])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[2]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[2])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
        elif i == 4:
            temp1[0:3]=st.columns(4)
            with temp1[0]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[0])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[1]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[1])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[2]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[2])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[3]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[3])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
        elif i == 5:
            temp1[0:4]=st.columns(5)
            with temp1[0]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[0])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[1]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[1])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[2]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[2])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[3]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[3])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[4]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[4])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
        
        elif i == 6:
            temp1[0:5]=st.columns(6)
            with temp1[0]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[0])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[1]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[1])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[2]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[2])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[3]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[3])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[4]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[4])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[5]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[5])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)

        elif i == 7:
            temp1[0:6]=st.columns(7)
            with temp1[0]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[0])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[1]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[1])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[2]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[2])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[3]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[3])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[4]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[4])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[5]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[5])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[6]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[6])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
        
        elif i == 8:
            temp1[0:7]=st.columns(8)
            with temp1[0]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[0])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[1]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[1])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[2]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[2])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[3]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[3])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[4]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[4])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[5]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[5])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[6]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[6])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[7]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[7])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
        
        elif i == 9:
            temp1[0:8]=st.columns(9)
            with temp1[0]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[0])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[1]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[1])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[2]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[2])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[3]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[3])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[4]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[4])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[5]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[5])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[6]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[6])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[7]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[7])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[8]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[8])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
        
        elif i == 10:
            temp1[0:9]=st.columns(10)
            with temp1[0]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[0])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[1]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[1])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[2]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[2])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[3]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[3])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[4]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[4])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[5]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[5])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[6]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[6])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[7]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[7])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[8]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[8])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)
            with temp1[9]:
                loop_df = carolina_players_all_situations[carolina_players_all_situations['name'].str.contains(selected_name_var[9])]
                st.image(loop_df['photos'].loc[loop_df.index[0]], width = 100)

    autocolumn(length_selected_names)

    # store selected values in session state
    st.session_state.selected_name_var = selected_name_var

    # Filter Dataset based on names selected
    filtered_df1 = carolina_players_all_situations[carolina_players_all_situations['name'].isin(selected_name_var)]
    filtered_df1 = filtered_df1.sort_values('name', key=lambda x: pd.Categorical(x, categories=selected_name_var, ordered=True))
    st.dataframe(filtered_df1)
    #create columns
    col1, col2 = st.columns(2)
    with col1:
        st.write("**:red[Player Expected Goal %]**")
        # Bar Chart to compare Goals / Expected Goals
        expected_goal_chart = alt.Chart(filtered_df1).mark_bar().encode(
            x=alt.X('name', axis=alt.Axis(labelAngle=-90,title=""), sort = filtered_df1['name']).title("Name"),
            y='Expected Goal %'
        )
        # Created Data Labels Chart for Player Expected Goal %
        expected_goal_text = expected_goal_chart.mark_text(
            baseline='middle',
            dy=-7.5 
        ).encode(
            text ='Expected Goal %'
        )
        # Combine Chart and Data Labels into Layers
        bar_chart1 = (expected_goal_chart + expected_goal_text
        ).configure_bar(
            color='red'
        ).properties(
            height=350
        )
        st.altair_chart(bar_chart1, use_container_width=True)
    with col2:
        st.write("**:red[Player Expected High Danger Goals Percentage]**")
        # Bar Chart to compare High Danger Goals / Expected High Danger Goals
        high_danger_chart = alt.Chart(filtered_df1).mark_bar().encode(
            x=alt.X('name', axis=alt.Axis(labelAngle=-90,title=""), sort = filtered_df1['name']).title("Name"),
            y='Finishing Expected High Danger %'
        )
        # Created Data Labels Chart for High Danger Expected %
        high_danger_text = high_danger_chart.mark_text(
            baseline='middle',
            dy=-7.5 
        ).encode(
            text ='Finishing Expected High Danger %'
        )
        # Combine Chart and Data Labels into Layers
        bar_chart2 = (high_danger_chart + high_danger_text
        ).configure_bar(
            color='red'
        ).properties(
            height=350
        )
        st.altair_chart(bar_chart2, use_container_width=True)
    
    # Create on Ice +/- Bar Chart
    st.write('**:red[On Ice Impact (+/-)]**')
    bar_chart3 = alt.Chart(carolina_players_all_situations).mark_bar().encode(
        x=alt.X('name', axis=alt.Axis(labelAngle=-90,title="")).sort('-y').title("Name"),
        y='On Ice +/-',
        color=alt.Color('position').title("Player Position")
    ).properties(
    height=350
    )
    st.altair_chart(bar_chart3, use_container_width=True)   

    

# Page Navigation
fn_map = {
    "home_page": home_page,
    "player_page": player_page
}
main_window = st.container()
main_workflow = fn_map.get(st.session_state.current_page, home_page)
main_workflow()



