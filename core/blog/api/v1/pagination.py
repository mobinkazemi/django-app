from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class GlobalPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "custom_key_for_total": self.page.paginator.count,
                "custom_key_for_page_size": self.page_size,
                "custom_key_for_current_page": self.page.number,
                "custom_key_for_total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
        return super().get_paginated_response(data)
