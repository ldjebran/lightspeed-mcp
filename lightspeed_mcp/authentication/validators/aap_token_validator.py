from .aap_base_validator import AAPBaseValidator


class AAPTokenValidator(AAPBaseValidator):
    AUTHENTICATION_HEADER_NAME = "Authorization"
