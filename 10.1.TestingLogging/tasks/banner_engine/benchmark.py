import random

from banner_engine import (
    BannerStorage, Banner, EpsilonGreedyBannerEngine
)

N_TRIALS = 100000

if __name__ == "__main__":
    banners = [
        Banner("b1", cost=1),
        Banner("b2", cost=25),
        Banner("b3", cost=100),
        Banner("b4", cost=1000),
    ]

    # Ground truth click probabilities
    banner_click_probas = {
        "b1": 0.13,
        "b2": 0.2,
        "b3": 0.01,
        "b4": 0.01
    }

    storage = BannerStorage(banners)
    engine = EpsilonGreedyBannerEngine(storage, random_banner_probability=0.1)

    for _ in range(N_TRIALS):
        banner_id = engine.show_banner()
        if random.random() < banner_click_probas[banner_id]:  # simulate user click
            engine.send_click(banner_id)

    print("Total money earned: ", engine.total_cost)

    best_banner = banners[0]

    def banner_value(b: Banner) -> float:
        return banner_click_probas[b.banner_id] * b.cost

    for banner in banners:
        if banner_value(banner) > banner_value(best_banner):
            best_banner = banner

    print("Banner statistics:")
    storage.print_stats()
    print("Maximum expected money", N_TRIALS * banner_value(best_banner))
