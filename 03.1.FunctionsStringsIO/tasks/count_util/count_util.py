import copy


def count_util(text: str, flags: str | None = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """
    symbols_mapping: dict[str, str] = {'m': 'chars', 'l': 'lines', 'L': 'longest_line', 'w': 'words'}
    dict_base: dict[str, int] = {'lines': 0, 'words': 0, 'chars': 0, 'longest_line': 12}
    txt = copy.copy(text)
    words = len(txt.split())
    dict_base['words'] = words
    lst_lines = txt.split('\n')
    tabulated_tokens = txt.split('\t')
    chars = 0
    for e in tabulated_tokens:
        chars = chars + len(e)
    lines = len(lst_lines) - 1
    max_line = -1
    for e in lst_lines:
        length = len(e)
        if length > max_line:
            max_line = length
    dict_base['lines'] = lines
    dict_base['longest_line'] = max_line
    dict_base['chars'] = chars
    res_dict: dict[str, int] = {}
    if flags is None or flags == '':
        return dict_base
    else:
        for symbol in flags:
            if symbol == 'm' or symbol == 'l' or symbol == 'L' or symbol == 'w':
                res_dict[symbols_mapping[symbol]] = dict_base[symbols_mapping[symbol]]
    return res_dict
