import requests
from flask import current_app

from flaskapp.models import ProductModel


class SearchService:
    required_fields = ["uniqueId", "title", "availability", "productDescription", "productImage", "price"]

    @classmethod
    def fire_search_query(cls, search_params):
        search_url = current_app.config['UNBXD_SEARCH_URL'] + current_app.config['UNBXD_API_KEY'] \
                     + "/" + current_app.config['SITE_KEY'] + "/search/"

        search_params["fields"] = ",".join(SearchService.required_fields)

        search_data = requests.get(search_url, params=search_params).json()

        return search_data

    @classmethod
    def parse_search_results(cls, search_data):
        if "response" not in search_data or "products" not in search_data["response"] or "numberOfProducts" not in search_data["response"]:
            return 500, "Search API Down"

        number_of_products = search_data["response"]["numberOfProducts"]

        product_list = []

        for dataItem in search_data["response"]["products"]:
            if "uniqueId" not in dataItem or "price" not in dataItem:
                number_of_products -= 1
                continue

            product_id = dataItem["uniqueId"]
            title = dataItem.get("title", None)

            if "availability" in dataItem:
                availability = dataItem["availability"].lower() == "true"
            else:
                availability = False

            product_description = dataItem.get("productDescription", None)
            image_url = dataItem.get("productImage", None)  # Replace this maybe
            price = dataItem["price"]

            product = ProductModel(
                id=product_id,
                title=title,
                availability=availability,
                productDescription=product_description,
                imageURL=image_url,
                price=price
            )

            product_list.append(product)

        if len(product_list) == 0:
            return 400, "No match found"

        return 200, {
            "products": product_list,
            "total": number_of_products
        }
