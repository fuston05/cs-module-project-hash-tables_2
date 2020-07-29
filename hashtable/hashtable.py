class HashTableEntry:
    """
    Linked List hash table key/value pair
    """

    def __init__(self, key, value, next=None):
        self.key = key
        self.value = value
        self.next = next


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity=MIN_CAPACITY):
        self.capacity = capacity
        self.storage = [0] * capacity
        self.itemCount = 0

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.storage)

    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        load = self.itemCount / self.capacity
        return load

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here

    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        # Your code here
        hash = 5381
        for x in key:
            hash = ((hash << 5) + hash) + ord(x)
        return hash & 0xFFFFFFFF

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # check load factor 
        if self.get_load_factor() > 0.7:
            self.resize(self.capacity * 2)

        # get index from hash
        ind = self.hash_index(key)
        # if self.storage[ind] == 0:
        # self.storage[ind]= HashTableEntry(key, value)
        # self.itemCount+= 1

        # # if index is empty
        if self.storage[ind] == 0:
            # add newNode
            self.storage[ind] = HashTableEntry(key, value)
        # else: 'chain' new node to end, or 'overwrite' the existing node
        else:
            curr = self.storage[ind]
            while curr.next != None:
                # overwrite if keys match
                if curr.key == key:
                    curr.value = value
                    self.itemCount += 1
                    break
                # if keys dont match, add a new entry
                else:
                    curr = curr.next
                # add new node at the end of linked-list chain
            curr.next = HashTableEntry(key, value)
            self.itemCount += 1

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        ind = self.hash_index(key)
        # if self.storage[ind] != 0:
        #     self.storage[ind]= 0
        #     self.itemCount-= 1
        # else:
        #     print('Warning! That key was not found!')

        # possibilities:
        # one node,
        # empty,
        # there's more than one node
        curr = self.storage[ind]
        prev = curr
        if curr != 0:
            count = 0
            while curr.key != None:
                if curr.key == key:
                    # is only node?
                    if curr.next == None and count == 0:
                        self.storage[ind] = 0
                        break
                    # is first but not the only node
                    elif curr.next != None and count == 0:
                        self.storage[ind] = curr.next
                        break
                    # is last node?
                    elif curr.next == None and count > 0:
                        prev.next = None
                        break
                    # is middle node?
                    else:
                        prev.next = curr.next
                        break
                else:
                    count += 1
                    prev = prev.next
                    curr = curr.next
        else:
            print('Warning key not found')

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # if self.storage[ind] != 0:
        #     return self.storage[ind].value
        # else:
        #     return None

        # get ind hash key
        ind = self.hash_index(key)
        result = None
        # if not empty
        if self.storage[ind] != 0:
            curr = self.storage[ind]
            while curr:
                if curr.key == key:
                    result = curr.value
                curr = curr.next
        return result

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        
        self.capacity= new_capacity
        oldArr= self.storage
        newArr= [0] * new_capacity

        self.storage= newArr

        # loop through old arr, and rehash all items into the new arr
        # if slot has a next node, then traverse all nodes
        for i in range(len(oldArr) -1):
            if oldArr[i] != 0:
                curr = oldArr[i]
                while curr:
                    ind= self.hash_index(curr.key)
                    newArr[ind]= curr
                    curr= curr.next


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")
    ht.put("line_13", "And stood awhile in thought.")
    ht.put("line_14", "And stood awhile in thought.")
    ht.put("line_15", "And stood awhile in thought.")
    ht.put("line_16", "And stood awhile in thought.")
    ht.put("line_17", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print('')

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
