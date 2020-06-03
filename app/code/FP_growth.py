import math
from collections import Counter


class _Node:
    def __init__(self, item=None, count=1):
        self.parent = None
        self.children = dict()  # {item: node, ...}
        self.item = item
        self.count = count
        
    def add_count(self, n=1):
        self.count += n
    
    def add_child(self, node):
        node.parent = self
        self.children[node.item] = node
    
    def __repr__(self):
        return (f'Node(item: {self.item}, count: {self.count}, '
            f'parent: {self.parent.item if self.parent else None}, '
            f'child: {tuple(self.children.keys())})')

class FPTree:
    def __init__(self):
        self.root = None
        # header_table = {item: (count, heads), ...}, heads = [head, ...]
        self.header_table = dict()
        self.min_support = 0  # minimum number of frequent pattern
        
    @staticmethod
    def _construct_fptree(transactions, min_support):
        """Construct FP-tree and return (root, header_table) of FP-tree"""
        # count number of each item in transactions
        counter = Counter()
        for transaction in transactions:
            counter.update(transaction)
        # remove the items that are not frequent (less than min_support)
        counter = Counter(dict(filter(
            lambda x: x[1] >= min_support, counter.items())))
        # because sorting result may be diffrent (if 2 items have same number)
        # so generate item's fixed priorities
        priorities = dict(zip(
            sorted(counter.keys(), key=lambda x: counter[x]), 
            range(len(counter))))
        
        # order frequent items in frequency descending order and store
        ordered_frequent_items_list = list()
        for transaction in transactions:
            frequent_items = tuple(
                filter(lambda x: x in priorities.keys(), transaction))
            ordered_frequent_items_list.append(
                sorted(frequent_items, key=lambda x: priorities[x], reverse=True))

        # scan (ordered) frequent items list, construct FP-tree
        root = _Node()
        header_table = dict(
            (item, (count, [])) for item, count in counter.items())
        for items in ordered_frequent_items_list:
            current = root
            for item in items:
                if item in current.children:
                    current = current.children[item]
                    current.add_count()
                else:
                    node = _Node(item)
                    current.add_child(node)
                    # link node to the header table
                    header_table[item][1].append(node)
                    current = node
        
        return root, header_table
                    
    @staticmethod
    def _generate_cond_pattern_bases(heads):
        """Generate cond. pattern bases by heads for each frequent item"""
        bases = list()
        for head in heads:
            base = list()
            current = head
            while current.parent.item is not None:
                current = current.parent
                base.append(current.item)
            if base:  # length is not equal 0
                # times is equal to head
                for i in range(head.count):
                    bases.append(base)
        return bases
    
    def fit(self, transactions, support_rate=0.5):
        """Fit the input transactions construct FP-tree"""
        self.min_support = math.ceil(len(transactions) * support_rate)
        self.root, self.header_table = self._construct_fptree(
            transactions, self.min_support)
        return self
    
    def mine(self):
        """Find out frequent patterns by mining the FP-tree"""
        def mine_subtree(root, header_table):
            """Recursive mine the FP-tree and return frequent pattern"""
            res = list()  # list of (pattern, count)
            # add 1-itemset to frequent patterns
            for item, value in header_table.items():
                pattern = list()
                pattern.append(item)
                res.append((pattern, value[0]))
            # for each item in header table,
            # recursive call the function mine the frequent pattern
            for item, value in header_table.items():
                count, heads = value
                cond_pattern_bases = self._generate_cond_pattern_bases(heads)
                cond_root, cond_header_table = self._construct_fptree(
                    cond_pattern_bases, self.min_support)
                # add the item for each cond. pattern and insert into result list
                for cond_pattern, cond_count in mine_subtree(
                        cond_root, cond_header_table):
                    pattern = cond_pattern
                    pattern.append(item)
                    res.append((pattern, cond_count))
            return res
        
        if self.root is None or not self.header_table:
            raise Exception('You have to construct FP-tree first!')

        return mine_subtree(self.root, self.header_table)