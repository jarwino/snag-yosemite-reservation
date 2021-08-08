from bottle import route, run, template
import requests
import datetime
from datetime import datetime, timedelta

def get_date(date):
    #2021-08-26
    endpoint = f'https://www.recreation.gov/api/timedentry/availability/facility/10086745?date={date}'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'} 
    return requests.get(endpoint, headers=headers)

def check_count_for_date(date):
    d = get_date(date)
    if d:
        val = d.json()
        total_count = val[0]['inventory_count']['ANY']
        reservation_count = val[0]['reservation_count']['ANY']
        left = total_count - reservation_count
        if left > 0:
            return left
    return None

def get_resp_for_date(date):
    result = f'[{date}] no :('
    count = check_count_for_date(date)
    if count:
        result = f'[{date}] Yes, there are {count} tickets left'
    return result

@route('/check_date/<date>', method='POST')
def check_date(date):
    result = ''
    if '|' in date:
        dates = date.split('|')
        if len(dates) == 2:
            start = dates[0]
            end = dates[1]

            start = datetime.strptime(start, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')

            start_l = 0
            end_l = 30
            while start != end and start_l < end_l:
                d = start.strftime('%Y-%m-%d')
                result += get_resp_for_date(d)
                start += timedelta(days=1)
                start_l += 1
    else:
        result = get_resp_for_date(date)

    return result

@route('/')
def index():
    title = 'Do the ticket be not taken?'
    return template(
'''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>IS YOUR RESERVATION AVALIABLE</title>
  </style>
  <script src="https://code.jquery.com/jquery-3.5.0.js"></script>
</head>
<body>


<b>{{title}}</b>
<input type="text" id="date" value='2021-08-24'>
<br>
<button type="button" onclick="onSubmit()">Check pls!</button>
<br>
<p id="response"></p>
<script>
function onSubmit() {
    var value = $("#date").val() 
    var request = new Request('/check_date/' + value);
    var method = { method: 'POST' };
    fetch(request, method).then(function(response) {
        response.text().then(function(t) {
            return $("#response").text(t);
        });
    });
}
</script>
'''
        ,title=title)

def server_main():
    run(host='0.0.0.0', port=80)
