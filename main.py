import os
import json
import configparser
from datetime import datetime, timedelta
from json2html import *

from utils import get_time_range_vars


def main():
    # Reading Configs
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Setting configuration values
    chat_name = config['Telegram']['chat_name']
    phone = config['Telegram']['phone']
    limit = config['Telegram']['limit']
    time_range = config['Telegram']['time_range']

    # Getting students list from students.txt file
    students = []
    with open('students.txt') as students_file:
        for student in students_file:
            students.append(student.strip())

    command = f'telegram-messages-dump --chat="{chat_name}" -p {phone} -l {limit} -o tmp/chat_history.json -e jsonl'

    # Getting chat history
    os.system(command)

    if not os.path.isfile('./tmp/chat_history.json'):
        print('File "chat_history.json" doesn\'t exist')
        quit()

    # Getting time range variables
    lesson_date, start_time, end_time = get_time_range_vars(time_range)

    # Extracting needed data
    lesson_messages = []
    with open('./tmp/chat_history.json') as chat_history_file:
        for row in chat_history_file:
            if lesson_date not in row:
                continue
            message = json.loads(row)
            message_time = datetime.strptime(message['date'], '%Y-%m-%dT%H:%M:%S%z') + timedelta(hours=2)
            if start_time <= message_time <= end_time:
                lesson_messages.append(message)

    student_messages = {}
    for message in lesson_messages:
        if message['author'] in students:
            student_messages.setdefault(message['author'], [])
            student_messages[message['author']].append([message['date'], message['content']])

    # Reformatting data
    messages_json = json.dumps(student_messages, indent=2, ensure_ascii=False)
    messages_html = json2html.convert(json=messages_json)

    # Writing data
    # with open('data.html', 'w') as html_file:
    #     html_file.write(messages_html)

    dir_name = os.path.dirname(os.path.abspath(__file__)) + '/archive/' + lesson_date.replace('-', '_')
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name, exist_ok=True)
        print('Аrchive dir created!')

    file_name = start_time.strftime('%H:%M').replace(':', '_') + '__' + end_time.strftime('%H:%M').replace(':', '_')

    with open(dir_name + '/' + file_name + '.html', "w") as html_file:
        html_file.write(messages_html)


if __name__ == '__main__':
    main()
