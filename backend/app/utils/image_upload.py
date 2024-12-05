import os
import uuid
from typing import List
from fastapi import UploadFile, HTTPException
from PIL import Image

class ImageUploadService:
    @staticmethod
    def validate_image(file: UploadFile):
        """
        Validate image file
        """
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Only JPEG, PNG, and GIF are allowed."
            )
        
        # Optional: Check file size
        file.file.seek(0, 2)  # Move to end of file
        file_size = file.file.tell()
        file.file.seek(0)  # Reset file pointer
        
        if file_size > 5 * 1024 * 1024:  # 5MB limit
            raise HTTPException(
                status_code=400, 
                detail="File too large. Maximum size is 5MB."
            )

    @staticmethod
    def process_and_save_image(file: UploadFile, upload_dir: str) -> str:
        """
        Process and save uploaded image
        """
        # Validate image
        ImageUploadService.validate_image(file)
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        full_path = os.path.join(upload_dir, unique_filename)
        
        # Ensure upload directory exists
        os.makedirs(upload_dir, exist_ok=True)
        
        # Open and process image (optional resize/compression)
        with Image.open(file.file) as img:
            # Resize if needed (example: max 1024x1024)
            img.thumbnail((1024, 1024))
            img.save(full_path)
        
        return unique_filename

    @staticmethod
    def upload_multiple_images(
        files: List[UploadFile], 
        upload_dir: str
    ) -> List[str]:
        """
        Upload multiple images
        """
        uploaded_files = []
        
        for file in files:
            filename = ImageUploadService.process_and_save_image(file, upload_dir)
            uploaded_files.append(filename)
        
        return uploaded_files
