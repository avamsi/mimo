from marimo._server import file_router, start, tokens
from marimo._session import model


def main():
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
