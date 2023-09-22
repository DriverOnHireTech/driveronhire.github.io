# from location_field.models.plain import PlainLocationField

from datetime import date


class leavecalcu:
    
    @staticmethod
    def get_difference(date1, date2):
        delta = date2 - date1
        return delta.days

d1 = date(2023, 7, 20)
d2 = date(2023, 7, 25)
obj =leavecalcu
days=obj.get_difference(d2,d1)
# print(f'Difference is {days} days')