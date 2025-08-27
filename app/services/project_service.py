"""
Project CRUD service
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.project import Project
from app.models.asset import Asset
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    @staticmethod
    def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all projects with pagination"""
        return db.query(Project).offset(skip).limit(limit).all()

    @staticmethod
    def get_project_by_id(db: Session, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        return db.query(Project).filter(Project.project_id == project_id).first()

    @staticmethod
    def create_project(db: Session, project_data: ProjectCreate) -> Project:
        """Create new project"""
        db_project = Project(
            project_name=project_data.project_name,
            description=project_data.description
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def update_project(db: Session, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        """Update project"""
        db_project = ProjectService.get_project_by_id(db, project_id)
        if not db_project:
            return None
        
        # Update only provided fields
        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def delete_project(db: Session, project_id: int) -> bool:
        """Delete project"""
        db_project = ProjectService.get_project_by_id(db, project_id)
        if not db_project:
            return False
        
        db.delete(db_project)
        db.commit()
        return True

    @staticmethod
    def attach_assets_to_project(db: Session, project_id: int, asset_ids: List[int]) -> Optional[Project]:
        """Attach assets to project"""
        db_project = ProjectService.get_project_by_id(db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get assets
        assets = db.query(Asset).filter(Asset.asset_id.in_(asset_ids)).all()
        if len(assets) != len(asset_ids):
            found_ids = [asset.asset_id for asset in assets]
            missing_ids = [aid for aid in asset_ids if aid not in found_ids]
            raise HTTPException(status_code=404, detail=f"Assets not found: {missing_ids}")
        
        # Attach assets (avoid duplicates)
        for asset in assets:
            if asset not in db_project.assets:
                db_project.assets.append(asset)
        
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def detach_assets_from_project(db: Session, project_id: int, asset_ids: List[int]) -> Optional[Project]:
        """Detach assets from project"""
        db_project = ProjectService.get_project_by_id(db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Remove assets
        for asset_id in asset_ids:
            asset_to_remove = next((asset for asset in db_project.assets if asset.asset_id == asset_id), None)
            if asset_to_remove:
                db_project.assets.remove(asset_to_remove)
        
        db.commit()
        db.refresh(db_project)
        return db_project
