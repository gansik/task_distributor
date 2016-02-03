''' 	
	This problem is similar to https://en.wikipedia.org/wiki/Bin_packing_problem and we can to use a some library like https://pypi.python.org/pypi/openopt.
	I will use an algorithm similar to the "First Fit Decreasing". 

'''

class Task(object):

    def __init__(self, name, task_point=1):
        self.name = name
        self.task_point = int(task_point)
    
    def __str__(self):
        return 'Task [%6d]: %s' % (self.task_point, self.name)

    """ hack for debugging http://stackoverflow.com/questions/727761/python-str-and-lists
    def __repr__(self):
        return self.__str__()
    """

class Employee(object):

    def __init__(self, name, task_point=1):
        self.name = name
        self.task_point = int(task_point)
        self.tasks_cnt = 0
        self.tasks_sum = 0

        self.tasks = []

    @property
    def fullness(self):
        return float(self.tasks_sum) / self.task_point * 100

    def append(self, task, max_tp_sum=None):
        if max_tp_sum is None:
            max_tp_sum = self.task_point

        if (task.task_point + self.tasks_sum) > max_tp_sum:
            return False
        else:
            self.tasks.append(task)
            self.tasks_cnt += 1
            self.tasks_sum += task.task_point
            return True

    def __str__(self):
        return 'Employee [%6d]: %s (%d task(s), capacity - %.1f%%)' % (
		self.task_point, 
		self.name, 
		self.tasks_cnt,
		self.fullness
        )


class TaskDistributor(object):
    def __init__(self, employees):

        self.employees = employees
        self.sort_employees()
        self.fullness = .0

        self._tasks = []
        self._tasks_tp_sum = 0
        self._emps_tp_sum = sum(o.task_point for o in self.employees)

        self._amount_assigned_tasks = 0


    def sort_employees(self, by='task_point', reverse=True):
        self.employees.sort(key=lambda x: getattr(x, by), reverse=reverse)

    def add_tasks(self, tasks):
        self._tasks.extend(tasks)
        self._tasks.sort(key=lambda x: x.task_point, reverse=True)

        self._tasks_tp_sum = sum(o.task_point for o in self._tasks)
        self.fullness = float(self._tasks_tp_sum) / self._emps_tp_sum * 100

        if self.fullness > 100:
            raise ValueError('sum of task_point tasks bigger what sum of task_point employees')

        """	Main work. Using "First Fit Decreasing algorithm."
        """
        for tsk in self._tasks:

            added = False
            for emp in self.employees:
                max_tp_sum = emp.task_point * (self.fullness / 100) # maximum sum of "tasks task_point" for this employee
                added = emp.append(tsk, max_tp_sum)
                if added:
                    self._amount_assigned_tasks += 1
                    break

            """	Assign tasks to employees without to check a "max_tp_sum" value. 
            """
            if not added:
                self.sort_employees(by='fullness', reverse=False) # sort employees by congestion
                for emp in self.employees:
                    added = emp.append(tsk)
                    if added:
                        self._amount_assigned_tasks += 1
                        break

    """	Service method to assess the quality of the algorithm. The less result is better.
    """
    def calc_dispersion(self):
        l = len(self.employees)
        average = self.fullness
        disp_sum = 0
        for o in self.employees:
            disp_sum += (o.fullness - average) * (o.fullness - average)
        return disp_sum / l

    """	Method of debug for developer.
    """
    def _print_debug_dump(self):
        for attr in dir(self):
            t = type(getattr(self, attr))
            if t is int or t is str or t is float:
                print "TD.%s = %s" % (attr, getattr(self, attr))


if __name__ == '__main__':

    """ Initialize from files data/employees.csv and data/tasks.csv.
    """
    employees = []
    with open('data/employees.csv', "r") as f:
        for line in f:
            if '\t' in line:
                employees.append(Employee(*line.split('\t')))

    tasks = []
    with open('data/tasks.csv', "r") as f:
        for line in f:
            if '\t' in line:
                tasks.append(Task(*line.split('\t')))

    td = TaskDistributor(employees)

    td.add_tasks(tasks)

    #td._print_debug_dump()

    print '''STATS
	amount of employees: %d
	amount of tasks: %d
	amount of assigned tasks: %d
	total task_point of employees: %d
	total task_point of tasks: %d
	average fullness: %.1f%%
	dispersion: %.2f''' % (
		len(td.employees), 
		len(td._tasks), 
		td._amount_assigned_tasks, 
		td._emps_tp_sum, 
		td._tasks_tp_sum, 
		td.fullness,
		td.calc_dispersion()
	)

    print 'RESULTS'
    td.sort_employees(by='fullness')
    for emp in td.employees:
        print '%s [task_point: %d/%d, capacity: %.1f%%]' % (emp.name, emp.task_point, emp.tasks_sum, emp.fullness)
        for tsk in emp.tasks:
            print '\t%s [task_point: %d]' % (tsk.name, tsk.task_point)
    