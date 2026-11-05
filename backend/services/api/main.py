from fastapi import FastAPI, Query
from typing import Annotated
from database.db_connection import get_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# DOCS: When the backend is in a different "origin" than the frontend, use CORS (Cross-Origin Resource Sharing).
origins = [
    "http://localhost:3000",
    "https://fashion-data-vault.vercel.app",
    "https://www.fashiondatavault.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    # allow_credentials=True,
    allow_methods = ["GET"],
    allow_headers = ["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Create a path operation (route)
@app.get("/api/trends")
async def get_trends(
    entity_type: Annotated[str, Query(max_length = 50)] = "trend", 
    time_window: Annotated[int, Query(ge = 1, le = 3653)] = 30
):
    query = """
        SELECT e.entity_value, COUNT(*) AS total 
        FROM article_entities e
        JOIN aggregates_trend a ON a.id = e.article_id
        WHERE e.entity_type = %s AND a.published_at >= CURRENT_DATE - (%s * INTERVAL '1 day')
        GROUP BY e.entity_value
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

# Trends are counted from article_entities: one row per article per entity, so COUNT(*) is the number of articles that mentioned the entity.