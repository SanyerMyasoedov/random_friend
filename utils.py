
class Field(object):

    def __init__(self, field_name, extract_fn=None):
        self.field_name = field_name
        self.extract_fn = extract_fn


field = Field


def make_api_getter(field_list):
    """
    Return get url request
    """
    get_url = 'https://graph.facebook.com/%s?fields='
    fields_part = ','.join(field_list)
    return get_url + fields_part + '&access_token=%s'