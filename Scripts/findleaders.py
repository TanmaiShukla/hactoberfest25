""
GitHub: https://github.com/VeeruYadav45

def find_leaders(arr: List[int]) -> List[int]:
    """
    Returns a list of leader elements in the array.
    A leader is greater than all elements to its right.
    """
    n = len(arr)
    leaders_list = []
    max_from_right = arr[-1]
    leaders_list.append(max_from_right)

    for i in range(n - 2, -1, -1):
        if arr[i] > max_from_right:
            max_from_right = arr[i]
            leaders_list.append(max_from_right)
    
    # Reverse to maintain original order
    return leaders_list[::-1]

def main():
    arr = [16, 17, 4, 3, 5, 2]
    result = find_leaders(arr)
    print("Leaders in the array:", result)

if __name__ == "__main__":
    main()
