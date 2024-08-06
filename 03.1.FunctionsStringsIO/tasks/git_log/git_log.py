import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from `inp` stream, reformats it and prints to `out` stream

    Expected input format: `<sha-1>\t<date>\t<author>\t<email>\t<message>`
    Output format: `<first 7 symbols of sha-1>.....<message>`
    """

    string = inp.readline()
    while string:
        lst_str: list[str] = string.split('\t')
        sha = lst_str[0]
        sha_prefix = sha[:7]
        log_suffix = lst_str[4]
        print(log_suffix)
        left_len = 80 - len(log_suffix) - len(sha_prefix) + 1
        dots: list[str] = []
        for i in range(left_len):
            dots.append('.')
        dot_str = ''.join(dots)
        out.write("{}{}{}".format(sha_prefix, dot_str, log_suffix))
        string = inp.readline()
