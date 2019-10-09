from django.conf import settings
from django.core.exceptions import (
    ImproperlyConfigured,
    ValidationError,
)
from django.core.validators import URLValidator


class SecurityHeaderMiddleware:
    VALID_REFERRER_POLICIES = [
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        if (
            not hasattr(settings, "REFERRER_POLICY")
            or settings.REFERRER_POLICY not in self.VALID_REFERRER_POLICIES
        ):
            raise ImproperlyConfigured(
                "settings.REFERRER_POLICY is not set or has an illegal value."
            )
        if not hasattr(settings, "EXPECT_CT_MAX_AGE") or not isinstance(
            settings.EXPECT_CT_MAX_AGE, int
        ):
            raise ImproperlyConfigured(
                "settings.EXPECT_CT_MAX_AGE is not set or is not an integer."
            )
        if hasattr(settings, "EXPECT_CT_REPORT_URI"):
            try:
                URLValidator()(settings.EXPECT_CT_REPORT_URI)
            except ValidationError:
                raise ImproperlyConfigured(
                    "settings.EXPECT_CT_REPORT_URI is not a valid URL."
                )
        if hasattr(settings, "EXPECT_CT_ENFORCE"):
            if not isinstance(settings.EXPECT_CT_ENFORCE, bool):
                raise ImproperlyConfigured(
                    "settings.EXPECT_CT_ENFORCE must be a boolean."
                )

    def __call__(self, request):
        response = self.get_response(request)
        response["Referrer-Policy"] = settings.REFERRER_POLICY
        response["Expect-CT"] = self.build_expect_ct_header()
        return response

    @staticmethod
    def build_expect_ct_header() -> str:
        expect_ct_enforce = getattr(settings, "EXPECT_CT_ENFORCE", False)
        expect_ct_report_uri = getattr(settings, "EXPECT_CT_REPORT_URI", None)
        expect_ct_header = f"max-age={settings.EXPECT_CT_MAX_AGE}"
        if expect_ct_enforce is True:
            expect_ct_header += ", enforce"
        if expect_ct_report_uri is not None:
            expect_ct_header += f', report-uri="{settings.EXPECT_CT_REPORT_URI}"'
        return expect_ct_header
