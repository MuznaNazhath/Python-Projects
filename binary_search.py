# Implementation of binary search algorithm

import random
import time

# naive search using linear search approach


def naive_search(l, target):
    # example l = [1, 2, 8, 10, 5]
    for i in range(len(l)):
        if l[i] == target:  # Check if the current element is the target
            return i    # Return the index of the target element
    return -1  # Return -1 if the target is not found in the list


# binary search using devide and conquer approach
def binary_search(l, target, low=None, high=None):
    # example l = [1, 2, 8, 10, 5]
    if low is None:
        low = 0
    if high is None:
        high = len(l) - 1
    if low > high:
        return -1  # Base case: target not found

    # Calculate the middle index
    mid = (low + high) // 2
    if l[mid] == target:
        return mid
    elif l[mid] < target:
        return binary_search(l, target, mid + 1, high)
    else:
        return binary_search(l, target, low, mid - 1)


if __name__ == "__main__":
    # Example usage
    # l = [1, 2, 8, 10, 5]
    # target = 10
    # print("Naive Search:", naive_search(l, target))
    # print("Binary Search:", binary_search(l, target))

    length = 10000
    # Generate a sorted list of random integers
    sorted_list = set()
    while len(sorted_list) < length:
        sorted_list.add(random.randint(-3*length, 3*length))
    sorted_list = sorted(list(sorted_list))

    start = time.time()
    for target in sorted_list:
        naive_search(sorted_list, target)
    end = time.time()
    print("Naive Search Time:", (end - start)/length, "seconds")

    start = time.time()
    for target in sorted_list:
        binary_search(sorted_list, target)
    end = time.time()
    print("Binary Search Time:", (end - start)/length, "seconds")
