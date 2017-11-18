import datetime

current_time = datetime.datetime.now()
time_plus_two = current_time + datetime.timedelta(hours=2)
time_minus_two = current_time - datetime.timedelta(hours=2)
content = """
users:
  always_allowed:
    password: "pass"
    timeslot: "always"
    dateslot: "always"

  history:
    password: "pass"
    timeslot: "always"
    dateslot: "11-09-1982|2-1-1985"

  future:
    password: "pass"
    timeslot: "always"
    dateslot: "3-2-5000|3-2-5001"

  timeslot_not_allowed:
    password: "pass"
    timeslot: "{time_minus_two}|{time_minus_two}"
    dateslot: "{date_minus_two}|{date_minus_two}"

  timeslot_allowed:
    password: "pass"
    timeslot: "{time_minus_two}|{time_plus_two}"
    dateslot: "{date_minus_two}|{date_plus_two}"

  config_error:
    password: "pass"

""".format(
    time_minus_two=time_minus_two.strftime('%H:%M'),
    date_minus_two=time_minus_two.strftime('%d-%m-%Y'),

    time_plus_two=time_plus_two.strftime('%H:%M'),
    date_plus_two=time_plus_two.strftime('%d-%m-%Y'),
)