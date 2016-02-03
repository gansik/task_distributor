import sys
import random
import unittest
from task_distributor import Employee, Task, TaskDistributor

# names from https://github.com/treyhunner/names/tree/master/names
first_names_male = (
	'James','John','Robert','Michael','William','David','Richard','Charles','Joseph','Thomas','Christopher','Daniel','Paul','Mark','Donald','George',
	'Kenneth','Steven','Edward','Brian','Ronald','Anthony','Kevin','Jason','Matthew','Gary','Timothy','Jose','Larry','Jeffrey','Frank','Scott','Joe',
	'Eric','Stephen', 'Andrew','Raymond', 'Gregory', 'Joshua','Jerry','Dennis','Walter','Patrick','Peter','Harold','Douglas','Henry','Carl','Arthur',
	'Ryan','Roger','Juan','Jack','Albert', 'Jonathan', 'Justin', 'Terry','Gerald','Keith','Samuel','Willie','Ralph','Lawrence','Nicholas','Benjamin',
	'Bruce','Brandon', 'Adam', 'Harry', 'Fred', 'Wayne', 'Billy','Steve','Louis','Jeremy','Aaron','Randy','Howard','Eugene','Carlos','Roy','Russell',
	'Bobby','Victor','Martin','Ernest', 'Philip', 'Todd', 'Jesse','Craig','Alan','Shawn','Clarence','Sean','Phillip','Chris','Johnny','Earl','Jimmy',
	'Antonio','Danny','Bryan','Tony','Luis','Mike','Stanley','Leonard','Nathan','Dale','Manuel','Rodney','Curtis','Norman','Allen','Marvin', 'Edwin',
	'Joel','Vincent','Glenn','Jeffery','Travis','Jeff','Chad','Jacob','Lee','Melvin','Alfred','Kyle','Francis','Bradley','Jesus', 'Herbert','Marcus',
	'Clifford','Frederick','Ray','Don','Eddie','Ricky','Troy','Randall','Barry','Alexander','Bernard','Mario','Leroy','Francisco','Micheal','Miguel',
	'Oscar','Theodore', 'Jay','Jim','Tom','Calvin','Alex','Jon','Ronnie','Bill','Lloyd','Tommy','Leon','Derek','Warren','Darrell','Jerome','Maurice',
	'Floyd','Leo','Alvin','Tim','Wesley','Gordon','Dean','Greg','Jorge','Dustin','Pedro','Derrick','Dan','Lewis','Zachary','Corey','Herman','Vernon',
	'Roberto', 'Clyde', 'Glen','Hector','Shane','Ricardo','Sam','Rick','Lester','Brent','Ramon','Charlie','Tyler','Gilbert','Gene','Marc','Reginald',
	'Ruben', 'Brett','Angel','Nathaniel','Rafael','Leslie','Edgar','Milton','Raul','Ben','Chester','Cecil','Duane','Franklin','Andre','Elmer','Brad',
	'Gabriel','Mitchell', 'Roland', 'Arnold', 'Harvey', 'Jared', 'Adrian','Karl','Cory','Claude','Erik','Darryl','Jamie','Neil','Jessie','Christian',
	'Ron','Javier','Fernando','Clinton','Ted','Mathew','Tyrone','Darren','Lonnie','Lance','Cody','Julio','Kelly','Kurt','Allan','Nelson','Guy','Max',
	'Clayton','Hugh','Dwayne'
)

