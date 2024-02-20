from dependency_injector import containers, providers

from app.apis.v1.auth.authentication import Authentication
from app.apis.v1.auth.login.repositories.login_repositories import \
    LoginRepository
from app.apis.v1.auth.login.service.login_service import LoginService


class Container(containers.DeclarativeContainer):
    db = providers.Singleton()
    config = providers.Configuration()
    redis = providers.Resource()
    authentication = providers.Singleton(Authentication)

    wiring_config = containers.WiringConfiguration(packages=["app.apis.v1.auth.login"])

    # Repository
    login_repository = providers.Factory(LoginRepository, session_factory=db.provided.session)

    # Service
    login_service = providers.Factory(
        LoginService, login_repository=login_repository, config=config, authentication=authentication, redis=redis
    )
