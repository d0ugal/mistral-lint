Mint
====

|PyPI Version| |Build Status|

Usage
-----

::

    $ pip install mistral-lint
    $ mistral-lint path-to-files


Example Output
--------------

::

    workbooks/baremetal.yaml
    W101: Workbook tripleo.baremetal.v1 has no description
    W101: Workbook tripleo.baremetal.v1 has no description
    W101: Workbook tripleo.baremetal.v1 has no description
    E103: Input node_uuids is not used in Workflow tripleo.baremetal.v1.cellv2_discovery

    workbooks/deployment.yaml
    W101: Workbook tripleo.deployment.v1 has no description
    W101: Workbook tripleo.deployment.v1 has no description

    workbooks/plan_management.yaml
    W101: Workbook tripleo.plan_management.v1 has no description
    W101: Workbook tripleo.plan_management.v1 has no description
    W101: Workbook tripleo.plan_management.v1 has no description

    workbooks/stack.yaml
    W101: Workbook tripleo.stack.v1 has no description
    W101: Workbook tripleo.stack.v1 has no description
    W101: Workbook tripleo.stack.v1 has no description
    W101: Workbook tripleo.stack.v1 has no description

    workbooks/validations.yaml
    W101: Workbook tripleo.validations.v1 has no description
    W101: Workbook tripleo.validations.v1 has no description
    W101: Workbook tripleo.validations.v1 has no description
    W101: Workbook tripleo.validations.v1 has no description
    W101: Workbook tripleo.validations.v1 has no description
    W101: Workbook tripleo.validations.v1 has no description
    W101: Workbook tripleo.validations.v1 has no description
    E103: Input queue_name is not used in Workflow tripleo.validations.v1.add_validation_ssh_key_parameter


Ideas
-----

- Check that tasks exist (all those that are mentined in on-error, on-success
  on-complete etc.).
- Check all tasks are called.
- Check all tasks have an on-error/on-success or on-complete
- Check zaqar format
- Interactive workflow with zaqar posting the continue code.
- Check sub-workflows are provided the queue name

.. |PyPI Version| image:: https://img.shields.io/pypi/v/mistral-lint.png
   :target: https://pypi.python.org/pypi/mistral-lint
.. |Build Status| image:: https://img.shields.io/travis/d0ugal/mistral-lint/master.png
   :target: https://travis-ci.org/d0ugal/mistral-lint
