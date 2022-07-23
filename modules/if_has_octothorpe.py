from modules.notifiyer import add_notify

"""Удаление знака решётки # из имени рига в HiveOS
и предупрежение о необходимости переименования рига
(почему то телеграм не любит в сообщение этот знак)
"""


def del_octothorpe(has_octothorpe):
    clean_string = has_octothorpe.replace("#", "")
    if has_octothorpe != clean_string:
        add_notify(clean_string, "clean_string")
    return clean_string
