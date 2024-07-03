import streamlit as st
import psycopg2
import pandas as pd
import plotly.graph_objects as go
from psycopg2 import sql, OperationalError

# Set page configuration
st.set_page_config(
   page_title="Stock Data Viewer",
   page_icon="📈",
   layout="wide",
   initial_sidebar_state="collapsed",
)
st.title('📈 Stock Data Viewer')

st.write("View and analyze stock data including moving averages and real-time prices.")

# Database credentials
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOST"]
db_port = int(st.secrets["DB_PORT"])
db_name = st.secrets["DB_NAME"]

# Function to fetch ticker data
def fetch_ticker_data(ticker):
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cursor = connection.cursor()
        query = sql.SQL("""
            SELECT ticker, "365-day MA", "180-day MA", "90-day MA", "Real-time price"  
            FROM student.mc_stocks
            WHERE UPPER(ticker) = UPPER(%s);
        """)
        cursor.execute(query, (ticker,))
        data = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        connection.close()
        return pd.DataFrame(data, columns=colnames)
    except OperationalError as e:
        st.error(f"Database error: {e}")
        return None

# User input for ticker symbol
ticker = st.text_input('Enter the ticker symbol:', '').strip().upper()

if ticker:
    data = fetch_ticker_data(ticker)
    if data is not None and not data.empty:
        st.write('Stock Data:')
        st.table(data)
        
        # Prepare data for the bar chart
        labels = ['365-day MA', '180-day MA', '90-day MA', 'Real-time price']
        values = data.iloc[0, 1:].tolist()
        
        # Set colors, blue for MAs and red for 'Real-time price'
        colors = ['blue', 'blue', 'blue', 'red']
        
        # Create the figure
        fig = go.Figure()
        
        # Add bars to the figure
        for label, value, color in zip(labels, values, colors):
            fig.add_trace(go.Bar(
                x=[label],
                y=[value],
                name=label,
                marker_color=color,
                width=0.4  # Reduced bar width by 50%
            ))
        
        # Update layout
        fig.update_layout(
            title=f'Price and Moving Averages for {ticker}',
            xaxis_title='Metric',
            yaxis_title='Price ($)',
            yaxis_tickprefix='$',
            xaxis_tickangle=-45,
            showlegend=False
        )
        
        # Display the plot
        st.plotly_chart(fig)
    else:
        st.write(f'No data found for the ticker symbol: {ticker}')
