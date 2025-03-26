products_mapping = {
    "mappings": {
        "properties": {
            "brand_id": {
                "type": "integer"
            },
            "category_id": {
                "type": "integer"
            },
            "category_name_en": {
                "type": "search_as_you_type",
                "doc_values": False,
                "max_shingle_size": 3,
                "analyzer": "english",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "category_name_fr": {
                "type": "search_as_you_type",
                "doc_values": False,
                "max_shingle_size": 3,
                "analyzer": "french",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "country": {
                "type": "integer",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "created_at": {
                "type": "date"
            },
            "currency": {
                "type": "text",
                "analyzer": "standard"
            },
            "deleted_at": {
                "type": "date"
            },
            "description": {
                "type": "search_as_you_type",
                "doc_values": False,
                "max_shingle_size": 3,
                "analyzer": "english",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "description_fr": {
                "type": "search_as_you_type",
                "doc_values": False,
                "max_shingle_size": 3,
                "analyzer": "french",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "hash": {
                "type": "text",
                "analyzer": "standard"
            },
            "id": {
                "type": "integer"
            },
            "image": {
                "type": "text",
                "analyzer": "standard"
            },
            "latitude": {
                "type": "double",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "location": {
                "type": "geo_point"
            },
            "longitude": {
                "type": "double",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "name": {
                "type": "search_as_you_type",
                "doc_values": False,
                "max_shingle_size": 3,
                "analyzer": "english",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "name_fr": {
                "type": "search_as_you_type",
                "doc_values": False,
                "max_shingle_size": 3,
                "analyzer": "french",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "price": {
                "type": "integer",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "price_formatted": {
                "type": "text",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "search_index": {
                "type": "search_as_you_type",
                "doc_values": False,
                "max_shingle_size": 3,
                "analyzer": "standard",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "updated_at": {
                "type": "date"
            },
            "user_id": {
                "type": "integer"
            },
            "whole_sale": {
                "type": "integer"
            }
        }
    }
}
