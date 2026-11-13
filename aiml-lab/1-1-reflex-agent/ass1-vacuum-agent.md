Name: Lakshya Shrivastav

PRN: 202401040338@mitaoe.ac.in

Roll: 321


# Implementation of Intelligent Agent: Simple Reflex Agent

## Aim

To implement a **Simple Reflex Intelligent Agent** using a Vacuum Cleaner Agent and demonstrate the **PEAS (Performance Measure, Environment, Actuators, Sensors)** description of its task environment.

## Problem Description

The environment consists of two rooms, **A** and **B**. Each room can either be **Clean** or **Dirty**.

The vacuum cleaner agent can perform three actions:

- **Suck** – cleans the current room.
- **Move Right** – moves from Room A to Room B.
- **Move Left** – moves from Room B to Room A.

The agent uses the current room location and the current room's cleanliness as its percepts.

## PEAS Description

| Component | Description |
|---|---|
| **Performance Measure** | Keep both rooms clean while minimizing unnecessary actions and movement. |
| **Environment** | Two rooms, A and B. Each room can be Clean or Dirty. |
| **Actuators** | Suck, Move Left, Move Right. |
| **Sensors** | Detect the agent's current room and whether that room is Clean or Dirty. |

## Method

The agent follows simple condition-action rules:

1. If the current room is **Dirty**, the agent performs **Suck**.
2. If the current room is **Clean** and the agent is in **Room A**, it moves **Right** to Room B.
3. If the current room is **Clean** and the agent is in **Room B**, it moves **Left** to Room A.
4. The process continues until both rooms are clean.

This is a **Simple Reflex Agent** because the agent selects an action based only on the current percept. It does not maintain a history of previous states or an internal model of the environment.

## Python Implementation

```python
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
```

## Sample Execution

For the initial state:

```text
Room A: Dirty
Room B: Dirty
Agent Position: A
```

The agent performs:

```text
Agent is in Room A
Room A is Dirty
Action: SUCK

Agent is in Room A
Room A is Clean
Action: MOVE RIGHT

Agent is in Room B
Room B is Dirty
Action: SUCK

Both rooms are clean!
Task completed.
```

## Result

The Vacuum Cleaner Agent successfully identifies the state of its current room and performs the appropriate action using simple condition-action rules. Both rooms are cleaned successfully, demonstrating the working of a **Simple Reflex Intelligent Agent** and its **PEAS task environment**.
