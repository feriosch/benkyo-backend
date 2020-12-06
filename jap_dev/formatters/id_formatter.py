def _format_id(object_id):
    return str(object_id)


def format_response_id(object_id):
    return {
        'id': _format_id(object_id)
    }
