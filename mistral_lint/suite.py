from __future__ import print_function

import collections
import copy
import os
import pkg_resources

import yaml


class LintSuite(object):

    def __init__(self, print_messages):
        self._messages = collections.defaultdict(set)
        self.__print = print_messages
        self._verbose = False

    def _is_yaml(self, path):
        return path.endswith(".yaml") or path.endswith(".yml")

    def _walk_files(self, path):

        if os.path.isfile(path):
            yield path
        elif not os.path.isdir(path):
            print("The path '%s' can't be found.", path)
            raise StopIteration

        for root, dirs, filenames in os.walk(path):
            # Remove dot-directories from the dirs list.
            dirs[:] = sorted(d for d in dirs if not d.startswith('.'))
            for filename in sorted(filenames):
                if self._is_yaml(filename):
                    yield os.path.join(root, filename)

    def _find_linters(self):
        linters = {}
        for linter in pkg_resources.iter_entry_points(group='mistral.linters'):
            linters[linter.name] = linter.load()
        return linters

    def lint_file(self, path, linters):

        with open(path) as f:
            yaml_string = f.read()

        return self.lint_string(path, yaml_string, linters)

    def _print(self, path, message):

        if self.__print and path not in self._messages:
            if len(self._messages):
                print()
            print(path)

        self._messages[path].add(message)

        if self.__print:
            print(message)

    def messages(self):
        return self._messages

    def lint_string(self, path, yaml_string, linters, validate_file=True):

        loaded_yaml = yaml.safe_load(yaml_string)

        try:
            keys = set(loaded_yaml.keys())
        except AttributeError:
            if self._verbose:
                self._print(
                    path,
                    "Ignoring {}. It doesn't seem to be a workbook or workflow"
                    .format(path))
            return []

        base_spec = {'name', 'version', 'description', 'tags'}
        if not validate_file:
            pass
        elif keys.issubset(base_spec | {"version", "actions", "workflows"}):
            pass
        elif keys.issubset(base_spec | {"type", "task-default", "input",
                                        "output", "output-on-error", "vars"}):
            pass
        else:
            if self._verbose:
                self._print(
                    path,
                    "Ignoring {}. It doesn't seem to be a workbook or workflow"
                    .format(path))
            return []

        errors = []

        for name, linter in linters.items():
            for error in linter(path, yaml_string, copy.deepcopy(loaded_yaml)):
                if error is not None:
                    errors.append(error)

        if errors:
            for error in errors:
                self._print(path, error)

        return errors

    def run_lint(self, paths):

        passed = True

        linters = self._find_linters()
        for path in paths:
            for path in self._walk_files(path):
                file_result = self.lint_file(path, linters)
                passed = passed and len(file_result)

        return self._messages


def lint(paths, print_messages=True):
    suite = LintSuite(print_messages)
    return suite.run_lint(paths)
