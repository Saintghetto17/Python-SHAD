import typing as tp
from decimal import Decimal

import pytest
from sqlalchemy import select

from splitvise.models.base import Session
from splitvise.models import User
from splitvise.core import create_user, create_trip, add_user_to_trip, get_trip_users, create_event, make_summary
from splitvise.exceptions import SplitViseException


def _make_money(dct: tp.Mapping[int, int | float]) -> dict[int, Decimal]:
    return {key: Decimal(value) for key, value in dct.items()}


def _to_user_id(dct: tp.Mapping[str, tp.Any],
                username_to_id: tp.Mapping[str | None, int]) -> dict[int, tp.Any]:
    return {username_to_id[key]: value for key, value in dct.items()}


def _count_rows_in_table(table_name: str) -> int:
    """Note: Your should NOT use this way in ORM. Test purpose ONLY!"""
    with Session.begin() as session:
        cursor = session.connection().connection.cursor()
        return cursor.execute(f'''
            SELECT COUNT(*) FROM {table_name}
        ''').fetchone()[0]


DEFAULT_USERNAMES = ['a1', 'b2', 'c3', 'd4', 'e5']


def _create_default_users() -> dict[str | None, int]:
    with Session.begin() as session:
        users = [User(username=username) for username in DEFAULT_USERNAMES]
        session.add_all(users)
        session.flush()
        default_users_to_id: dict[str | None, int] = {str(u.username): int(u.user_id) for u in users}
        default_users_to_id[None] = 9999

    return default_users_to_id


@pytest.mark.usefixtures('clear_session')
class TestUsers:
    @pytest.mark.parametrize('usernames', [
        ['a', 'b', 'c'],
        ['aa', 'bb', 'cc', 'dd'],
        ['a1', 'b2'],
    ])
    def test_create_user(self, usernames: list[str], clear_session: Session) -> None:
        assert _count_rows_in_table('users') == 0

        for username in usernames:
            create_user(username, session=clear_session)

        with pytest.raises(SplitViseException):
            create_user(usernames[0], session=clear_session)

        assert _count_rows_in_table('users') == len(usernames)

        users = clear_session.execute(select(User)).scalars().all()
        users_usernames = [str(u.username) for u in users]
        assert set(users_usernames) == set(usernames)


@pytest.mark.usefixtures('clear_session')
class TestTrip:
    @pytest.mark.parametrize('username,title,description', [
        ('a1', 'some title', 'some description'),
        ('a1', 'some title', ''),
        ('b2', 'some title', ''),
        ('b2', 'other title', ''),
    ])
    def test_create_trip_valid(self, username: str, title: str, description: str, clear_session: Session) -> None:
        assert _count_rows_in_table('trips') == 0
        username_to_id = _create_default_users()

        create_trip(username_to_id[username], title, description, session=clear_session)

        assert _count_rows_in_table('trips') == 1

    @pytest.mark.parametrize('username,title,description', [
        ('b2', '', ''),
        (None, 'some title', 'some description'),
    ])
    def test_create_trip_invalid(self, username: str, title: str, description: str, clear_session: Session) -> None:
        assert _count_rows_in_table('trips') == 0
        username_to_id = _create_default_users()

        with pytest.raises(SplitViseException):
            create_trip(username_to_id[username], title, description, session=clear_session)

        assert _count_rows_in_table('trips') == 0

    def test_get_trip_users(self, clear_session: Session) -> None:
        username_to_id = _create_default_users()
        trip = create_trip(username_to_id['a1'], 'title', 'desc', session=clear_session)

        trip_users = get_trip_users(trip.trip_id, session=clear_session)
        assert len(trip_users) == 1

    def test_add_user_to_trip(self, clear_session: Session) -> None:
        username_to_id = _create_default_users()
        trip = create_trip(username_to_id['a1'], 'title', 'desc', session=clear_session)

        add_user_to_trip(username_to_id['b2'], trip.trip_id, session=clear_session)
        add_user_to_trip(username_to_id['c3'], trip.trip_id, session=clear_session)

        trip_users = get_trip_users(trip.trip_id, session=clear_session)
        assert len(trip_users) == 3

        with pytest.raises(SplitViseException):
            add_user_to_trip(username_to_id['c3'], trip.trip_id, session=clear_session)

        trip_users = get_trip_users(trip.trip_id, session=clear_session)
        assert len(trip_users) == 3

        with pytest.raises(SplitViseException):
            add_user_to_trip(username_to_id['d4'], 99999, session=clear_session)

        trip_users = get_trip_users(trip.trip_id, session=clear_session)
        assert len(trip_users) == 3


