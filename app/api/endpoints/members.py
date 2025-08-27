"""
Member API endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.services.member_service import MemberService
from app.schemas.member import (
    MemberResponse, 
    MemberDetailResponse, 
    MemberCreate, 
    MemberUpdate
)
from app.schemas.asset import AssetAttachRequest

router = APIRouter()


@router.get("/", response_model=List[MemberResponse])
def get_members(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    project_id: int = Query(None, description="Filter by project ID"),
    db: Session = Depends(get_db)
):
    """Get all members with pagination and optional project filter"""
    if project_id:
        members = MemberService.get_members_by_project(db, project_id)
    else:
        members = MemberService.get_members(db, skip=skip, limit=limit)
    return members


@router.get("/{member_id}", response_model=MemberDetailResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    """Get member by ID with related data"""
    member = MemberService.get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.post("/", response_model=MemberResponse, status_code=201)
def create_member(member_data: MemberCreate, db: Session = Depends(get_db)):
    """Create new member"""
    member = MemberService.create_member(db, member_data)
    return member


@router.patch("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: int, 
    member_data: MemberUpdate, 
    db: Session = Depends(get_db)
):
    """Update member"""
    member = MemberService.update_member(db, member_id, member_data)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    """Delete member"""
    success = MemberService.delete_member(db, member_id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member deleted successfully"}


@router.post("/{member_id}/assets/attach", response_model=MemberDetailResponse)
def attach_assets_to_member(
    member_id: int,
    request: AssetAttachRequest,
    db: Session = Depends(get_db)
):
    """Attach assets to member"""
    member = MemberService.attach_assets_to_member(db, member_id, request.asset_ids)
    return member


@router.post("/{member_id}/assets/detach", response_model=MemberDetailResponse)
def detach_assets_from_member(
    member_id: int,
    request: AssetAttachRequest,
    db: Session = Depends(get_db)
):
    """Detach assets from member"""
    member = MemberService.detach_assets_from_member(db, member_id, request.asset_ids)
    return member
