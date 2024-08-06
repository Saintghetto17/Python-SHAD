from queue import Queue
from abc import ABC, abstractmethod
from typing import Generator, Any


class SystemCall(ABC):
    """SystemCall yielded by Task to handle with Scheduler"""

    @abstractmethod
    def handle(self, scheduler: 'Scheduler', task: 'Task') -> bool:
        """
        :param scheduler: link to scheduler to manipulate with active tasks
        :param task: task which requested the system call
        :return: an indication that the task must be scheduled again
        """


# wrap above System calls (Tasks) обертка, чтоб исполнять код задачи
Coroutine = Generator[SystemCall | None, Any, None]


class Task:
    def __init__(self, task_id: int, target: Coroutine) -> None:
        """
        :param task_id: id of the task
        :param target: coroutine to run. Coroutine can produce system calls.
        System calls are being executed by scheduler and the result sends back to coroutine.
        """
        self._taskid: int = task_id
        self._target: Coroutine = target
        self._lastres: Any = None
        self.is_waited: bool = False

    def get_target(self) -> Coroutine:
        return self._target

    def get_id(self) -> int:
        return self._taskid

    def set_syscall_result(self, result: Any) -> None:
        """
        Saves result of the last system call
        """
        self._lastres = result

    def step(self) -> SystemCall | None:
        """
        Performs one step of coroutine, i.e. sends result of last system call
        to coroutine (generator), gets yielded value and returns it.
        """
        # here after every step we send a value to the left = operand
        yielded_sys_call: SystemCall | None = self._target.send(self._lastres)
        return yielded_sys_call


class Scheduler:
    """Scheduler to manipulate with tasks"""

    def __init__(self) -> None:
        self.task_id = 1
        self.task_queue: Queue[Task] = Queue()
        self.task_map: dict[int, Task] = {}  # task_id -> task
        self.wait_map: dict[int, list[Task]] = {}  # task_id -> list of waiting tasks

    def _schedule_task(self, task: Task) -> None:
        """
        Add task into task queue
        :param task: task to schedule for execution
        """
        self.task_queue.put(task)

    def new(self, target: Coroutine) -> int:
        """
        Create and schedule new task
        :param target: coroutine to wrap in task
        :return: id of newly created task
        """
        new_task = Task(self.task_id, target)
        self._schedule_task(new_task)
        # save our task in task_map
        self.task_map[self.task_id] = new_task
        self.task_id += 1
        return self.task_id - 1

    def exit_task(self, task_id: int) -> bool:
        """
        PRIVATE API: can be used only from scheduler itself or system calls
        Hint: do not forget to reschedule waiting tasks
        :param task_id: task to remove from scheduler
        :return: true if task id is valid
        """
        res: bool = False
        if task_id in self.task_map.keys():
            res = True
        if not res:
            return False
        # get the task by id
        task_exit = self.task_map[task_id]
        # get the coroutine
        task_code = task_exit.get_target()
        # stop coroutine because we want to get StopIteration while meet it again in Queue
        # by this it will be deleted from queue in 'run' by itself
        task_code.close()
        if task_id in self.wait_map.keys():
            for re_task in self.wait_map[task_id]:
                self._schedule_task(re_task)
                re_task.is_waited = False
        del self.task_map[task_id]
        return res

    def wait_task(self, task_id: int, wait_id: int) -> bool:
        """
        PRIVATE API: can be used only from scheduler itself or system calls
        :param task_id: task to hold on until another task is finished
        :param wait_id: id of the other task to wait for
        :return: true if task and wait ids are valid task ids
        """
        res: bool = False
        if task_id in self.task_map.keys() and wait_id in self.task_map.keys():
            res = True
        if not res:
            return False
        if wait_id not in self.wait_map.keys():
            lst_wait: list[Task] = [self.task_map[task_id]]
            self.wait_map[wait_id] = lst_wait
        else:
            self.wait_map[wait_id].append(self.task_map[task_id])
        return res

    def run(self, ticks: int | None = None) -> None:
        """
        Executes tasks consequently, gets yielded system calls,
        handles them and reschedules task if needed
        :param ticks: number of iterations (task steps), infinite if not passed
        """

        try:
            index: int = 0
            while True:
                if ticks is not None and index >= ticks:
                    break
                index += 1
                task_popped = self.task_queue.get()

                try:
                    if task_popped and task_popped.is_waited:
                        continue
                    yielded_sys = task_popped.step()
                    if isinstance(yielded_sys, SystemCall):
                        yielded_sys.handle(self, task_popped)
                except StopIteration:
                    if self.task_queue.qsize() != 0:
                        self.exit_task(task_popped.get_id())
                        continue
                    else:
                        self.exit_task(task_popped.get_id())
                        if len(self.task_map) != 0:
                            continue
                        break
                else:
                    self.task_queue.put(task_popped)
        except KeyboardInterrupt:
            return

    def empty(self) -> bool:
        """Checks if there are some scheduled tasks"""
        return not bool(self.task_map)


class GetTid(SystemCall):
    """System call to get current task id"""

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        task_id = task.get_id()
        task.set_syscall_result(task_id)
        return True


class NewTask(SystemCall):
    """System call to create new task from target coroutine"""

    def __init__(self, target: Coroutine) -> None:
        self.target = target

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        task_id = scheduler.new(self.target)
        task.set_syscall_result(task_id)
        return False


class KillTask(SystemCall):
    """System call to kill task with particular task id"""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        scheduler.exit_task(self.task_id)
        return False


class WaitTask(SystemCall):
    """System call to wait task with particular task id"""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        # Note: One shouldn't reschedule task which is waiting for another one.
        # But one must reschedule task if task id to wait for is invalid.
        res = scheduler.wait_task(task.get_id(), self.task_id)
        task.set_syscall_result(res)
        if res is True:
            task.is_waited = True
        return False
