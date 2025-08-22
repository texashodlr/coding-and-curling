# Detect a Cycle in a Linked List given the head of a linked list, determine if it has a cycle in it.
#   Linked Lists consist of nodes and nodes have two elements i.e. data and a reference to another node

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        # If we only have /one/ node then there is nothing in its reference

class LinkedList:
    def __init__(self):
        self.head = None
    
    def insertAtBegin(self, data):
        new_node = Node(data)
        # Create a new node with the given data, check if the head of the LL is empty
        #   if yes, set the new node as the head of the LL
        #   if no, set proceed to the next step 
        #       next pointer of the new node to current head, make the new node the new head, return updated head
        if self.head is None:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node
    def insertAtIndex(self, data, index):
        if (index == 0):
            self.insertAtBegin(data)
            return
        
        position = 0
        current_node = self.head
        while (current_node != None and position+1 != index):
            position = position+1
            current_node  = current_node.next
        
        if current_node != None:
            new_node = Node(data)
            new_node.next = current_node.next
            current_node.next = new_node
        else:
            print("Index not present")
    def insertAtEnd(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current_node = self.head
        while(current_node.next):
            current_node = current_node.next
        current_node.next = new_node
    def insertCycleAtEnd(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current_node = self.head
        while(current_node.next):
            current_node = current_node.next
        current_node.next = new_node
        current_node.next.next = self.head

    def updateNode(self, val, index):
        current_node = self.head
        position = 0
        if position == index:
            current_node.data = val
        else:
            while(current_node != None and position != index):
                position = position+1
                current_node = current_node.next
            
            if current_node != None:
                current_node.data = val
            else:
                print("Index not present")
    def removeFirstNode(self):
        if(self.head == None):
            return
        self.head = self.head.next
    def removeLastNode(self):
        if(self.head == None):
            return
        current_node = self.head
        while(current_node.next != None and current_node.next.next != None):
            current_node = current_node.next
        current_node.next = None
    def removeAtIndex(self, index):
        if(self.head == None):
            return
        current_node = self.head
        position = 0 
        if(index == 0):
            self.removeFirstNode()
        else:
            while current_node is not None and position < index - 1:
                position += 1
                current_node = current_node.next
                
            if current_node is None or current_node.next is None:
                print("Index not present")
            else:
                current_node.next = current_node.next.next
    def removeAtData(self, data):
        current_node = self.head
        if(current_node.data == data):
            self.removeFirstNode()
            return
        while current_node is not None and current_node.next.data != data:
            current_node = current_node.next
        
        if current_node is None:
            return
        else:
            current_node.next = current_node.next.next
    def printLL(self):
        current_node = self.head
        while(current_node):
            print(current_node.data)
            current_node = current_node.next
    def sizeOfLL(self):
        size = 0
        if(self.head):
            current_node = self.head
            while(current_node):
                size = size + 1
                current_node = current_node.next
            return size
        else:
            return 0
    def hasCycle(self):
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

## Operational Code ##
llist = LinkedList()
llist.insertAtEnd('a')
llist.printLL()

llist.insertAtBegin('b')
llist.insertAtBegin('aa')
llist.insertAtBegin('C')
llist.insertAtBegin('E')
llist.insertAtBegin('D')
llist.printLL()

# remove nodes from the linked list
print("\nRemove First Node:")
llist.removeFirstNode()
llist.printLL()

print("\nRemove Last Node:")
llist.removeLastNode()
llist.printLL()

print("\nRemove Node at Index 1:")
llist.removeAtIndex(1)
llist.printLL()

# print the linked list after all removals
print("\nLinked list after removing a node:")
llist.printLL()

print("\nUpdate node Value at Index 0:")
llist.updateNode('z', 0)
llist.printLL()

print("\nSize of linked list:", llist.sizeOfLL())

llist.insertAtEnd('aa')
llist.insertAtEnd('b')
llist.insertAtEnd('aa')
llist.insertAtEnd('b')
llist.insertAtEnd('aa')
llist.insertAtEnd('b')
llist.insertAtEnd('aa')
llist.insertAtEnd('b')
llist.insertAtEnd('aa')
llist.insertAtEnd('b')
llist.printLL()

# To determine a cycle we're given a LL head and then we can traverse the LL to see where the recurring elements are 
print(llist.hasCycle())
llist.insertCycleAtEnd('aa')
print(llist.hasCycle())