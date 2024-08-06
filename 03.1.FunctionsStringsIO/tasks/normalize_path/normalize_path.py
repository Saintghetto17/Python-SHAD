from collections import deque


def normalize_path(path: str) -> str:
    """
    :param path: unix path to normalize
    :return: normalized path
    """
    if len(path) == 0:
        return '.'
    deque_slash: deque[str] = deque(path.split('/'))
    length = len(deque_slash)
    stack: deque[str] = deque()
    two_dots = '..'
    one_dot = '.'
    empty = ''
    length_stack = 0
    while length != 0:
        token = deque_slash.popleft()
        length = length - 1
        if token == empty:
            continue
        elif token == one_dot:
            continue
        elif token == two_dots:
            if length_stack == 0:
                if path[0] == '/':
                    continue
                stack.append(token)
                length_stack = length_stack + 1
                continue

            elif stack[length_stack - 1] != two_dots:
                stack.pop()
                length_stack = length_stack - 1
                continue
            stack.append(token)
            length_stack = length_stack + 1
        else:
            stack.append(token)
            length_stack = length_stack + 1
    if path[0] == '/':
        stack.appendleft('/')
        to_list = list(stack)
        if length_stack == 0:
            return ''.join(to_list)
        string = '/'.join(stack)
        res_string = string.replace('/', '', 1)
        return res_string
    to_list = list(stack)
    if length_stack == 0:
        return '.'
    return '/'.join(to_list)
