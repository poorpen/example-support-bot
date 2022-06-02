from aiogram_dialog import DialogRegistry

from .dialog_windows import user_menu, user_dialog, role_reversal


async def registry_dialog(registry: DialogRegistry):
    registry.register(role_reversal)
    registry.register(user_menu)
    registry.register(user_dialog)
