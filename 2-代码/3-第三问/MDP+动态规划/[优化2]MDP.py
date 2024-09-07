import numpy as np
from itertools import product
from joblib import Parallel, delayed

# Constants for the problem
NUM_COMPONENTS = 8
NUM_HALF_PRODUCTS = 3
NUM_FINAL_PRODUCTS = 1
DISCOUNT_FACTOR = 0.9
MAX_ITERATIONS = 1000
CONVERGENCE_THRESHOLD = 1e-4

# Define costs and revenue details (example values)
components = [
    {"defect_rate": 0.1, "purchase_cost": 2, "inspection_cost": 1},
    # Add remaining components with similar structure
]
half_products = [
    {
        "defect_rate": 0.1,
        "assembly_cost": 8,
        "inspection_cost": 4,
        "disassembly_cost": 6,
    },
    # Add remaining half-products with similar structure
]
final_product = {
    "defect_rate": 0.1,
    "assembly_cost": 8,
    "inspection_cost": 6,
    "disassembly_cost": 10,
    "market_price": 200,
    "exchange_loss": 40,
}

# Define possible actions and states
actions = list(product(["inspect", "not_inspect"], repeat=NUM_COMPONENTS))
states = list(
    product([0, 1], repeat=NUM_COMPONENTS + NUM_HALF_PRODUCTS + NUM_FINAL_PRODUCTS)
)


# Reward function
def reward(state, action):
    # Example calculation for components
    component_costs = sum(
        c["inspection_cost"] if act == "inspect" else 0
        for c, act in zip(components, action)
    )
    revenue = final_product["market_price"] * (1 - final_product["defect_rate"])
    total_cost = (
        component_costs + final_product["exchange_loss"] * final_product["defect_rate"]
    )
    return revenue - total_cost


# Transition probability function
def transition_probability(state, action, next_state):
    # Example transition probability
    return 1.0 if next_state == state else 0.0


# Function to compute state values
def compute_state_value(s, V, states, actions):
    state = states[s]
    return max(
        reward(state, action)
        + DISCOUNT_FACTOR
        * sum(
            transition_probability(state, action, next_state)
            * V[states.index(next_state)]
            for next_state in states
        )
        for action in actions
    )


# Main execution code for value iteration
V = np.zeros(len(states))
for iteration in range(MAX_ITERATIONS):
    print(f"Iteration {iteration + 1} starting...")
    new_V = Parallel(n_jobs=-1)(
        delayed(compute_state_value)(s, V, states, actions) for s in range(len(states))
    )
    delta = np.max(np.abs(V - new_V))
    V = new_V
    print(f"Iteration {iteration + 1} completed. Max delta: {delta:.6f}")
    if delta < CONVERGENCE_THRESHOLD:
        print(f"Converged after {iteration + 1} iterations.")
        break

# Output optimal policy
policy = {
    state: max(
        actions,
        key=lambda a: reward(state, a)
        + DISCOUNT_FACTOR
        * np.clip(
            sum(
                transition_probability(state, a, next_state)
                * V[states.index(next_state)]
                for next_state in states
            ),
            -1e10,
            1e10,
        ),
    )
    for state in states
}

print("Optimal Policy:")
for state, action in policy.items():
    print(f"State {state}: {action}")
