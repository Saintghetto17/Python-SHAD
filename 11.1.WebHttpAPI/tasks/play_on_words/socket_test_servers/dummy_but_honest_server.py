import argparse
import copy
import socketserver
import sys


KNOW_WORDS = {
    'aberdeen', 'abandoned', 'aaron',
    'babes', 'bachelor', 'babies',
    'cabinets', 'cabinet', 'cabin',
    'dairy', 'daddy', 'daily',
    'earlier', 'eagles', 'eagle',
    'fabulous', 'fabric', 'fabrics',
    'gabriel', 'gadgets', 'gained',
    'habits', 'habitat', 'hacker',
    'icons', 'idaho', 'iceland',
    'jackie', 'jackets', 'jacket',
    'karen', 'kansas', 'karaoke',
    'labeled', 'label', 'labels',
    'machine', 'machinery', 'macedonia',
    'nails', 'named', 'naked',
    'obesity', 'oakland', 'oasis',
    'package', 'pacific', 'packages',
    'qatar', 'qualification', 'qualifications',
    'races', 'rabbit', 'rachel',
    'sacrifice', 'sacred', 'sacramento',
    'tablet', 'table', 'tables',
    'uganda', 'ultimate', 'ukraine',
    'vacation', 'vacancies', 'vacations',
    'wagon', 'wages', 'wagner',
    'xhtml', 'xanax', 'xerox',
    'yahoo', 'yamaha', 'yacht',
    'zambia', 'zealand', 'zdnet',
}


class TCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class GameHandler(socketserver.StreamRequestHandler):
    def _send(self, message: str) -> None:
        self.wfile.write(f'{message}\n'.encode('utf-8'))

    def setup(self) -> None:
        super(GameHandler, self).setup()
        self._send('WELCOME')
        self._send('PLAY dummy')
        self._send('MESSAGE Love you, player!')

        self._available_words: set[str] = copy.copy(KNOW_WORDS)
        self._used_words: set[str] = set()

    def handle(self) -> None:
        try:
            while True:
                command = self.rfile.readline().decode('utf-8').rstrip()
                if command.startswith('PLAY'):
                    word = command[5:].lower()

                    if word in self._used_words:
                        self._send('NOT VALID')
                        continue

                    self._used_words.add(word)
                    if word in self._available_words:
                        self._available_words.remove(word)
                    self._send('VALID')
                    self._send('MESSAGE You are cool!')

                    found_word = None
                    for search_word in self._available_words:
                        if search_word[0] == word[-1]:
                            found_word = search_word
                    if found_word:
                        self._available_words.remove(found_word)
                        self._used_words.add(found_word)
                        self._send('MESSAGE He-he, take this!!!')
                        self._send(f'PLAY {found_word}')
                        continue

                    self._send('PLAYER_VICTORY')
                    break
        except Exception as e:
            print('Exception', e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=59898)
    args = parser.parse_args(sys.argv[1:])

    with TCPServer(('localhost', int(args.port)), GameHandler) as server:
        server.serve_forever()
