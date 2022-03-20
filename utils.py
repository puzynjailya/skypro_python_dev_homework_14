from queries import MovieQueries
import json


def get_movie_by_title(movie_title):
    """
    Функция для преобразования результатов поиска к удобному для вывода формату
    :param movie_title: str - наименование фильма, который ищем
    :return: output: dict - словарь с заполненными значениями
    output_text:
    """
    if not isinstance(movie_title, str):
        raise TypeError('Ошибка ввода типа данных')

    # Создаем объект MovieQueries
    movie_query = MovieQueries()
    # Выполняем поиск
    search_result = movie_query.query_movie_by_title(movie_title)

    if len(search_result) == 0:
        output = dict({"title": None,
                       "country": None,
                       "release_year": None,
                       "genre": None,
                       "description": None})
        output_text = f'По вашему запросу: {movie_title} ничего не найдено. Уточните результаты поиска.'
        return output, output_text

    if len(search_result) == 1:
        output = dict({"title": search_result[0][0],
                       "country": search_result[0][1],
                       "release_year": search_result[0][2],
                       "genre": search_result[0][3],
                       "description": search_result[0][4]})
        output_text = f'По вашему запросу: {movie_title} найден 1 фильм'
        return output, output_text

    elif len(search_result) > 1:
        output = dict({"title": search_result[0][0],
                       "country": search_result[0][1],
                       "release_year": search_result[0][2],
                       "genre": search_result[0][3],
                       "description": search_result[0][4]})
        nl = '\n'
        output_text = f'По вашему запросу: {movie_title} найдено фильмов: {len(search_result)}' \
                      f'Пожалуйста, уточните Ваш запрос.{nl} Ближайшие 2 совпадения:{nl}{search_result[1][0]}' \
                      f'{nl}{search_result[2][0]}'

        return output, output_text


def get_movies_by_year(start_year, end_year):
    """
    Функция преобразования получаемого запроса из БД к формату списка словарей
    :param start_year: Год начала поиска
    :param end_year: Год конца поиска
    :return: list_of_dicts: list - список словарей требуемого формата
    """
    # Проверка на корректность внесенных данных
    if not isinstance(start_year, int):
        raise TypeError('Ошибка ввода типа данных для начального года')
    if not isinstance(end_year, int):
        raise TypeError('Ошибка ввода типа данных для окончательного года')

    # Создаем пустой список, куда будем складывать словари
    list_of_dicts = []
    # Получаем результаты поиска
    movie_query = MovieQueries()
    list_of_results = movie_query.query_movie_by_year(start_year, end_year)
    # Проходимся циклом по каждому из найденных результатов
    for result in list_of_results:
        movie_dict = dict({
            "title": result[0],
            "release_year": result[1]
        })
        list_of_dicts.append(movie_dict)
    return list_of_dicts


def get_movies_by_rating(requested_rating):
    """
    Функция преобразования получаемого запроса из БД к формату списка словарей
    :param requested_rating: tuple
    :return: list_of_dicts: list - список словарей требуемого формата
    """
    # Проверка на тип данных
    if not isinstance(requested_rating, str):
        raise TypeError('Ошибка ввода типа данных')

    # Ценз для детей
    if requested_rating == 'children':
        rating_group = "G"
    # Ценз для семейного просмотра
    elif requested_rating == 'family':
        rating_group = ('G', 'PG', 'PG-13')
    # Ценз для взрослых
    elif requested_rating == 'adult':
        rating_group = ('R', 'NC-17', 'NR', 'UR')
    else:
        return ['Ошибка', '<h2>Введена неверная возрастная группа. Повторите попытку</h2>']

    # Создаем пустой список, куда будем складывать словари
    list_of_dicts = []
    # Получаем результаты поиска
    movie_query = MovieQueries()
    list_of_results = movie_query.query_movie_by_rating(rating_group)
    for result in list_of_results:
        movie_dict = dict({
            "title": result[0],
            "rating": result[1],
            "description": result[2]
        })
        list_of_dicts.append(movie_dict)
    return list_of_dicts


