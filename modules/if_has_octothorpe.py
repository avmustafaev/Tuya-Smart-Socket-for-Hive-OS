from modules.send_to_telegram import do_telega

"""Удаление знака решётки # из имени рига в HiveOS
и предупрежение о необходимости переименования рига
(почему то телеграм не любит в сообщение этот знак)
"""


def del_octothorpe(has_octothorpe):
    clean_string = has_octothorpe.replace("#", "")
    if has_octothorpe != clean_string:
        part = f'🐣 {clean_string}: содержит в имени знак решётки, лучше переименовать'
        do_telega(part)
    return clean_string
