from flask import Flask, render_template, send_file, request
import pandas as pd

app = Flask(__name__)

# Load the CSV file into a DataFrame
def load_data():
    try:
        df = pd.read_csv('terrorist_activity_2024_full.csv')
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Month", "Date", "Incident"])

@app.route('/', methods=['GET', 'POST'])
def index():
    # Load the data
    df = load_data()

    # Check if a specific month is selected
    selected_month = request.form.get('month', 'Jan-2024')  # Default to January if no month is selected

    # Filter the DataFrame based on the selected month
    filtered_data = df[df['Month'] == selected_month]

    # Convert the DataFrame to a list of dictionaries for easier rendering in the template
    data = filtered_data.to_dict(orient='records')

    # Available months
    months = [
        "Jan-2024", "Feb-2024", "Mar-2024", "Apr-2024", "May-2024",
        "Jun-2024", "Jul-2024", "Aug-2024", "Sep-2024", "Oct-2024",
        "Nov-2024", "Dec-2024"
    ]

    return render_template('index.html', data=data, months=months, selected_month=selected_month)

@app.route('/download_year')
def download_year():
    file_path = 'terrorist_activity_2024_full.csv'
    return send_file(file_path, as_attachment=True)

@app.route('/download_month', methods=['POST'])
def download_month():
    month = request.form.get('month')
    df = load_data()
    
    # Filter the DataFrame based on the selected month
    month_data = df[df['Month'] == month]
    
    # Save the filtered data to a temporary file
    temp_file_path = f'terrorist_activity_{month}.csv'
    month_data.to_csv(temp_file_path, index=False)
    
    return send_file(temp_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
