

import random

class VacuumCleanerAgent:
    def __init__(self, room_a, room_b, position):
        self.rooms = {
            "A": room_a,
            "B": room_b
        }
        self.position = position

    def perceive_and_act(self):
        current_room = self.rooms[self.position]

        print(f"\nAgent is in Room {self.position}")
        print(f"Room {self.position} is {current_room}")

        # Simple Reflex Rules
        if current_room == "Dirty":
            print("Action: SUCK")
            self.rooms[self.position] = "Clean"

        elif self.position == "A":
            print("Action: MOVE RIGHT")
            self.position = "B"

        elif self.position == "B":
            print("Action: MOVE LEFT")
            self.position = "A"

    def display(self):
        print(f"Room A: {self.rooms['A']}")
        print(f"Room B: {self.rooms['B']}")
        print(f"Agent Position: {self.position}")


# Initial environment
room_a = random.choice(["Clean", "Dirty"])
room_b = random.choice(["Clean", "Dirty"])
position = random.choice(["A", "B"])

agent = VacuumCleanerAgent(room_a, room_b, position)

print("\nInitial Environment:")
agent.display()

# Run the agent
for step in range(10):
    agent.perceive_and_act()

    print("\nCurrent Environment:")
    agent.display()

    # Stop when both rooms are clean
    if agent.rooms["A"] == "Clean" and agent.rooms["B"] == "Clean":
        print("\nBoth rooms are clean!")
        print("Task completed.")
        break
