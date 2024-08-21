import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")


def fetch_current_table():
    url = 'https://www.bbc.com/sport/football/premier-league/table'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')

    if table is None:
        st.error("Could not find the table. Please check the website's HTML structure.")
        return None

    teams = []
    positions = []
    points = []
    matches_played = []
    goal_difference = []  # New list to store Goal Difference

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) >= 10:  # Ensuring there are enough cells to extract data
            position = cells[0].text.strip()
            team = cells[1].text.strip()
            matches = cells[2].text.strip()
            gd = cells[8].text.strip()  # Goal Difference is usually in the 9th cell (index 8)
            pts = cells[9].text.strip()  # Adjust index if necessary based on HTML structure
            positions.append(position)
            teams.append(team)
            matches_played.append(matches)
            goal_difference.append(gd)  # Append Goal Difference
            points.append(pts)

    current_table_df = pd.DataFrame({
        'Position': positions,
        'Team': teams,
        'Matches Played': matches_played,
        'Goal Difference': goal_difference,  # Add Goal Difference to DataFrame
        'Points': points
    })

    current_table_df['Position'] = current_table_df['Position'].astype(int)
    current_table_df['Matches Played'] = current_table_df['Matches Played'].astype(int)
    current_table_df['Goal Difference'] = current_table_df['Goal Difference'].astype(int)  # Convert GD to int
    current_table_df['Points'] = current_table_df['Points'].astype(int)
    current_table_df['Team'] = current_table_df['Team'].str.strip()

    return current_table_df



# Function to calculate the points
def calculate_points(prediction_df, current_table_df):
    comparison_df = prediction_df.merge(current_table_df, on='Team', suffixes=('_predicted', '_current'))
    comparison_df['Position Difference'] = abs(comparison_df['Position_current'] - comparison_df['Position_predicted'])
    total_points = comparison_df['Position Difference'].sum()
    return comparison_df, total_points

# Function to determine color formatting
def get_color(val):
    if val == 0:
        return '#006400'  # Dark Green
    elif val <= 3:
        return '#99ff99'  # Light Green
    elif 3 < val <= 5:
        return '#ffe680'  # Light Yellow
    else:
        return '#ff9999'  # Light Red

# Updated function to display the logos and data with color formatting applied directly in Streamlit
def display_logos_and_data(comparison_df):
    logos = {
        'Arsenal': 'Logos/Arsenal.png',
        'Aston Villa': 'Logos/Aston Villa.png',
        'AFC Bournemouth': 'Logos/Bournemouth.png',
        'Brentford': 'Logos/Brentford.png',
        'Brighton & Hove Albion': 'Logos/Brighton.png',
        'Chelsea': 'Logos/Chelsea.png',
        'Crystal Palace': 'Logos/Crystal Palace.png',
        'Everton': 'Logos/Everton.png',
        'Fulham': 'Logos/Fulham.png',
        'Ipswich Town': 'Logos/Ipswich.png',
        'Leicester City': 'Logos/Leicester.png',
        'Liverpool': 'Logos/Liverpool.png',
        'Manchester City': 'Logos/Manchester City.png',
        'Manchester United': 'Logos/Manchester United.png',
        'Newcastle United': 'Logos/Newcastle.png',
        'Nottingham Forest': 'Logos/Nottingham Forest.png',
        'Southampton': 'Logos/Southampton.png',
        'Tottenham Hotspur': 'Logos/Tottenham.png',
        'West Ham United': 'Logos/West Ham.png',
        'Wolverhampton Wanderers': 'Logos/Wolves.png'
    }
    
    # Adding column headers
    col0, col1, col2, col3, col4, col5 = st.columns([0.5, 1, 3, 1, 1, 1])
    with col0:
        st.write("")
    with col1:
        st.write("")
    with col2:
        st.write("Team")
    with col3:
        st.write("Current Position")
    with col4:
        st.write("Position Difference")
    
    # Iterate through the regular DataFrame to display positions, logos, and data
    for index, row in comparison_df.iterrows():
        logo_path = logos.get(row['Team'])
        position_number = row['Position_predicted']
        position_current = row['Position_current']
        position_difference = row['Position Difference']
        color = get_color(position_difference)
        
        col0, col1, col2, col3, col4, col5 = st.columns([0.5, 1, 3, 1, 1, 1])
        with col0:
            st.markdown(f"<span style='display: inline-block; width: 30px; height: 30px; line-height: 30px; text-align: center; background-color: #000000; color: white; border-radius: 5px;'>{position_number}</span>", unsafe_allow_html=True)
        with col1:
            st.image(logo_path, width=30)
        with col2:
            st.write(row['Team'])
        with col3:
            st.markdown(f"<span style='display: inline-block; width: 30px; height: 30px; line-height: 30px; text-align: center; background-color: #000000; color: white; border-radius: 5px;'>{position_current}</span>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<span style='display: inline-block; width: 30px; height: 30px; line-height: 30px; text-align: center; background-color: {color}; color: black; border-radius: 5px;'>{position_difference}</span>", unsafe_allow_html=True)

