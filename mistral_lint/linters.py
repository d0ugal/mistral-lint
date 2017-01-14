import yaml as pyyaml


def description(path, string, yaml):
    """Verify that Workbooks and Workflows have descriptions"""

    if 'workflows' not in yaml:
        print("Probably not a workbook. Not supported")
        return

    W102 = "W101: Workbook {} has no description"
    W101 = "W102: Workflow {}.{} has no description"

    workbook = yaml['name']

    if 'description' not in yaml:
        print(W101.format(workbook))

    for workflow, struct in yaml['workflows'].items():
        if 'description' not in struct:
            print(W102.format(workbook, workflow))


def type(path, string, yaml):
    """Check that type 'direct' isn't specified as it isn't needed"""

    if 'workflows' not in yaml:
        print("Probably not a workbook. Not supported")
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
        print("Probably not a workbook. Not supported")
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

    task_list = task.get(key)

    if not task_list:
        return

    W104 = "W104: Call to task {} in {} which isn't found"

    if isinstance(task_list, str):
        task_list = task_list.split(' ', 1)[0]
        if task_list not in names:
            print(W104.format(task_list, key))
    elif isinstance(task_list, (list, dict)):
        for task in task_list:
            if isinstance(task, dict):
                task = next(iter(task.keys()))
            if task not in names:
                print(W104.format(task, key))
    else:
        raise Exception(task_list)


def tasks(path, string, yaml):
    """Check that all tasks exist"""

    if 'workflows' not in yaml:
        print("Probably not a workbook. Not supported")
        return

    for workflow_name, workflow in yaml['workflows'].items():

        tasks = list(workflow['tasks'].keys())

        for task_name, task in workflow['tasks'].items():
            _check_exists(task, 'on-success', tasks)
            _check_exists(task, 'on-error', tasks)
            _check_exists(task, 'on-complete', tasks)
