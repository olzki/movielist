from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load movies from CSV
def load_movies():
    return pd.read_csv('IMDBTop250Movies.csv')[['rank', 'name', 'year', 'rating', 'genre', 'watched']]

@app.route('/')
def index():
    movies = load_movies()
    return render_template('index.html', movies=movies.to_dict(orient='records'))

@app.route('/update', methods=['POST'])
def update():
    movie_name = request.form['name']
    movies = load_movies()

    # Toggle the 'watched' state for the movie
    movie_index = movies[movies['name'] == movie_name].index[0]
    current_status = movies.at[movie_index, 'watched']
    movies.at[movie_index, 'watched'] = not current_status

    # Save the updated movies back to the CSV
    movies.to_csv('IMDBTop250Movies.csv', index=False)

    return jsonify({'status': 'success', 'watched': not current_status})

if __name__ == '__main__':
    app.run(debug=True)
