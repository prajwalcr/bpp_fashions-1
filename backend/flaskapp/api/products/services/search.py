import requests
from flask import current_app
from typing import Tuple, Union

from flaskapp.api.products.dal.product import ProductDAL


class SearchService:
    """Service layer for search operations."""

    # List of fields to be return by Search API for each product.
    required_fields = ["uniqueId", "title", "availability", "productDescription", "productImage", "price"]

    @classmethod
    def fire_search_query(cls, search_params: dict) -> dict:
        """
        Run Unbxd's search query according to the search parameters passed.

        For information about possible search parameters,
        refer Unbxd's search documentation at https://unbxd.com/docs/site-search/integration-documentation/search-api/

        Parameters
        ----------
        search_params: dict
            Contains search parameters including the one for defining the search query.

        Returns
        ----------
        dict:
            Collection of metadata and products returned by Unbxd's search API.
        """

        search_url = current_app.config['UNBXD_SEARCH_URL'] + current_app.config['UNBXD_API_KEY'] \
                     + "/" + current_app.config['SITE_KEY'] + "/search/"

        search_params["fields"] = ",".join(SearchService.required_fields)

        search_data = requests.get(search_url, params=search_params).json()

        return search_data

    @classmethod
    def parse_search_results(cls, search_data: dict) -> Tuple[int, Union[str, dict]]:
        """
        Parse the results returned from Unbxd's search API.

        Parameters
        ----------
        search_data: dict
            Contains metadata and products returned by Unbxd's search API.

        Returns
        ----------
        int:
            Status code for the request.
        dict:
            Status code and list of products if no errors. In case of errors, error message returned with status code.
        """

        if "response" not in search_data or "products" not in search_data["response"] or "numberOfProducts" not in search_data["response"]:
            return 500, "Search API Down"

        number_of_products = search_data["response"]["numberOfProducts"]

        product_list = []

        for dataItem in search_data["response"]["products"]:
            item_is_bad = "uniqueId" not in dataItem or "price" not in dataItem
            if item_is_bad:
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

            product = ProductDAL.create(
                id=product_id,
                title=title,
                availability=availability,
                product_description=product_description,
                image_url=image_url,
                price=price
            )

            product_list.append(product)

        # Return 404 error if no matching products found
        if len(product_list) == 0:
            return 404, "No match found"

        return 200, {
            "products": product_list,
            "total": number_of_products
        }
