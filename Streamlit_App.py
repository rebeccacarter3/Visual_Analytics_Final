# Import python packages
import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data
import string
import random

# Sidebar
st.set_page_config(layout = "wide", initial_sidebar_state='expanded')
st.sidebar.subheader("Navigation")

# Initalizes the current page in the session state if it does not exist
if "current_page" not in st.session_state:
    st.session_state.current_page = "home_page"

# initialized the name filter selection in session state (chart 2 player page)
if "selected_name_var" not in st.session_state:
    st.session_state.selected_name_var = ['Sebastian Aho', 'Seth Jarvis', 'Andrei Svechnikov']  # Default players

#Create Sidebar Buttons Action
def switch_page(page: str):
    st.session_state.current_page = page

#Create Sidebar Buttons
home_page_button = st.sidebar.button(
    "Home".upper(), on_click=switch_page, args=["home_page"]
)

team_stats_buttom = st.sidebar.button(
    "Team Stats".upper(), on_click=switch_page, args=["team_stats"]
)

player_page_button = st.sidebar.button(
    "Player Performance".upper(), on_click=switch_page, args=["player_page"]
)

compare_page_buttom = st.sidebar.button(
    "Player Comparison".upper(), on_click=switch_page, args=["compare_page"]
)

@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    df = pd.read_csv(url)
    return df

#Import Players Data with changes
players = load_data('skaters 23-24.csv')
carolina_players = players[players['team'] == 'CAR']
carolina_players_all_situations = carolina_players[carolina_players['situation'] == 'all']
carolina_players_other_situations = carolina_players[carolina_players['situation'] != 'all']

# Add Metrics to Carolina Players
carolina_players_all_situations['Expected Goal %'] = round(carolina_players_all_situations['I_F_goals'] / carolina_players_all_situations['I_F_xGoals'],3)
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

# Create Second Page (Player Page)
def player_page():
    st.title(':red[Individual Player Performance]')

    # Create GoalsxAssists Scatter Plot
    # Text Above Scatter Plot
    st.subheader("Player Goals vs Assists", divider='red')
        
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

    # Create on Ice +/- Bar Chart
    st.subheader('**On Ice Impact (+/-)**', divider='red')
    carolina_players_all_situations['plusminus'] = carolina_players_all_situations['On Ice +/-']
    plusminus_chart = alt.Chart(carolina_players_all_situations).mark_bar().encode(
        x=alt.X('name', axis=alt.Axis(labelAngle=-90,title="")).sort('-y').title("Name"),
        y='On Ice +/-',
        color=alt.Color('position').title("Player Position")
    )

    #function for above or below functions
    above = alt.datum.num_cars > 100

        # Created Data Labels Chart for Player Expected Goal %
    plusminus_text = plusminus_chart.mark_text(
        baseline='middle',
        dy= alt.expr(alt.expr.if_(alt.datum.plusminus >= 0, -5, 7.5))       
    ).encode(
        text ='On Ice +/-'
    )
    # Combine Chart and Data Labels into Layers
    bar_chart1 = (plusminus_chart + plusminus_text
    ).properties(
    height=350
    )
    st.altair_chart(bar_chart1, use_container_width=True)


