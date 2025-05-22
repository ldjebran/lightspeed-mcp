from .aap_base_validator import AAPBaseValidator


class AAPJWTValidator(AAPBaseValidator):
    AUTHENTICATION_HEADER_NAME = "X-DAB-JW-TOKEN"
