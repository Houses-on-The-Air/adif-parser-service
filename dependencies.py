"""
Dependencies module for the ADIF Parser Service.

This module provides dependency injection functions for FastAPI.
"""

from repositories.adif_repository import AdifIoRepository
from services.adif_service import AdifService
from services.award_service import AwardService


def get_adif_repository():
    """
    Get an instance of the ADIF repository.

    Returns:
        AdifIoRepository: A repository for ADIF data.
    """
    return AdifIoRepository()


def get_award_service():
    """
    Get an instance of the award service.

    Returns:
        AwardService: A service for determining award tiers.
    """
    return AwardService()


def get_adif_service(
    repository=get_adif_repository(), award_service=get_award_service()
):
    """
    Get an instance of the ADIF service.

    Args:
        repository: A repository for ADIF data.
        award_service: A service for determining award tiers.

    Returns:
        AdifService: A service for processing ADIF files.
    """
    return AdifService(repository, award_service)
