from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the data
data = pd.read_excel('static/prof_grades.xlsx')  # Ensure this file is in the same directory as app.py

# Ensure columns are consistently formatted as strings for filtering
data['Year'] = data['Year'].astype(str).str.strip()
data['Semester'] = data['Semester'].astype(str).str.strip()
data['Course'] = data['Course'].str.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search_course():
    course_name = request.args.get('course_name', '').strip()
    results = data[data['Course'].str.contains(course_name, case=False, na=False)]
    return jsonify(results[['Year', 'Semester', 'Course', 'Grade', 'Count']].to_dict(orient='records'))

@app.route('/suggest')
def suggest_course():
    search_text = request.args.get('query', '').strip()
    suggestions = data[data['Course'].str.contains(search_text, case=False, na=False)]['Course'].unique().tolist()
    return jsonify(suggestions)

@app.route('/get_years')
def get_years():
    course_name = request.args.get('course_name', '').strip()
    years = data[data['Course'] == course_name]['Year'].unique().tolist()
    return jsonify(years)

@app.route('/get_semesters')
def get_semesters():
    course_name = request.args.get('course_name', '').strip()
    year = request.args.get('year', '').strip()
    semesters = data[(data['Course'] == course_name) & (data['Year'] == year)]['Semester'].unique().tolist()
    return jsonify(semesters)

@app.route('/get_grades')
def get_grades():
    course_name = request.args.get('course_name', '').strip()
    year = request.args.get('year', '').strip()
    semester = request.args.get('semester', '').strip()

    # Debugging output to verify inputs and dataframe filtering
    print(f"Received Course: {course_name}, Year: {year}, Semester: {semester}")

    # Filter by course, year, and semester after ensuring consistency in data types and trimming whitespace
    results = data[
        (data['Course'] == course_name) &
        (data['Year'] == year) &
        (data['Semester'] == semester)
    ]

    print(f"Filtered Results: {results}")  # Debugging output to confirm data availability

    results = results.sort_values(by='Grade')[['Semester', 'Grade', 'Count']]
    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
