import pandas as pd
from elasticsearch.helpers import bulk
from sqlalchemy import text
from src.data import products_mapping
from src.db_connection.mysqlDBconnection import DBConnection
from src.db_connection.elasticsearchDBconnection import ElasticsearchDBConnection
from src.utils import utils
import logging


class IngestionService:
    def __init__(self):
        self.db_connection = DBConnection()
        self.engine = self.db_connection.create_db_connection()
        self.es = ElasticsearchDBConnection().es_connection()
        self.utils = utils.Utils()

    def fetch_products(self):
        """
        Function to fetch data from MySQL database.

        Returns:
            list: A list of dictionaries containing the fetched data.
        """

        query = """
        SELECT
            p.*,
            c.name AS category_name_en,
            c.name_fr AS category_name_fr
        FROM
            products p
        JOIN
            categories c ON p.category_id = c.id;
        """
        try:
            with self.engine.connect() as connection:
                result = pd.read_sql(text(query), connection)

            result = result.to_dict(orient='records')

            for item in result:
                if 'price' in item and item['price'] is not None:
                    item['price_formatted'] = self.utils.format_large_number(item['price'])

                if item.get("latitude") is not None and item.get("longitude") is not None:
                    latitude = round(item["latitude"], 2)
                    longitude = round(item["longitude"], 2)
                    item["location"] = {"lat": latitude, "lon": longitude}
                else:
                    item['price_formatted'] = None
            logging.info("Products data fetched successfully.")
            return result
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")

    def create_index(self, index_name, mapping):
        """
        Function to create an index in Elasticsearch.

        Args:
            index_name (str): The name of the index to be created.
            mapping (dict): The mapping for the index.

        Returns:
            dict: The response from Elasticsearch.
        """

        return self.es.indices.create(index=index_name, body=mapping)

    def delete_index(self, index_name):
        """
        Function to delete an index in Elasticsearch.

        Args:
            index_name (str): The name of the index to be deleted.

        Returns:
            dict: The response from Elasticsearch.
        """

        return self.es.indices.delete(index=index_name)

    def document_exists(self, index_name, doc_id):
        """
        Function to check if a document exists in an index.
        :param index_name:
        :param doc_id:
        :return:

        """
        query = {
            "query": {
                "term": {"id": doc_id}
            }
        }
        result = self.es.search(index=index_name, body=query)
        return result['hits']['total']['value'] > 0

    def index_exists(self, index_name):
        """
        Function to check if an index exists in Elasticsearch.
        :param index_name:
        :return:

        """
        return self.es.indices.exists(index=index_name)

    def bulk_index_documents(self, data, index_name):
        """
        Function to bulk index data in Elasticsearch.
        :param data:
        :param index_name:
        :return:
            dict: The response from Elasticsearch.
        """
        actions = []
        for item in data:
            actions.append({
                "_index": index_name,
                "_id": item["id"],
                "_source": item
            })

        try:
            response = bulk(self.es, actions, index=index_name, raise_on_error=False)
            logging.info(f"Indexed {len(data)} documents")
            return response
        except Exception as e:
            return f"error: {str(e)}"

    def setup_products_index(self):
        """
        Function to setup the products index in Elasticsearch.

        Returns:
            dict: The response from Elasticsearch.
        """

        index_name = "products_index"
        mapping = products_mapping.products_mapping

        try:
            if self.index_exists(index_name):
                self.delete_index(index_name)
                self.create_index(index_name, mapping)

            data = self.fetch_products()
            result = self.bulk_index_documents(data, index_name)
            return result

        except Exception as e:
            return f"error: {str(e)}"

    def index_product(self, product_document, index_name="products_index"):
        """
        Function to index a product in Elasticsearch.
        :param product_document:
        :return:

        """
        if product_document["id"] is None:
            return f"error: product id is required"

        if 'price' in product_document and product_document['price'] is not None:
            product_document['price_formatted'] = self.utils.format_large_number(product_document['price'])
        else:
            product_document['price_formatted'] = None

        try:
            # if document exist, update it
            if self.document_exists(index_name, product_document["id"]):
                response = self.es.update_by_query(
                    index=index_name,
                    body={
                        "script": {
                            "source": f"""
                                {"".join([f"ctx._source.{field} = params.document.{field};" for field in product_document.keys()])}
                            """,
                            "lang": "painless",
                            "params": {"document": product_document}
                        },
                        "query": {"term": {"id": product_document.get("id")}}
                    }
                )

                if response.get("updated", 0) > 0:
                    logging.info("Product updated successfully.")
                    return True
                else:
                    return False
            else:
                if "latitude" and "longitude" in product_document:
                    product_document["location"] = {"lat": product_document["latitude"], "lon": product_document["longitude"]}

                self.es.index(index=index_name, id=product_document["id"], body=product_document)
                logging.info("Product indexed successfully.")
                return True
        except Exception as e:
            return f"error: {str(e)}"