# Function to add Premier League logo at the top of the app
def add_logo():
    st.markdown("""
        <style>
            .logo-container {
                display: flex; 
                justify-content: center; 
                align-items: center; 
                margin-bottom: 40px;
            }
            .main-heading {
                margin-bottom: 30px;
            }
            .subheading {
                margin-top: 50px;
                margin-bottom: 20px;
            }
        </style>
        <div class="logo-container">
            <img src="https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg" 
            style="width: 200px; height: auto; filter: invert(1);">
        </div>
    """, unsafe_allow_html=True)

# Updated function to display the current Premier League standings in a custom format
def display_current_standings(current_table_df):
    logos = {
        'Arsenal': 'Logos/Arsenal.png',
        'Aston Villa': 'Logos/Aston Villa.png',
        'AFC Bournemouth': 'Logos/Bournemouth.png',
        'Brentford': 'Logos/Brentford.png',
        'Brighton & Hove Albion': 'Logos/Brighton.png',
        'Chelsea': 'Logos/Chelsea.png',
        'Crystal Palace': 'Logos/Crystal Palace.png',
        'Everton': 'Logos/Everton.png',
        'Fulham': 'Logos/Fulham.png',
        'Ipswich Town': 'Logos/Ipswich.png',
        'Leicester City': 'Logos/Leicester.png',
        'Liverpool': 'Logos/Liverpool.png',
        'Manchester City': 'Logos/Manchester City.png',
        'Manchester United': 'Logos/Manchester United.png',
        'Newcastle United': 'Logos/Newcastle.png',
        'Nottingham Forest': 'Logos/Nottingham Forest.png',
        'Southampton': 'Logos/Southampton.png',
        'Tottenham Hotspur': 'Logos/Tottenham.png',
        'West Ham United': 'Logos/West Ham.png',
        'Wolverhampton Wanderers': 'Logos/Wolves.png'
    }

    st.markdown("<h2 style='margin-bottom: 40px;'>Current Premier League Standings 2024/2025</h2>", unsafe_allow_html=True)

    # Display column headers
    col0, col1, col2, col3, col4, col5 = st.columns([0.2, 0.2, 1, 0.2, 0.2, 0.2])
    with col0:
        st.write("Position")
    with col1:
        st.write("")
    with col2:
        st.write("Team")
    with col3:
        st.write("Matches Played")
    with col4:
        st.write("Goal Difference")  # New column header
    with col5:
        st.write("Points")

    # Iterate through the current table DataFrame and display each team
    for index, row in current_table_df.iterrows():
        logo_path = logos.get(row['Team'])
        position = row['Position']
        team_name = row['Team']
        matches_played = row['Matches Played']
        goal_diff = row['Goal Difference']  # New data field
        points = row['Points']

        col0, col1, col2, col3, col4, col5 = st.columns([0.2, 0.2, 1, 0.2, 0.2, 0.2])
        with col0:
            st.markdown(f"<span style='display: inline-block; width: 30px; height: 30px; line-height: 30px; text-align: center; background-color: #000000; color: white; border-radius: 5px;'>{position}</span>", unsafe_allow_html=True)
        with col1:
            st.image(logo_path, width=30)
        with col2:
            st.write(team_name)
        with col3:
            st.markdown(f"<span style='display: inline-block; width: 30px; height: 30px; line-height: 30px; text-align: center; background-color: #000000; color: white; border-radius: 5px;'>{matches_played}</span>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<span style='display: inline-block; width: 30px; height: 30px; line-height: 30px; text-align: center; background-color: #000000; color: white; border-radius: 5px;'>{goal_diff}</span>", unsafe_allow_html=True)  # Display Goal Difference
        with col5:
            st.markdown(f"<span style='display: inline-block; width: 30px; height: 30px; line-height: 30px; text-align: center; background-color: #000000; color: white; border-radius: 5px;'>{points}</span>", unsafe_allow_html=True)




