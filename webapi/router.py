import re

ROUTE_KEY_NOT_MACHED = ('', '')
def method_not_matched(**key_args):
    return 'no route matched your request'

class Routes(object):

    def __init__(self):
        self.__routes = {}

    def add(self, http_method, route_regex, controller_method):
        self.__routes[(http_method, route_regex)] = controller_method

    def matches(self, http_method, url, **params):
        iter_matched_routes = iter(
            filter(lambda route_keys: 
                route_keys[0] == http_method and re.match(route_keys[1], url), self.__routes
            )
        )
        first_matched_keys = next(iter_matched_routes, ROUTE_KEY_NOT_MACHED)
        controller_method = self.__routes.get(first_matched_keys, method_not_matched)
        url_params = re.match(first_matched_keys[1], url).groupdict()
        return controller_method(**url_params, **params)

class Router(object):
    def __init__(self, routes = Routes()):
        self.__routes = routes

    def route(self, http_method, url_regex):
        def decorated_func(func):
            self.__routes.add(http_method, url_regex, func)
            return func
        return decorated_func

    def handle(self, http_method, url, **params):
        return self.__routes.matches(http_method, url, **params)