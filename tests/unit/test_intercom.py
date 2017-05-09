# -*- coding: utf-8 -*-

import intercom
import mock
import time
import unittest

from datetime import datetime
from nose.tools import assert_raises
from nose.tools import eq_
from nose.tools import istest


class ExpectingArgumentsTest(unittest.TestCase):

    def setUp(self):  # noqa
        self.intercom = intercom.Intercom
        self.intercom.access_token = 'my_personal_access_token'

    @istest
    def it_raises_argumenterror_if_no_access_token_specified(self):  # noqa
        self.intercom.access_token = None
        with assert_raises(intercom.ArgumentError):
            self.intercom.target_base_url

    @istest
    def it_returns_the_access_token_previously_set(self):
        eq_(self.intercom.access_token, 'my_personal_access_token')

    @istest
    def it_defaults_to_https_to_api_intercom_io(self):
        eq_(self.intercom.target_base_url,
            'https://my_personal_access_token@api.intercom.io')


class OverridingProtocolHostnameTest(unittest.TestCase):
    def setUp(self):  # noqa
        self.intercom = intercom.Intercom
        self.protocol = self.intercom.protocol
        self.hostname = self.intercom.hostname
        self.intercom.endpoints = None

    def tearDown(self):  # noqa
        self.intercom.protocol = self.protocol
        self.intercom.hostname = self.hostname
        self.intercom.endpoints = ["https://api.intercom.io"]

    @istest
    def it_allows_overriding_of_the_endpoint_and_protocol(self):
        self.intercom.protocol = "http"
        self.intercom.hostname = "localhost:3000"
        eq_(
            self.intercom.target_base_url,
            "http://my_personal_access_token@localhost:3000")

    @istest
    def it_prefers_endpoints(self):
        self.intercom.endpoint = "https://localhost:7654"
        eq_(self.intercom.target_base_url,
            "https://my_personal_access_token@localhost:7654")

        # turn off the shuffle
        with mock.patch("random.shuffle") as mock_shuffle:
            mock_shuffle.return_value = ["http://example.com", "https://localhost:7654"]  # noqa
            self.intercom.endpoints = ["http://example.com", "https://localhost:7654"]  # noqa
            eq_(self.intercom.target_base_url,
                'http://my_personal_access_token@example.com')

    @istest
    def it_has_endpoints(self):
        eq_(self.intercom.endpoints, ["https://api.intercom.io"])
        self.intercom.endpoints = ["http://example.com", "https://localhost:7654"]  # noqa
        eq_(self.intercom.endpoints, ["http://example.com", "https://localhost:7654"])  # noqa

    @istest
    def it_should_randomize_endpoints_if_last_checked_endpoint_is_gt_5_minutes_ago(self):  # noqa
        now = time.mktime(datetime.utcnow().timetuple())
        self.intercom._endpoint_randomized_at = now
        self.intercom.endpoints = ["http://alternative"]
        self.intercom.current_endpoint = "http://start"

        self.intercom._endpoint_randomized_at = now - 120
        eq_(self.intercom.current_endpoint, "http://start")
        self.intercom._endpoint_randomized_at = now - 360
        eq_(self.intercom.current_endpoint, "http://alternative")
