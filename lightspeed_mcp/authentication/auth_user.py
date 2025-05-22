from starlette.authentication import SimpleUser


class AuthenticationInfo:
    def __init__(
        self,
        header_name: str,
        header_value: str,
        server_url: str,
        verify_cert: bool = True,
    ) -> None:
        self.header_name = header_name
        self.header_value = header_value
        self.server_url = server_url
        self.verify_cert = verify_cert

    def get_headers(self) -> dict:
        return {self.header_name: self.header_value}


class AuthenticationUser(SimpleUser):
    def __init__(self, username: str, authentication_info: AuthenticationInfo) -> None:
        self.authentication_info = authentication_info
        super().__init__(username)
