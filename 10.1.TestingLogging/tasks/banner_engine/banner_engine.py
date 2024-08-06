import random
import typing


class NoBannerError(Exception):
    pass


class EmptyBannerStorageError(Exception):
<<<<<<< HEAD
    def __init__(self, message: str = "BannerStorage should not be empty") -> None:
        self.message = message
        super().__init__(message)
=======
    pass
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b


class BannerStat:
    def __init__(self, clicks: int, shows: int):
        self._clicks = clicks
        self._shows = shows

    def add_click(self) -> None:
        self._clicks += 1

    def add_show(self) -> None:
<<<<<<< HEAD
        self._shows += 1
=======
        self._clicks += 1
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b

    @property
    def clicks(self) -> int:
        return self._clicks

    @property
    def shows(self) -> int:
        return self._shows

    def compute_ctr(self, default_ctr: float) -> float:
        """
        Compute banner CTR (click through rate) as clicks / shows
        If banner has zero shows - return `default_ctr`
        """
        if self.shows == 0:
            return default_ctr
        else:
<<<<<<< HEAD
            return self._clicks / self._shows
=======
            return self.shows / self.clicks
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b


class Banner:
    def __init__(self, banner_id: str, cost: int, stat: BannerStat | None = None):
        self._banner_id = banner_id
        self._cost = cost
        self._stat = stat if stat is not None else BannerStat(0, 0)

    @property
    def banner_id(self) -> str:
        return self._banner_id

    @property
    def cost(self) -> int:
        return self._cost

    @property
    def stat(self) -> BannerStat:
        return self._stat


class BannerStorage:
    def __init__(self, banners: typing.Iterable[Banner], default_ctr: float = 0.1):
<<<<<<< HEAD
        # ID -> BANNER
        self._banner_dict = {b.banner_id: b for b in banners}
        # [ID1, ID2, ..., ]
=======
        self._banner_dict = {b.banner_id: b for b in banners}
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
        self._banner_id_list = [b.banner_id for b in banners]
        self._default_ctr = default_ctr

    def is_empty(self) -> bool:
        return len(self._banner_dict) == 0

    def add_click(self, banner_id: str) -> None:
        self._banner_dict[banner_id].stat.add_click()

    def add_show(self, banner_id: str) -> None:
        if banner_id not in self._banner_dict:
            raise NoBannerError("Unknown banner {}!".format(banner_id))

        self._banner_dict[banner_id].stat.add_show()

    def get_banner(self, banner_id: str) -> Banner:
        if banner_id not in self._banner_dict:
            raise NoBannerError("Unknown banner {}!".format(banner_id))

        return self._banner_dict[banner_id]

    def banner_with_highest_cpc(self) -> Banner:
        """
        :return: banner with highest CPC(cost per click = cost * CTR))
        """

        if self.is_empty():
            raise NoBannerError("Storage is empty!")

        selected_banner = self._banner_dict[self._banner_id_list[0]]
        selected_cpc = selected_banner.stat.compute_ctr(self._default_ctr) * selected_banner.cost

        for banner_id in self._banner_id_list:
            current_banner = self._banner_dict[banner_id]
            current_cpc = current_banner.stat.compute_ctr(self._default_ctr) * current_banner.cost
            if current_cpc > selected_cpc:
                selected_cpc = current_cpc
                selected_banner = current_banner

        return selected_banner

    def random_banner(self) -> Banner:
        if self.is_empty():
            raise NoBannerError("Storage is empty!")

        return self._banner_dict[random.choice(self._banner_id_list)]

    def print_stats(self) -> None:
        for b in self._banner_dict.values():
            print("Id:", b.banner_id, "Cost", b.cost, "Shows", b.stat.shows, "Clicks", b.stat.clicks)


class EpsilonGreedyBannerEngine:
    """
    Banner engine that with 1 - epsilon probability shows banner with highest CPC (cost per click = cost * CTR)
    With epsilon probability shows random banner to gather more stats
    """
<<<<<<< HEAD

=======
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
    def __init__(self, banner_storage: BannerStorage, random_banner_probability: float):
        """
        :param banner_storage: None empty banner storage
        :param random_banner_probability: 1.0 - every show is random. 0.0 - every show is greedy
        """
<<<<<<< HEAD
        if banner_storage.is_empty():
            raise EmptyBannerStorageError("Banner should not be empty")
        # 1 - eps is the final probability
=======
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
        self._epsilon = random_banner_probability
        self._storage = banner_storage

        self._show_count = 0
        self._total_cost = 0

    def show_banner(self) -> str:
        """
        Engine is asked to show banner.
        Engine selects banner with epsilon-greedy algorithms and updates banner show statistics.
        """
<<<<<<< HEAD
        # С ВЕРОЯТНОСТЬЮ EPS = ЕСЛИ EPS >= ВОЗМОЖНОЙ ВЕРОЯТНОСТИ, ИНАЧЕ ПОПАДАЕМ В 1 - EPS
        if random.random() < self._epsilon:
=======
        if random.random() > self._epsilon:
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
            selected_banner = self._storage.random_banner()
        else:
            selected_banner = self._storage.banner_with_highest_cpc()

        self._storage.add_show(selected_banner.banner_id)
        self._show_count += 1

        return selected_banner.banner_id

    def send_click(self, banner_id: str) -> None:
        """
        Web page sends user click conformation for `banner_id` and engine must update banner click statistics
        Important! Web page can send incorrect `banner_id`. Engine must not fail in that case!
        """
        try:
            self._storage.add_show(banner_id)
<<<<<<< HEAD
            self._storage.add_click(banner_id)
            self._total_cost += self._storage.get_banner(banner_id).cost
=======
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
        except NoBannerError:
            pass

    @property
    def shown_count(self) -> int:
        """
        :return: Total shows since start
        """
        return self._show_count

    @property
    def total_cost(self) -> int:
        """
        :return: Total earned money since start
        """
        return self._total_cost
