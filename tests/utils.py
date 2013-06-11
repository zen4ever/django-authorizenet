from django.contrib.auth.models import User


def create_user(id=None, username='', password=''):
    user = User(username=username)
    user.id = id
    user.set_password(password)
    user.save()
    return user


def xml_to_dict(node):
    """Recursively convert minidom XML node to dictionary"""
    node_data = {}
    if node.nodeType == node.TEXT_NODE:
        node_data = node.data
    elif node.nodeType not in (node.DOCUMENT_NODE, node.DOCUMENT_TYPE_NODE):
        node_data.update(node.attributes.items())
    if node.nodeType not in (node.TEXT_NODE, node.DOCUMENT_TYPE_NODE):
        for child in node.childNodes:
            child_name, child_data = xml_to_dict(child)
            if not child_data:
                child_data = ''
            if child_name not in node_data:
                node_data[child_name] = child_data
            else:
                if not isinstance(node_data[child_name], list):
                    node_data[child_name] = [node_data[child_name]]
                node_data[child_name].append(child_data)
        if node_data.keys() == ['#text']:
            node_data = node_data['#text']
    if node.nodeType == node.DOCUMENT_NODE:
        return node_data
    else:
        return node.nodeName, node_data
