# cmupy

**cmupy** is a Python library for [ScottyLabs CMU APIs](https://apis.scottylabs.org).

## Usage
To use the library, you must be affiliated with CMU. Register your application with [apis@cmu](https://apis.scottylabs.org/apps) to get an app ID and an app secret key. Then, to use the library, you simply need to include `cmu.py` in your app.
```python
import cmu

scheduling_api = cmu.Scheduling(app_id='YOUR_APP_ID', app_secret_key='YOUR_SECRET_KEY')

departments = scheduling_api.departments(semester='S14')
cs_courses = scheduling_api.courses(semester='S14', department=15)

# the following are equivalent
course_info = scheduling_api.course(semester='S14', course_number=15251)
course_info = scheduling_api.course(semester='S14', department=15,
                                    course_id=251)
```

You can omit the semester parameter to use the current semester's info by default. Department IDs, course numbers, and course IDs can be either strings or integers.

More documentation can be found in [docs.html](https://rawgithub.com/tomshen/cmupy/master/cmu.html).