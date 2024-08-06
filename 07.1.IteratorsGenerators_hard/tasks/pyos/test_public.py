import pytest
from _pytest.capture import CaptureFixture  # typing

from .pyos import Task, Scheduler, GetTid, NewTask, KillTask, WaitTask, Coroutine


def task1() -> Coroutine:
    print('start')
    yield None  # SystemCall is omitted, but stupid mypy still wants explicit None
    print('next')
    yield None


def test_single_task_running(capsys: CaptureFixture[str]) -> None:
    t1 = Task(task_id=1, target=task1())
    t1.step()
    stdout = capsys.readouterr().out
    assert stdout.strip() == 'start'


def infinite_ping() -> Coroutine:
    while True:
        print('ping!')
        yield None


def infinite_pong() -> Coroutine:
    while True:
        print('pong!')
        yield None


def test_schedule_infinite_tasks(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(infinite_ping())
    sched.new(infinite_pong())
    sched.run(ticks=1)

    stdout = capsys.readouterr().out
    assert stdout.strip() == 'ping!'

    sched.run(ticks=1)

    stdout = capsys.readouterr().out
    assert stdout.strip() == 'pong!'

    sched.run(ticks=2)

    stdout = capsys.readouterr().out
    assert stdout.split() == ['ping!', 'pong!']


def test_schedule_for_zero_ticks(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(infinite_ping())
    sched.run(ticks=0)

    stdout = capsys.readouterr().out
    assert stdout == ''


def finite_counter() -> Coroutine:
    for i in range(5):
        print(i)
        yield None


def test_schedule_single_finite_task(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(finite_counter())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.split() == [str(i) for i in range(5)]

    assert sched.empty()


def finite_constant() -> Coroutine:
    for _ in range(3):
        print(42)
        yield None


def test_schedule_finite_tasks(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(finite_counter())
    sched.new(finite_constant())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.split() == ['0', '42', '1', '42', '2', '42', '3', '4']

    assert sched.empty()


def finite_greedy_task(message: str) -> Coroutine:
    for _ in range(3):
        print(message)
    yield None  # task without yield is not a coroutine


def test_schedule_non_cooperative_tasks(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(finite_greedy_task('ping'))
    sched.new(finite_greedy_task('pong'))
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    # tasks executes consequently until reach their yield
    # so there is no much sense to execute such greedy tasks in cooperative multitasking scheduler
    assert stdout.split() == ['ping', 'ping', 'ping', 'pong', 'pong', 'pong']

    assert sched.empty()


def ping_with_tid() -> Coroutine:
    tid = yield GetTid()
    for i in range(5):
        print('ping from', tid)
        yield None


def pong_with_tid() -> Coroutine:
    tid = yield GetTid()
    for i in range(3):
        print('pong from', tid)
        yield None


def test_schedule_tasks_with_tid(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(ping_with_tid())
    sched.new(pong_with_tid())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.strip().split('\n') == [
        'ping from 1',
        'pong from 2',
        'ping from 1',
        'pong from 2',
        'ping from 1',
        'pong from 2',
        'ping from 1',
        'ping from 1'
    ]

    assert sched.empty()


def spawner() -> Coroutine:
    print('spawn new task')
    yield NewTask(finite_counter())
    for _ in range(5):
        print('tick')
        yield None


def test_schedule_spawner_task(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(spawner())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.strip().split('\n') == [
        'spawn new task',
        '0',
        'tick',
        '1',
        'tick',
        '2',
        'tick',
        '3',
        'tick',
        '4',
        'tick'
    ]

    assert sched.empty()


def spawner_killer(target: Coroutine) -> Coroutine:
    print('spawn new task')
    child = yield NewTask(target)
    for _ in range(2):
        print('tick')
        yield None
    yield KillTask(child)
    print('task killed')


def test_schedule_killer_task(capsys: CaptureFixture[str]) -> None:
    pinger = infinite_ping()
    sched = Scheduler()
    sched.new(spawner_killer(target=pinger))
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.strip().split('\n') == [
        'spawn new task',
        'ping!',
        'tick',
        'ping!',
        'tick',
        'ping!',
        'task killed'
    ]

    assert sched.empty()
    # target generator should be closed after killing task
    with pytest.raises(StopIteration):
        next(pinger)


def self_killer() -> Coroutine:
    print('starting...')
    tid = yield GetTid()
    print('stopping...')
    yield KillTask(tid)
    print('oops... not stopped')


def test_schedule_self_killer_task(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(self_killer())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.strip().split('\n') == ['starting...', 'stopping...']

    assert sched.empty()


def bad_killer_task() -> Coroutine:
    print('killing...')
    result = yield KillTask(42)
    if result:
        print('done.')
    else:
        print('bad tid!')


def test_schedule_bad_killer_task(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(bad_killer_task())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.strip().split('\n') == [
        'killing...',
        'bad tid!'
    ]

    assert sched.empty()


def waiter_task() -> Coroutine:
    print('spawn new task')
    child = yield NewTask(finite_counter())
    print('waiting...')
    yield WaitTask(child)
    print('done.')


def test_schedule_waiter_task(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(waiter_task())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.strip().split('\n') == [
        'spawn new task',
        '0',
        'waiting...',
        '1',  # do not execute task which is waiting
        '2',
        '3',
        '4',
        'done.'
    ]

    assert sched.empty()


def killer_task(tid: int) -> Coroutine:
    for i in range(3):
        print(f'tick {i}')
        yield None
    print('kill waiter')
    yield KillTask(tid)


def spawn_and_wait_self_killer() -> Coroutine:
    print('starting')
    tid = yield GetTid()
    print('spawn new task')

    child = yield NewTask(killer_task(tid))
    print('waiting...')
    yield WaitTask(child)
    print('We can not be here.')


def test_schedule_kill_waiter_task(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(spawn_and_wait_self_killer())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.strip().split('\n') == [
        'starting',
        'spawn new task',
        'tick 0',
        'waiting...',
        'tick 1',
        'tick 2',
        'kill waiter'
    ]

    assert sched.empty()


def bad_waiter_task() -> Coroutine:
    print('waiting...')
    result = yield WaitTask(42)
    if result:
        print('done.')
    else:
        print('bad tid!')


def test_schedule_bad_waiter_task(capsys: CaptureFixture[str]) -> None:
    sched = Scheduler()
    sched.new(bad_waiter_task())
    sched.run(ticks=100)

    stdout = capsys.readouterr().out
    assert stdout.strip().split('\n') == [
        'waiting...',  # immedialely continue task if it tries to wait for unexisting task_id
        'bad tid!'
    ]

    assert sched.empty()
