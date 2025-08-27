"""
Project API endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.services.project_service import ProjectService
from app.schemas.project import (
    ProjectResponse, 
    ProjectDetailResponse, 
    ProjectCreate, 
    ProjectUpdate
)
from app.schemas.asset import AssetAttachRequest

router = APIRouter()


@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all projects with pagination"""
    projects = ProjectService.get_projects(db, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=ProjectDetailResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get project by ID with related data"""
    project = ProjectService.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """Create new project"""
    project = ProjectService.create_project(db, project_data)
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int, 
    project_data: ProjectUpdate, 
    db: Session = Depends(get_db)
):
    """Update project"""
    project = ProjectService.update_project(db, project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete project"""
    success = ProjectService.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}


@router.post("/{project_id}/assets/attach", response_model=ProjectDetailResponse)
def attach_assets_to_project(
    project_id: int,
    request: AssetAttachRequest,
    db: Session = Depends(get_db)
):
    """Attach assets to project"""
    project = ProjectService.attach_assets_to_project(db, project_id, request.asset_ids)
    return project


@router.post("/{project_id}/assets/detach", response_model=ProjectDetailResponse)
def detach_assets_from_project(
    project_id: int,
    request: AssetAttachRequest,
    db: Session = Depends(get_db)
):
    """Detach assets from project"""
    project = ProjectService.detach_assets_from_project(db, project_id, request.asset_ids)
    return project
