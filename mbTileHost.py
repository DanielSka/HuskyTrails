from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import StreamingResponse
import sqlite3
import os

app = FastAPI()

MBTILES_PATH = "uconnVector.mbtiles"

@app.get("/tiles/{z}/{x}/{y}.pbf")
def get_tile(z: int, x: int, y: int):
    if not os.path.exists(MBTILES_PATH):
        raise HTTPException(status_code=404, detail="MBTiles file not found")

    # Flip Y axis for TMS (most MBTiles use TMS layout)
    y_flipped = (1 << z) - 1 - y

    try:
        conn = sqlite3.connect(MBTILES_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?",
            (z, x, y_flipped)
        )
        row = cursor.fetchone()
        conn.close()
        if row is None:
            raise HTTPException(status_code=404, detail="Tile not found")

        headers = {
            "Content-Type": "application/x-protobuf",
            "Content-Encoding": "gzip",
            "Cache-Control": "public, max-age=86400"
        }

        return Response(content=row[0], headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run("mbTileHost:app", host="0.0.0.0", port=port)
