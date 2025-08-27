"""
Cloudinary service for file upload and management
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import Dict, Any, Optional
from fastapi import UploadFile, HTTPException
import mimetypes
import os

from app.config import settings
from app.models.asset import AssetType

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


class CloudinaryService:
    @staticmethod
    def get_asset_type_from_mime(mime_type: str) -> AssetType:
        """Determine asset type from MIME type"""
        if mime_type.startswith('image/'):
            return AssetType.IMAGE
        elif mime_type.startswith('video/'):
            return AssetType.VIDEO
        elif mime_type in ['application/pdf', 'text/plain', 'application/msword', 
                          'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return AssetType.DOCUMENT
        else:
            return AssetType.OTHER

    @staticmethod
    def get_folder_by_type(asset_type: AssetType) -> str:
        """Get Cloudinary folder based on asset type"""
        folder_mapping = {
            AssetType.IMAGE: "pixerse/images",
            AssetType.VIDEO: "pixerse/videos", 
            AssetType.DOCUMENT: "pixerse/documents",
            AssetType.OTHER: "pixerse/others"
        }
        return folder_mapping.get(asset_type, "pixerse/others")

    @staticmethod
    async def upload_file(file: UploadFile) -> Dict[str, Any]:
        """
        Upload file to Cloudinary and return metadata
        """
        try:
            # Validate file
            if not file.filename:
                raise HTTPException(status_code=400, detail="No file selected")
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(file.filename)
            if not mime_type:
                mime_type = file.content_type or "application/octet-stream"
            
            # Determine asset type and folder
            asset_type = CloudinaryService.get_asset_type_from_mime(mime_type)
            folder = CloudinaryService.get_folder_by_type(asset_type)
            
            # Read file content
            file_content = await file.read()
            
            # Upload options
            upload_options = {
                "folder": folder,
                "resource_type": "auto",  # Auto-detect resource type
                "use_filename": True,
                "unique_filename": True,
                "overwrite": False
            }
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(file_content, **upload_options)
            
            # Prepare response data
            upload_data = {
                "filename": os.path.splitext(result["public_id"].split("/")[-1])[0],
                "original_filename": file.filename,
                "cloudinary_public_id": result["public_id"],
                "cloudinary_url": result["url"],
                "cloudinary_secure_url": result["secure_url"],
                "asset_type": asset_type,
                "file_size": result.get("bytes"),
                "mime_type": mime_type,
                "width": result.get("width"),
                "height": result.get("height")
            }
            
            return upload_data
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    @staticmethod
    def delete_file(public_id: str, resource_type: str = "auto") -> bool:
        """
        Delete file from Cloudinary
        """
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
            return result.get("result") == "ok"
        except Exception as e:
            print(f"Error deleting file from Cloudinary: {str(e)}")
            return False

    @staticmethod
    def get_file_info(public_id: str) -> Optional[Dict[str, Any]]:
        """
        Get file information from Cloudinary
        """
        try:
            result = cloudinary.api.resource(public_id)
            return result
        except Exception as e:
            print(f"Error getting file info from Cloudinary: {str(e)}")
            return None
