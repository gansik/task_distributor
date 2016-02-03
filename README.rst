:Author:
	Gansik <gansik@tagv.com>

Task Distributor
================

We have a group of employees who can achieve a certain amount of work, depending on his or her capability.  We represent this amount of work as task_point (a integer).

This group of employees needs to complete a list of tasks.

The task complexity is also represented by task_point.

The harder the task, the higher the task_point is.

The goal of this exercise is to find, using Python, the best possible way to dispatch tasks between all the employees so that the workload of each employee is as evenly spread as possible (so that one employee is not overworked, while another has almost nothing to do)

Every task has a name, and each employee has a nickname.

For each employee, the result should display the following as a minimum:

employee's nickname

employee's personal task_point

the list of all tasks assigned to the employee (name and corresponding task_point)

the total amount of task_point assigned to the employee


Requirements
------------

 * Python 2.x

Installation
------------

To prepare data files (employees.csv, tasks.csv) please run:

`./test_data_generator.py`


Run
---

Just run `task_distributor.py`