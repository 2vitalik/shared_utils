
def remove_stress(value):
    return value.replace('́', '').replace('̀', '').replace('ѐ', 'е'). \
        replace('ѝ', 'и')
