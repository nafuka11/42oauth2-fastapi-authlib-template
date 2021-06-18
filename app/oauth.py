from authlib.integrations.starlette_client import OAuth, StarletteRemoteApp
from httpx import Timeout

from app import config

settings = config.get_settings()
oauth = OAuth()
oauth.register(
    name="ft",
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    access_token_url=settings.access_token_url,
    access_token_params=None,
    authorize_url=settings.authorize_url,
    authorize_params=None,
    api_base_url=settings.api_base_url,
    client_kwargs={"timeout": Timeout(10.0)},
)

ft_oauth: StarletteRemoteApp = oauth.create_client("ft")
