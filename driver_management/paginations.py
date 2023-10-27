from rest_framework import pagination

class cutomepegination(pagination.PageNumberPagination):
    page_size= 10
    page_size_query_param='count'
    max_page_size= 10