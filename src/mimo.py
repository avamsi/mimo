from base64 import b64encode
from os import environ

from marimo._server import file_router, registry, start, tokens
from marimo._session import model
from starlette import middleware, responses, types


class MimoMiddleware:
    def __init__(self, app: types.ASGIApp, username: str, password: str):
        self._app = app
        self._credentials = b"Basic " + b64encode(f"{username}:{password}".encode())

    async def __call__(
        self, scope: types.Scope, receive: types.Receive, send: types.Send
    ):
        if (
            scope["type"] in ("http", "websocket")
            and dict(scope["headers"]).get(b"authorization") != self._credentials
        ):
            return await responses.Response(
                None, status_code=401, headers={"WWW-Authenticate": "Basic"}
            )(scope, receive, send)
        return await self._app(scope, receive, send)


def main():
    registry.MIDDLEWARE_REGISTRY.register(
        "mimo",
        middleware.Middleware(
            MimoMiddleware, environ["MIMO_USERNAME"], environ["MIMO_PASSWORD"]
        ),
    )
    start.start(
        file_router=file_router.AppFileRouter.from_directory("."),
        mode=model.SessionMode.EDIT,
        development_mode=False,
        quiet=False,
        include_code=True,
        ttl_seconds=None,
        headless=True,
        port=6573,
        host="localhost",
        proxy=None,
        watch=True,
        cli_args={},
        argv=[],
        auth_token=tokens.AuthToken(""),
        redirect_console_to_browser=True,
        skew_protection=False,
        mcp=True,
    )


if __name__ == "__main__":
    main()
