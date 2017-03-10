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
    W102: Workflow tripleo.baremetal.v1.set_node_state has no description
    W102: Workflow tripleo.baremetal.v1.set_power_state has no description
    W102: Workflow tripleo.baremetal.v1.manual_cleaning has no description
    E103: Input node_uuids is not used in Workflow tripleo.baremetal.v1.cellv2_discovery

    workbooks/deployment.yaml
    W102: Workflow tripleo.deployment.v1.deploy_on_server has no description
    W102: Workflow tripleo.deployment.v1.deploy_on_servers has no description

    workbooks/plan_management.yaml
    W102: Workflow tripleo.plan_management.v1.create_deployment_plan has no description
    W102: Workflow tripleo.plan_management.v1.update_deployment_plan has no description
    W102: Workflow tripleo.plan_management.v1.create_default_deployment_plan has no description

    workbooks/stack.yaml
    W102: Workflow tripleo.stack.v1.wait_for_stack_complete_or_failed has no description
    W102: Workflow tripleo.stack.v1.wait_for_stack_in_progress has no description
    W102: Workflow tripleo.stack.v1.wait_for_stack_does_not_exist has no description
    W102: Workflow tripleo.stack.v1.delete_stack has no description

    workbooks/validations.yaml
    W102: Workflow tripleo.validations.v1.run_validation has no description
    W102: Workflow tripleo.validations.v1.run_validations has no description
    W102: Workflow tripleo.validations.v1.run_groups has no description
    W102: Workflow tripleo.validations.v1.list has no description
    W102: Workflow tripleo.validations.v1.list_groups has no description
    W102: Workflow tripleo.validations.v1.add_validation_ssh_key_parameter has no description
    W102: Workflow tripleo.validations.v1.copy_ssh_key has no description
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
