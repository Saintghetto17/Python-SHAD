from pathlib import Path
<<<<<<< HEAD
import re
import requests
from bs4 import BeautifulSoup, PageElement
=======

>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b

# Directory to save your .json files to
# NB: create this directory if it doesn't exist
SAVED_JSON_DIR = Path(__file__).parent / 'visited_paths'
<<<<<<< HEAD
bad_tags: list[str] = ['<br/>']


def delete_bad_tags(soup: BeautifulSoup) -> None:
    table_tags = soup.find_all('table')
    for table in table_tags:
        table.extract()


def recursive_distance(source_url: str, target_url: str, distance: int, global_set_ref: set[str]) -> int | None:
    print(source_url)
    response = requests.get(source_url)
    soup = BeautifulSoup(response.text)
    delete_bad_tags(soup)
    assumed_paragraphs = soup.find_all('p')
    good_first_paragraph: PageElement = assumed_paragraphs[0]
    flag_first: bool = False
    for elem in assumed_paragraphs:
        if elem.text == '':
            continue
        for bad_tag in bad_tags:
            if bad_tag in str(elem):
                break
            if bad_tag == '<br/>':
                good_first_paragraph = elem
                flag_first = True
        if flag_first:
            break
    indices_object = re.finditer(pattern='href="/wiki', string=str(good_first_paragraph))
    indices_start = [index.start() for index in indices_object]
    refs: list[str] = []
    for index in indices_start:
        count_symbol = 0
        index_end: int = index
        while True:
            if str(good_first_paragraph)[index_end] == '"':
                count_symbol += 1
            index_end += 1
            if count_symbol == 2:
                count_symbol = 0
                break
        refs.append(str(good_first_paragraph)[index + 5:index_end])

    for ref in refs:
        if "#cite_note" in ref or ".ogg" in ref:
            continue
        if ref in global_set_ref:
            continue
        global_set_ref.add(ref)
        if 'https://ru.wikipedia.org' + ref[1:len(ref) - 1] == target_url:
            return distance + 1
        ans_cur_ref_distance: int | None = recursive_distance('https://ru.wikipedia.org' + ref[1:len(ref) - 1],
                                                              target_url, distance + 1, global_set_ref)
        if ans_cur_ref_distance is not None:
            return ans_cur_ref_distance
    return None
=======
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b


def distance(source_url: str, target_url: str) -> int | None:
    """Amount of wiki articles which should be visited to reach the target one
    starting from the source url. Assuming that the next article is choosing
    always as the very first link from the first article paragraph (tag <p>).
    If the article does not have any paragraph tags or any links in the first
    paragraph then the target is considered unreachable and None is returned.
    If the next link is pointing to the already visited article, it should be
    discarded in favor of the second link from this paragraph. And so on
    until the first not visited link will be found or no links left in paragraph.
    NB. The distance between neighbour articles (one is pointing out to the other)
    assumed to be equal to 1.
    :param source_url: the url of source article from wiki
    :param target_url: the url of target article from wiki
    :return: the distance calculated as described above
    """
<<<<<<< HEAD
    dist: int = 0
    global_set_ref: set[str] = set()
    result = recursive_distance(source_url, target_url, dist, global_set_ref)
    return result
=======
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
