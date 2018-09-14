import logging
import time
from collections import defaultdict
from threading import RLock

from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_EXCEPTION

from .async_utils import AsyncRequestType, AsyncRequest
from arctic.exceptions import AsyncArcticException

ARCTIC_ASYNC_NTHREADS = 4
BATCH_SIZE = 10


def _task_exec(request):
    request.start_time = time.time()
    logging.info("Executing asynchronous request for library: {}".format(request.library, request.symbol))
    result = request.fun(*request.args, **request.kwargs)
    request.data = result
    request.end_time = time.time()
    return result


class AsyncArctic(object):
    _instance = None
    _SINGLETON_LOCK = RLock()
    _POOL_INIT_LOCK = RLock()
    _TASK_SUBMIT_LOCK = RLock()

    @staticmethod
    def get_instance():
        # Lazy init
        with AsyncArctic._SINGLETON_LOCK:
            if AsyncArctic._instance is None:
                AsyncArctic._instance = AsyncArctic()
        return AsyncArctic._instance

    @property
    def _workers_pool(self):
        # lazy init the workers pool
        with AsyncArctic._POOL_INIT_LOCK:
            if self._pool is None:
                self._pool = ThreadPoolExecutor(max_workers=self._pool_size,
                                                thread_name_prefix='AsyncArcticWorker')
        return self._pool

    def __init__(self):
        # Only allow creation via get_instance
        if not AsyncArctic._SINGLETON_LOCK._is_owned():
            raise AsyncArcticException("AsyncArctic is a singleton, can't create a new instance")

        # Enforce the singleton pattern
        with AsyncArctic._SINGLETON_LOCK:
            if AsyncArctic._instance is not None:
                raise AsyncArcticException("AsyncArctic is a singleton, can't create a new instance")
            self._lock = RLock()
            self._pool = None
            self._pool_size = ARCTIC_ASYNC_NTHREADS
            self.requests_per_library = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    def __reduce__(self):
        return "ASYNC_ARCTIC"

    def reset(self, wait=True, pool_size=ARCTIC_ASYNC_NTHREADS):
        with AsyncArctic._POOL_INIT_LOCK:
            self._workers_pool.shutdown(wait=wait)
            pool_size = max(pool_size, 1)
            self._pool = None
            self._pool_size = pool_size
            # pool will be lazily initialized with pool_size on next request submission

    def _get_modifiers(self, library_name, symbol=None):
        return self.requests_per_library[library_name][symbol][AsyncRequestType.MODIFIER]

    def _get_accessors(self, library_name, symbol=None):
        return self.requests_per_library[library_name][symbol][AsyncRequestType.ACCESSOR]

    @staticmethod
    def _verify_request(store, is_modifier, **kwargs):
        if store is None:
            raise AsyncArcticException("Can't submit async arctic task passing an empty store")

        library_name = store._arctic_lib.get_name()
        symbol = kwargs.get('symbol')
        kind = AsyncRequestType.MODIFIER if is_modifier else AsyncRequestType.ACCESSOR

        callback = kwargs.get('async_callback')
        if 'async_callback' in kwargs:
            kwargs.pop('async_callback')

        block = bool(kwargs.get('async_block'))
        if 'async_block' in kwargs:
            kwargs.pop('async_block')

        if block and callback:
            raise AsyncArcticException("Can't use both async_callback and async_block")

        return library_name, symbol, kind, callback, block
    
    def submit_request(self, store, fun, is_modifier, *args, **kwargs):
        library_name, symbol, kind, callback, block = AsyncArctic._verify_request(store, is_modifier, **kwargs)

        with AsyncArctic._TASK_SUBMIT_LOCK:
            if self._get_modifiers(library_name, symbol):
                raise AsyncArcticException("Can't submit async task as there are "
                                           "being processed one or more {} tasks".format(AsyncRequestType.MODIFIER))

            if is_modifier and self._get_accessors(library_name, symbol):
                raise AsyncArcticException("Can't submit async {} task as there are being processed one or "
                                           "more {} tasks".format(AsyncRequestType.ACCESSOR, AsyncRequestType.MODIFIER))

            # Create the request object
            request = AsyncRequest(kind, library_name, symbol, fun, *args, **kwargs)

            # Update the state of tracked tasks
            self.requests_per_library[library_name][symbol][kind].append(request)

            # Submit the task
            try:
                request.future = self._workers_pool.submit(_task_exec, request)
                if block:
                    AsyncArctic._wait_request(request)
                elif callback:
                    request.future.add_done_callback(lambda the_future: self._request_finished(request, callback))
            except:
                # clean up the state
                self.requests_per_library[request.library][request.symbol][request.kind].remove(request)
                raise

            return request

    def _request_finished(self, request, callback):
        request.future = None
        with AsyncArctic._TASK_SUBMIT_LOCK:
            self.requests_per_library[request.library][request.symbol][request.kind].remove(request)
        if callback:
            callback(request)

    @staticmethod
    def _wait_request(request):
        if request is not None and request.future is not None:
            wait((request.future,), return_when=FIRST_EXCEPTION)
            # Force-raise any exceptions
            request.future.result()
            request.future = None


ASYNC_ARCTIC = AsyncArctic.get_instance()
async_arctic_submit = ASYNC_ARCTIC.submit_request