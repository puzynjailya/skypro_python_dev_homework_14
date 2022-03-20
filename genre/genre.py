from flask import Blueprint, jsonify
from utils import *
from queries import MovieQueries

genre = Blueprint('genre', __name__, url_prefix='/genre')

@genre.route('/<genre>/')
def search_by_genre(genre):
    result = get_movies_by_genre(genre)
    if len(result) == 0:
        return f'<h2>По вашему запросу "{genre}" ничего не найдено. Попробуйте еще раз </h2>'
    else:
        return jsonify(result)