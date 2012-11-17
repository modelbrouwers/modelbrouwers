from django.shortcuts import get_object_or_404
from datetime import date

def get_current_ss(ss_class):
    today = date.today()
    this_year = today.year
    if today.month in [1,2]:
        this_year -= 1
    secret_santa = get_object_or_404(ss_class, year=this_year)
    return secret_santa
