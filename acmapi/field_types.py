import flask

from flask.ext.restful.fields import Url
from flask.ext.restful.fields import Raw
from flask.ext.restful.fields import MarshallingException

try:
    from urlparse import urlparse
    from urlparse import urlunparse
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlparse
    from urllib.parse import urlunparse
    from urllib.parse import urlencode

class Date(Raw):
    """ Renders a Date obj as a string """

    def __init__(self, date_format, default=None, attribute=None):
        super(Date, self).__init__(default, attribute)
        self.date_format = date_format            

    def format(self, x):
        try:
            return x.strftime(self.date_format)
        except AttributeError:
            raise MarshallingException("Must be a valid date")

class DateTime(Raw):
    """ Renders a DateTime obj as a string """

    def __init__(self, datetime_format, default=None, attribute=None):
        super(DateTime, self).__init__(default, attribute)
        self.datetime_format = datetime_format            

    def format(self, x):
        try:
            return x.strftime(self.datetime_format)
        except AttributeError:
            raise MarshallingException("Must be a valid date and time")

class UrlUsage(Raw):
    """ Renders all the usages for a endpoint """
    
    def __init__(self, endpoint, absolute=False, scheme=None):
        self.endpoint = endpoint
        self.absolute = absolute
        self.scheme = scheme

    def output(self, obj, key):
        urls = []
        for rule in flask.current_app.url_map.iter_rules():
            if rule.endpoint == self.endpoint:
                o = urlparse(flask.url_for(self.endpoint, _external = self.absolute))
                scheme = self.scheme if self.scheme is not None else o.scheme
                urls.append(urlunparse((scheme, o.netloc, rule.rule, "", "", "")))
        return urls

class UrlWithParams(Url):
    """ Will render the a url with specified params
    
    params can be either a list or a dict. If params is a list then 
    the url will contain a param key contained in the list
    and the value will be looked up in the obj by the same name. Using
    a dict allow you to specify a different key to look up in the obj.

    ## Example using a list
    
    ```python
    fields = {
        foo: Integer,
        url: UrlWithParams('root', params=['foo'])
    }

    marshal({foo: 1}, fields)
    ```

    Will produce:

    http://example.com/?foo=1

    ## Example using a dict

     
    ```python
    fields = {
        bar: Integer,
        url: UrlWithParams('root', params={'foo': 'bar'})
    }

    marshal({foo: 1}, fields)
    ```

    Will produce:

    http://example.com/?foo=1
    """
    def __init__(self, endpoint, params=None, absolute=False, scheme=None):
        assert(isinstance(params, (type(None), list, dict)))
        super(UrlWithParams, self).__init__(
                endpoint, absolute, scheme)
        self.params = params

    def output(self, key, obj):
        url = super(UrlWithParams, self).output(key,obj)
        o = urlparse(url)
        if self.params is None:
            return url
        elif isinstance(self.params, list):
            return urlunparse((o.scheme, o.netloc, o.path, "", 
                urlencode({ k:obj[k] for k in self.params}), ""))
        elif isinstance(self.params, dict):
            return urlunparse((o.scheme, o.netloc, o.path, "", 
                urlencode({ k:obj[v] for k,v in self.params.items()}), ""))
        else:
            raise TypeError("params must be of type None, list, or dict")

class UrlBuilder(Raw):
    """ Will render a url from value marshaled with """
    
    def __init__(self):
        super(UrlBuilder, self).__init__(None, None)

    def format(self, o):
        url = None
        params = None

        if 'endpoint' in o and o['endpoint']:
            url = urlparse(flask.url_for(o['endpoint'], _external = True))
            if 'params' in o and o['params']:
                params = urlencode(o['params'])
            url = urlunparse(
                (url.scheme, url.netloc, url.path, url.params, 
                    params, url.fragment)) 

        return url
