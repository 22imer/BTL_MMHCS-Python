import os
import base64
from datetime import datetime
import uuid

# Create uploads folder if it doesn't exist
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

def upload_image(image_data: str) -> str:
    """Save image locally and return relative URL"""
    try:
        # Check if image_data is base64
        if image_data.startswith("data:image"):
            # Extract base64 data
            # Format: data:image/jpeg;base64,<base64_data>
            parts = image_data.split(",")
            if len(parts) == 2:
                base64_data = parts[1]
                # Get image format from the data URI
                format_part = parts[0]  # data:image/jpeg;base64
                if "image/" in format_part:
                    image_format = format_part.split("/")[1].split(";")[0]
                else:
                    image_format = "jpg"
            else:
                image_format = "jpg"
                base64_data = image_data
        else:
            # Assume it's already base64 without the data URI prefix
            base64_data = image_data
            image_format = "jpg"
        
        # Decode base64
        image_bytes = base64.b64decode(base64_data)
        
        # Generate unique filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"image_{timestamp}_{unique_id}.{image_format}"
        
        # Save to uploads folder
        filepath = os.path.join(UPLOADS_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        
        # Return relative URL (backend will serve it via static files)
        return f"/uploads/{filename}"
        
    except Exception as e:
        print(f"Error saving image locally: {e}")
        raise
