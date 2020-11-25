from lxml import etree

def find_password(xml_string):
    root = etree.fromstring(xml_string)
    if "password" in root.keys():
        return root.get("password")
    else:
        return travel(root)


def travel(root):
    if "password" in root.keys():
        return root.get("password")
    for elem in root:
        return travel(elem)
