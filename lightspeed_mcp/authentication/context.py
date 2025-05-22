import contextvars

from .auth_user import AuthenticationUser

auth_context_var = contextvars.ContextVar[AuthenticationUser | None](
    "auth_context", default=None
)


def get_authentication_headers() -> dict | None:
    auth_user = auth_context_var.get()
    return auth_user.authentication_info.get_headers() if auth_user else None
