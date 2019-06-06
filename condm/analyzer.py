

class Analyzer:

    sub_collections = {}

    def __init__(self):
        pass

    def sub_collection(self, collection):
        if collection in self.sub_collections:
            count = self.sub_collections[collection]
            count += 1
            self.sub_collections[collection] = count
        else:
            self.sub_collections[collection] = 1

    def print_sub_collection_rpt(self):
        for name in self.sub_collections:
            print('{:4d}: {:>10}'.format(self.sub_collections[name], name))

