from flask import Blueprint, jsonify
from utils import *

movie = Blueprint('movie', __name__, url_prefix='/movie')


@movie.route('/<movie_title>')
def search_by_title_page(movie_title):
    search_result, output_text = get_movie_by_title(movie_title)
    return jsonify(search_result)


@movie.route('/<int:start_year>/to/<int:end_year>/')
def search_by_year_range(start_year, end_year):
    list_of_dics = get_movies_by_year(start_year, end_year)
    return jsonify(list_of_dics)


