import sqlite3


class MovieQueries:

    def __init__(self):
        self.path = './static/data/netflix.db'

    def execute_query(self, query, return_one=True, return_all=False, return_many=False, size=50):
        """
        Вспомогательный метод, запускающий поиск по запросу
        :param query: входной параметр
        :param return_one: bool - вернуть только один результат
        :param return_all: bool - вернуть все результаты
        :param return_many: bool - вернуть выбранное количество результатов
        :param size: int - количество результатов для вывода при выборе параметра return_many
        :return: output: tuple - кортеж с результатами
        """
        # Проверяем, чтобы не было несколько параметров вывода одновременно
        if (return_one and return_all) or (return_all and return_many):
            return_all, return_one, return_many = True, False, False
        if return_one and return_many:
            return_all, return_one, return_many = False, False, True

        # Подключаемся к БД
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()

        # Выполняем запрос и сохраняем данные
        cursor.execute(query)
        # Если задан формат вывода, то выводим количество результатов, которое нужно

        # один
        if return_one:
            output = cursor.fetchone()
        # Все
        if return_all:
            output = cursor.fetchall()
        # По запросу
        if return_many:
            output = cursor.fetchmany(size)

        connection.close()
        # Возвращаем результат
        return output

    def query_movie_by_title(self, movie_title):
        """
        Получение данных из БД по названию.
        :param movie_title: str - наименование фильма, который необходимо найти, подается в формате строки.
        :return: output - кортеж с найденными данными
        """
        query = f"""
                    SELECT netflix.title, country, MAX(release_year), listed_in, description
                    FROM netflix
                    WHERE title LIKE LOWER ('%{movie_title.lower()}%')
                    AND netflix.type = 'Movie'
                    GROUP BY netflix.title
                    ORDER BY release_year DESC
                    """

        output = self.execute_query(query, return_all=True)
        return output

    def query_movie_by_year(self, start_year, end_year):
        """
        Выполняет запрос в БД и ищет список фильмов по заданным годам
        :param start_year: int - год, начиная с которого ищем
        :param end_year: int - год, заканчивая которым ищем
        :return: output - кортеж списков результатов
        """

        query = f"""SELECT netflix.title, 
                            netflix.release_year
                    FROM netflix
                    WHERE netflix.release_year BETWEEN {start_year} AND {end_year}
                    AND netflix.type = 'Movie'
                    ORDER BY release_year
                    LIMIT 100
                    """
        output = self.execute_query(query, return_all=True)

        return output

    def query_movie_by_rating(self, rating_group):
        """
        Выполняет запрос в БД и ищет список фильмов по заданному возрастному рейтингу
        :param rating_group: tuple - кортеж из рейтингов для поиска
        :return: output: tuple - кортеж списков результатов
        """

        if isinstance(rating_group, str):
            where_clause = f'WHERE netflix.rating LIKE "{rating_group}"'
        if isinstance(rating_group, tuple):
            where_clause = f'WHERE netflix.rating in {rating_group}'
        query = f"""SELECT netflix.title, netflix.rating, netflix.description
                    FROM netflix
                    {where_clause}
                    AND netflix.type = 'Movie'
                    ORDER BY netflix.title
                    LIMIT 100
                """
        output = self.execute_query(query, return_all=True)
        return output

    def query_movie_by_genre(self, genre):
        """
        Метод поиска в БД по жанру
        :param genre: str: - значение жанра для поиска
        :return: output: tuple - кортеж списков результатов
        """
        query = f"""
                    SELECT netflix.title, netflix.description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    AND netflix.type = 'Movie'
                    ORDER BY release_year DESC
                """
        output = self.execute_query(query, return_many=True, size=10)
        return output

    def query_movie_by_actors(self, actors):
        """
        Метод поиска в БД по двум актерам
        :param actors: tuple - кортеж из данных для поиска по двум актерам
        :return: output: tuple - кортеж списков результатов
        """
        # В первом запросе получаем количество строк в которых снимались актеры вместе
        query_get_count = f"""
                    SELECT count(*) as counter
                    FROM netflix
                    WHERE netflix.cast LIKE '%{actors[0].title()}%'
                    AND netflix.cast LIKE '%{actors[1].title()}%'
                    AND netflix.type = 'Movie'
                    GROUP BY "type"
                    """
        # Во втором запросе получаем список актеров, где играли оба актера одновременно
        # С группировкой по названию фильма, дабы убрать дубли
        query_get_actors = f"""
                            SELECT netflix.cast
                            FROM netflix
                            WHERE netflix.cast LIKE '%{actors[0].title()}%'
                            AND netflix.cast LIKE '%{actors[1].title()}%'
                            AND netflix.type = 'Movie'
                            GROUP BY "title"
                            """
        result = self.execute_query(query_get_count, return_all=True)
        # Если количество фильмов, в которых актеры снялись вместе более 2х, то возвращаем списки
        if result[0][0] >= 2:
            return self.execute_query(query_get_actors, return_all=True)

        # Если нет, то возвращаем ошибку
        else:
            return ['Ошибка'], ['Результаты, удовлетворяющие критериям поиска не найдены. Измените запрос']

    def query_movie_by_params(self, content_type, year, genre):
        """
        Функция по поиска по заданным параметрам
        :param content_type: str - Кино или сериал
        :param year: int - год выпуска
        :param genre: str жанр контента,
        :return: output: tuple - кортеж списков результатов
        """
        query = f"""SELECT netflix.title, netflix.description
                    FROM  netflix
                    WHERE netflix.type = '{content_type}'
                    AND listed_in LIKE '%{genre.title()}%'
                    AND release_year = {year}
                    ORDER BY netflix.title
                """
        output = self.execute_query(query, return_all=True)
        return output
