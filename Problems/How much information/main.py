from lxml import etree


def task(line):
    root = etree.fromstring(line)
    return len(root), len(root.keys())


n = input()
answ = task(n)
print(answ[0], answ[1])
