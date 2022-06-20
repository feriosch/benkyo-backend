def format_deleted_fields(kanji_info):
    deleted_fields = list()
    if 'v2' not in kanji_info:
        deleted_fields.append('v2')
    if 'on' not in kanji_info:
        deleted_fields.append('on')
    if 'kun' not in kanji_info:
        deleted_fields.append('kun')
    if 'components' not in kanji_info or len(kanji_info['components']) == 0:
        deleted_fields.append('components')
    if 'story' not in kanji_info:
        deleted_fields.append('story')
    return deleted_fields
