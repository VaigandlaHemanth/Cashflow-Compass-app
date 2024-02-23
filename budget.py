class BudgetingTool:
    def __init__(self, budget):
        self.users = {}  # Format: {user_name: {"priority": priority, "items": []}}
        self.budget = budget
        self.base_score = 1000  # Starting score for Elo rating adaptation
        self.k_factor = 32  # K-factor for Elo adjustments

    def add_user(self, user_name, priority):
        if user_name not in self.users:
            self.users[user_name] = {"priority": priority, "items": []}
        else:
            print(f"User {user_name} already exists.")

    def add_item(self, user_name, item_name, cost, time_range, need, item_priority, compulsory=False):
        if user_name in self.users:
            # Normalize need from 0-100 scale to 0-1 scale
            normalized_need = need / 100
            item = {
                "name": item_name,
                "cost": cost,
                "time_range": time_range,
                "need": normalized_need,
                "priority": item_priority,
                "compulsory": compulsory,
                "score": self.base_score  # Initialize every item with the base score
            }
            self.users[user_name]["items"].append(item)
        else:
            print(f"User {user_name} not found. Please add the user before adding items.")

    def allocate_budget(self):
        compulsory_cost = sum(item["cost"] for user in self.users.values() for item in user["items"] if item["compulsory"])
        if compulsory_cost > self.budget:
            raise ValueError("Budget insufficient for all compulsory items.")
        available_budget = self.budget - compulsory_cost

        self.calculate_item_scores()

        # Filter and sort non-compulsory items by score (descending)
        non_compulsory_items = [(user_name, item) for user_name, user in self.users.items() for item in user["items"] if not item["compulsory"]]
        sorted_items = sorted(non_compulsory_items, key=lambda x: x[1]["score"], reverse=True)

        purchased_items = []
        compulsory_items= [(user_name, item) for user_name, user in self.users.items() for item in user["items"] if item["compulsory"]]

        for user_name, item in sorted_items:
                purchased_items.append((user_name, item["name"]))

        for user_name, item in sorted_items:
            if item["cost"] <= available_budget:
                available_budget -= item["cost"]
                purchased_items.append((user_name, item["name"]))
            else:
                # Stop if the next item cannot be purchased due to budget constraints
                break
                
        return purchased_items, available_budget

    def calculate_item_scores(self):
        # Adjust item scores based on priority and need using an Elo-like system
        for user in self.users.values():
            for item in user["items"]:
                expected_score = 1 / (1 + 10 ** ((self.base_score - item["score"]) / 400))
                score_adjustment = self.k_factor * (item["need"] - expected_score)
                item["score"] += score_adjustment

    def display_sorted_items(self):
        all_items = [(user_name, item) for user_name, user in self.users.items() for item in user["items"]]
        sorted_items = sorted(all_items, key=lambda x: x[1]["score"], reverse=True)
        for user_name, item in sorted_items:
            print(f"{user_name}: {item['name']} (Score: {item['score']}, Cost: {item['cost']}, Priority: {item['priority']}, Need: {item['need']*100})")

# Example usage
budget_tool = BudgetingTool(1250)
budget_tool.add_user("John Doe", 1)
budget_tool.add_user("Jane Doe", 2)
budget_tool.add_item("John Doe", "Laptop", 1000, 6, 100, 1, compulsory=True)
budget_tool.add_item("Jane Doe", "Desk Chair", 200, 2, 80, 2)
budget_tool.add_item("John Doe", "Office Desk", 250, 3, 60, 2)

purchased_items, remaining_budget = budget_tool.allocate_budget()
print("Purchased items:", purchased_items)
print("Remaining budget:", remaining_budget)
budget_tool.display_sorted_items()
