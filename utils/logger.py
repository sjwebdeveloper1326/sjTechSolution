import logging
import logging.handlers
import os
import traceback
from datetime import datetime
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_ROOT = os.path.join(BASE_DIR, "logs")
ERRORS_DIR = os.path.join(LOG_ROOT, "errors")
PAGES_DIR = os.path.join(LOG_ROOT, "pages")


def _ensure_dirs():
    os.makedirs(ERRORS_DIR, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)


def _sanitize(msg: str) -> str:
    if not isinstance(msg, str):
        try:
            msg = str(msg)
        except Exception:
            msg = "<unrepresentable>"
    # remove non-ascii characters to keep logs ASCII-safe
    return msg.encode("ascii", errors="ignore").decode("ascii")


def _get_rotating_handler(path: str, level=logging.INFO, max_bytes=5 * 1024 * 1024, backup=5):
    handler = logging.handlers.RotatingFileHandler(
        path, maxBytes=max_bytes, backupCount=backup, encoding="utf-8"
    )
    handler.setLevel(level)
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(module)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(fmt)
    return handler


def get_page_logger(page_name: str):
    """Return a page-scoped logger that writes to logs/pages/<page_name>.log"""
    _ensure_dirs()
    name = f"page.{page_name}"
    logger = logging.getLogger(name)
    if not logger.handlers:
        log_path = os.path.join(PAGES_DIR, f"{page_name}.log")
        handler = _get_rotating_handler(log_path)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False
    return logger


def _get_system_logger():
    _ensure_dirs()
    logger = logging.getLogger("system.errors")
    if not logger.handlers:
        sys_path = os.path.join(ERRORS_DIR, "system.log")
        handler = _get_rotating_handler(sys_path, level=logging.ERROR)
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)
        logger.propagate = False
    return logger


def _write_latest_error(text: str):
    _ensure_dirs()
    path = os.path.join(ERRORS_DIR, "latest_error.log")
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    except Exception:
        pass


def log_info(message: str, *, request=None, module: Optional[str] = None, logger_name: Optional[str] = None):
    msg = _sanitize(message)
    name = logger_name or (f"page.{module}" if module else "application")
    log = logging.getLogger(name)
    if not log.handlers:
        # default to a page logger if module provided
        if module:
            log = get_page_logger(module)
        else:
            # fallback to root basic config
            logging.basicConfig(level=logging.INFO)
            log = logging.getLogger(name)
    extra = _build_request_extra(request)
    log.info(f"{msg} {extra}")


def log_warning(message: str, *, request=None, module: Optional[str] = None):
    msg = _sanitize(message)
    name = f"page.{module}" if module else "application"
    log = logging.getLogger(name)
    if not log.handlers and module:
        log = get_page_logger(module)
    log.warning(f"{msg} {_build_request_extra(request)}")


def log_error(message: str, *, request=None, module: Optional[str] = None):
    msg = _sanitize(message)
    name = "system.errors"
    sys_logger = _get_system_logger()
    sys_logger.error(f"{msg} {_build_request_extra(request)}")


def log_exception(exc: Exception, *, request=None, module: Optional[str] = None):
    tb = traceback.format_exc()
    text = f"Exception: {repr(exc)}\nTraceback:\n{tb}\nRequest: {_build_request_extra(request)}"
    _get_system_logger().error(_sanitize(text))
    # also write a latest error shortcut
    _write_latest_error(text)


def _build_request_extra(request):
    if not request:
        return ""
    try:
        user = getattr(request, "user", None)
        username = getattr(user, "username", "anonymous") if user else "anonymous"
        ip = request.META.get("REMOTE_ADDR", "-")
        path = request.path
        method = request.method
        ua = request.META.get("HTTP_USER_AGENT", "-")
        return f"[user={username} ip={ip} path={path} method={method} ua={_sanitize(ua)}]"
    except Exception:
        return ""
