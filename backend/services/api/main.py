from fastapi import FastAPI, Query
from typing import Annotated
from database.db_connection import get_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# DOCS: When the backend is in a different "origin" than the frontend, use CORS (Cross-Origin Resource Sharing).
origins = [
    # Add vercel frontend url here when deployed
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    # allow_credentials=True,
    allow_methods = ["GET"],
    allow_headers = ["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

# Create a path operation (route)
@app.get("/api/trends")
async def get_trends(
    entity_type: Annotated[str, Query(max_length = 50)] = "trend", 
    time_window: Annotated[int, Query(ge = 1, le = 3653)] = 30
):
    query = """
        SELECT entity_value, SUM(count) AS total 
        FROM trend_summary
        WHERE entity_type = %s AND snapshot_date  >= CURRENT_DATE - (%s * INTERVAL '1 day')
        GROUP BY entity_value
        ORDER BY total DESC
        LIMIT 50;  
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (
                entity_type,
                time_window
            ))

            rows = cur.fetchall()

    return [{"entity": row[0], "total": row[1]} for row in rows]


# trend_summary schema
#  CREATE TABLE IF NOT EXISTS trend_summary (
#  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),                                                               
#  entity_type TEXT NOT NULL,
#  entity_value TEXT NOT NULL,
#  count INTEGER NOT NULL,
#  snapshot_date DATE NOT NULL,
#  created_at TIMESTAMP DEFAULT NOW(),
#  CONSTRAINT unique_values UNIQUE(entity_type, entity_value, snapshot_date)
# );