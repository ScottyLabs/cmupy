# cmupy
**cmupy** is a Python library for CMU data. Scheudling API data uses the [ScottyLabs CMU APIs](https://apis.scottylabs.org).

## APIs
To use this library, you must be affiliated with CMU. Register your application with [apis@cmu](https://apis.scottylabs.org/apps) to get an app ID and an app secret key. Then, to use the library, you simply need to include `cmu.py` in your app.

### Scheduling

```python
import cmu

schedule = cmu.Scheduling(app_id='YOUR_APP_ID', app_secret_key='YOUR_SECRET_KEY')

departments = schedule.departments(semester='S14')
cs_courses = schedule.courses(semester='S14', department=15)

# the following are equivalent
course_data = schedule.course(semester='S14', course_number=15251)
course_data = schedule.course(semester='S14', department=15, course_id=251)
```

You can omit the semester parameter to use the current semester's data by default. Department IDs, course numbers, and course IDs can be either strings or integers.

More documentation can be found in [docs.html](https://rawgithub.com/tomshen/cmupy/master/cmu.html).

## Printer Status
To use this library, you need to install [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/) (`pip install beautifulsoup4`) as a dependency, and include `printerstatus.py` in your app.

```python
>>> from printerstatus import PrinterStatus
>>> ps = PrinterStatus()
>>> ps.get_status('gates 3')
{'status': 'ready', 'details': 'ready'}
>>> ps.get_all_statuses()
{
  'clusters - cyert b&w': {'status': 'ready', 'details': 'ready'},
  'housing - mudge b&w': {'status': 'caution', 'details': 'tray 3 empty plain letter   ready'},
  .
  .
  .
  'library - hunt 1 ref 1 b&w': {'status': 'not ready', 'details': 'no response'}
}
```

You can look up a printer by calling `get_status` using a string containing any part of a printer's name. For example, `'Mudge'`, `'Mudge B&W'`, and `'housing - mudge b&w'` will all return the status of the printer in Mudge.
