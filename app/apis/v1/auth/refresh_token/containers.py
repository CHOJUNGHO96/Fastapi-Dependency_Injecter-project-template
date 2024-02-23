from dependency_injector import containers, providers

from app.apis.v1.auth.authentication import Authentication
from app.apis.v1.auth.refresh_token.repositories.refresh_token_repositories import (
    RefreshTokenRepository,
)
from app.apis.v1.auth.refresh_token.service.refresh_token_service import (
    RefreshTokenService,
)


class Container(containers.DeclarativeContainer):
    db = providers.Singleton()
    config = providers.Configuration()
    redis = providers.Resource()
    authentication = providers.Singleton(Authentication)

    wiring_config = containers.WiringConfiguration(packages=["app.apis.v1.auth.refresh_token"])

    # Repository
    refresh_token_repository = providers.Factory(RefreshTokenRepository, session_factory=db.provided.session)

    # Service
    refresh_token_service = providers.Factory(
        RefreshTokenService,
        refresh_token_repository=refresh_token_repository,
        config=config,
        authentication=authentication,
        redis=redis,
    )
