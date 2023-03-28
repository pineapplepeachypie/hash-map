# Name: Guyllian Dela Rosa
# OSU Email: delarosg@oregonstate.edu   
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/17
# Description: This is the Hash Map implmentation using Open Addressing


from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method determines the index where to put the new key-value pair
        and adds/updates them to the HM. 
        """
        #check if table load is equal to or greater than 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity *2)
        #hash to find correct index for the key.
        index = self._hash_function(key) % self._capacity
        moving_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        j = 0
        #if the bucket is not Not None, if it's a tombstone insert there, 
        #if a matching key is found update the value. 
        while bucket is not None:
            if bucket.is_tombstone:
                bucket.key = key
                bucket.value = value
                bucket.is_tombstone = False
                self._size += 1
                return
            elif bucket.key == key:
                bucket.value = value
                return
            #rehash if we keep getting a not empty spot
            moving_index = (index + (j**2)) % self._capacity
            j += 1
            bucket = self._buckets[moving_index]
        #add to the HM and adjust size. 
        self._buckets[moving_index] = HashEntry(key, value)
        self._size += 1


    def table_load(self) -> float:
        """
        This method returns the load factor of the HM.
        """
        #return size/capacity
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        #return cap -size
        return self._capacity - self._size


    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All 
        existing key-value pairs remain in the new hash map, and all hash 
        table links rehashed.
        """
        #check that new capacity is valid, get next prime. 
        if new_capacity < self._size:
            return
        if self._is_prime(new_capacity) == False: 
            new_capacity = self._next_prime(new_capacity)
        #save old bucket in a variable, then create new DA and udpate capacity 
        #and size. 
        old_buckets = self._buckets
        old_capacity = self._capacity
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0
        #append to the new self._buckets the same amount of times as new cap
        for _ in range(self._capacity):
            self._buckets.append(None)
        #call put on any non-empty, non-tombstone elements in the HM
        for i in range(old_capacity):
            if old_buckets[i] is not None and not old_buckets[i].is_tombstone:
                self.put(old_buckets[i].key, old_buckets[i].value)
        

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key 
        is not in the HM, method returns None.
        """
        #hash to find correct bucket
        index = self._hash_function(key) % self._capacity
        moving_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        #if bucket is None, this means key is not in HM
        if bucket == None:
            return None
        j = 0
        #while not None, and not is_tombstone, keep searching. 
        while bucket is not None and not bucket.is_tombstone:
            #if matching key is found, return its value.
            if bucket.key == key:
                return bucket.value
            moving_index = (index + (j**2)) % self._capacity
            bucket = self._buckets[moving_index]
            j+= 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        This returns true if the key passed in is in the HM, if not, 
        return False.
        """
        #hash to find correct bucket
        index = self._hash_function(key) % self._capacity
        moving_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        j = 0
        if bucket == None:
            return False
        #if key in the HM matches key passed in, return True.
        while bucket is not None:
            if bucket.key == key:
                return True
            #keep hashing till we find an empty bucket. 
            moving_index = (index + (j**2)) % self._capacity
            bucket = self._buckets[moving_index]
            j+= 1
        return False


    def remove(self, key: str) -> None:
        """
        This method removes key-value pair from the hash map. If 
        the key is not in the hash map, the method does nothing.
        """
        #loop through all buckets to find the bucket with the matching key.
        for i in range(self._capacity):
            if self._buckets[i] is not None: 
                #if a matching key is found and it's TS is False, change its TS to True
                if self._buckets[i].key == key and not self._buckets[i].is_tombstone:
                    self._buckets[i].is_tombstone = True
                    #decrement size by 1. 
                    self._size -= 1


    def clear(self) -> None:
        """
        This method clears the contents of the hashmap but does not change the
        underlying table capacity. 
        """
        #change self._buckets' reference to a new DA
        self._buckets = DynamicArray()
        #append None to it using the existing cap.
        for _ in range(self._capacity):
            self._buckets.append(None)
        #resest size to 0
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a DA where each index contains a tuple of a
        key-value pair stored in the HM. 
        """
        #create new instance of DA
        keys_values = DynamicArray()
        #loop through all the elements of the HM
        for i in range(self._capacity):
            #if the bucket is not empty and its TS is False, add to keys_values.
            if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                pair = self._buckets[i].key, self._buckets[i].value
                keys_values.append(pair)
        return keys_values

    def __iter__(self):
        """
        This method enables the hash map to iterate across itself.
        """
        #set self._index to 0
        self._index = 0
        return self

    def __next__(self):
        """
        This method will return the next item in the hash map, based 
        on the current location of the iterator.
        """
        try:
            value = None
            #while loop skips over 'empty' spots in the HM
            while value is None or value.is_tombstone:
                value = self._buckets[self._index]
                #increment self._index. 
                self._index += 1
        except DynamicArrayException:
            raise StopIteration
        return value



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    # print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
