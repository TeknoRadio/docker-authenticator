import datetime
import requests
import subprocess

container = None
image = 'teknoradio/authenticator'
users_file = '/tmp/.users.yml'
service_url = 'http://localhost:10080'

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


def write_users_file(container):
    with open(users_file, 'w') as fh:
        fh.write(content)

    print(content)

    dest = '/usr/local/apache2/htdocs/.users.yml'
    subprocess.check_call(
        'docker cp {} {}:{}'.format(users_file, container.strip().decode("utf-8"), dest).split()
    )


def test_that_container_can_be_build():
    subprocess.check_call(['docker', 'build', '-t', image, '.'])


def test_that_container_can_be_started():
    global container
    container = subprocess.check_output([
        'docker', 'run', '-i', '-d', '--rm', '-p', '10080:80', image
    ])
    write_users_file(container.strip())


def test_that_get_request_to_service_returns_false():
    ret = requests.get(service_url)
    ret.raise_for_status()
    assert ret.json()['success'] is False


def test_that_post_request_from_always_allowed_returns_true():
    ret = requests.post(service_url, data={"username": "always_allowed", "password": "pass"})
    ret.raise_for_status()
    assert ret.json()['success'] is True


def test_that_post_request_from_history_returns_false():
    ret = requests.post(service_url, data={"username": "history", "password": "pass"})
    ret.raise_for_status()
    assert ret.json()['success'] is False


def test_that_post_request_in_future_forbidden_returns_false():
    ret = requests.post(service_url, data={"username": "future", "password": "pass"})
    ret.raise_for_status()
    assert ret.json()['success'] is False


def test_that_post_request_from_timeslot_not_allowed_returns_false():
    ret = requests.post(service_url, data={"username": "timeslot_not_allowed", "password": "pass"})
    ret.raise_for_status()
    assert ret.json()['success'] is False


def test_that_post_request_from_timeslot_allowed_returns_true():
    ret = requests.post(service_url, data={"username": "always_allowed", "password": "pass"})
    ret.raise_for_status()
    assert ret.json()['success'] is True


def test_that_post_request_with_config_error_returns_502():
    ret = requests.post(service_url, data={"username": "always_allowed", "password": "pass"})
    ret.raise_for_status()
    assert ret.json()['success']


def test_that_container_can_be_removed():
    subprocess.check_call(['docker', 'rm', '-f', container.strip()])
