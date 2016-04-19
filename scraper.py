import html.parser
import json
import datetime
from bs4 import BeautifulSoup


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


def parse_time(time, day):
    day_offset = datetime.timedelta('MTWRF'.find(day))
    first_day = datetime.datetime(2016, 3, 28)
    times = time.split('-')
    timezone = 'US/Pacific'

    date = first_day + day_offset
    start_time = date + format_time(times[0])
    end_time = date + format_time(times[1])

    start = {'dateTime': start_time.isoformat(), 'timeZone': timezone}
    end = {'dateTime': end_time.isoformat(), 'timeZone': timezone}
    return start, end


def format_time(time):
    hour = int(time.split(':')[0])
    if time.endswith("pm") and not time.startswith('12'):
        hour += 12
    minute = int(time[time.find(':')+1:time.find(':')+3])
    return datetime.timedelta(hours=hour, minutes=minute)


def get_recurrence(repeat):
    until = datetime.date(2016, 6, 2).isoformat().replace('-','')

    byday = repeat.replace('', ',').strip(',')
    byday = byday.replace('M', 'MO')
    byday = byday.replace('T', 'TU')
    byday = byday.replace('W', 'WE')
    byday = byday.replace('R', 'TH')
    byday = byday.replace('F', 'FR')

    rrule = 'RRULE:FREQ=WEEKLY;UNTIL={0};BYDAY={1}'.format(until, byday)

    return [rrule]

html_file = 'ecs_courses.html'
with open(html_file, 'r') as html:
    html_string = html.read()

soup = BeautifulSoup(html_string, 'html.parser')
rows = soup.find_all('tr')
course_list = dict()

for lecture_row, discussion_row in pairwise(rows[2:]):
    lecture_cells = lecture_row.find_all('td')
    discussion_cells = discussion_row.find_all('td')

    lecture = dict()
    lecture['summary'] = lecture_cells[2].text + ' ' + lecture_cells[3].text
    lecture['location'] = lecture_cells[21].text
    lecture['description'] = lecture_cells[7].text
    repeat = lecture_cells[8].text
    lecture['start'], lecture['end'] = parse_time(lecture_cells[9].text, repeat[0])
    lecture['recurrence'] = get_recurrence(repeat)

    discussion = lecture.copy()
    discussion['summary'] += ' ' + lecture_cells[4].text
    discussion['location'] = discussion_cells[21].text
    discussion['description'] += ' Discussion'
    repeat = discussion_cells[8].text
    discussion['start'], discussion['end'] = parse_time(discussion_cells[9].text, repeat[0])
    discussion['recurrence'] = get_recurrence(repeat)

    course_list[lecture['summary']] = lecture  # adds the course to the list using its name as key
    course_list[discussion['summary']] = discussion  # adds the course to the list using its name as key


with open('courses.json', 'w') as f:
    f.write(json.dumps(course_list, indent=4, sort_keys=True))