# Create third page (comparison page)
def compare_page():
    # Create Second Section
    st.title(":red[Player Shooting Comparisons]")
    
    # Create multiselect drop-down
    names = carolina_players_all_situations['name'].tolist()

    # Check if session state is already set for selected players
    if st.session_state.selected_name_var is None:
        st.session_state.selected_name_var = ['Sebastian Aho', 'Seth Jarvis', 'Andrei Svechnikov']

    # Use session state as default for the multiselect
    selected_name_var = st.multiselect(
        "**Select Players to Compare:**",
        names,
        default=st.session_state.selected_name_var,
        max_selections=10,
        placeholder='Choose a Player',
    )

    # Update session state with the selected players
    st.session_state.selected_name_var = selected_name_var

    # Number of selected players
    length_selected_names = len(selected_name_var)

    # Create loop for dynamic columns based on the number of selected names
    def autocolumn(i):
        if i == 0:
            st.write("No players selected for comparison.")
            return
        cols = st.columns(i)
        for idx, col in enumerate(cols):
            player_name = selected_name_var[idx]
            loop_df = carolina_players_all_situations[carolina_players_all_situations['name'] == player_name]
            with col:
                st.image(loop_df['photos'].iloc[0], width=100)
                st.write(player_name)

    autocolumn(length_selected_names)

    # Filter Dataset1 based on names selected
    filtered_df1 = carolina_players_all_situations[carolina_players_all_situations['name'].isin(selected_name_var)]
    filtered_df1 = filtered_df1.sort_values('name', key=lambda x: pd.Categorical(x, categories=selected_name_var, ordered=True))

    # Create visualizations
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("**Player Expected Goal Percentage**", divider='red')
        # Bar Chart to compare Goals / Expected Goals
        expected_goal_chart = alt.Chart(filtered_df1).mark_bar().encode(
            x=alt.X('name', axis=alt.Axis(labelAngle=-90, title=""), sort=filtered_df1['name']).title("Name"),
            y='Expected Goal %'
        )
        # Created Data Labels Chart for Player Expected Goal %
        expected_goal_text = expected_goal_chart.mark_text(
            baseline='middle',
            dy=-7.5
        ).encode(
            text='Expected Goal %'
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
        st.subheader("**Player Expected High Danger Goals Percentage**", divider='red')
        # Bar Chart to compare High Danger Goals / Expected High Danger Goals
        high_danger_chart = alt.Chart(filtered_df1).mark_bar().encode(
            x=alt.X('name', axis=alt.Axis(labelAngle=-90, title=""), sort=filtered_df1['name']).title("Name"),
            y='Finishing Expected High Danger %'
        )
        # Created Data Labels Chart for High Danger Expected %
        high_danger_text = high_danger_chart.mark_text(
            baseline='middle',
            dy=-7.5
        ).encode(
            text='Finishing Expected High Danger %'
        )
        # Combine Chart and Data Labels into Layers
        bar_chart2 = (high_danger_chart + high_danger_text
        ).configure_bar(
            color='red'
        ).properties(
            height=350
        )
        st.altair_chart(bar_chart2, use_container_width=True)

    # Filter Dataset2 based on names selected
    filtered_df2 = carolina_players_other_situations[carolina_players_other_situations['name'].isin(selected_name_var)]
    filtered_df2 = filtered_df2.sort_values('name', key=lambda x: pd.Categorical(x, categories=selected_name_var, ordered=True))
    filtered_df2.rename(columns={'I_F_goals': 'Goals'}, inplace=True)

    # Create Other Situations Goals and Assists
    st.subheader("**Goals in Different Scenarios**", divider='red')
    # Bar Chart to compare High Danger Goals / Expected High Danger Goals
    situationschart = alt.Chart(filtered_df2).encode(
        x=alt.X('name', axis=alt.Axis(labelAngle=-90, title=""), sort=filtered_df1['name']).title("Name"),
        xOffset='situation',
        y='Goals',
    ) 
    situationschart_color = situationschart.mark_bar().encode(
        color=alt.Color('situation:N'),
    )
    # Created Data Labels Chart for Goals In All situations
    situationschart_text = situationschart.mark_text(
        baseline='middle', 
        dx=5,
        dy=-5,
    ).encode(
        text='Goals'
    )
    # Print Goals in Situations 
    st.altair_chart(situationschart_color + situationschart_text, use_container_width=True)

def team_stats():
    # create team stats dataframe for the 2023/2024 Season. Could do all years but this site is focused on one season.
    team_data = pd.read_csv('Carolina Hurricanes.csv')
    
    # remove duplicate data in other situations
    team_data = team_data[team_data['situation'] == 'all'] 
    
    #only select 2023 season
    team_data = team_data[team_data['season'] == 2023]
    
    #format game date
    team_data['gameDate'] = pd.to_datetime(team_data['gameDate'], format='%Y%m%d')
    
    # Create Expected Goal % Rate
    team_data['Expected Goal %'] = round(team_data['goalsFor'] / team_data['xGoalsFor'],3)
    
    # Create win stat
    team_data['game_result'] = team_data.apply(lambda row: 1 if row['goalsFor'] > row['goalsAgainst'] 
                        else (0 if row['goalsFor'] < row['goalsAgainst'] else .5), axis=1)
    team_data['game_result_text'] = team_data.apply(lambda row: 'won' if row['goalsFor'] > row['goalsAgainst'] 
                    else ('lost' if row['goalsFor'] < row['goalsAgainst'] else 'ot'), axis=1)

    # Add month column
    team_data['month'] = team_data['gameDate'].dt.to_period('M')  # Convert date to period (month)

    # get team info 
    team_info = pd.read_csv('NHL Teams.csv')
    team_info = team_info[['abbreviation', 'division/name']]
    team_info['division'] = team_info['division/name']

    # merge team_data and info to get the division
    team_data = pd.merge(team_data, team_info, left_on='opposingTeam', right_on='abbreviation', how='left')

    # Add a title to the page
    st.title("**:red[Team Shooting Performance]**")

        # Create Win Percentage Chart vs Teams
    st.subheader('**Win Percentages against other Teams**', divider='red')
    # Create table
    win_percentages = team_data.groupby('opposingTeam').agg(
        total_games=('game_result', 'size'),
        total_wins=('game_result', 'sum')
    ).reset_index()
    # Create win percentage metric
    win_percentages['win_percentage'] = (win_percentages['total_wins'] / win_percentages['total_games'])
    
    # Order the divisions in a list
    division_order = ['Metropolitan', 'Atlantic', 'Central', 'Pacific']
    
    # merge to get division name
    win_percentages = pd.merge(win_percentages, team_info, left_on='opposingTeam', right_on='abbreviation', how='left')
    win_percentages['division'] = pd.Categorical(win_percentages['division'], categories=division_order, ordered=True)
    win_percentages = win_percentages.sort_values(by=['division', 'win_percentage'], ascending=[True, False])
    
    # Get unique team names in division order
    team_order = win_percentages['opposingTeam'].unique()

    # create bar chart for win percentages against other teams
    win_perc_chart = alt.Chart(win_percentages).mark_bar().encode(
        x=alt.X('opposingTeam:N', title='Team', sort=team_order),
        y=alt.Y('win_percentage:Q', title='Win Percentage', axis=alt.Axis(format='.0%')),
        color=alt.Color('division', scale=alt.Scale(scheme='category10')), 
        tooltip=['opposingTeam:N', 'win_percentage:Q']  # Display win percentage on hover
    ).configure_view(
        stroke=None  
    )
    # print chart for win percentages against other teams
    st.altair_chart(win_perc_chart)

    # Add a header to the linechart
    st.subheader("**Team Expected Goal Percentage**", divider="red")
    # create line chart for expected goal %
    linechart = alt.Chart(team_data).mark_line(color='red').encode(
        x=alt.X('gameDate', axis=alt.Axis(title='Game Date', labelAngle=-45)),
        y='Expected Goal %',
    )
    reference_line = alt.Chart(pd.DataFrame({'y': [1]})).mark_rule(color='black').encode(
        y=alt.Y('y:Q', axis=alt.Axis(title='Expected Goal %')),
    )
    # Print the line chart and reference line
    st.altair_chart(linechart+reference_line, use_container_width=True)

    # create function to determine game result
    def game_outcome(row):
        if row['goalsFor'] > row['goalsAgainst'] and row['xGoalsFor'] > row['xGoalsAgainst']:
            return 'Won'
        elif row['goalsFor'] < row['goalsAgainst'] and row['xGoalsFor'] < row['xGoalsAgainst']:
            return 'Lost'
        elif row['goalsFor'] < row['goalsAgainst'] and row['xGoalsFor'] > row['xGoalsAgainst']:
            return 'Should Have Won'
        elif row['goalsFor'] > row['goalsAgainst'] and row['xGoalsFor'] < row['xGoalsAgainst']:
            return 'Should Have Lost'
        else:    
            return 'OT'
        
    team_data['game_outcome'] = team_data.apply(game_outcome, axis=1)

    # Month Order
    month_order = ['October','November','December','January','February','March','April','May','June']
    result_order = ['Won','Lost','OT','Should Have Lost','Should Have Won']

    # Get number of games in a month per game outcome
    game_counts = team_data.groupby(['month','game_outcome'])['gameId'].count().reset_index(name='game_count_per_result')
    team_data = team_data.merge(game_counts, on=['month','game_outcome'], how='left')

    # Create Header for HeatMap
    st.subheader("**Team Performance throughout the Season**", divider='red')
    # Create HeatMap over months for win%
    heatmap = alt.Chart(team_data).mark_rect().encode(
        alt.X("game_outcome", sort=result_order).axis(labelAngle=0, orient='top').title("Game Outcome"),
        alt.Y("month(gameDate):O", sort= month_order).title("Month"),
        color = alt.Color('Expected Goal %',legend=alt.Legend(orient='bottom', title="Expected Goal Percentage",)).title("Expected Goal %"),
        tooltip=[
            'game_outcome:N', 
            'month(gameDate):O',
            alt.Tooltip('Expected Goal %:Q', title='Expected Goal %'),
            alt.Tooltip('game_count_per_result', title='Game Count')
        ]
    )
    st.altair_chart(heatmap, use_container_width=True)
   
    
# Page Navigation
fn_map = {
    "home_page": home_page
    , "player_page": player_page
    , "compare_page": compare_page 
    , "team_stats": team_stats
}
main_window = st.container()
main_workflow = fn_map.get(st.session_state.current_page, home_page)
main_workflow()



