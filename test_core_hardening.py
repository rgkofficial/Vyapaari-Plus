from pathlib import Path

from app.core.security import PBKDF2_ITERATIONS, hash_password, verify_password
from app.db.session import get_db_session


def test_password_hashing_uses_pbkdf2_and_verifies_only_the_original_password():
    password_hash, salt = hash_password("correct horse battery staple")

    assert len(password_hash) == 64
    assert PBKDF2_ITERATIONS >= 600_000
    assert verify_password("correct horse battery staple", password_hash, salt)
    assert not verify_password("wrong password", password_hash, salt)


def test_get_db_session_closes_session_after_context():
    with get_db_session() as session:
        connection = session.connection()
        assert not connection.closed

    assert session.is_active
    assert connection.closed


def test_desktop_logo_references_a_tracked_asset():
    logo = Path(__file__).parents[2] / "assets" / "logo.jpg"
    assert logo.is_file()
