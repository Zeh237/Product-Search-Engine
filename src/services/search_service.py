
from src.db_connection.mysqlDBconnection import DBConnection
from src.db_connection.elasticsearchDBconnection import ElasticsearchDBConnection
from src.utils import utils
import logging


class SearchService:
    def __init__(self):
        self.db_connection = DBConnection()
        self.engine = self.db_connection.create_db_connection()
        self.es = ElasticsearchDBConnection().es_connection()
        self.utils = utils.Utils()

    def search_products(self, search_term, latitude=None, longitude=None, sort_by="relevance_high_low",
                        limit=20, page_num=1, country=1, radius_km=20, min_price=None,
                        max_price=None, category_id=None, locale="En"):
        """
        Function to search products using Elasticsearch, incorporating relevance and boosting functionality.
        :param search_term:
        :param latitude:
        :param longitude:
        :param sort_by:
        :param limit:
        :param page_num:
        :param country:
        :param radius_km:
        :param min_price:
        :param max_price:
        :param category_id:
        :param locale: The locale of the user.
        :return:
            tuple: A tuple containing a list of products and the total result count.
        """

        offset = (page_num - 1) * limit

        if locale == "En":
            search_fields = [
                "name^2",
                "category_name_en^2",
                "description",
                "search_index",
                "hash"
            ]
        else:
            search_fields = [
                "name_fr^2",
                "category_name_fr^2",
                "description_fr",
                "search_index",
                "hash"
            ]

        # base query
        search_query = {
            "size": limit,
            "from": offset,
            "min_score": 4.7,
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "multi_match": {
                                        "query": search_term,
                                        "fields": search_fields,
                                        "fuzziness": "AUTO"
                                    }
                                },
                                {
                                    "term": {"country": country}
                                }
                            ],
                            "filter": []
                        }
                    },
                    "functions": [
                        {
                            "gauss": {
                                "created_at": {
                                    "origin": "now",
                                    "scale": "90d",
                                    "offset": "30d",
                                    "decay": 0.7
                                }
                            },
                            "weight": 0.8
                        }
                    ],
                    "boost_mode": "sum",
                    "score_mode": "avg"
                }
            },
            "sort": []
        }

        # category filter
        if category_id:
            search_query["query"]["function_score"]["query"]["bool"]["must"].append({
                "bool": {
                    "should": [
                        {"match": {"category_id": category_id}},
                        {"match": {"category_id": category_id}}
                    ],
                    "minimum_should_match": 1
                }
            })

        # location filter
        if latitude and longitude:
            search_query["query"]["function_score"]["query"]["bool"]["filter"].append({
                "geo_distance": {
                    "distance": f"{radius_km}km",
                    "location": {
                        "lat": latitude,
                        "lon": longitude
                    }
                }
            })

        # price filter
        if min_price:
            search_query["query"]["function_score"]["query"]["bool"]["filter"].append(
                {"range": {"price": {"gte": min_price}}})
        if max_price:
            search_query["query"]["function_score"]["query"]["bool"]["filter"].append(
                {"range": {"price": {"lte": max_price}}})

        # Sorting
        if sort_by == 'alphabetically_az':
            search_query["sort"].append({"name.keyword": "asc"})
        elif sort_by == 'alphabetically_za':
            search_query["sort"].append({"name.keyword": "desc"})
        elif sort_by == 'price_low_high':
            search_query["sort"].append({"price": "asc"})
        elif sort_by == 'price_high_low':
            search_query["sort"].append({"price": "desc"})
        elif sort_by == 'date_old_new':
            search_query["sort"].append({"created_at": "asc"})
        elif sort_by == 'date_new_old':
            search_query["sort"].append({"created_at": "desc"})
        elif sort_by == 'relevance_low_high':
            search_query["sort"].append({"_score": "asc"})
        elif sort_by == 'relevance_high_low':
            search_query["sort"].append({"_score": "desc"})
        elif sort_by == 'distance_near_far' and latitude and longitude:
            search_query["sort"].append({
                "_geo_distance": {
                    "location": {"lat": latitude, "lon": longitude},
                    "order": "asc",
                    "unit": "km",
                    "mode": "min"
                }
            })
        elif sort_by == 'distance_far_near' and latitude and longitude:
            search_query["sort"].append({
                "_geo_distance": {
                    "location": {"lat": latitude, "lon": longitude},
                    "order": "desc",
                    "unit": "km",
                    "mode": "min"
                }
            })
        else:
            search_query["sort"].append({"_score": "desc"})

        response = self.es.search(index="products_index", body=search_query, request_timeout=30)

        total_results_count = response["hits"]["total"]["value"]
        search_results = [hit["_source"] for hit in response["hits"]["hits"]]
        return search_results, total_results_count

    def product_suggestions(self, index_name, country, user_input, limit=20, page_num=1, locale="En"):
        """
        Function to provide product suggestions based on user input using Elasticsearch,
        incorporating relevance and boosting functionality.

        Parameters:
            index_name (str): The name of the index to search.
            country (int): Country where product is found
            user_input (str): The user's search input.
            limit (integer): The number of suggestions to return.
            page_num (integer): The page/offset of suggestions to return.
            locale (str): The locale of the user.

        Returns:
            tuple: A tuple containing a list of relevant product names and the total result count.
        """

        offset = int((page_num - 1) * limit)

        if locale == "En":
            search_fields = ["name^2"]
        else:
            search_fields = ["name_fr^2"]

        search_query = {
            "size": limit,
            "from": offset,
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "multi_match": {
                                        "query": user_input,
                                        "fields": search_fields,
                                        "fuzziness": "AUTO",
                                        "type": "bool_prefix"
                                    }
                                }
                            ],
                            "filter": [
                                {
                                    "term": {
                                        "country": country
                                    }
                                }
                            ]
                        }
                    },
                    "functions": [
                        {
                            "gauss": {
                                "created_at": {
                                    "origin": "now",
                                    "scale": "90d",
                                    "offset": "30d",
                                    "decay": 0.5
                                }
                            }
                        }
                    ],
                    "boost_mode": "multiply"
                }
            },
            "sort": [
                {"_score": "desc"}
            ]
        }

        response = self.es.search(index=index_name, body=search_query, request_timeout=30)

        total_results_count = response["hits"]["total"]["value"]

        hits = response["hits"]["hits"]
        suggestions = [hit["_source"]["name"] if locale == "En" else hit["_source"]["name_fr"] for hit in hits]

        return suggestions, total_results_count
