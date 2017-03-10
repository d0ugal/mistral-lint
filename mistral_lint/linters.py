from __future__ import print_function

import six
import yaml as pyyaml


def _find_line(match, contents):

    for lineno, line in enumerate(contents.splitlines(), start=1):
        if match in line:
            return lineno


def description(path, string, yaml):
    """Verify that Workbooks and Workflows have descriptions"""

    if 'workflows' not in yaml:
        print("Probably not a workbook. Not supported. {}".format(path))
        return

    W102 = "W101: Workbook {} has no description"
    W101 = "W102: Workflow {}.{} has no description"

    workbook = yaml['name']

    if 'description' not in yaml:
        print(W101.format(workbook))

    for workflow, struct in yaml['workflows'].items():
        if 'description' not in struct:
            print(W102.format(workbook, workflow))


def type_(path, string, yaml):
    """Check that type 'direct' isn't specified as it isn't needed"""

    if 'workflows' not in yaml:
        print("Probably not a workbook. Not supported. {}".format(path))
        return

    W103 = ("W103: Type 'direct' is the default and can be removed from "
            "Workflow {}.{}")

    workbook = yaml['name']
    for workflow, struct in yaml['workflows'].items():
        if struct.get('type') == "direct":
            print(W103.format(workbook, workflow))


def inputs(path, string, yaml):
    """Check that the workflow inputs are used"""

    if 'workflows' not in yaml:
        print("Probably not a workbook. Not supported. {}".format(path))
        return

    E101 = "E103: Input {} is not used in Workflow {}.{}"

    workbook = yaml['name']
    for workflow, struct in yaml['workflows'].items():

        inputs = struct.get('input')
        if not inputs:
            continue

        for i in inputs:
            i = next(iter(i.keys())) if not isinstance(i, str) else i
            if i not in pyyaml.dump(struct.get('tasks')):
                print(E101.format(i, workbook, workflow))


def _check_exists(task, key, names):

    ENGINE_COMMANDS = ["fail", "pause", "succeed"]

    task_list = task.get(key)

    if not task_list:
        return

    W104 = "W104: Call to task {} in {} which isn't found"

    if isinstance(task_list, str):
        task_list = task_list.split(' ', 1)[0]
        if task_list not in names:
            if task_list in ENGINE_COMMANDS:
                return
            print(W104.format(task_list, key))
    elif isinstance(task_list, (list, dict)):
        for task in task_list:
            if isinstance(task, dict):
                task = next(iter(task.keys()))
            if task in ENGINE_COMMANDS:
                continue
            if task not in names:
                print(W104.format(task, key))
    else:
        raise Exception(task_list)


def tasks(path, string, yaml):
    """Check that all tasks exist"""

    if 'workflows' not in yaml:
        print("Probably not a workbook. Not supported. {}".format(path))
        return

    for workflow_name, workflow in yaml['workflows'].items():

        tasks = list(workflow['tasks'].keys())

        for task_name, task in workflow['tasks'].items():
            _check_exists(task, 'on-success', tasks)
            _check_exists(task, 'on-error', tasks)
            _check_exists(task, 'on-complete', tasks)


def _find_strings(value):
    if value is None or isinstance(value, int):
        pass
    elif isinstance(value, six.string_types):
        yield value
    elif isinstance(value, list):
        for thing in value:
            for s in _find_strings(thing):
                yield s
    elif isinstance(value, dict):
        for k, v in value.items():
            for s in _find_strings(k):
                yield s
            for s in _find_strings(v):
                yield s
    else:
        raise Exception(type(value))


def expressions(path, string, yaml):

    for expr in _find_strings(yaml):
        W105 = "W105: Invalid expression '{}' on line {} in {}"

        if expr.count("<%") != expr.count("%>"):
            lineno = _find_line(expr, string)
            print(W105.format(expr, lineno, path))
        elif expr.count("{{") != expr.count("}}"):
            lineno = _find_line(expr, string)
            print(W105.format(expr, lineno, path))
