from datetime import datetime


def parse_datetime(year, month_name):
    year = int(year)

    month_names = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
    month = 0
    for i in range(12):
        if month_name == month_names[i]:
            month = i+1
            break
    return datetime(year, month, 1)