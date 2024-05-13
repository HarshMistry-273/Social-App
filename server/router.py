from fastapi import APIRouter
from server.endpoints import user, post, interaction

router = APIRouter()

router.include_router(user.route)
router.include_router(post.route)
router.include_router(interaction.route)