import logging
from typing import Optional

from fastapi import APIRouter, Depends
from open_webui.env import SRC_LOG_LEVELS
from open_webui.models.domain_lookups import (
    CreateDomainLookupRequest,
    DomainLookupModel,
    DomainLookups,
)
from open_webui.utils.auth import get_verified_user
from pydantic import BaseModel

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()


############################
# GetDomainLookupsCount
############################


@router.get("/count", response_model=int)
async def get_domain_lookups_count(
    user=Depends(get_verified_user),
):
    return DomainLookups.get_num_domain_lookups_by_user_id(user.id)


@router.post("/", response_model=DomainLookupModel)
async def create_domain_lookup(
    request: CreateDomainLookupRequest,
    user=Depends(get_verified_user),
):
    return DomainLookups.create_domain_lookup_for_user_id(user.id, request.domain)
