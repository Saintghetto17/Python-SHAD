import typing

import pytest

from .banner_engine import (
<<<<<<< HEAD
    BannerStat, Banner, BannerStorage, EmptyBannerStorageError, EpsilonGreedyBannerEngine, NoBannerError
=======
    BannerStat, Banner
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
)

TEST_DEFAULT_CTR = 0.1


@pytest.fixture(scope="function")
def test_banners() -> list[Banner]:
    return [
        Banner("b1", cost=1, stat=BannerStat(10, 20)),
        Banner("b2", cost=250, stat=BannerStat(20, 20)),
        Banner("b3", cost=100, stat=BannerStat(0, 20)),
        Banner("b4", cost=100, stat=BannerStat(1, 20)),
    ]


@pytest.mark.parametrize("clicks, shows, expected_ctr", [(1, 1, 1.0), (20, 100, 0.2), (5, 100, 0.05)])
def test_banner_stat_ctr_value(clicks: int, shows: int, expected_ctr: float) -> None:
<<<<<<< HEAD
    assert BannerStat(clicks, shows).compute_ctr(TEST_DEFAULT_CTR) == pytest.approx(expected_ctr)


def test_empty_stat_compute_ctr_returns_default_ctr() -> None:
    assert BannerStat(1, 0).compute_ctr(TEST_DEFAULT_CTR) == TEST_DEFAULT_CTR


def test_banner_stat_add_show_lowers_ctr() -> None:
    banner_test: BannerStat = BannerStat(1, 1)
    banner_test.add_show()
    assert banner_test.shows == 2


def test_banner_stat_add_click_increases_ctr() -> None:
    clicks: int = 1
    banner_test: BannerStat = BannerStat(clicks, 1)
    banner_test.add_click()
    assert banner_test.clicks == clicks + 1


def test_get_banner_with_highest_cpc_returns_banner_with_highest_cpc(test_banners: list[Banner]) -> None:
    banner_storage_test: BannerStorage = BannerStorage(test_banners)
    assert banner_storage_test.banner_with_highest_cpc() == test_banners[1]


def test_banner_engine_raise_empty_storage_exception_if_constructed_with_empty_storage() -> None:
    with pytest.raises(EmptyBannerStorageError):
        EpsilonGreedyBannerEngine(BannerStorage([]), 0.05)


def test_engine_send_click_not_fails_on_unknown_banner(test_banners: list[Banner]) -> None:
    test_engine: EpsilonGreedyBannerEngine = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0.05)
    try:
        test_engine.send_click("a1")
    except NoBannerError:
        assert False


def test_engine_with_zero_random_probability_shows_banner_with_highest_cpc(test_banners: list[Banner]) -> None:
    test_engine: EpsilonGreedyBannerEngine = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0)
    assert test_engine.show_banner() == BannerStorage(test_banners).banner_with_highest_cpc().banner_id


# Тестируется рандом без рандома засчет monkeypatch. Что мы делаем? Подменяем метод random_banner внутри метода
# show banner при помощи monkeypatch и возвращаем
# не что-то рандомное, а что-то конкретное, делая проверку.
# Это позволяет проверить
# заходим мы в функцию или нет
=======
    pass


def test_empty_stat_compute_ctr_returns_default_ctr() -> None:
    pass


def test_banner_stat_add_show_lowers_ctr() -> None:
    pass


def test_banner_stat_add_click_increases_ctr() -> None:
    pass


def test_get_banner_with_highest_cpc_returns_banner_with_highest_cpc(test_banners: list[Banner]) -> None:
    pass


def test_banner_engine_raise_empty_storage_exception_if_constructed_with_empty_storage() -> None:
    pass


def test_engine_send_click_not_fails_on_unknown_banner(test_banners: list[Banner]) -> None:
    pass


def test_engine_with_zero_random_probability_shows_banner_with_highest_cpc(test_banners: list[Banner]) -> None:
    pass


>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
@pytest.mark.parametrize("expected_random_banner", ["b1", "b2", "b3", "b4"])
def test_engine_with_1_random_banner_probability_gets_random_banner(
        expected_random_banner: str,
        test_banners: list[Banner],
        monkeypatch: typing.Any
<<<<<<< HEAD
) -> None:
    test_banner_engine: EpsilonGreedyBannerEngine = EpsilonGreedyBannerEngine(BannerStorage(test_banners, 1.0), 1.0)

    def expected_banner(*args: BannerStorage, **kwargs: BannerStorage) -> Banner:
        return Banner(expected_random_banner, cost=100, stat=BannerStat(1, 20))

    monkeypatch.setattr(BannerStorage, "random_banner", expected_banner)
    assert expected_random_banner == test_banner_engine.show_banner()


def test_total_cost_equals_to_cost_of_clicked_banners(test_banners: list[Banner]) -> None:
    test_banner_engine: EpsilonGreedyBannerEngine = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0.5)
    sum: int = 0
    for banner in test_banners:
        sum += banner.cost * banner.stat.clicks
        for i in range(banner.stat.clicks):
            test_banner_engine.send_click(banner.banner_id)
    assert test_banner_engine.total_cost == sum


def test_engine_show_increases_banner_show_stat(test_banners: list[Banner]) -> None:
    test_banner_engine: EpsilonGreedyBannerEngine = EpsilonGreedyBannerEngine(
        BannerStorage(test_banners, TEST_DEFAULT_CTR), 0.5)
    dct_id_show: dict[str, int] = dict()
    for banner in test_banners:
        dct_id_show[banner.banner_id] = banner.stat.shows
    id_banner = test_banner_engine.show_banner()
    for banner in test_banners:
        if banner.banner_id == id_banner:
            assert dct_id_show[id_banner] < banner.stat.shows


def test_engine_click_increases_banner_click_stat(test_banners: list[Banner]) -> None:
    test_banner_engine: EpsilonGreedyBannerEngine = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0.5)
    clicks_stat_before: int = 0
    clicks_stat_after: int = 0
    for banner in test_banners:
        if banner.stat.clicks != 0:
            clicks_stat_before = banner.stat.clicks
            test_banner_engine.send_click(banner.banner_id)
            clicks_stat_after = banner.stat.clicks
            break
    assert clicks_stat_before < clicks_stat_after
=======
        ) -> None:
    pass


def test_total_cost_equals_to_cost_of_clicked_banners(test_banners: list[Banner]) -> None:
    pass


def test_engine_show_increases_banner_show_stat(test_banners: list[Banner]) -> None:
    pass


def test_engine_click_increases_banner_click_stat(test_banners: list[Banner]) -> None:
    pass
>>>>>>> 5b921105b3b183ffd0545c94df6acb72c453398b
