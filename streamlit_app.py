import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_host = st.secrets["DB_HOST"]
db_port = int(st.secrets["DB_PORT"])
db_name = st.secrets["DB_NAME"]

def fetch_ticker_data(ticker):
    conn = None
    try:
        conn = psycopg2.connect(
            database=db_name,    
            user=db_user,
            host=db_host,
            password=db_password,
            port=db_port
        )
        
        query = """
        SELECT ticker, "365-day MA", "180-day MA", "90-day MA", "Real-time price"  
        FROM student.mc_stocks
        WHERE UPPER(ticker) = UPPER(%s);
        """
        
        df = pd.read_sql(query, conn, params=(ticker.upper(),))
        return df
    
    except (psycopg2.OperationalError, psycopg2.ProgrammingError, psycopg2.DatabaseError) as e:
        st.error(f"Database error: {e}")
        return None
    
    finally:
        if conn:
            conn.close()

st.title('Stock Data Viewer')

ticker = st.text_input('Enter the ticker symbol:', '').strip().upper()

if ticker:
    data = fetch_ticker_data(ticker)
    if data is not None and not data.empty:
        st.write('Stock Data:')
       
        data_list = data.values.tolist()
   
        columns = data.columns.tolist()
       
        st.table([columns] + data_list)
    
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Reorder labels and values
        labels = ['365-day MA', '180-day MA', '90-day MA', 'Real-time price']
        values = data[labels].values[0]
        
        # Set bar width to 20% of the default (which is 0.8)
        bar_width = 0.8 * 0.2
        
        # Define colors: blue for MAs, red for 'Real-time price'
        colors = ['blue'] * 3 + ['red']
        
        for i, (label, value) in enumerate(zip(labels, values)):
            ax.bar(label, value, color=colors[i], width=bar_width)
        
        # Add a line connecting the tops of the bars
        ax.plot(labels, values, color='black', linestyle='-', marker='o', linewidth=2, markersize=6)
        
        ax.set_title(f'Price and Moving Averages for {ticker}', fontsize=16)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.set_xlabel('Metric', fontsize=12)
        
        ax.grid(True, linestyle='--', alpha=0.3)
        
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.2f}'))
        
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        st.pyplot(fig)
    else:
        st.write(f'No data found for the ticker symbol: {ticker}')