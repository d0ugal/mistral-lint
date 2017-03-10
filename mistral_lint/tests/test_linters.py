import pytest

from mistral_lint import linters


@pytest.fixture
def expressions(suite):
    def lint(yaml):
        return suite.lint_string("path", yaml, {
            "expressions": linters.expressions
        })
    return lint


class TestExpressionLinters(object):

    def test_non_matching_brackets_jinja2(self, expressions):
        YAML = """---
        obj: "{{ test }} }}"
        """
        result = expressions(YAML)
        assert result == [
            ("W105: Expression brackets don't match '{{ test }} }}' on line 2 "
             "in path")
        ]

    def test_matching_brackets_jinja2(self, expressions):
        YAML = """---
        obj: "{{ test }}"
        """
        result = expressions(YAML)
        assert result == []

    def test_non_matching_brackets_yaql(self, expressions):
        YAML = """---

        obj: "<% test %> %>"
        """
        result = expressions(YAML)
        assert result == [
            ("W105: Expression brackets don't match '<% test %> %>' on line 3 "
             "in path")
        ]

    def test_matching_brackets_yaql(self, expressions):
        YAML = """---
        obj: <% test %>
        """
        assert not expressions(YAML)

    def test_invalid_jinja_expression(self, expressions):
        YAML = """---
        obj: "{{ test test }}"
        """
        result = expressions(YAML)
        assert result == [
            ("W106: Failed to parse jinja2 expression '{{ test test }}' on "
             "line 2 in path")
        ]

    def test_valid_jinja_expression(self, expressions):
        YAML = """---
        obj: "{{ one }}{{ two }}"
        """
        assert not expressions(YAML)

    def test_invalid_yaql_expression(self, expressions):
        YAML = """---
        obj: "stuff <% test test %> after"
        """
        result = expressions(YAML)
        assert result == [
            ("W106: Failed to parse yaql expression 'stuff <% test test %> "
             "after' on line 2 in path")
        ]

    def test_valid_yaql_expression(self, expressions):
        YAML = """---
        obj: "stuff before <% $.test %> and after"
        """
        assert not expressions(YAML)
