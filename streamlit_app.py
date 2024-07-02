import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Access secrets
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
        SELECT ticker, "Real-time price", "90-day MA", "180-day MA", "365-day MA"
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

# ... rest of your code remains the same ...

# Streamlit app
st.title('Stock Data Viewer')

ticker = st.text_input('Enter the ticker symbol:', '').strip().upper()

if ticker:
    data = fetch_ticker_data(ticker)
    if data is not None and not data.empty:
        st.write('Stock Data:')
        # Convert dataframe to a list of lists, excluding the index
        data_list = data.values.tolist()
        # Get column names
        columns = data.columns.tolist()
        # Display as a table
        st.table([columns] + data_list)
        
        # Create a chart using matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Prepare data for plotting
        labels = ['Real-time price', '90-day MA', '180-day MA', '365-day MA']
        values = data[labels].values[0]
        
        # Create the bar chart
        bars = ax.bar(labels, values)
        
        # Color the bars
        bars[0].set_color('red')
        for bar in bars[1:]:
            bar.set_color('blue')
        
        # Customize the chart
        ax.set_title(f'Price and Moving Averages for {ticker}')
        ax.set_ylabel('Price')
        ax.set_xlabel('Metric')
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Adjust layout to prevent cutting off labels
        plt.tight_layout()
        
        # Display the chart
        st.pyplot(fig)
    else:
        st.write(f'No data found for the ticker symbol: {ticker}')
