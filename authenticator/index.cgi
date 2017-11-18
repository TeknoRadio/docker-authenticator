#!/usr/bin/env python
from __future__ import print_function
import cgi
import datetime
import yaml
import json


class Users(dict):
    def __init__(self, filename):
        super(Users, self).__init__(self.read(filename))

    def read(self, filename):
        with open(filename) as fh:
            return yaml.safe_load(fh.read())['users']

    def get_attr(self, username, attr):
        if username not in self or attr not in self[username]:
            return
        return self[username][attr]

    def password(self, username):
        return self.get_attr(username, 'password')

    def timeslot(self, username):
        slot = self.get_attr(username, 'timeslot')
        if slot == 'always':
            return '00:00|23:59'
        return slot

    def dateslot(self, username):
        slot = self.get_attr(username, 'dateslot')
        if slot == 'always':
            return '11-09-1982|11-09-6982'    # TODO: Adjust in 5000 years
        return slot

    def strftime(self, dateslot, timeslot, element):
        timestring = "{} {}".format(timeslot.split('|')[element],
                                    dateslot.split('|')[element])
        return datetime.datetime.strptime(timestring, "%H:%M %d-%m-%Y")

    def start_time(self, username):
        return self.strftime(self.dateslot(username), self.timeslot(username), 0)

    def stop_time(self, username):
        return self.strftime(self.dateslot(username), self.timeslot(username), 1)

    def validate_user(self, username, password):
        try:
            return self.password(username) == password and \
                   self.start_time(username) <= datetime.datetime.now() <= self.stop_time(username)
        except:
            return False


if __name__ == "__main__":
    form = cgi.FieldStorage()
    username = form.getvalue('username')
    password = form.getvalue('password')
    user_dict = Users(filename=".users.yml")

    print('Content-Type: application/json\r\n\r')
    print(json.dumps(dict(success=user_dict.validate_user(username, password))))
