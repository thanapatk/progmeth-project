class Node[T]:
    def __init__(self, data: T):
        self.data = data
        self.next: Node | None = None
        self.prev: Node | None = None


class DoublyLinkedList[T]:
    def __init__(self):
        self.head: Node[T] | None = None

    def append(self, data: T):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
        new_node.prev = last_node

    def prepend(self, data: T):
        new_node = Node(data)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        self.head = new_node

    def __delete_node(self, node: Node):
        if node == self.head:
            if node.next:
                node.next.prev = None
                self.head = node.next
            else:
                self.head = None
        elif node.next is None and node.prev:
            node.prev.next = None
        elif node.prev and node.next:
            node.prev.next, node.next.prev = node.next, node.prev

        del node

    def __delete_key(self, key: T):
        current_node = self.head

        if current_node and current_node.data == key:
            if current_node.next:
                current_node.next.prev = None
            self.head = current_node.next
            current_node = None
            return

        while current_node and current_node.data != key:
            current_node = current_node.next

        if current_node is None:
            return

        if current_node.next:
            current_node.next.prev = current_node.prev
        if current_node.prev:
            current_node.prev.next = current_node.next
        current_node = None

    def delete(self, *, key: T | None = None, node: Node | None = None):
        if key is None and node is None:
            raise AttributeError('pass in a key or node')

        if node is not None:
            self.__delete_node(node)
        elif key is not None:
            self.__delete_key(key)

    def __iter__(self):
        current_node = self.head
        while current_node:
            yield current_node.data
            current_node = current_node.next

    def iter_node(self):
        current_node = self.head
        while current_node:
            yield current_node
            current_node = current_node.next

    def __str__(self):
        return '->'.join(map(str, self))


# Example usage:
if __name__ == "__main__":
    ll = DoublyLinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.prepend(0)
    print("Original doubly linked list:", ll)  # Output: 0->1->2->3
    # ll.delete(key=2)
    # print("Doubly linked list after deleting element '2':", ll)  # Output: 0->1->3

    for i, node in enumerate(ll.iter_node()):
        # print(node.data)

        if i % 2 != 0:
            ll.delete(node=node)
        print(ll)

    print(ll)