@pytest.mark.usefixtures('clear_session')
class TestEvent:
    @pytest.mark.parametrize('usernames,payments,debts', [
        (['a1'], {'a1': 100}, {'a1': 100}),
        (['a1', 'b2'], {'a1': 100}, {'a1': 100}),
        (['a1', 'b2'], {'a1': 100}, {'b2': 100}),
        (['a1', 'b2'], {'a1': 100}, {'a1': 30, 'b2': 70}),
        (['a1', 'b2', 'c3', 'd4'], {'a1': 100}, {'a1': 30, 'b2': 70}),
        (['a1', 'b2'], {'a1': 50, 'b2': 50}, {'a1': 100}),
        (['a1', 'b2'], {'a1': 50, 'b2': 50}, {'a1': 40, 'b2': 60}),
        (['a1', 'b2', 'c3'], {'a1': 50, 'b2': 50}, {'a1': 40, 'c3': 60}),
        (['a1', 'b2', 'c3'], {'a1': 60, 'b2': 30, 'c3': 10}, {'a1': 100}),
    ])
    def test_create_event_valid(self, usernames: list[str], payments: dict[str, float], debts: dict[str, float],
                                clear_session: Session) -> None:
        username_to_id = _create_default_users()

        assert _count_rows_in_table('events') == 0

        trip = create_trip(username_to_id[usernames[0]], 'trip', 'description', session=clear_session)

        for username in usernames[1:]:
            add_user_to_trip(username_to_id[username], trip.trip_id, session=clear_session)

        debts_ids = {username_to_id[k]: v for k, v in debts.items()}
        payments_ids = {username_to_id[k]: v for k, v in payments.items()}
        event = create_event(
            trip.trip_id,
            _make_money(debts_ids),
            _make_money(payments_ids),
            'event title',
            session=clear_session
        )
        assert not event.settled_up

        assert _count_rows_in_table('events') == 1
        assert _count_rows_in_table('expenses') == len(payments)
        assert _count_rows_in_table('debts') == len(debts)

    def test_create_event_invalid_trip(self, clear_session: Session) -> None:
        username_to_id = _create_default_users()

        assert _count_rows_in_table('events') == 0

        create_trip(username_to_id['a1'], 'trip', 'description', session=clear_session)

        with pytest.raises(SplitViseException):
            create_event(9999, {}, {}, 'event title', session=clear_session)

        assert _count_rows_in_table('events') == 0
        assert _count_rows_in_table('expenses') == 0
        assert _count_rows_in_table('debts') == 0

    @pytest.mark.parametrize('usernames,payments,debts', [
        (['a1'], {'a1': 100}, {'a1': 200}),
        (['a1'], {'a1': 100}, {'c3': 200}),
        (['a1'], {'a1': 100}, {None: 200}),
        (['a1', 'b2'], {'a1': 100}, {'c3': 100}),
        (['a1', 'b2'], {'c3': 100}, {'a1': 100}),
        (['a1', 'b2'], {'a1': 100}, {'b2': 200}),
        (['a1', 'b2'], {'a1': 100}, {'a1': 70, 'b2': 70}),
        (['a1', 'b2', 'c3', 'd4'], {'a1': 100}, {}),
        (['a1', 'b2', 'c3', 'd4'], {}, {'a1': 100}),
    ])
    def test_create_event_invalid(self, usernames: list[str], payments: dict[str, float], debts: dict[str, float],
                                  clear_session: Session) -> None:
        username_to_id = _create_default_users()

        assert _count_rows_in_table('events') == 0

        trip = create_trip(username_to_id[usernames[0]], 'trip', 'description', session=clear_session)

        for username in usernames[1:]:
            add_user_to_trip(username_to_id[username], trip.trip_id, session=clear_session)

        debts_ids = {username_to_id[k]: v for k, v in debts.items()}
        payments_ids = {username_to_id[k]: v for k, v in payments.items()}
        with pytest.raises(SplitViseException):
            create_event(
                trip.trip_id,
                _make_money(debts_ids),
                _make_money(payments_ids),
                'event title',
                session=clear_session
            )

        assert _count_rows_in_table('events') == 0
        assert _count_rows_in_table('expenses') == 0
        assert _count_rows_in_table('debts') == 0


