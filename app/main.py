from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from pydantic import ValidationError

from db import get_connection, init_db
from models import Weapon

app = FastAPI(title="Weapon API")

@app.on_event("startup")
def startup():
     init_db()


@app.post("/upload")
def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")

    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file")

    if df.empty:
        raise HTTPException(status_code=400, detail="CSV is empty")

    rows = df.to_dict(orient="records")
    valid_rows = []

    for i, row in enumerate(rows, start=1):
        try:
            data = Weapon(**row)
            valid_rows.append(data.model_dump())

        except ValidationError as e:
            raise HTTPException(
                status_code=422,
                detail={
                    "row": i,
                    "error": e.errors()
                }
            )
    df = pd.read_csv(file.file)

    bins = [-100, 20 , 100, 300, 10000]
    labels = ["low", "medium", "high","extreme"]
    df["risk_level"] = pd.cut(df["range_km"], bins=bins, labels=labels)

    df = df.fillna("Unknown")
    weapon_list = df.to_dict(orient="records")

    conn = get_connection()
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO weapon (weapon_id, weapon_name, weapon_type, range_km ,weight_kg,manufacturer,
                            origin_country,storage_location,year_estimated,risk_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)
    """

    values = [
        (w["weapon_id"], w["weapon_name"], w["weapon_type"], w["range_km"],w["weight_kg"],
         w["manufacturer"],w["origin_country"],w["storage_location"],w["year_estimated"],w["risk_level"])
        for w in weapon_list
    ]

    cursor.executemany(insert_sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return {"status": "success",
            "inserted_records": len(weapon_list)
            }
