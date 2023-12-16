import logging

import torch
from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Project
from utils import get_embedding_model
from config import db
from models import *
from api.schemas import *

router = APIRouter()

logger = logging.getLogger("uvicorn.access")


@router.post(
    "/search",
    response_model=SearchResponse,
)
async def search_directions(
    body: SearchBody,
    session: AsyncSession = Depends(db.get_db_session),
):
    query = " ".join(
        [
            body.city_title,
            body.about,
            body.activities,
            body.books,
            body.games,
            body.interests,
        ]
    )
    logger.info(f"search query: {query}")
    embedding_model = get_embedding_model()
    logger.info(f"done get embedding_model")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    query_embedding = embedding_model.encode(query, convert_to_tensor=True, show_progress_bar=True)
    query_embedding = query_embedding.to(device)
    logger.info(f"done transform query to query_embedding")
    # university_id
    # university_name
    # faculty_id
    # faculty_name
    logger.info(f"Search body: {body}")
    cosine_distance_to_embedding = AdditionalData.embedding.cosine_distance(query_embedding)
    query = (
        select(
            *EducationDirection.__table__.c,
            cosine_distance_to_embedding.label("cosine_distance"),
        )
        .select_from(AdditionalData)
        .join(EducationDirection, EducationDirection.direction_id == AdditionalData.direction_id)
        .order_by(cosine_distance_to_embedding)  # Get the nearest neighbors to a vector
        .limit(body.limit)
    )
    if body.threshold is not None:
        # Get items within a certain distance
        query = query.where(cosine_distance_to_embedding < body.threshold)
    logger.info(f"search query: {query}")
    result = await session.execute(query)
    items = result.fetchall()
    # items = [i[0] for i in items]
    logger.info(f"items: {items}")
    return {
        "items": items,
    }
