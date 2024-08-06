import enum


class Status(enum.Enum):
    NEW = 0
    EXTRACTED = 1
    FINISHED = 2


def dfs(v: str, ans: list[str], mark: dict[str, Status], graph: dict[str, set[str]]) -> None:
    mark[v] = Status.EXTRACTED
    for u in graph[v]:
        if mark[u] is not Status.EXTRACTED:
            dfs(u, ans, mark, graph)
    ans.append(v)


def extract_alphabet(
        graph: dict[str, set[str]]
) -> list[str]:
    # TopSort
    """
    Extract alphabet from graph
    :param graph: graph with partial order
    :return: alphabet
    """
    ans_to_reverse: list[str] = []
    mark: dict[str, Status] = {}
    # default value -> not_visited
    for key in graph.keys():
        mark[key] = Status.NEW
    for v in graph.keys():
        if mark[v] is not Status.EXTRACTED:
            dfs(v, ans_to_reverse, mark, graph)
    ans_to_reverse.reverse()
    return ans_to_reverse


def build_graph(
        words: list[str]
) -> dict[str, set[str]]:
    """
    Build graph from ordered words. Graph should contain all letters from words
    :param words: ordered words
    :return: graph
    """
    res_dict: dict[str, set[str]] = {}
    set_letters: set[str] = set()
    for e in words:
        # O(K) where K is the largest str length in given list
        for i in range(len(e)):
            alpha_letter = e[i]
            if alpha_letter in set_letters:
                continue
            else:
                set_letters.add(alpha_letter)
                res_dict[alpha_letter] = set()
    # O(n * K) K - const -> O(n)
    prev_len = -1
    prev_str = ''
    for e in words:
        if prev_len == -1:
            prev_len = len(e)
            prev_str = e
            continue
        else:
            for i in range(min(prev_len, len(e))):
                if e[i] is prev_str[i] or e[i] == prev_str[i]:
                    continue
                else:
                    res_dict[prev_str[i]].add(e[i])
                    prev_str = e
                    prev_len = len(e)
                    break
            prev_str = e
            prev_len = len(e)
    return res_dict


#########################
# Don't change this code
#########################

def get_alphabet(
        words: list[str]
) -> list[str]:
    """
    Extract alphabet from sorted words
    :param words: sorted words
    :return: alphabet
    """
    graph = build_graph(words)
    return extract_alphabet(graph)

#########################
