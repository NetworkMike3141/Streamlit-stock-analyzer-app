import streamlit as st
import psycopg2
import pandas as pd
import plotly.graph_objects as go
from psycopg2 import sql, OperationalError

st.set_page_config(
   page_title="Stock Data Viewer",
   page_icon="📈",
   layout="wide",
   initial_sidebar_state="collapsed",
)
st.title('📈 Stock Data Viewer')

st.write("View and analyze stock data including moving averages and real-time prices.")

db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOST"]
db_port = int(st.secrets["DB_PORT"])
db_name = st.secrets["DB_NAME"]

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

ticker = st.text_input('Enter the ticker symbol:', '').strip().upper()

if ticker:
    data = fetch_ticker_data(ticker)
    if data is not None and not data.empty:
        st.write('Stock Data:')
        st.table(data)
        
        # Individual graphs for each moving average vs real-time price
        for ma in ['365-day MA', '180-day MA', '90-day MA']:
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=[ma],
                y=[data.iloc[0][ma]],
                name=ma,
                marker_color='blue',
                width=0.4 
            ))
            
            fig.add_trace(go.Bar(
                x=['Real-time price'],
                y=[data.iloc[0]['Real-time price']],
                name='Real-time price',
                marker_color='red',
                width=0.4 
            ))
            
            fig.update_layout(
                title=f'{ma} vs Real-time Price for {ticker}',
                xaxis_title='Metric',
                yaxis_title='Price ($)',
                yaxis_tickprefix='$',
                xaxis_tickangle=-45,
                showlegend=False
            )
            
            st.plotly_chart(fig)

        # Graph with all 4 values
        labels = ['365-day MA', '180-day MA', '90-day MA', 'Real-time price']
        values = data.iloc[0, 1:].tolist()
        
        colors = ['blue', 'blue', 'blue', 'red']
        
        fig_all = go.Figure()
        
        for label, value, color in zip(labels, values, colors):
            fig_all.add_trace(go.Bar(
                x=[label],
                y=[value],
                name=label,
                marker_color=color,
                width=0.4 
            ))
        
        fig_all.update_layout(
            title=f'Price and Moving Averages for {ticker}',
            xaxis_title='Metric',
            yaxis_title='Price ($)',
            yaxis_tickprefix='$',
            xaxis_tickangle=-45,
            showlegend=False
        )
        
        st.plotly_chart(fig_all)

    else:
        st.write(f'No data found for the ticker symbol: {ticker}')