class SortService:
    @classmethod
    def parse_parameters(cls, parameters):
        if "sort" in parameters and parameters["sort"].lower().split()[0] == "price":
            sort_field = "price"
            sort_order = parameters["sort"].lower().split()[-1]
            reverse = False

            if sort_order == "desc":
                reverse = True

            return sort_field, reverse

        return None, None
