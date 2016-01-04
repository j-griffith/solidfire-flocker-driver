import json
import logging
import time

import warnings
import requests
import six
from requests.packages.urllib3 import exceptions

LOG = logging.getLogger(__name__)


def retry(exc_tuple, tries=5, delay=1, backoff=2):
    def retry_dec(f):
        @six.wraps(f)
        def func_retry(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return f(*args, **kwargs)
                except exc_tuple:
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
                    LOG.debug('Retrying %(args)s, %(tries)s attempts '
                              'remaining...',
                              {'args': args, 'tries': _tries})
            # NOTE(jdg): Don't log the params passed here
            # some cmds like createAccount will have sensitive
            # info in the params, grab only the second tuple
            # which should be the Method
            msg = ('Retry count exceeded for command: %s' %
                   args[1],)
            LOG.error(msg)
            raise SolidFireRequestException(message=msg)
        return func_retry
    return retry_dec


class SolidFireRequestException(Exception):
    message = "An unknown exception occurred."

    def __init__(self, arg):
        self.msg = arg


class SolidFireRetryableException(SolidFireRequestException):
    message = "Retryable SolidFire Exception encountered"


class SolidFireClient(object):
    """The API for controlling a SolidFire cluster."""

    retry_exc_tuple = (SolidFireRetryableException,
                       requests.exceptions.ConnectionError)
    retryable_errors = ['xDBVersionMismatch',
                        'xMaxSnapshotsPerVolumeExceeded',
                        'xMaxClonesPerVolumeExceeded',
                        'xMaxSnapshotsPerNodeExceeded',
                        'xMaxClonesPerNodeExceeded',
                        'xNotReadyForIO']

    def __init__(self, *args, **kwargs):
        self.endpoint_dict = kwargs.get('endpoint_dict')
        self.endpoint_version = kwargs.get('endpoint_version', '7.0')
        self.raw = True
        self.request_history = []

    def issue_request(self, method, params, endpoint=None):
        if params is None:
            params = {}

        # NOTE(jdg): We allow passing in a new endpoint to issue_api_req
        # to enable some of the multi-cluster features like replication etc
        if endpoint is None:
            endpoint_dict = self.endpoint_dict
        payload = {'method': method, 'params': params}
        url = '%s/json-rpc/%s/' % (endpoint_dict['url'], self.endpoint_version)
        LOG.debug('Issue SolidFire API call: %s' % json.dumps(payload))

        start_time = time.time()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", exceptions.InsecureRequestWarning)
            req = requests.post(url,
                                data=json.dumps(payload),
                                auth=(endpoint_dict['login'],
                                      endpoint_dict['password']),
                                verify=False,
                                timeout=30)

        # FIXME(jdg): Failure cases like wrong password
        # missing something that cause req.json to puke
        response = req.json()
        req.close()
        end_time = time.time()
        duration = end_time - start_time

        LOG.debug('Raw response data from SolidFire API: %s' % response)
        # TODO(jdg): Add check/retry catch for things where it's appropriate
        if 'error' in response:
            if response['error']['name'] in self.retryable_errors:
                msg = ('Retryable error (%s) encountered during '
                       'SolidFire API call.' % response['error']['name'])
                LOG.debug(msg)
                raise SolidFireRetryableException(message=msg)
            else:
                msg = ('API response: %s'), response
                self.request_history.append(
                    (method, start_time, duration, 'failed'))
                LOG.error('Error in API request: %s' % response['error'])
                raise SolidFireRequestException(msg)

        self.request_history.append(
            (method, start_time, duration, 'ok'))
        return response['result']
