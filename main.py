import sqlite3
import shutil
from fastapi import FastAPI, File, UploadFile
from predict_model import *

DATABASE = "database/app-db.sqlite"
app = FastAPI()


@app.get("/diseases/")
def get_diseases():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diseases")
    diseases = cursor.fetchall()
    conn.close()
    return diseases


# Ruta para agregar enfermedad
@app.post("/diseases/")
def create_disease(name: str, description: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO diseases (name, description) VALUES (?, ?)", (name, description)
    )
    conn.commit()
    conn.close()
    return {"message": "Disease created successfully"}

@app.put("/diseases/{disease_id}")
def update_disease(disease_id: int, name: str, description: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE diseases SET name = ?, description = ? WHERE id = ?",
        (name, description, disease_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Disease updated successfully"}

# Eliminar una enfermedad por su ID
@app.delete("/diseases/{disease_id}")
def delete_disease(disease_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM diseases WHERE id = ?", (disease_id,))
    conn.commit()
    conn.close()
    return {"message": "Disease deleted successfully"}


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"database/images/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "info": f"File '{file.filename}' saved at '{file_location}'",
        "result": predict_img(file_location),
    }
