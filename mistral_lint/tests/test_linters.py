import pytest

from mistral_lint import linters


@pytest.fixture
def expressions(suite):
    def lint(yaml):
        return suite.lint_string("path", yaml, {
            "expressions": linters.expressions,
        }, validate_file=False)
    return lint


@pytest.fixture
def task_names(suite):
    def lint(yaml):
        return suite.lint_string("path", yaml, {
            "task_names": linters.task_names,
        }, validate_file=False)
    return lint


class TestExpressionLinters(object):

    def test_non_matching_brackets_jinja2(self, expressions):
        YAML = """---
        obj: "{{ test }} }}"
        """
        result = expressions(YAML)
        assert result == [
            ("E103: Expression brackets don't match '{{ test }} }}' on line 2 "
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
            ("E103: Expression brackets don't match '<% test %> %>' on line 3 "
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
            ("E104: Failed to parse jinja2 expression '{{ test test }}' on "
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
            ("E105: Failed to parse yaql expression 'stuff <% test test %> "
             "after' on line 2 in path")
        ]

    def test_valid_yaql_expression(self, expressions):
        YAML = """---
        obj: "stuff before <% $.test %> and after"
        """
        assert not expressions(YAML)


class TestTaskNameCheck(object):

    def test_task_name_only_used_when_needed(self, task_names):

        YAML = """---
        version: '2.0'
        name: wb

        workflows:
          wf:
            tasks:
              t1:
                action: std.echo output="output"
                publish:
                  out: "<% task(t1).result %>"
              t2:
                action: std.echo output="output"
                publish:
                  out: "<% task(t1).result %>"
              t3:
                action: std.echo output="output"
                publish:
                  out: "<% task(t3).result %>"
        """
        result = task_names(YAML)
        assert sorted(result) == [
            ("W104: task 't1' should reference itself with task() and not "
             "include its own name line task(t1). In workflow wf"),
            ("W104: task 't3' should reference itself with task() and not "
             "include its own name line task(t3). In workflow wf"),
        ]
