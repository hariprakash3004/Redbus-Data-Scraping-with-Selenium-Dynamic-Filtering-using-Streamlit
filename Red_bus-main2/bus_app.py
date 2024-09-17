import streamlit as st
import pandas as pd
import pymysql

# Function to connect to MySQL database and fetch data
def fetch_data(query):
    try:
        # Connect to MySQL database
        connection = pymysql.connect(host='localhost', user='root', passwd='', database="redbus")
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    except pymysql.Error as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()

# Load the data from the MySQL table
query = "SELECT * FROM bus_routes"
df = fetch_data(query)

if df.empty:
    st.write("No data found.")
else:
    st.title("RED BUS")

    # State filter dropdown
    state_list = df['state'].unique()
    selected_state = st.selectbox('Select State', state_list)

    # Filter DataFrame based on selected state
    state_filtered_df = df[df['state'] == selected_state]

    # Route name filter dropdown
    route_list = state_filtered_df['route_name'].unique()
    selected_route = st.selectbox('Select Route', route_list)

    # Filter DataFrame based on selected route
    route_filtered_df = state_filtered_df[state_filtered_df['route_name'] == selected_route]

    # Bus type filter dropdown
    bus_type_list = route_filtered_df['bus_type'].unique()
    selected_bus_type = st.selectbox('Select Bus Type', bus_type_list)

    # Route link display
    route_link = route_filtered_df['route_link'].iloc[0]
    st.markdown(f"[View Route Link]({route_link})")

    # Price slider
    min_price, max_price = route_filtered_df['price'].min(), route_filtered_df['price'].max()
    selected_price = st.slider('Select Price', int(min_price), int(max_price), (int(min_price), int(max_price)))

    # Star rating slider
    min_rating, max_rating = route_filtered_df['star_rating'].min(), route_filtered_df['star_rating'].max()
    selected_rating = st.slider('Select Star Rating', float(min_rating), float(max_rating), (float(min_rating), float(max_rating)))

    # Departing time
    selected_departing_time = st.time_input('Select Departing Time', key='departing_time')

    # Reaching time
    selected_reaching_time = st.time_input('Select Reaching Time', key='reaching_time')

    # Apply filters to the DataFrame
    filtered_df = route_filtered_df[
        (route_filtered_df['price'] >= selected_price[0]) & 
        (route_filtered_df['price'] <= selected_price[1]) & 
        (route_filtered_df['star_rating'] >= selected_rating[0]) & 
        (route_filtered_df['star_rating'] <= selected_rating[1])
    ]

    # Display the filtered DataFrame
    st.write("Filtered Bus Routes:")
    st.dataframe(filtered_df[['route_name', 'bus_type', 'price', 'star_rating', 'departing_time', 'reaching_time']])
