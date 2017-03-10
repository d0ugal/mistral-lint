from __future__ import print_function

import copy
import os
import pkg_resources

import yaml


class LintSuite(object):

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
            loaded_file = f.read()
            loaded_yaml = yaml.safe_load(loaded_file)

        for name, linter in linters.items():
            linter(path, loaded_file, copy.deepcopy(loaded_yaml))

        print()

    def run_lint(self, paths):

        linters = self._find_linters()

        for path in paths:
            for path in self._walk_files(path):

                self.lint_file(path, linters)


def lint(paths):
    suite = LintSuite()
    suite.run_lint(paths)
