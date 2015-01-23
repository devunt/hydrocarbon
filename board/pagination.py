from django.core.paginator import Paginator


class HCPaginator(Paginator):
    adjacent_pages = 5

    def page(self, number):
        self.page_num = number
        return super().page(number)

    @property
    def page_range(self):
        start = max(1, self.page_num - self.adjacent_pages)
        end = min(self.num_pages, self.page_num + self.adjacent_pages)
        if (end - start) < (self.adjacent_pages * 2):
            if start == 1:
                end += self.adjacent_pages - (self.page_num - start)
            if end == self.num_pages:
                start -= self.adjacent_pages - (end - self.page_num)
        return list(range(start, end + 1))
