"""
Util module
"""

def make_api_getter(field_list):
    """
    Return get url request
    """
    get_url = 'https://graph.facebook.com/%s?fields='
    fields_part = ','.join([p[0] for p in field_list])
    return get_url + fields_part + '&access_token=%s'


def make_permission(field_list):
    """
    Returns {'scope' : 'permission_attr1, ...permission_attrN}
    """
    perm_parts = [p[1] for p in field_list if p[1]]
    perm_line = ','.join(perm_parts)
    return { 'scope': perm_line }