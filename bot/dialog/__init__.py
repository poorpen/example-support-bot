from .dialog_windows import user_menu
from aiogram_dialog import DialogRegistry


async def registry_dialog(registry: DialogRegistry):
    registry.register(user_menu)
