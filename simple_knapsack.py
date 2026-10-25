import os


def simple_knapsack():
    # 1. Prompt user for the data file name or path
    while True:
        file_name = input("0-1 Knapsack Problem \n Please enter the data file name or path: ").strip()
        if os.path.exists(file_name):
            break
        print(f"Error: The file '{file_name}' was not found. Please try again.")

    # 2. Read and parse the input file
    print("Processing...")
    try:
        with open(file_name, 'r') as f:
            lines = f.readlines()

        # First line = capacity
        capacity = int(lines[0].strip())

        # Subsequent lines = items
        items = []
        for line in lines[1:]:
            parts = line.strip().split()
            if parts:
                items.append([int(parts[0]), int(parts[1]), int(parts[2])])

    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 3. Build the dynamic programming table:dp_table[i][w] 
    n = len(items)
    dp_table = [[0 for j in range(capacity + 1)] for i in range(n + 1)] #(n+1)x(w+1)

    for i in range(1, n + 1):                                   # since dp_table[0][j] == 0: no item
        item_id, weight, price = items[i - 1]
        for w in range(capacity + 1):                           #w=0 => dp_table[i][0]==0, 
            if weight <= w:
                dp_table[i][w] = max(
                    dp_table[i - 1][w],                          # NOT pick item i
                    dp_table[i - 1][w - weight] + price          # pick item i
                )
            else:
                dp_table[i][w] = dp_table[i - 1][w]              # weight > w, can't pick

    # 4. Backtrack to find which items were selected
    selected_items = []
    w = capacity

    for i in range(n, 0, -1):                                    #check n,n-1,n-2....1
        if dp_table[i][w] != dp_table[i - 1][w]:                 # item i was used
            item_id, weight, price = items[i - 1]                # item i index: [i - 1] in item list, [i] in dp_table
            selected_items.append(item_id)
            w -= weight
        if w == 0:                                              # guaranteed by dp-table, w<0 will never happen.
            break

    selected_items.reverse()                                     # restore original order

   
    # 5. Print results to console
    print("Done!")
    print("Result:")
    print("-" * 66)
    print(f"Total Value: {dp_table[n][capacity]}")
    print(f"Item ID List: {', '.join(map(str, selected_items))}")
    print("-" * 66)

    # 6. Write DP table to dynamic_table.txt
    print("Outputting dynamicTable.txt...")
    try:
        with open("dynamic_table.txt", "w") as f:
            for row in dp_table:
                f.write(" ".join(map(str, row)) + "\n")
    except IOError as e:
        print(f"Error writing output file: {e}")
        return

    print("Done!")
    print("End of Processing.")


if __name__ == "__main__":
    simple_knapsack()