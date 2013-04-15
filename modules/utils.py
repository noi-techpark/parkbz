import xmlrpclib
import httplib

__all__ = ['TimeoutTransport']

class TimeoutTransport(xmlrpclib.Transport):
    timeout = 10.0
    def set_timeout(self, timeout):
        self.timeout = timeout
    def make_connection(self, host):
        return httplib.HTTPConnection(host, timeout=self.timeout)