last_names = (
	'Smith','Johnson','Williams','Jones','Brown','Davis','Miller','Wilson','Moore','Taylor','Anderson','Thomas','Jackson','White','Harris','Martin',
	'Thompson','Garcia','Martinez','Robinson','Clark','Rodriguez','Lewis','Lee','Walker','Hall','Allen','Young','Hernandez','King','Wright','Lopez',
	'Hill','Scott','Green','Adams','Baker','Gonzalez','Nelson','Carter','Mitchell','Perez','Roberts','Turner','Phillips','Campbell','Parker','Reed',
	'Evans','Edwards','Collins','Stewart','Sanchez','Morris','Rogers','Cook','Morgan','Bell','Murphy','Bailey','Rivera','Cooper','Richardson','Cox',
	'Howard','Ward','Torres','Peterson','Gray','Ramirez','James','Watson','Brooks','Kelly','Sanders','Price','Bennett','Wood','Barnes','Ross','Fox',
	'Henderson','Coleman','Jenkins','Perry','Powell','Long','Patterson','Hughes','Flores','Washington','Butler','Simmons','Foster','Gonzales','Day',
	'Bryant', 'Alexander','Russell','Griffin','Diaz','Hayes','Myers','Ford','Hamilton','Graham','Sullivan','Wallace','Woods','Cole','West','Jordan',
	'Owens','Reynolds','Henry','Ellis','Harrison','Gibson','Mcdonald','Cruz','Marshall','Ortiz','Gomez','Murray','Freeman','Wells','Webb','Simpson',
	'Stevens', 'Fisher', 'Tucker', 'Porter','Hunter','Hicks','Crawford','Boyd','Mason','Morales','Kennedy','Warren','Dixon','Ramos','Reyes','Burns',
	'Gordon','Shaw', 'Holmes', 'Rice', 'Robertson', 'Hunt', 'Black','Daniels','Palmer','Mills','Nichols','Grant','Knight','Ferguson','Rose','Stone',
	'Hawkins','Dunn','Perkins', 'Hudson', 'Spencer', 'Gardner', 'Stephens','Payne','Pierce','Berry','Matthews','Arnold','Wagner','Willis','Watkins',
	'Olson', 'Carroll', 'Duncan', 'Snyder', 'Hart','Cunningham','Bradley','Lane','Andrews','Ruiz','Harper','Riley','Armstrong','Carpenter','Weaver',
	'Greene','Lawrence','Elliott','Chavez','Sims','Austin','Peters','Kelley','Franklin','Lawson','Fields', 'Gutierrez', 'Ryan', 'Schmidt','Vasquez',
	'Castillo','Carr','Wheeler','Chapman','Oliver','Montgomery','Richards','Williamson','Johnston','Banks','Meyer', 'Bishop','Mccoy','Howell','Ray',
	'Alvarez','Morrison','Hansen','Fernandez','Garza','Harvey','Little','Burton','Stanley','Nguyen','George','Jacobs','Reid','Kim','Fuller','Lynch',
	'Dean','Gilbert','Garrett','Romero','Welch','Larson','Frazier','Burke','Hanson','Mendoza','Moreno','Bowman','Medina','Fowler','Brewer','Hofman',
	'Carlson','Silva','Pearson','Holland'
)

FN_LEN = len(first_names_male) - 1
LN_LEN = len(last_names) - 1


class TestTaskDistributor(unittest.TestCase):

    @staticmethod
    def _get_random_name():
        return '%s %s' % (
		first_names_male[random.randint(0, FN_LEN)],
		last_names[random.randint(0, LN_LEN)],
        )

    @staticmethod
    def _get_random_phrase(prefix=''):
        ret = ''
        for i in range(6):
            ret += '%s ' % last_names[random.randint(0, LN_LEN)].lower()[::-1]
        return prefix + ret

    def test_create_employee(self):
        em1 = Employee(self._get_random_name(), 10)

        self.assertEqual(em1.task_point, 10)

    def test_create_task(self):
        tsk1 = Task(self._get_random_phrase(), 3)

        self.assertEqual(tsk1.task_point, 3)

    def test_complex_employees_tasks(self):
        em1 = Employee('John Doe', 10)
        em2 = Employee('Ivan Ivanov', 6)

        em1.append(Task('Some task', 3))
        em1.append(Task('Some other task', 2))
        em2.append(Task('## super task %43%', 3))

        self.assertEqual(em1.fullness, 50.)
        self.assertEqual(em1.tasks_sum, 5)
        self.assertEqual(em2.tasks_cnt, 1)

    def test_taskdistributor(self):
        employees = [ Employee(self._get_random_name(), random.randint(20, 50)) for i in range(30) ]
        tasks = [ Task(self._get_random_phrase('TASK %d: ' % i), random.randint(1, 11)) for i in range(100) ]

        td = TaskDistributor(employees)
        td.add_tasks(tasks)

        fullness = float(td._tasks_tp_sum) / td._emps_tp_sum * 100

        self.assertEqual(len(td.employees), len(employees))
        self.assertEqual(len(td._tasks), len(tasks))
        self.assertEqual(td.fullness, fullness)
        self.assertEqual(td._amount_assigned_tasks, len(tasks))



if __name__ == '__main__':

    tp_emp_sum = 0
    with open('employees.csv', 'w') as f:
        for i in range(10):
            tp = random.randint(10, 40)
            tp_emp_sum += tp
            f.write('%s	%d\n' % (TestTaskDistributor._get_random_name(), tp))


    tp_tsk_sum = 0
    with open('tasks.csv', 'w') as f:
        for i in range(30):
            tp = random.randint(2, 12)
            tp_tsk_sum += tp

            if tp_tsk_sum > tp_emp_sum: # stop if "task_point sum" of tasks bigger what "task_point sum" of employees 
                break

            f.write('%s	%d\n' % (TestTaskDistributor._get_random_phrase('TASK %d: ' % i), tp))

    print "\n".join(sys.argv)

    unittest.main()
