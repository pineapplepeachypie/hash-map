# Name: Guyllian Dela Rosa
# OSU Email: delarosg@oregonstate.edu   
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/17
# Description: This is the Hash Map implmentation using Separate Chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        #resize DA if table load is equal to or greater than 1.0.
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity*2)
        #use hash_function 1 to find the right bucket.
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        #iterate through the Linkedlist in the bucket to see if key already exists
        #if yes, update value. 
        for node in bucket:
            if node.key == key:
                node.value = value
                return
        #if we get here, key was not found and we just insert the key-value pair. 
        bucket.insert(key, value)
        self._size += 1
        

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table. 
        """
        empty_buckets = 0
        #for loop loops through all the buckets and if length is 0, this means 
        #that bucket is empty
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empty_buckets += 1
        return empty_buckets

    def table_load(self) -> float:
        """
        This method returns the load factor of the HM. 
        """
        #return size/cap
        return self._size/self._capacity

    def clear(self) -> None:
        """
        This method clears the contents of the hashmap but does not change the
        underlying table capacity. 
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All 
        existing key-value pairs remain in the new hash map, and all hash 
        table links rehashed.
        """
        if new_capacity < 1:
            return        
        #check if new_cap is prime, if not, get next prime. 
        if self._is_prime(new_capacity) == False:
            new_capacity = self._next_prime(new_capacity)
        #while loop checks table load without changing self._capacity. 
        #if table load is over 1, double new_cap and pass it in next_prime again.
        while self._size > new_capacity:
            new_capacity = self._next_prime(new_capacity*2)
        #create new DA and append additional LL based on new_cap
        new_da = DynamicArray()
        for _ in range(new_capacity):
            new_da.append(LinkedList())
        #re-hash each of the existing keys from the old DA and re-chain them
        for i in range(self._capacity):
            bucket = self._buckets[i]
            for node in bucket:
                index = self._hash_function(node.key) % new_capacity
                new_da[index].insert(node.key, node.value)
        #update self._buckets to point to the new DA, update capacity. 
        self._buckets = new_da
        self._capacity = new_capacity
        

    def get(self, key: str):
        """
        This method returns the value associated with the given key. If the key 
        is not in the HM, method returns None. 
        """
        #find the right bucket
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        #if bucket is None, return None
        if bucket == None:
            return None
        #iterate through all the nodes in the bucket; return value if key is found
        else: 
            for node in bucket:
                if node.key == key:
                    return node.value
        return None


    def contains_key(self, key: str) -> bool:
        """
        This returns true if the key passed in is in the HM, if not, 
        return False. 
        """
        #find the right bucket
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        #if bucket is None, return False
        if bucket == None:
            return False
        #iterate through the nodes in the bucket, if key is found, return true.
        else: 
            for node in bucket:
                if node.key == key:
                    return True
        return False


    def remove(self, key: str) -> None:
        """
        This method removes key-value pair from the hash map. If 
        the key is not in the hash map, the method does nothing.
        """
        #find the correct bucket
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        if bucket == None:
            return
        #iterate through the keys, if match is found, use LL remove() method
        #to remove the key. Then decrement size. 
        else: 
            for node in bucket:
                if node.key == key:
                    bucket.remove(key)
                    self._size -=1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a DA where each index contains a tuple of a
        key-value pair stored in the HM. 
        """
        #create new instance of DA
        new_da = DynamicArray()
        #iterate through all the buckets and all the nodes within the bucket
        for i in range(self._capacity):
            bucket = self._buckets[i]
            for node in bucket:
                pair = (node.key, node.value)
                #append key-value pair to the new_da
                new_da.append(pair)
        return new_da



def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    This function receives a DA and puts its contents in a HM as keys. If 
    the key is already in the HM, its value is incremented by 1. This function
    returns a tuple containing a DA of the most occuring value(s), and how often
    it/they appear. O(N) complexity
    """
    #create new instance of HM
    map = HashMap()
    #for loop loops through all the elements in the DA, and adds them to the HM
    #as keys. If the key is already in the HM, its value is incremented by 1.
    for i in range(da.length()):
        key = da[i]
        if not map.contains_key(key):
            map.put(key, 1)
        else: 
            map.put(key, map.get(key) + 1)
    mode = 0
    #put all the key_value pairs in the variable, and create a new DA to return later.
    new_da = map.get_keys_and_values()
    mode_da = DynamicArray()
    #for looop loops through all the elements of new_da and if mode is less than the 
    #corresponding value of that key, mode is updated. 
    for i in range(new_da.length()):
        value = new_da[i][1]
        if mode < value:
            mode = value
    #this for loop loops through all the elements of the new_da again and appends all
    #keys to the mode_da if their value matches the mode that we found.
    for i in range(new_da.length()):
        if new_da[i][1] == mode:
            mode_da.append(new_da[i][0])
    return mode_da, mode


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
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
