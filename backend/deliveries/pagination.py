from rest_framework.pagination import PageNumberPagination

class DeliveriesPageNumberPagination(PageNumberPagination):
    page_size = 10                    # значение по умолчанию
    page_size_query_param = 'page_size'  # параметр запроса
    max_page_size = 100               # максимальный размер страницы
