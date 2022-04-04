from flask import Blueprint
from app.controllers import animes_controller

bp = Blueprint("anime", __name__, url_prefix="/animes")

bp.post("")(animes_controller.register_anime)
bp.get("")(animes_controller.get_all_animes)
bp.get("/<int:anime_id>")(animes_controller.get_anime_by_id)
bp.patch("/<int:anime_id>")(animes_controller.update_anime)
bp.delete("/<int:anime_id>")(animes_controller.remove_anime)
