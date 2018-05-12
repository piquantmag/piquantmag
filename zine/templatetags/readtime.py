import math

from django import template
from django.contrib.humanize.templatetags.humanize import apnumber

register = template.Library()


AVERAGE_READING_SPEED_WPM = 200


@register.filter
def readtime(text):
    minutes_of_read_time = len(text.split(' ')) / AVERAGE_READING_SPEED_WPM
    minutes_of_read_time_rounded = math.floor(minutes_of_read_time + 0.5)
    return apnumber(minutes_of_read_time_rounded)
