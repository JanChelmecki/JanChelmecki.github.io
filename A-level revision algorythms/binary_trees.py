class Node():
    def __init__(self, data) -> None:
        self.data = data
        self.left = -1
        self.right = -1

    #region Set-Get
    def set_left(self, index):
        self.left = index

    def get_left(self):
        return self.left

    def set_right(self, index):
        self.right = index

    def get_right(self):
        return self.right

    def get_data(self):
        return self.data
    #endregion

class Tree():
    def __init__(self, root_data) -> None:
        self.items = [Node(root_data)]
        self.root = 0

    def add(self, item):
        index = self.root
        found = False
        while not found:
            if item < self.items[index].get_data():
                if self.items[index].get_left() == -1:
                    found = True
                    self.items[index].set_left(len(self.items))
                index = self.items[index].get_left()
            else:
                if self.items[index].get_right() == -1:
                    found = True
                    self.items[index].set_right(len(self.items))
                index = self.items[index].get_right()
        self.items.append(Node(item))

    def delete(self, item):
        pass

    def search(self, sought, index = False):
        if index == -1:
            return False
        else:
            if index == False:
                index = self.get_root()
            current = tree.get_item(index)
            if current.get_data() > sought:
                return self.search(sought, current.get_left())
            elif current.get_data() < sought:
                return self.search(sought, current.get_right())
            else:
                return index
    
    def traverse_in_order(self, index = False):
        if index == False:
            index = self.root
        item = tree.get_item(index)
        if item.get_left() != -1:
            self.traverse_in_order(item.get_left())
        print(item.get_data())
        if item.get_right() != -1:
            self.traverse_in_order(item.get_right())

    def get_item(self, index):
        return self.items[index]
    
    def get_root(self):
        return self.root

tree = Tree("D")
for char in ["B", "A", "C", "G", "E", "F"]:
    tree.add(char)

"""         tree:
                D
        B               G
    A       C       E
                        F

"""

tree.traverse_in_order()