"""Test for subclasses of asyncprawcore.auth.BaseAuthenticator class."""
import pytest

import asyncprawcore

from . import UnitTest


class TestTrustedAuthenticator(UnitTest):
    async def setUp(self):
        await super().setUp()
        self.authenticator = asyncprawcore.TrustedAuthenticator(
            self.requestor,
            pytest.placeholders.client_id,
            pytest.placeholders.client_secret,
            pytest.placeholders.redirect_uri,
        )

    def test_authorize_url(self):
        url = self.authenticator.authorize_url(
            "permanent", ["identity", "read"], "a_state"
        )
        assert f"client_id={pytest.placeholders.client_id}" in url
        assert "duration=permanent" in url
        assert "response_type=code" in url
        assert "scope=identity+read" in url
        assert "state=a_state" in url

    def test_authorize_url__fail_with_implicit(self):
        with pytest.raises(asyncprawcore.InvalidInvocation):
            self.authenticator.authorize_url(
                "temporary", ["identity", "read"], "a_state", implicit=True
            )

    def test_authorize_url__fail_without_redirect_uri(self):
        authenticator = asyncprawcore.TrustedAuthenticator(
            self.requestor,
            pytest.placeholders.client_id,
            pytest.placeholders.client_secret,
        )
        with pytest.raises(asyncprawcore.InvalidInvocation):
            authenticator.authorize_url(
                "permanent",
                ["identity"],
                "...",
            )


class TestUntrustedAuthenticator(UnitTest):
    async def setUp(self):
        await super().setUp()
        self.authenticator = asyncprawcore.UntrustedAuthenticator(
            self.requestor,
            pytest.placeholders.client_id,
            pytest.placeholders.redirect_uri,
        )

    def test_authorize_url__code(self):
        url = self.authenticator.authorize_url(
            "permanent", ["identity", "read"], "a_state"
        )
        assert f"client_id={pytest.placeholders.client_id}" in url
        assert "duration=permanent" in url
        assert "response_type=code" in url
        assert "scope=identity+read" in url
        assert "state=a_state" in url

    def test_authorize_url__token(self):
        url = self.authenticator.authorize_url(
            "temporary", ["identity", "read"], "a_state", implicit=True
        )
        assert f"client_id={pytest.placeholders.client_id}" in url
        assert "duration=temporary" in url
        assert "response_type=token" in url
        assert "scope=identity+read" in url
        assert "state=a_state" in url

    def test_authorize_url__fail_with_token_and_permanent(self):
        with pytest.raises(asyncprawcore.InvalidInvocation):
            self.authenticator.authorize_url(
                "permanent",
                ["identity", "read"],
                "a_state",
                implicit=True,
            )

    def test_authorize_url__fail_without_redirect_uri(self):
        authenticator = asyncprawcore.UntrustedAuthenticator(
            self.requestor, pytest.placeholders.client_id
        )
        with pytest.raises(asyncprawcore.InvalidInvocation):
            authenticator.authorize_url(
                "temporary",
                ["identity"],
                "...",
            )
