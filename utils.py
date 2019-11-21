from datetime import datetime


def get_time_range_vars(time_range):
    lesson_date, start_time, end_time = time_range.split('__')

    start_time = datetime.strptime(lesson_date + 'T' + start_time + ':00+00:00', '%Y-%m-%dT%H:%M:%S%z')
    end_time = datetime.strptime(lesson_date + 'T' + end_time + ':00+00:00', '%Y-%m-%dT%H:%M:%S%z')

    return lesson_date, start_time, end_time
