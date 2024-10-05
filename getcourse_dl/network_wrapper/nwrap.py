"""
Cookies
Limit ops/s not to get banned.
Follow requests api.
"""
from typing import Any
import requests
import browser_cookie3
from getcourse_dl.logger.logger import logger, Verbosity


class NWrap:
    _browser: str | None = None
    _cookies: requests.cookies.RequestsCookieJar

    def load_cookies(self, browser: str | None = None) -> None:
        self._browser = browser
        load_method = browser_cookie3.load
        if browser:
            try:
                logger.print(Verbosity.INFO, 'Loading cookies from "{}"'.format(browser))
                load_method = getattr(browser_cookie3, browser)
            except Exception as e:
                logger.print(Verbosity.ERROR, 'browser "{}" is invalid or not supported. Falling back to all browsers'.format(browser))
        self._cookies = load_method(domain_name='getcourse.ru')
        logger.print(Verbosity.INFO, 'loaded cookies: {}'.format(self._cookies))

    def get(self, *args: Any, **kwargs: Any) -> requests.Response:
        return requests.get(*args, **kwargs, cookies=self._cookies)  # by far dummy


nwrap = NWrap()
