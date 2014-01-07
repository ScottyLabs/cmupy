#!/usr/bin/env python
import unittest

import cmu
import secrets

schedule_api = cmu.Scheduling(app_id=secrets.APP_ID,
    app_secret_key=secrets.APP_SECRET_KEY)