import numpy as np

# Parameters setup based on the given problem 3
costs = {
    "buy": np.array([2, 8, 12, 2, 8, 12, 8, 12]),  # Purchase cost per part
    "test": np.array([1, 1, 2, 1, 1, 2, 1, 2]),  # Testing cost per part
    "assemble": np.array(
        [8, 8, 8, 0, 0, 0, 0, 0]
    ),  # Assembly cost per semi-finished good
    "disassemble": np.array(
        [6, 6, 6, 0, 0, 0, 0, 0]
    ),  # Disassembly cost per semi-finished good
    "sell": 200,  # Market price of the final product
    "exchange_loss": 40,  # Exchange loss per returned product
    "final_test": 6,  # Testing cost of the final product
    "final_assembly": 8,  # Assembly cost of the final product
}

# Failure rates
failure_rates = {
    "parts": np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
    "semi_products": np.array([0.1, 0.1, 0.1]),
    "final_product": 0.1,
}

# Initial inventory of parts (all available at start)
inventory = np.array([100, 100, 100, 100, 100, 100, 100, 100])

# Decision variables: Test or not (1 if testing, 0 if not)
decisions = {
    "test_parts": np.array([1, 1, 1, 1, 1, 1, 1, 1]),
    "assemble_semi": np.array([1, 1, 1]),  # Decision to assemble semi-finished products
    "test_final": 1,  # Decision to test the final product
    "disassemble_final": 1,  # Decision to disassemble the final product
}


# Simulating the production process based on MDP model
def simulate_production(decisions, inventory, failure_rates, costs):
    # Calculate total costs and revenues
    total_cost = 0
    total_revenue = 0

    # Testing parts
    if decisions["test_parts"].all():
        test_costs = np.sum(inventory * costs["test"])
        total_cost += test_costs
        # Adjust inventory based on testing and failure rates
        inventory = inventory * (1 - failure_rates["parts"])

    # Assemble semi-products
    semi_finished = np.minimum.reduce(
        [inventory[i] for i in range(len(failure_rates["parts"]))]
    )
    if decisions["assemble_semi"].all():
        assembly_costs = np.sum(semi_finished * costs["assemble"])
        total_cost += assembly_costs
        # Adjust for failures in semi-products
        semi_finished = semi_finished * (
            1 - failure_rates["semi_products"][0]
        )  # Simplified for one type of semi-product

    # Final product assembly
    if decisions["test_final"]:
        final_product = semi_finished * (1 - failure_rates["final_product"])
        final_test_cost = costs["final_test"] * final_product
        final_assembly_cost = costs["final_assembly"] * final_product
        total_cost += final_test_cost + final_assembly_cost
    else:
        final_product = semi_finished
        final_assembly_cost = costs["final_assembly"] * final_product
        total_cost += final_assembly_cost

    # Revenue from selling final products
    total_revenue = final_product * costs["sell"]

    # Disassemble returned products (if any)
    if decisions["disassemble_final"]:
        returned_products = final_product * failure_rates["final_product"]
        disassemble_cost = returned_products * costs["disassemble"]
        total_cost += disassemble_cost + returned_products * costs["exchange_loss"]
        # Reintegrate disassembled parts (simplified: immediate re-use)
        inventory += returned_products

    # Net profit calculation
    net_profit = total_revenue - total_cost

    return net_profit, total_cost, total_revenue


# Running the simulation
net_profit, total_cost, total_revenue = simulate_production(
    decisions, inventory, failure_rates, costs
)
net_profit, total_cost, total_revenue
