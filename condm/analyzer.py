
class Analyzer:

    sub_collections = {}
    unprocessed_collections = {}
    excluded_collections = {}
    compound_objects = 0
    items = 0
    multiple_item_records = 0

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
        print('\nItem counts for sub-collections')
        for name in self.sub_collections:
            print('{:4d}: {:>10}'.format(self.sub_collections[name], name))

    def unprocessed_collection(self, collection):
        if collection in self.unprocessed_collections:
            count = self.unprocessed_collections[collection]
            count += 1
            self.unprocessed_collections[collection] = count
        else:
            self.unprocessed_collections[collection] = 1

    def print_unprocessed_collection_rpt(self):
        if len(self.unprocessed_collections) > 0:
            print('\nItem counts for all unprocessed collections (these will be added to the "base" saf directory).')
            for name in self.unprocessed_collections:
                print('{:3d}: {:>10}'.format(self.unprocessed_collections[name], name))
        else:
            print('\nThere were no unprocessed collections.')

    def excluded_collection(self, collection):
        if collection in self.excluded_collections:
            count = self.excluded_collections[collection]
            count += 1
            self.excluded_collections[collection] = count
        else:
            self.excluded_collections[collection] = 1

    def print_excluded_collection_rpt(self):
        if len(self.excluded_collections) > 0:
            print('\nItem counts for collections that were excluded by configuration.')
            for name in self.excluded_collections:
                print('{:3d}: {:>10}'.format(self.excluded_collections[name], name))
        else:
            print('\nThere were no collections excluded by configuration.')

    def add_compound_object(self):
        self.compound_objects += 1

    def add_single_item(self):
        self.items += 1

    def add_multiple_item_record(self):
        self.multiple_item_records += 1

    def print_item_type_report(self):
        print('{:4d}: {:>10}'.format(self.compound_objects, 'Compound Objects'))
        print('{:4d}: {:>10}'.format(self.multiple_item_records, 'Items with multiple bitstreams'))
        print('{:4d}: {:>10}'.format(self.items, 'Single bitstream items'))
