from lxml import etree


def task(line, attr):
    root = etree.fromstring(line)
    return root.get(attr)


n = input()
a = input()
print(task(n, a))
