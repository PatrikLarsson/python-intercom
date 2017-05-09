# -*- coding: utf-8 -*-

import os
import unittest
from intercom import Intercom
from intercom import Admin

Intercom.access_token= os.environ.get('INTERCOM_ACCESS_TOKEN')


class AdminTest(unittest.TestCase):

    def test(self):
        # Iterate over all admins
        for admin in Admin.all():
            self.assertIsNotNone(admin.id)
            self.assertIsNotNone(admin.email)
