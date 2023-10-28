from rest_framework import pagination
from rest_framework.response import Response

class cutomepegination(pagination.PageNumberPagination):
    page_size= 10
    page_size_query_param='count'
    max_page_size= 100000
    page_query_param = 'page' 

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,  # Add the total number of pages
            'next': self.get_next_link(),
            'previous': self.get_previous_link()
        })