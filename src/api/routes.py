from flask import Flask, jsonify, request, abort, make_response, Response, Blueprint
from src.utils.utils import Utils
from src.services.search_service import SearchService
from src.services.data_ingestion_service import IngestionService

utils = Utils()
search_service = SearchService()
ingestion_service = IngestionService()
api = Blueprint('api', __name__)

@api.route("/", methods=["GET"])
def hello():
    return "Hello world"

@api.route("/index_or_update_product", methods=["POST"])
def index():
    data = request.get_json()
    if not data or not data.get("id"):
        return make_response(jsonify({"error": "id is required"}), 400)

    response = ingestion_service.index_product(data, index_name="products_index")
    return make_response(jsonify(response), 200)

@api.route("/setup_products_index", methods=["GET"])
def setup():
    response = ingestion_service.setup_products_index()
    return make_response(jsonify(response), 200)

@api.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    if not data or not data.get("query"):
        return make_response(jsonify({"error": "query is required"}), 400)

    search_term = data.get("query")
    latitude = data.get("latitude", None)
    longitude = data.get("longitude", None)
    sort_by = data.get("sort_by", "relevance_high_low")
    limit = data.get("limit", 20)
    page_num = data.get("page_num", 1)
    country = data.get("country", 1)
    radius_km = data.get("radius_km", 20)
    min_price = data.get("min_price", None)
    max_price = data.get("max_price", None)
    category_id = data.get("category_id", None)
    locale = data.get("locale", "En")

    extracted_prices = utils.extract_prices(search_term)
    if len(extracted_prices) and max(extracted_prices) > 50 and not min_price and not max_price:
        max_price = max(extracted_prices)
        min_price = max_price - 0.2 * max_price

    print(max_price)
    print(min_price)

    products, total = search_service.search_products(search_term, latitude, longitude, sort_by, limit, page_num, country, radius_km, min_price, max_price, category_id, locale)

    return make_response(jsonify({"products": products, "total": total}), 200)

@api.route("/suggest_search_terms", methods=["POST"])
def suggest():
    data = request.get_json()
    if not data or not data.get("query"):
        return make_response(jsonify({"error": "query is required"}), 400)

    search_term = data.get("query")
    suggestions = search_service.product_suggestions(search_term)

    return make_response(jsonify({"suggestions": suggestions}), 200)
