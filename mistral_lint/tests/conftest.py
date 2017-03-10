import pytest

from mistral_lint import suite as _suite


@pytest.fixture
def suite():
    return _suite.LintSuite()