def get_movies_by_genre(genre):
    """
    Функция преобразования получаемого запроса из БД к формату списка словарей
    :param genre: str - заданный жанр для поиска
    :return: list_of_dicts: list - список словарей требуемого формата
    """
    # Проверка на тип данных
    if not isinstance(genre, str):
        raise TypeError('Ошибка ввода типа данных')
    # Создаем пустой список, куда будем складывать словари
    list_of_dicts = []
    # Получаем результаты поиска
    movie_query = MovieQueries()
    list_of_results = movie_query.query_movie_by_genre(genre)
    for result in list_of_results:
        movie_dict = dict({
            "title": result[0],
            "description": result[1]
        })
        list_of_dicts.append(movie_dict)
    return list_of_dicts


def get_actors_list(actors):
    """
    Функция нахождения списка актеров, которые играли более двух раз с заданными актерами
    :param actors: список имен (полных или сокращенных) для поиска. Может быть задан как строкой, так и списком
    :return: actors_match: list - список актеров, которые снимались с искомой парой более чем в двух фильмах
    """
    # Создаем пустой список, в котором будем хранить наши совпадения по актерам
    actors_match = []

    # Проверяем на введенный тип данных и выполняем преобразование, если требуется
    if isinstance(actors, str):
        actors = tuple(actors.split(', '))
    if isinstance(actors, list|tuple):
        actors = tuple(actors)
    else:
        raise TypeError('Ошибка ввода типа данных')

    # Создаем объект для получения результата по запросу
    movie_query = MovieQueries()
    query_result = movie_query.query_movie_by_actors(actors)

    # Если нам вернулась ошибка, то возвращаем текст с ошибкой
    if len(query_result) == 1 and query_result[0][0] == 'Ошибка':
        return query_result[0][1]
    else:

        # Создаем словарь ключ: имя артиста, значение: количество попаданий в список cast
        # За основу берем первый фильм
        actors_dict = {key: 1 for key in query_result[0][0].split(', ')}

        # Проходимся циклом по каждому найденному списку актеров
        for i in range(1, len(query_result)):
            # Преобразуем строку найденных актеров к списку
            query_result[i] = list(query_result[i][0].split(', '))

            # Проходимся по каждому имени актера
            for name in query_result[i]:
                # Если имя актера есть в ключах словаря, то увеличиваем значений на 1
                if name in actors_dict.keys():
                    actors_dict[name] += 1
                # Если нет, то создаем ключ со значением 1
                else:
                    actors_dict[name] = 1

        # Удаляем актеров, которых мы ищем
        list_to_remove = []
        for key in actors_dict.keys():
            for actor in actors:
                if actor in key:
                    list_to_remove.append(key)
        for key in list_to_remove:
            del actors_dict[key]
            del list_to_remove

        # Далее находим всех, для которых частота попадания больше двух раз
        for key, value in actors_dict.items():
            if value >= 2:
                actors_match.append(key)

    return actors_match


def get_movie_by_params(content_type, year, genre):
    """
    Функция поиска списка фильмов по параметрам
    :param content_type: str - Кино или сериал
    :param year: int - год выпуска
    :param genre: str жанр контента
    :return: list_of_dicts: list - список словарей требуемого формата
    """
    # Проверяем на формат вводных данных
    if isinstance(content_type, str) or isinstance(year, int) or isinstance(genre, str):
        raise TypeError('Вы что-то не то ввели. Исправьте, пожалуйста :)')

    # Создаем пустой список, куда будем складывать словари
    list_of_dicts = []

    # Получаем результаты поиска
    movie_query = MovieQueries()
    list_of_results = movie_query.query_movie_by_params(content_type, year, genre)

    # Преобразуем результаты к словарю
    for result in list_of_results:
        movie_dict = dict({
            "title": result[0],
            "description": result[1]
                        })
        list_of_dicts.append(movie_dict)

    # Возвращаем json форматированный список
    return json.dumps(list_of_dicts)
