from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncpg
from datetime import datetime
from typing import Optional
import os

app = FastAPI()

# Database config
DB_CONFIG = {
    "host": "dpg-d3dpcpbuibrs73a83c20-a.oregon-postgres.render.com",
    "port": 5432,
    "database": "image_store_imzd",
    "user": "image_store_imzd_user",
    "password": "ZuRrIHMRedJTkFlEWRp3vU2VcvDxd5LA",
}

# Database pool
db_pool = None

@app.on_event("startup")
async def startup():
    global db_pool
    db_pool = await asyncpg.create_pool(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        min_size=5,
        max_size=20
    )
    await ensure_table_schema()

@app.on_event("shutdown")
async def shutdown():
    await db_pool.close()

async def ensure_table_schema():
    async with db_pool.acquire() as conn:
        # Check if description column exists
        result = await conn.fetchval("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='webcam_images' AND column_name='description'
        """)
        if not result:
            await conn.execute("ALTER TABLE webcam_images ADD COLUMN description TEXT")

# HTML Templates
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Webcam Image Manager</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: center; }
        .images-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .image-card { border: 1px solid #ddd; border-radius: 4px; overflow: hidden; }
        .image-card img { width: 100%; height: 250px; object-fit: cover; }
        .image-info { padding: 10px; }
        .image-actions { display: flex; gap: 10px; padding: 10px; }
        .btn { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; text-align: center; }
        .btn-primary { background-color: #007bff; color: white; }
        .btn-danger { background-color: #dc3545; color: white; }
        .btn-warning { background-color: #ffc107; color: black; }
        .btn-view { background-color: #17a2b8; color: white; }
        .flash-messages { padding: 10px; margin-bottom: 20px; }
        .flash-message { padding: 10px; margin-bottom: 10px; border-radius: 4px; }
        .flash-success { background-color: #d4edda; color: #155724; }
        .flash-error { background-color: #f8d7da; color: #721c24; }
        .modal { display: none; position: fixed; z-index: 1; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.4); }
        .modal-content { background-color: #fefefe; margin: 10% auto; padding: 20px; border: 1px solid #888; width: 50%; max-width: 500px; }
        .close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
        .close:hover { color: black; }
        .form-group { margin-bottom: 15px; }
        .form-control { width: 100%; padding: 8px; box-sizing: border-box; }
        .form-label { display: block; margin-bottom: 5px; }
        .image-view { max-width: 100%; max-height: 80vh; margin: 0 auto; display: block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Webcam Image Manager</h1>
            <button class="btn btn-primary" onclick="showUploadModal()">Upload New Image</button>
        </div>

        {% if message %}
        <div class="flash-messages">
            <div class="flash-message flash-{{ message_type }}">{{ message }}</div>
        </div>
        {% endif %}

        <div class="images-grid">
            {% for image in images %}
            <div class="image-card">
                <img src="/image/{{ image['id'] }}" alt="Image {{ image['id'] }}">
                <div class="image-info">
                    <p><strong>ID:</strong> {{ image['id'] }}</p>
                    <p><strong>Created:</strong> {{ image['created_at'].strftime('%Y-%m-%d %H:%M:%S') }}</p>
                    {% if image['description'] %}
                    <p><strong>Description:</strong> {{ image['description'] }}</p>
                    {% endif %}
                </div>
                <div class="image-actions">
                    <a href="/view/{{ image['id'] }}" class="btn btn-view">View</a>
                    <a href="/edit/{{ image['id'] }}" class="btn btn-warning">Edit</a>
                    <a href="/delete/{{ image['id'] }}" class="btn btn-danger" onclick="return confirm('Are you sure you want to delete this image?');">Delete</a>
                </div>
            </div>
            {% else %}
            <p>No images found in the database.</p>
            {% endfor %}
        </div>
    </div>

    <div id="uploadModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeUploadModal()">&times;</span>
            <h2>Upload New Image</h2>
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <div class="form-group">
                    <label class="form-label" for="image">Select Image:</label>
                    <input type="file" class="form-control" id="image" name="image" accept="image/*" required>
                </div>
                <div class="form-group">
                    <label class="form-label" for="description">Description (optional):</label>
                    <textarea class="form-control" id="description" name="description" rows="3"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Upload</button>
            </form>
        </div>
    </div>

    <script>
        function showUploadModal() {
            document.getElementById('uploadModal').style.display = 'block';
        }
        
        function closeUploadModal() {
            document.getElementById('uploadModal').style.display = 'none';
        }
        
        window.onclick = function(event) {
            const modal = document.getElementById('uploadModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
</body>
</html>
'''

IMAGE_VIEW_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>View Image</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: center; }
        .btn { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn-primary { background-color: #007bff; color: white; }
        .image-container { margin-top: 20px; text-align: center; }
        .image-view { max-width: 100%; max-height: 80vh; }
        .image-info { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>View Image</h1>
            <a href="/" class="btn btn-primary">Back to Gallery</a>
        </div>

        <div class="image-container">
            <img src="/image/{{ image['id'] }}" alt="Image {{ image['id'] }}" class="image-view">
        </div>

        <div class="image-info">
            <p><strong>ID:</strong> {{ image['id'] }}</p>
            <p><strong>Created:</strong> {{ image['created_at'].strftime('%Y-%m-%d %H:%M:%S') }}</p>
            {% if image['description'] %}
            <p><strong>Description:</strong> {{ image['description'] }}</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

EDIT_IMAGE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Edit Image</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: center; }
        .btn { padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; text-align: center; }
        .btn-primary { background-color: #007bff; color: white; }
        .btn-secondary { background-color: #6c757d; color: white; }
        .form-group { margin-bottom: 15px; }
        .form-control { width: 100%; padding: 8px; box-sizing: border-box; }
        .form-label { display: block; margin-bottom: 5px; }
        .image-preview { max-width: 100%; max-height: 300px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Edit Image</h1>
            <a href="/" class="btn btn-secondary">Cancel</a>
        </div>

        <img src="/image/{{ image['id'] }}" alt="Image {{ image['id'] }}" class="image-preview">

        <form action="/update/{{ image['id'] }}" method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label class="form-label" for="description">Description:</label>
                <textarea class="form-control" id="description" name="description" rows="3">{{ image['description'] or '' }}</textarea>
            </div>
            <div class="form-group">
                <label class="form-label" for="new_image">Replace Image (optional):</label>
                <input type="file" class="form-control" id="new_image" name="new_image" accept="image/*">
            </div>
            <button type="submit" class="btn btn-primary">Save Changes</button>
        </form>
    </div>
</body>
</html>
'''

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, message: str = None, message_type: str = None):
    async with db_pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, created_at, description FROM webcam_images ORDER BY created_at DESC"
        )
        images = [dict(row) for row in rows]
    
    from jinja2 import Template
    template = Template(HTML_TEMPLATE)
    html_content = template.render(images=images, message=message, message_type=message_type)
    return HTMLResponse(content=html_content)

@app.get("/image/{image_id}")
async def get_image(image_id: int):
    async with db_pool.acquire() as conn:
        result = await conn.fetchval(
            "SELECT image FROM webcam_images WHERE id = $1", image_id
        )
    
    if result:
        return Response(content=bytes(result), media_type="image/jpeg")
    else:
        raise HTTPException(status_code=404, detail="Image not found")

@app.get("/view/{image_id}", response_class=HTMLResponse)
async def view_image(image_id: int):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, created_at, description FROM webcam_images WHERE id = $1", image_id
        )
    
    if row:
        image = dict(row)
        from jinja2 import Template
        template = Template(IMAGE_VIEW_TEMPLATE)
        html_content = template.render(image=image)
        return HTMLResponse(content=html_content)
    else:
        return RedirectResponse(url="/?message=Image not found&message_type=error")

@app.get("/edit/{image_id}", response_class=HTMLResponse)
async def edit_image(image_id: int):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, created_at, description FROM webcam_images WHERE id = $1", image_id
        )
    
    if row:
        image = dict(row)
        from jinja2 import Template
        template = Template(EDIT_IMAGE_TEMPLATE)
        html_content = template.render(image=image)
        return HTMLResponse(content=html_content)
    else:
        return RedirectResponse(url="/?message=Image not found&message_type=error")

@app.post("/update/{image_id}")
async def update_image(
    image_id: int,
    description: str = Form(""),
    new_image: Optional[UploadFile] = File(None)
):
    async with db_pool.acquire() as conn:
        if new_image and new_image.filename:
            image_data = await new_image.read()
            await conn.execute(
                "UPDATE webcam_images SET image = $1, description = $2 WHERE id = $3",
                image_data, description, image_id
            )
        else:
            await conn.execute(
                "UPDATE webcam_images SET description = $1 WHERE id = $2",
                description, image_id
            )
    
    return RedirectResponse(url="/?message=Image updated successfully&message_type=success", status_code=303)

@app.get("/delete/{image_id}")
async def delete_image(image_id: int):
    async with db_pool.acquire() as conn:
        await conn.execute("DELETE FROM webcam_images WHERE id = $1", image_id)
    
    return RedirectResponse(url="/?message=Image deleted successfully&message_type=success", status_code=303)

@app.post("/upload")
async def upload_image(
    image: UploadFile = File(...),
    description: str = Form("")
):
    if not image:
        return RedirectResponse(url="/?message=No image uploaded&message_type=error", status_code=303)
    
    image_data = await image.read()
    
    async with db_pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO webcam_images (image, description, created_at) VALUES ($1, $2, $3)",
            image_data, description, datetime.now()
        )
    
    return RedirectResponse(url="/?message=Image uploaded successfully&message_type=success", status_code=303)

