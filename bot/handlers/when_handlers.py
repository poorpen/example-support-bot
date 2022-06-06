from typing import Dict
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedRadioAdapter


def evaluation_check(data: Dict, widget, dialog_manager: DialogManager) -> bool:
    mark_radio: ManagedRadioAdapter = dialog_manager.dialog().find('evaluate_operator')
    mark = mark_radio.get_checked()
    if mark:
        return True
    else:
        return False


def evaluation_not_check(data: Dict, widget, dialog_manager: DialogManager) -> bool:
    mark_radio: ManagedRadioAdapter = dialog_manager.dialog().find('evaluate_operator')
    mark = mark_radio.get_checked()
    if mark:
        return False
    else:
        return True