@pytest.mark.usefixtures('clear_session')
class TestSummary:
    @pytest.mark.parametrize('debts,payments', [
        ({'a1': 100}, {'b2': 100}),
        ({'a1': 60, 'b2': 30, 'c3': 10}, {'a1': 100}),
        ({'a1': 100}, {'a1': 99, 'b2': 1}),
        ({'a1': 44, 'b2': 0.5, 'c3': 11}, {'a1': 55.5}),
    ])
    def test_create_summary_single_event(
            self, clear_session: Session, debts: dict[str, float], payments: dict[str, float]
    ) -> None:
        username_to_id = _create_default_users()

        trip = create_trip(username_to_id['a1'], 'trip', 'description', session=clear_session)
        add_user_to_trip(username_to_id['b2'], trip.trip_id, session=clear_session)
        add_user_to_trip(username_to_id['c3'], trip.trip_id, session=clear_session)

        event = create_event(
            trip.trip_id,
            _make_money(_to_user_id(debts, username_to_id)),
            _make_money(_to_user_id(payments, username_to_id)),
            'event title',
            session=clear_session
        )

        make_summary(trip.trip_id, session=clear_session)

        assert 0 < _count_rows_in_table('summaries') <= len(debts | payments)
        assert event.settled_up, 'Dont forget to mark events as counted'

    @pytest.mark.parametrize('debts_payments_pairs', [
        [({'a1': 100}, {'b2': 100}), ({'a1': 60, 'b2': 30, 'c3': 10}, {'a1': 100})],
        [({'a1': 100}, {'a1': 99, 'b2': 1}), ({'a1': 44, 'b2': 0.5, 'c3': 11}, {'a1': 55.5})],
        [({'a1': 100}, {'a1': 29.5, 'b2': 20.5, 'c3': 50}), ({'a1': 94.5, 'b2': 0.5, 'c3': 5}, {'a1': 100})],
    ])
    def test_create_summary_multiple_events(
            self, clear_session: Session, debts_payments_pairs: list[tuple[dict[str, float], dict[str, float]]]
    ) -> None:
        username_to_id = _create_default_users()

        trip = create_trip(username_to_id['a1'], 'trip', 'description', session=clear_session)
        add_user_to_trip(username_to_id['b2'], trip.trip_id, session=clear_session)
        add_user_to_trip(username_to_id['c3'], trip.trip_id, session=clear_session)

        usernames: set[str] = set()
        for debts, payments in debts_payments_pairs:
            usernames.update(debts.keys())
            usernames.update(payments.keys())
            create_event(
                trip.trip_id,
                _make_money(_to_user_id(debts, username_to_id)),
                _make_money(_to_user_id(payments, username_to_id)),
                'event title',
                session=clear_session
            )

        make_summary(trip.trip_id, session=clear_session)

        assert 0 < _count_rows_in_table('summaries') < len(usernames)

        # Note: Your should NOT use this way in ORM. Test purpose ONLY!
        cursor = clear_session.connection().connection.cursor()
        summarised = cursor.execute('''
            SELECT user_id, summary_incomes, events_incomes FROM
            (
                SELECT user_id, SUM(income) as events_incomes FROM
                (
                    SELECT debtor_id as user_id, -SUM(value) as income FROM debts
                    GROUP BY debtor_id
                    UNION ALL
                    SELECT payer_id as user_id, SUM(value) as income FROM expenses
                    GROUP BY payer_id
                )
                GROUP BY user_id
            )
            LEFT JOIN
            (
                SELECT user_id, SUM(incomes) as summary_incomes FROM
                (
                    SELECT user_from_id as user_id, SUM(value) as incomes FROM summaries
                    GROUP BY user_from_id
                    UNION ALL
                    SELECT user_to_id as user_id, -SUM(value) as incomes FROM summaries
                    GROUP BY user_to_id
                )
                GROUP BY user_id
            ) as summ
            USING (user_id)
        ''').fetchall()
        for user_id, from_events, from_summary in summarised:
            assert from_events == from_summary, f'Incorrect sum for user {user_id}'
