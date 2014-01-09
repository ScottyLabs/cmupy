#!/usr/bin/env python
'''
A library for ScottyLabs APIs

Exported Classes:
Scheduling -- A library for accessing ScottyLabs's API for CMU
Scheduling.

'''

import datetime
import itertools
import json
import urllib2

def current_semester():
    '''
    Returns the most recent semester that the APIs will have data for
    '''
    today = datetime.date.today()
    if today.month in range(1,6):
        return 'S' + str(today.year)[2:]
    else:
        return 'F' + str(today.year)[2:]

class Scheduling:
    '''
    A library for accessing ScottyLabs's API for CMU Scheduling.

    Public functions:
    request -- Make a request to the scheduling API

    departments -- Get a list of all the departments for a given
    semester

    courses -- Get a list of all the courses under a given
    department for a given semester

    course -- Get information about a given course for a given
    semester

    '''

    def __init__(self, app_id=None, app_secret_key=None):
        if not app_id or not app_secret_key:
            raise ValueError('Using the Scheduling API requires an app ID and an app secret key')
        self.id = app_id
        self.secret_key = app_secret_key
        self.valid_departments = {}

    def request(self, uri, limit=None, page=None, debug=False):
        '''
        Make a request to the scheduling API
        '''
        req_url = 'https://apis.scottylabs.org/v1/schedule%s?app_id=%s&app_secret_key=%s' % (uri, self.id, self.secret_key)
        if limit is not None:
            req_url += '&limit=' + str(limit)
        if page is not None:
            req_url += '&page=' + str(page)
        if debug: print('[DEBUG] GET %s' % req_url)
        req = urllib2.Request(req_url)
        handler = urllib2.urlopen(req)
        if handler.getcode() != 200:
            try:
                return json.load(handler.fp)
            except:
                return {
                    'error': '%d: %s' % (handler.getcode(), handler.msg)
                }
        try:
            return json.load(handler.fp)
        except:
            return None

    def __validate_department(self, semester, department):
        department = int(department)
        if semester not in self.valid_departments:
            self.valid_departments[semester] = [d['id'] for d in self.departments(semester)]
        if department not in self.valid_departments[semester]:
            raise ValueError('%d is not a valid department for semester %s' % (department, semester))

    def departments(self, semester=current_semester()):
        '''
        Get a list of all the departments for a given semester
        '''
        return self.request('/%s/departments/' % semester, limit=100)['departments']

    def courses(self, semester=current_semester(), department=None):
        '''
        Get a list of all the courses under a given department for
        a given semester
        '''
        if department is None:
            if semester not in self.valid_departments:
                self.valid_departments[semester] = [d['id'] for d in self.departments(semester)]
            departments = self.valid_departments[semester]
            return itertools.chain.from_iterable((self.courses(semester, department) for department in departments))
        department = int(department)
        self.__validate_department(semester, department)
        req = self.request('/%s/departments/%d/courses' % (semester, department), limit=1000)
        if 'courses' not in req:
            return None
        return req['courses']

    def course(self, semester=current_semester(), course_number=None, department=None, course_id=None):
        '''
        Get information about a given course for a given semester
        '''
        def pad_string_with_zeros(s, expected_len):
            if len(s) < expected_len:
                return '0' * (expected_len - len(s)) + s
            return s
        if course_number is not None:
            course_number = pad_string_with_zeros(str(course_number), 5)
            req = self.request('/%s/courses/%s' % (semester, course_number))
            if 'course' not in req:
                return None
            return req['course']
        elif department is not None and course_id is not None:
            self.__validate_department(semester, department)
            department = pad_string_with_zeros(str(department), 2)
            course_id = pad_string_with_zeros(str(course_id), 3)
            req = self.request('/%s/departments/%s/courses/%s' % (semester, department, course_id))
            if 'course' not in req:
                return None
            return req['course']
        else:
            raise ValueError('Must provide either a five-digit course ID or a department number and a course number')