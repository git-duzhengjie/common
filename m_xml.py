import json
import traceback
import xml.etree.ElementTree as Et


class Mxml:
    def __init__(self, doc):
        self.doc = doc
        self.tree = Et.parse(self.doc)
        self.root = self.tree.getroot()

    def modify(self, node, attr, value, c_attr=None, c_value=None):
        try:
            nd = self.root.findall(node)
            if nd is None:
                return
            for n in nd:
                if c_attr:
                    if n.attrib[c_attr] == c_value:
                        print(value)
                        n.attrib[attr] = value
                else:
                    n.attrib[attr] = value
            self.tree.write(self.doc)
            return True
        except:
            traceback.print_exec()
            return False

    def insert(self, f_node, node, content, pos):
        try:
            n = self.root.find(f_node)
            n.insert(pos, Et.Element(node, json.loads(content)))
            self.tree.write(self.doc)
            return True
        except:
            traceback.print_exc()
            return False

# ml = Mxml('../config/conf.xml')
# ml.modify('xml_modify/file', 'value', '2', 'name', '2')
# ml.insert('xml_insert', 'file', '{"a":"1"}', 0)
