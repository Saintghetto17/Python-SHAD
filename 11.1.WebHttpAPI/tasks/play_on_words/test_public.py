import subprocess
import time
import signal
from collections.abc import Generator
from pathlib import Path
import typing as tp
from contextlib import contextmanager


TASK_FOLDER = Path(__file__).parent
TEST_SERVER_FOLDER = TASK_FOLDER / 'socket_test_servers'
CLIENT_FILE_FULL_PATH = str(TASK_FOLDER / 'client.py')


@contextmanager
def run_socket_server(filename: str | Path, *args: tp.Any) -> Generator[None, None, None]:
    proc = subprocess.Popen(
        ['python', filename, *args],
    )
    try:
        time.sleep(0.5)  # a little sleep in order for the server to rise
        yield
        time.sleep(0.5)  # a little sleep in order for the server to fall down
    except Exception as e:
        proc.kill()
        time.sleep(0.5)  # a little sleep in order for the server to fall down
        raise e
    proc.kill()


def test_run_client_without_server() -> None:
    run = subprocess.run(
        ['python', CLIENT_FILE_FULL_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert run.returncode != 0
    assert b'Connection refused' in run.stderr


def test_first_step_win_server(free_port: int) -> None:
    """Simple server, where player win after first step"""
    with run_socket_server(TEST_SERVER_FOLDER / 'first_step_win_server.py', f'--port={free_port}'):
        run = subprocess.run(
            ['python', CLIENT_FILE_FULL_PATH, f'--port={free_port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = run.stdout.decode('utf-8')
<<<<<<< HEAD

        assert run.returncode == 0
=======
        stderr = run.stderr.decode('utf-8')

        assert run.returncode == 0, stderr
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b

        # check logging works somehow
        assert 'WELCOME' in stdout
        assert 'hello' in stdout
        assert 'PLAY' in stdout
        assert 'MESSAGE' in stdout
        assert 'lol' in stdout
        assert 'PLAYER_VICTORY' in stdout


def test_first_step_lose_server(free_port: int) -> None:
    """Simple server, where player lose after first step"""
    with run_socket_server(TEST_SERVER_FOLDER / 'first_step_lose_server.py', f'--port={free_port}'):
        run = subprocess.run(
            ['python', CLIENT_FILE_FULL_PATH, f'--port={free_port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = run.stdout.decode('utf-8')

        assert run.returncode != 0

        # check logging works somehow
        assert 'WELCOME' in stdout
        assert 'lose' in stdout
        assert 'PLAY' in stdout
        assert 'MESSAGE' in stdout
        assert 'lol' in stdout
        assert 'PLAYER_DEFEAT' in stdout


def test_win_after_n_iterations_server(free_port: int) -> None:
    """Simple server, where player win after n steps"""
    with run_socket_server(TEST_SERVER_FOLDER / 'win_after_n_iterations_server.py', f'--port={free_port}'):
        run = subprocess.run(
            ['python', CLIENT_FILE_FULL_PATH, f'--port={free_port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = run.stdout.decode('utf-8')
<<<<<<< HEAD

        assert run.returncode == 0
=======
        stderr = run.stderr.decode('utf-8')

        assert run.returncode == 0, stderr
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b

        # check logging works somehow
        assert 'WELCOME' in stdout
        assert 'wait' in stdout
        assert 'PLAY' in stdout
        assert 'PLAYER_VICTORY' in stdout


def test_never_win_server(free_port: int) -> None:
    """Simple server, where player can not win and should SURRENDER somewhere"""
    with run_socket_server(TEST_SERVER_FOLDER / 'never_win_server.py', f'--port={free_port}'):
        run = subprocess.run(
            ['python', CLIENT_FILE_FULL_PATH, f'--port={free_port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = run.stdout.decode('utf-8')

        assert run.returncode != 0

        # check logging works somehow
        assert 'WELCOME' in stdout
        assert 'long' in stdout
        assert 'PLAY' in stdout
        assert 'SURRENDER' in stdout
        assert 'PLAYER_DEFEAT' in stdout


def test_dummy_but_honest_server(free_port: int) -> None:
    """Dummy server, knows a few words, but do it honest work"""
    with run_socket_server(TEST_SERVER_FOLDER / 'dummy_but_honest_server.py', f'--port={free_port}'):
        run = subprocess.run(
            ['python', CLIENT_FILE_FULL_PATH, f'--port={free_port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout = run.stdout.decode('utf-8')
<<<<<<< HEAD

        assert run.returncode == 0
=======
        stderr = run.stderr.decode('utf-8')

        assert run.returncode == 0, stderr
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b

        # check logging works somehow
        assert 'WELCOME' in stdout
        assert 'dummy' in stdout
        assert 'MESSAGE' in stdout
        assert 'PLAY' in stdout
        assert 'NOT VALID' not in stdout
        assert 'PLAYER_VICTORY' in stdout


def test_slow_waiting_for_quit_server(free_port: int) -> None:
    """Simple server, where player can not win and should QUIT on control+c"""
    with run_socket_server(TEST_SERVER_FOLDER / 'slow_waiting_for_quit_server.py', f'--port={free_port}'):
        proc = subprocess.Popen(
            ['python', CLIENT_FILE_FULL_PATH, f'--port={free_port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(0.6)
        proc.send_signal(signal.SIGINT)
        time.sleep(0.6)

        # assert proc.wait()

        stdout = b'\n'.join(proc.stdout.readlines()).decode('utf-8') if proc.stdout else ''

        assert proc.returncode != 0

        # check logging works somehow
        assert 'WELCOME' in stdout
        assert 'PLAY' in stdout
        assert 'QUIT' in stdout


# @pytest.mark.parametrize('game_server_memory', [10, 100, 1000, 5000])
# def test_custom_server(game_server_memory: int, free_port: int) -> None:
#     with run_socket_server(
#             TASK_FOLDER / 'server.py', f'--game-server-memory={game_server_memory}', f'--port={free_port}'
#     ):
#         run = subprocess.run(
#             ['python', CLIENT_FILE_FULL_PATH, f'--port={free_port}'],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#         )
#         stdout = run.stdout.decode('utf-8')
<<<<<<< HEAD
#
#         assert run.returncode == 0
=======
#         stderr = run.stderr.decode('utf-8')
#
#         assert run.returncode == 0, stderr
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
#
#         # check logging works somehow
#         assert 'WELCOME' in stdout
#         assert 'PLAY' in stdout
#         assert 'PLAYER_VICTORY' in stdout
