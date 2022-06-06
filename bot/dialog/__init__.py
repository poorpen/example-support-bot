from aiogram_dialog import DialogRegistry

from .dialog_windows import user_menu, user_dialog, role_reversal, operator_dialog, operator_menu


async def registry_dialog(registry: DialogRegistry):
    registry.register(role_reversal)
    registry.register(operator_menu)
    registry.register(user_menu)
    registry.register(user_dialog)
    registry.register(operator_dialog)