# Fetch the current table
current_table_df = fetch_current_table()

if current_table_df is not None:
    # Load predictions from CSV files (You can add more friends here)
    predictions = {
        'Renan': pd.read_csv('prediction_renan.csv', delimiter=';'),
        'Simão': pd.read_csv('prediction_simao.csv', delimiter=','),
        'Nina': pd.read_csv('prediction_nina.csv', delimiter=','),
        'Tope': pd.read_csv('prediction_tope.csv', delimiter=','),
        'Vicente': pd.read_csv('prediction_vicente.csv', delimiter=','),
        'Tiago': pd.read_csv('prediction_tiago.csv', delimiter=','),
        'Xala': pd.read_csv('prediction_xala.csv', delimiter=','),
        # Add more friends here
    } 

    # Ensure consistent formatting
    for name, df in predictions.items():
        df['Team'] = df['Team'].str.strip()

    # Add Premier League logo at the top of the app
    add_logo()
        
    # Streamlit app layout
    st.sidebar.title("Premier League 2024/2025 Prediction Challenge")
    selected_friend = st.sidebar.selectbox("Choose a friend to see their predictions:", list(predictions.keys()))

    st.markdown(f"<h1 class='main-heading'>{selected_friend}'s Premier League Predictions</h1>", unsafe_allow_html=True)
    
    prediction_df = predictions[selected_friend]
    comparison_df, total_points = calculate_points(prediction_df, current_table_df)

    # Display Total Points with larger font size
    st.subheader("Total Points")
    st.markdown(f"<h1 style='font-size: 40px; color: #FFD700;'>{selected_friend}: {total_points} points</h1>", unsafe_allow_html=True)

    st.markdown("<h2 class='subheading'>Prediction vs Actual Standings</h2>", unsafe_allow_html=True)
    display_logos_and_data(comparison_df)

    # Replace the previous Premier League Standings table with the new formatted display
    st.markdown('<div style="margin-top: 100px;"></div>', unsafe_allow_html=True)
    display_current_standings(current_table_df)

# Leaderboard Calculation
leaderboard = []
for name, prediction_df in predictions.items():
    _, points = calculate_points(prediction_df, current_table_df)
    leaderboard.append({'Name': name, 'Points': points})

# Create a DataFrame and sort by points
leaderboard_df = pd.DataFrame(leaderboard).sort_values(by='Points', ascending=True).reset_index(drop=True)

# Reset the index to start from 1
leaderboard_df.index = leaderboard_df.index + 1

# Convert the DataFrame to HTML and simplify the style
leaderboard_html = leaderboard_df.to_html(classes='clean', index=True, header=True)

# CSS to remove all borders and grid lines, increase column width, and control spacing
st.sidebar.markdown("""
    <style>
    .clean {
        font-size: 15px;
        border: none;
        border-collapse: collapse;
        margin-top: 10px; /* Remove margin-top for the table */
        width: 100%;
    }
    .clean th, .clean td {
        padding: 10px 15px; /* Increase padding to make columns wider */
        text-align: left; /* Align text to the left */
        border: none; /* Ensure no borders (grid lines) are displayed */
        outline: none; /* Remove any default cell outlines */
    }
    .clean th {
        font-weight: bold;
    }
    .clean td {
        background-color: transparent;
    }
    .leaderboard-title {
        margin-top: 60px; /* Add 50px top margin for the title */
        margin-bottom: 10px; /* Keep the title close to the table */
        font-size: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Add the "Overall Leaderboard" title with adjusted margin
st.sidebar.markdown('<div class="leaderboard-title">Overall Leaderboard</div>', unsafe_allow_html=True)

# Display the HTML in the sidebar
st.sidebar.markdown(leaderboard_html, unsafe_allow_html=True)





