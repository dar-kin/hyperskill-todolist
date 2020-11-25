from lxml import etree


def travel(root):
    a = root.text
    if a:
        print(a)
    for elem in root:
        travel(elem)


def launch(line):
    root = etree.fromstring(line)
    travel(root)


line = input()
launch(line)
