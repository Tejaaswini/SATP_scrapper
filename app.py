from flask import Flask, render_template, send_file, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the CSV file into a DataFrame
def load_data():
    try:
        df = pd.read_csv('terrorist_activity_2024_full.csv')
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Month", "Date", "Incident"])

@app.route('/')
def index():
    # Load the data
    df = load_data()

    # Filter the DataFrame to show only January 2024 data by default
    january_data = df[df['Month'] == 'Jan-2024']

    # Convert the DataFrame to a list of dictionaries for easier rendering in the template
    data = january_data.to_dict(orient='records')

    # Available months
    months = [
        "Jan-2024", "Feb-2024", "Mar-2024", "Apr-2024", "May-2024",
        "Jun-2024", "Jul-2024", "Aug-2024", "Sep-2024", "Oct-2024",
        "Nov-2024", "Dec-2024"
    ]

    return render_template('index.html', data=data, months=months)

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

@app.route('/get_month_data', methods=['POST'])
def get_month_data():
    month = request.form.get('month')
    df = load_data()

    # Filter the DataFrame based on the selected month
    month_data = df[df['Month'] == month]
    data = month_data.to_dict(orient='records')

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
