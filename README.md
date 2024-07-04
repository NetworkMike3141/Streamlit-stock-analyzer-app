Stock Data Viewer
Stock Data Viewer is a web application that allows users to view and analyze stock data, including moving averages and real-time prices. This application is built using Streamlit and retrieves data from a PostgreSQL database.

Features
Display stock data for a given ticker symbol.
Show 365-day, 180-day, and 90-day moving averages.
Display real-time price.
Interactive bar chart visualization using Plotly.
Installation
To run this application, you need to have Python installed on your system along with the following packages:

streamlit
psycopg2
pandas
plotly
You can install the required packages using pip:

bash
Copy code
pip install streamlit psycopg2 pandas plotly
Configuration
The application requires database credentials to connect to the PostgreSQL database. These credentials should be stored in the secrets.toml file in the .streamlit directory of your project. The file should have the following structure:

toml
Copy code
[secrets]
DB_USER = "your_db_username"
DB_PASSWORD = "your_db_password"
DB_HOST = "your_db_host"
DB_PORT = "your_db_port"
DB_NAME = "your_db_name"
Usage
To run the application, navigate to the directory containing the script and run:

bash
Copy code
streamlit run your_script_name.py
Replace your_script_name.py with the name of your script file.

Steps to Use the Application
Enter the ticker symbol of the stock you want to view in the text input field.
The application will fetch the data for the entered ticker symbol from the PostgreSQL database.
If data is found, it will display the stock data in a table.
An interactive bar chart will be shown, visualizing the moving averages and real-time price for the entered ticker symbol.
Example
Here's an example of how to use the application:

Run the application using streamlit run your_script_name.py.
Enter a ticker symbol, e.g., AAPL, in the text input field.
View the stock data and the corresponding bar chart visualization.
Error Handling
If there is a database connection error, an error message will be displayed in the application.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Feel free to contribute to this project by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

Enjoy using the Stock Data Viewer! 📈