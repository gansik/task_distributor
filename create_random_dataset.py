import random
from tests import TestTaskDistributor

if __name__ == '__main__':

    tp_emp_sum = 0
    with open('data/employees.csv', 'w') as f:
        for i in range(10):
            tp = random.randint(10, 40)
            tp_emp_sum += tp
            f.write('%s	%d\n' % (TestTaskDistributor._get_random_name(), tp))


    tp_tsk_sum = 0
    with open('data/tasks.csv', 'w') as f:
        for i in range(30):
            tp = random.randint(2, 12)
            tp_tsk_sum += tp

            if tp_tsk_sum > tp_emp_sum: # stop if "task_point sum" of tasks bigger what "task_point sum" of employees 
                break

            f.write('%s	%d\n' % (TestTaskDistributor._get_random_phrase('TASK %d: ' % i), tp))

    print """Random dataset created in files 'data/employees.csv' and 'data/tasks.csv'."""

