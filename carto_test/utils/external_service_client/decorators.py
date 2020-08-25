def add_headers(make_request):
    def wrap(self, *args, **kwargs):
        headers = kwargs.get('headers', {})

        if self.auth_token is not None:
            headers.update({'Authorization': 'Bearer ' + self.auth_token})
        if self.headers is not None:
            headers.update(self.headers)
        kwargs['headers'] = headers
        return make_request(self, *args, **kwargs)

    wrap.__doc__ = make_request.__doc__
    wrap.__name__ = make_request.__name__
    return wrap
