import os

""" 
Building on the code of 0-1 knapsack problem,extend the solution by incorporating the following constraints: 
1. The total weight of the selected items must be an odd number . 
2. The total price of the selected items must be an even number.  
"""


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

    # 3. Build the dynamic programming table
    n = len(items)
    
    # 4D table: dp_table[i][w][weight_parity][price_parity]
    # Initialize 4D table with:
        #   Base case: dp_table[0][w][0][0] = 0 (0 items used, weight 0 is even, price 0)
        #   All other base cases are -1 (meaning unreachable state)
    dp_table = [[[[-1 for _ in range(2)] for _ in range(2)] for _ in range(capacity + 1)]  for _ in range(n + 1)]
    
    for w in range(capacity + 1):
        dp_table[0][w][0][0] = 0

    # Fill the table
    for i in range(1, n + 1):
        item_id, weight, price = items[i - 1]
        
        for w in range(capacity + 1):
            # Copy states from the row above (assume NOT picking item i)
            for w_par in range(2):
                for p_par in range(2):
                    dp_table[i][w][w_par][p_par] = dp_table[i - 1][w][w_par][p_par]
            
            # Try to pick item i
            if weight <= w: 
                item_w_par = weight % 2
                item_p_par = price % 2
                
                for w_par in range(2):
                    for p_par in range(2):
                        # Find the previous state needed to reach current state:
                        """ 
                        Suppose our target parity for weight is Odd (1). If the item we are picking has Odd (1) weight, then the previous weight must have been Even (0), match (1 - 1) % 2 = 0. 
                        
                        Suppose our target parity for weight is Even (0).If the item we are picking has Odd (1) weight, the previous weight must have been Odd (1), match(0 - 1) % 2 = 1.
                        
                        Same for price.
                         
                        This is because Python's % 2 always returns 0 or 1.
                        """
                        prev_w_par = (w_par - item_w_par) % 2
                        prev_p_par = (p_par - item_p_par) % 2
                        
                        prev_val = dp_table[i - 1][w - weight][prev_w_par][prev_p_par]
                        
                        # If the previous state is reachable (prev_val != -1), update max value
                        if prev_val != -1: 
                            dp_table[i][w][w_par][p_par] = max(dp_table[i][w][w_par][p_par],prev_val +price)

    # 4. Find the optimal value with constraints
    # We need: total weight odd (w_par = 1), total price even (p_par = 0)
    max_value = dp_table[n][capacity][1][0]

    selected_items = []
    
    if max_value == -1:
        print("Done!")
        print("Result:")
        print("-" * 66)
        print("No valid solution exists for the given input data.")
        print("-" * 66)
        return  # Exit early, no solution to output

    # 5. Backtrack to find which items were selected
    w = capacity
    target_w_par = 1  # total weight must be odd
    target_p_par = 0  # total price must be even

    for i in range(n, 0, -1):
        # Check if the current state value differs from the row above
        if dp_table[i][w][target_w_par][target_p_par] != dp_table[i - 1][w][target_w_par][target_p_par]:
            item_id, weight, price = items[i - 1]
            selected_items.append(item_id)
            
            # Update remaining capacity and required parities
            w -= weight
            target_w_par = (target_w_par - (weight % 2)) % 2
            target_p_par = (target_p_par - (price % 2)) % 2

    selected_items.reverse()

    # 6. Print results to console
    print("Done!")
    print("Result:")
    print("-" * 66)
    print(f"Total Value: {max_value}")
    print(f"Item ID List: {', '.join(map(str, selected_items))}")
    print("-" * 66)

    # 7. Write DP table to dynamic_table.txt
    # Since the DP table is now 4D, we will output the optimal state (w_parity=1, p_parity=0) 
    # for each item and capacity, as this represents the solution path.
    print("Outputting dynamicTable.txt...")
    try:
        with open("dynamic_table.txt", "w") as f:
            for i in range(n + 1):
                row_str = " ".join(str(dp_table[i][w][1][0]) for w in range(capacity + 1))
                f.write(row_str + "\n")
    except IOError as e:
        print(f"Error writing output file: {e}")
        return

    print("Done!")
    print("End of Processing.")


if __name__ == "__main__":
    simple_knapsack()