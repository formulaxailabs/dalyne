from rest_framework.pagination import LimitOffsetPagination,\
             PageNumberPagination


class CSLimitOffestpagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class CSPageNumberTenderPagination(PageNumberPagination):
    page_size = 20


class CSPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_count'


class OnOffPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_size(self, request):
        if self.page_size_query_param:
            page_size = min(
                int(
                    request.query_params.get(
                        self.page_size_query_param, self.page_size)
                        ), self.max_page_size)
            if page_size > 0:
                return page_size
            elif page_size == 0:
                return None
        return self.page_size
