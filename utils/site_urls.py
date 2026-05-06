from urllib.parse import urljoin

from django.conf import settings


LOCAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "testserver"}


def production_base_url():
    return getattr(settings, "SITE_BASE_URL", "https://sgautomixtech.info/").rstrip("/")


def request_base_url(request=None):
    if request is None:
        return production_base_url()

    host = request.get_host()
    hostname = host.split(":")[0].lower()

    if hostname in LOCAL_HOSTS or hostname.endswith(".local"):
        return request.build_absolute_uri("/").rstrip("/")

    return production_base_url()


def absolute_url(path="", request=None):
    base_url = request_base_url(request)
    return urljoin(f"{base_url}/", str(path).lstrip("/"))
