from flask import Flask, render_template
from movie.movie import movie
from rating.rating import rating
from genre.genre import genre

app = Flask(__name__, template_folder='./templates/')

app.register_blueprint(movie)
app.register_blueprint(rating)
app.register_blueprint(genre)


@app.route('/')
def index_page():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()