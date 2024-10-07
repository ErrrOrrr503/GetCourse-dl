"""
Cookies
Limit ops/s not to get banned.
Follow requests api.
"""
from typing import Any
import requests
from requests.api import request
import browser_cookie3
from getcourse_dl.logger.logger import logger, Verbosity
import time


class NWrapException(Exception):
    ...


class NWrap:
    _browser: str | None = None
    _cookies: requests.cookies.RequestsCookieJar
    _session: requests.Session
    retries: int = 3

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0'
        })

    def _reset_session(self) -> None:
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0'
        })
        self._session.cookies.update(self._cookies)

    def load_cookies(self, browser: str | None = None) -> None:
        self._browser = browser
        load_method = browser_cookie3.load
        if browser:
            try:
                logger.print(Verbosity.INFO,
                             'Loading cookies from "{}"'.format(browser))
                load_method = getattr(browser_cookie3, browser)
            except Exception:
                logger.print(
                    Verbosity.ERROR, 'browser "{}" is invalid or not supported. Falling back to all browsers'.format(browser))
        self._cookies = load_method(domain_name='getcourse.ru')
        self._session.cookies.update(self._cookies)
        logger.print(Verbosity.INFO,
                     'loaded cookies: {}'.format(self._cookies))

    def get(self, *args: Any, **kwargs: Any) -> requests.Response:
        # by far dummy
        resp = self._get_retry(*args, **kwargs)
        if not resp:
            logger.print(Verbosity.INFO, 'Resetting session...')
            self._reset_session()
            resp = self._get_retry()
        if not resp:
            raise NWrapException('Even session reset would not work...')
        time.sleep(0.5)  # no more than 1 request per second
        return resp

    def _get_retry(self, *args: Any, **kwargs: Any) -> requests.Response | None:
        resp = None
        for _ in range(self.retries):
            try:
                resp = self._session.get(*args, **kwargs, timeout=5)
                break
            except requests.exceptions.Timeout:
                logger.print(Verbosity.WARNING,
                             'Geting {} timed out'.format(args[0]))
        return resp


nwrap = NWrap()
