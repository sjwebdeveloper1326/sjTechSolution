import time
import traceback
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from .logger import log_exception, log_error, _write_latest_error


class ErrorLoggingMiddleware:
    """Middleware that logs unhandled exceptions with request info and redirects safely.

    It records traceback to logs/errors/system.log and writes a latest_error.log
    as a quick shortcut for operators.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        try:
            response = self.get_response(request)
        except Exception as exc:
            # log exception with request context
            try:
                log_exception(exc, request=request, module=__name__)
            except Exception:
                # ensure middleware never raises
                pass
            # also write a brief latest error file
            try:
                text = f"Unhandled exception on {request.path}\n{traceback.format_exc()}"
                _write_latest_error(text)
            except Exception:
                pass

            # Add a friendly message and redirect to a safe page
            try:
                messages.error(request, "An unexpected error occurred. The team has been notified.")
            except Exception:
                pass

            safe = getattr(settings, "ERROR_REDIRECT_URL", "/")
            return redirect(safe)

        # slow request logging
        try:
            duration = time.time() - start
            slow_threshold = getattr(settings, "SLOW_REQUEST_THRESHOLD", 1.0)
            if duration > slow_threshold:
                log_error(f"Slow request: {duration:.3f}s for {request.path}", request=request, module=__name__)
        except Exception:
            pass

        return response
