"""
Member CRUD service
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.member import Member
from app.models.asset import Asset
from app.schemas.member import MemberCreate, MemberUpdate
from app.services.project_service import ProjectService


class MemberService:
    @staticmethod
    def get_members(db: Session, skip: int = 0, limit: int = 100) -> List[Member]:
        """Get all members with pagination"""
        return db.query(Member).offset(skip).limit(limit).all()

    @staticmethod
    def get_member_by_id(db: Session, member_id: int) -> Optional[Member]:
        """Get member by ID"""
        return db.query(Member).filter(Member.member_id == member_id).first()

    @staticmethod
    def get_members_by_project(db: Session, project_id: int) -> List[Member]:
        """Get all members of a specific project"""
        return db.query(Member).filter(Member.project_id == project_id).all()

    @staticmethod
    def create_member(db: Session, member_data: MemberCreate) -> Member:
        """Create new member"""
        # Verify project exists
        project = ProjectService.get_project_by_id(db, member_data.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        db_member = Member(
            project_id=member_data.project_id,
            team_type=member_data.team_type,
            role=member_data.role,
            experience=member_data.experience,
            summary=member_data.summary
        )
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        return db_member

    @staticmethod
    def update_member(db: Session, member_id: int, member_data: MemberUpdate) -> Optional[Member]:
        """Update member"""
        db_member = MemberService.get_member_by_id(db, member_id)
        if not db_member:
            return None
        
        # Update only provided fields
        update_data = member_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_member, field, value)
        
        db.commit()
        db.refresh(db_member)
        return db_member

    @staticmethod
    def delete_member(db: Session, member_id: int) -> bool:
        """Delete member"""
        db_member = MemberService.get_member_by_id(db, member_id)
        if not db_member:
            return False
        
        db.delete(db_member)
        db.commit()
        return True

    @staticmethod
    def attach_assets_to_member(db: Session, member_id: int, asset_ids: List[int]) -> Optional[Member]:
        """Attach assets to member"""
        db_member = MemberService.get_member_by_id(db, member_id)
        if not db_member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Get assets
        assets = db.query(Asset).filter(Asset.asset_id.in_(asset_ids)).all()
        if len(assets) != len(asset_ids):
            found_ids = [asset.asset_id for asset in assets]
            missing_ids = [aid for aid in asset_ids if aid not in found_ids]
            raise HTTPException(status_code=404, detail=f"Assets not found: {missing_ids}")
        
        # Attach assets (avoid duplicates)
        for asset in assets:
            if asset not in db_member.assets:
                db_member.assets.append(asset)
        
        db.commit()
        db.refresh(db_member)
        return db_member

    @staticmethod
    def detach_assets_from_member(db: Session, member_id: int, asset_ids: List[int]) -> Optional[Member]:
        """Detach assets from member"""
        db_member = MemberService.get_member_by_id(db, member_id)
        if not db_member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Remove assets
        for asset_id in asset_ids:
            asset_to_remove = next((asset for asset in db_member.assets if asset.asset_id == asset_id), None)
            if asset_to_remove:
                db_member.assets.remove(asset_to_remove)
        
        db.commit()
        db.refresh(db_member)
        return db_member
