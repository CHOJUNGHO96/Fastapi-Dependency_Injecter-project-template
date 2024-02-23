from dependency_injector import containers, providers

from app.apis.v1.auth.authentication import Authentication
from app.apis.v1.auth.registration.repositories.registration_repositories import (
    RegistrationRepository,
)
from app.apis.v1.auth.registration.service.registration_service import (
    RegistrationService,
)


class Container(containers.DeclarativeContainer):
    db = providers.Singleton()
    config = providers.Configuration()
    authentication = providers.Singleton(Authentication)

    wiring_config = containers.WiringConfiguration(packages=["app.apis.v1.auth.registration"])

    # Repository
    registration_repository = providers.Factory(RegistrationRepository, session_factory=db.provided.session)

    # Service
    registration_service = providers.Factory(
        RegistrationService,
        Registration_repository=registration_repository,
        config=config,
        authentication=authentication,
    )
