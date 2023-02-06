class PaginationService:
    @classmethod
    def parse_parameters(cls, parameters):
        page = parameters.get("page", 1)
        rows = parameters.get("rows", None)
        return page, rows
