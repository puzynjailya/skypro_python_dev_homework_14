from flask import Blueprint, jsonify
from utils import *

rating = Blueprint('rating', __name__, url_prefix='/rating')


@rating.route('/<rating_group>')
def rating_page(rating_group):
    result = get_movies_by_rating(rating_group)
    if result[0] == 'Ошибка':
        return result[1]
    else:
        return jsonify(result)
