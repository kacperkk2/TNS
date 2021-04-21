
BLACK = True
RED = False


class Node:
    def __init__(self):
        self.rule = None
        self.color = BLACK
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    def __init__(self):
        self.size = 0
        self.root = None

    def size(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x is x.parent.left: #is?
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x is x.parent.right: #is?
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        
    def add(self, element):
        z = Node()
        z.rule = element

        y = None
        x = self.root
        while x is not None:
            y = x
            compare = z.rule.compare(x.rule)
            if compare < 0:
                x = x.left
            else:
                x = x.right
        z.parent = y
        # empty tree
        if y is None:
            self.root = z
        elif z.rule.compare(y.rule) < 0:
            y.left = z
        else:
            y.right = z
        self.size += 1

        z.left = None
        z.right = None
        z.color = RED
        self.after_add_fix(z)
        
    def after_add_fix(self, z):
        while z is not self.root and z.parent.color is RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color is RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self.rotate_left(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color is RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self.rotate_right(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.rotate_left(z.parent.parent)
        self.root.color = BLACK
        
    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        if v is not None:
            v.parent = u.parent

    def remove(self, element):
        z = self.find(self.root, element)
        if z is None:
            return
        self.delete(z)
        
    def delete(self, z):
        y = z
        y_original_color = y.color
        if z.left is None:
            x = z.right
            self.transplant(z, z.right)
        elif z.right is None:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.get_minimum_with_node(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color is BLACK:
            self.after_delete_fix(x)
        self.size -= 1
    
    def after_delete_fix(self, x):
        while x is not self.root and x.color is BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color is RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.rotate_left(x.parent)
                    w = x.parent.right
                if w.left.color is BLACK and w.right.color is BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color is BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.rotate_right(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color is RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.rotate_right(x.parent)
                    w = x.parent.left
                if w.right.color is BLACK and w.left.color is BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color is BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.rotate_left(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.rotate_right(x.parent)
                    x = self.root
        x.color = BLACK
    
    def lower(self, k):
        result = self.lower_node(k)
        if result is None:
            return None
        else:
            return result.rule

    def lower_node(self, k):
        x = self.root
        while x is not None:
            if k.compare(x.rule) > 0:
                if x.right is not None:
                    x = x.right
                else:
                    return x
            else:
                if x.left is not None:
                    x = x.left
                else:
                    current = x
                    while current.parent is not None and current.parent.left is current:
                        current = current.parent
                    return current.parent
        return None
    
    def pop_minimum(self):
        if self.root is None:
            return None
        x = self.root
        while x.left is not None:
            x = x.left
        value = x.rule
        self.delete(x)
        return value
    
    def pop_maximum(self):
        if self.root is None:
            return None
        x = self.root
        while x.right is not None:
            x = x.right
        value = x.rule
        self.delete(x)
        return value
    
    def get_minimum(self):
        if self.root is None:
            return None
        x = self.root
        while x.left is not None:
            x = x.left
        return x.rule

    def get_minimum_with_node(self, node):
        while node.left is not None:
            node = node.left
        return node.rule

    def get_maximum(self):
        if self.root is None:
            return None
        x = self.root
        while x.right is not None:
            x = x.right
        return x.rule
    
    def find(self, x, k):
        while x is not None and k is not x.rule:
            if k.compare(x.rule) < 0:
                x = x.left
            else:
                x = x.right
        return x

    def __str__(self):
        if self.root is None:
            return ""
        return self.to_str(self.root, "")

    def to_str(self, node, s):
        if node is not None:
            if node.left is not None:
                s = self.to_str(node.left, s)
            s += str(node.rule) + " | "
            if node.right is not None:
                s = self.to_str(node.right, s)
        return s
