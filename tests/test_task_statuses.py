from models.task import ALLOWED_STATUSES, BOARD_STATUSES, STATUS_BACKLOG


def test_backlog_status_is_allowed() -> None:
    assert STATUS_BACKLOG in ALLOWED_STATUSES


def test_board_statuses_are_subset_of_allowed_statuses() -> None:
    assert set(BOARD_STATUSES).issubset(set(ALLOWED_STATUSES))
