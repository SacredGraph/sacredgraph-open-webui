import time
import uuid
from typing import Optional

from open_webui.internal.db import Base, JSONField, get_db
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text

####################
# Domain Lookup DB Schema
####################


class DomainLookup(Base):
    __tablename__ = "domain_lookup"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    domain = Column(String)
    created_at = Column(BigInteger)


class DomainLookupModel(BaseModel):
    id: str
    user_id: str
    domain: str
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)


####################
# Forms
####################


class CreateDomainLookupRequest(BaseModel):
    domain: str


class DomainLookupResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    profile_image_url: str


class DomainLookupsTable:
    def insert_new_domain_lookup(
        self,
        id: str,
        user_id: str,
        domain: str,
        created_at: int,
    ) -> Optional[DomainLookupModel]:
        with get_db() as db:
            domain_lookup = DomainLookupModel(
                **{
                    "id": id,
                    "user_id": user_id,
                    "domain": domain,
                    "created_at": created_at,
                }
            )
            result = DomainLookup(**domain_lookup.model_dump())
            db.add(result)
            db.commit()
            db.refresh(result)
            if result:
                return domain_lookup
            else:
                return None

    def get_num_domain_lookups_by_user_id(self, user_id: str) -> Optional[int]:
        with get_db() as db:
            return (
                db.query(DomainLookup).filter(DomainLookup.user_id == user_id).count()
            )

    def get_domain_lookup_by_user_id_and_domain(
        self, user_id: str, domain: str
    ) -> Optional[DomainLookupModel]:
        with get_db() as db:
            result = (
                db.query(DomainLookup)
                .filter(DomainLookup.user_id == user_id, DomainLookup.domain == domain)
                .first()
            )
            if result:
                return DomainLookupModel.model_validate(result)
            return None

    def create_domain_lookup_for_user_id(
        self, user_id: str, domain: str
    ) -> Optional[DomainLookupModel]:
        # First check if a record already exists
        existing_lookup = self.get_domain_lookup_by_user_id_and_domain(user_id, domain)
        if existing_lookup:
            return existing_lookup

        with get_db() as db:
            domain_lookup = DomainLookupModel(
                **{
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "domain": domain,
                    "created_at": int(time.time()),
                }
            )
            result = DomainLookup(**domain_lookup.model_dump())
            db.add(result)
            db.commit()
            db.refresh(result)
            if result:
                return domain_lookup
            else:
                return None


DomainLookups = DomainLookupsTable()
