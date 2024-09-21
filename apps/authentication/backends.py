from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .cryptowrapper import CryptoWrapper

SECRET_DIR = str(settings.BASE_DIR) + "/.secrets"


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except user_model.DoesNotExist:
            return None

    def authenticate_without_password(self, request, username=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if self.user_can_authenticate(user):
                return user
        except user_model.DoesNotExist:
            return None

    def get_user(self, user_id):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None


class EmailAndSMSBackend(EmailBackend):
    account_sid = None
    auth_token = None
    messaging_service_id = None
    validation_code = None

    def __init__(self):
        self.account_sid = self.loadAccountSID()
        self.auth_token = self.loadAuthenticationToken()
        self.messaging_service_id = self.loadMessagingServiceID()
        self.validation_code = self.generateValidationCode()

    def loadAccountSID(self):
        decryptor = CryptoWrapper()

        decrypted = str(
            decryptor.decrypt(
                SECRET_DIR + "/account_sid.encrypted", CryptoWrapper.default_key
            )
        ).rstrip()

        return decrypted

    def loadAuthenticationToken(self):
        decryptor = CryptoWrapper()

        decrypted = str(
            decryptor.decrypt(
                SECRET_DIR + "/authentication_token.encrypted",
                CryptoWrapper.default_key,
            )
        ).rstrip()

        return decrypted

    def loadMessagingServiceID(self):
        decryptor = CryptoWrapper()

        decrypted = str(
            decryptor.decrypt(
                SECRET_DIR + "/messaging_service_sid.encrypted",
                CryptoWrapper.default_key,
            )
        ).rstrip()

        return decrypted

    def generateValidationCode(self):
        # import the Pyotp 2FA validation library
        import pyotp

        pyotp.random_base32()
        totp = pyotp.TOTP("base32secret3232")

        return totp.now()

    def verifyValidationCode(self, code):
        return self.validation_code == code

    def sendVerificationSMS(self, target_number, sms_msg=None):
        # import the Twilio interface for SMS
        from twilio.rest import Client

        self.generateValidationCode()

        if not sms_msg:
            sms_msg = "Welcome to Besity!"
        sms_msg += "\n\nYour activation code is " + self.validation_code

        client = Client(self.account_sid, self.auth_token)

        _ = client.messages.create(
            body=sms_msg,
            messaging_service_sid=self.messaging_service_id,
            to=target_number,
        )
        return self.validation_code

        # try:

        # except:
        #     return None
