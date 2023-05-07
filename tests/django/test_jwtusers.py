from unittest.mock import MagicMock, patch
import pytest
from azjwt.django import _auth_backend
from azjwt.django import _conf as conf
from azjwt.django._auth_backend import JwtUsers


class TestJwtUsers:
    def test_should_be_able_to_get_instance(self):
        users = JwtUsers.get_instance()
        assert isinstance(users, JwtUsers)

    def test_should_allow_create_missing_when_missinguseraction_config_setting_is_create(
        self,
        users: JwtUsers,
        conf_missing_user_action_is_create,
    ):
        assert users.create_missing

    def test_should_not_allow_create_missing_when_missinguseraction_config_setting_is_ignore(
        self,
        users: JwtUsers,
        conf_missing_user_action_is_ignore,
    ):
        assert not users.create_missing

    def test_should_get_existing_user_from_user_model(
        self,
        users: JwtUsers,
        get_user_model_patch,
    ):
        claims = MagicMock()
        user = users.get_for_claims(claims)
        get_user_model_patch.assert_called_once_with()
        get_mock = get_user_model_patch.return_value.objects.get
        get_mock.assert_called_once_with(username=claims.username)
        assert user is get_mock.return_value

    def test_should_create_missing_user_when_allowed(
        self,
        users: JwtUsers,
        user_does_not_exist,
        conf_missing_user_action_is_create,
        create_for_claims_patch,
    ):
        result = users.get_for_claims("claims")
        create_for_claims_patch.assert_called_once_with("claims")
        assert result is create_for_claims_patch.return_value

    def test_should_get_none_for_missing_user_when_create_missing_user_not_allowed(
        self,
        users: JwtUsers,
        user_does_not_exist,
        conf_missing_user_action_is_ignore,
        create_for_claims_patch,
    ):
        result = users.get_for_claims("claims")
        create_for_claims_patch.assert_not_called()
        assert result is None


@pytest.fixture(name="users")
def given_users() -> JwtUsers:
    return JwtUsers()


@pytest.fixture(name="conf_missing_user_action_is_create")
def given_missing_user_action_is_create():
    with patch.object(
        _auth_backend.conf, "MISSING_USER_ACTION", conf.MissingUserAction.CREATE
    ):
        yield _auth_backend.conf.MISSING_USER_ACTION


@pytest.fixture(name="conf_missing_user_action_is_ignore")
def given_missing_user_action_is_ignore():
    with patch.object(
        _auth_backend.conf, "MISSING_USER_ACTION", conf.MissingUserAction.IGNORE
    ):
        yield _auth_backend.conf.MISSING_USER_ACTION


@pytest.fixture(name="get_user_model_patch")
def given_get_user_model_patch():
    with patch.object(_auth_backend, "get_user_model") as func_mock:
        yield func_mock

@pytest.fixture(name="user_does_not_exist")
def given_user_does_not_exist(get_user_model_patch):
    model = get_user_model_patch.return_value
    model.DoesNotExist = Exception
    exception = model.DoesNotExist
    model.objects.get.side_effect = exception
    return get_user_model_patch

@pytest.fixture(name="create_for_claims_patch")
def given_create_for_claims_patch(users):
    with patch.object(users, "create_for_claims") as func_mock:
        yield func_mock
