import heapq
import string
from collections import defaultdict
from collections import Counter
from collections import deque


def normalize(
        text: str
) -> str:
    """
    Removes punctuation and digits and convert to lower case
    :param text: text to normalize
    :return: normalized query
    """
    # object.translate(table), where table is mapping what and how to delete.
    # str.maketrans(from, to, delete) - what to what and what to delete
    res = text.translate(str.maketrans('', '', string.punctuation))
    res = res.translate(str.maketrans('', '', string.digits))
    return res.lower()


def get_words(
        query: str
) -> list[str]:
    """
    Split by words and leave only words with letters greater than 3
    :param query: query to split
    :return: filtered and split query by words
    """
    query = normalize(query)
    return [s for s in query.split() if len(s) > 3]


def build_index(
        banners: list[str]
) -> dict[str, list[int]]:
    """
    Create index from words to banners ids with preserving order and without repetitions
    :param banners: list of banners for indexation
    :return: mapping from word to banners ids
    """
    index = 0
    def_dic: defaultdict[str, list[int]] = defaultdict(list)
    unique_items: set[str] = {''}
    for ban in banners:
        for word in get_words(normalize(ban)):
            if word not in unique_items:
                def_dic[word].append(index)
                unique_items.add(word)
        index = index + 1
        unique_items.clear()
    return dict(def_dic)


def get_banner_indices_by_query(
        query: str,
        index: dict[str, list[int]]
) -> list[int]:
    """
    Extract banners indices from index, if all words from query contains in indexed banner
    :param query: query to find banners
    :param index: index to search banners
    :return: list of indices of suitable banners
    """

    str_normalized = normalize(query)
    lst_words: list[str] = get_words(str_normalized)
    set_words: set[str] = set(lst_words)
    heap: list[deque[int]] = []
    sum = 0
    res: list[int] = []
    res_banners: list[int] = []
    for word in index.keys():
        if word not in set_words:
            continue
        sum = sum + len(index[word])
        deq: deque[int] = deque(index[word])
        heapq.heappush(heap, deq)
    set_len = len(set_words)
    for i in range(sum):
        deq_new: deque[int] = heapq.heappop(heap)
        if len(deq_new) == 0:
            break
        val = deque.popleft(deq_new)
        res.append(val)
        if len(deq_new) == 0:
            continue
        heapq.heappush(heap, deq_new)
    res_dict: dict[int, int] = dict(Counter(res))
    for key in res_dict.keys():
        if res_dict[key] == set_len:
            res_banners.append(key)
    return res_banners


#########################
# Don't change this code
#########################
def get_banners(
        query: str,
        index: dict[str, list[int]],
        banners: list[str]
) -> list[str]:
    """
    Extract banners matched to queries
    :param query: query to match
    :param index: word-banner_ids index
    :param banners: list of banners
    :return: list of matched banners
    """
    indices = get_banner_indices_by_query(query, index)
    return [banners[i] for i in indices]

#########################
