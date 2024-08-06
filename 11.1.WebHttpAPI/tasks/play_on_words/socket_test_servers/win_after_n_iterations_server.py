import argparse
import socketserver
import sys

WIN_STEP = 100


class TCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class GameHandler(socketserver.StreamRequestHandler):
    def _send(self, message: str) -> None:
        self.wfile.write(f'{message}\n'.encode('utf-8'))

    def setup(self) -> None:
        super(GameHandler, self).setup()
        self._send('WELCOME')
        self._send('PLAY wait')

        self._n = 0

    def handle(self) -> None:
        try:
            while True:
                command = self.rfile.readline().decode('utf-8').rstrip()
                if command.startswith('PLAY'):
                    word = command[5:].lower()
                    self._send('VALID')
                    self._n += 1

                    if self._n > WIN_STEP:
                        self._send('PLAYER_VICTORY')
                        break

                    self._send(f'PLAY {word[::-1]}')
        except Exception as e:
            print('Exception', e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=59898)
    args = parser.parse_args(sys.argv[1:])

    with TCPServer(('localhost', int(args.port)), GameHandler) as server:
        server.serve_forever()
