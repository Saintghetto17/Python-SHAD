from pathlib import Path
import socketserver
import threading
import random


FILE_DIR = Path(__file__).parent
random.seed(42)


class ThreadedTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class GameHandler(socketserver.StreamRequestHandler):
    def _send(self, message: str) -> None:
        self.wfile.write(f'{message}\n'.encode('utf-8'))

    def setup(self) -> None:
        super(GameHandler, self).setup()

        self._send('WELCOME')
        self._send(f'PLAY {self.last_server_word}')

    def handle(self) -> None:
        client = f'{self.client_address} on {threading.current_thread().name}'
        print(f'Connected: {client}')
        try:
            while True:
                command = self.rfile.readline().decode('utf-8').rstrip()
                self._send('PLAYER_VICTORY')
        except Exception as e:
            print('Exception', e)
        print(f'Closed: {client}')

    def finish(self) -> None:
        self._send('MESSAGE Thank you for the game!')


if __name__ == '__main__':
    with ThreadedTCPServer(('localhost', 59898), GameHandler) as server:
        print('The game server is running...')
        server.serve_forever()
