# Architecture & Design

Our system follows a **multi-agent, DAG-based (Directed Acyclic Graph) architecture**. A single user prompt can be orchestrated into multiple tool invocations, where execution order is governed by **`TOOL_PRIORITY`**.

To facilitate smooth data handoff between tasks, we have introduced a **Context Manager**. It maintains the execution context of previously completed tasks, making their outputs readily accessible for downstream tasks. As a result, every tool operates with the most relevant, updated context, significantly reducing redundancy and improving orchestration efficiency.

<p align="center">
  <img src="assets/dag.png" alt="DAG Architecture" width="600"/>
</p>

### Example DAG Flow

Consider the user prompt:
_"Add 10 to the average temperature in Paris and London right now."_

The orchestration layer builds the following DAG:

- **Tool A (Temp Tool)**

  - Fetches the current temperature in Paris.
  - No dependencies.

- **Tool B (Temp Tool)**

  - Fetches the current temperature in London.
  - No dependencies.

- **Tool C (Calc Tool)**

  - Computes the average of Paris and London temperatures.
  - Adds 10 to the computed average.
  - **Depends on Tool A and Tool B**.

# Installation & Running

There is a `Makefile` to simplify setup, testing, and running. You can either use the provided make targets or follow the manual steps.

---

### Using Makefile

Ensure you have **Python 3.9+** installed.

1. **Setup the virtual environment and install dependencies:**

   ```bash
   make setup
   ```

2. **Run tests (pytest):**

   ```bash
   make test
   ```

3. **Run the agent with a sample prompt:**

   ```bash
   make run
   ```

4. **Format code (placeholder – configure with your formatter, e.g., black/isort):**

   ```bash
   make fmt
   ```

---

### Manual Setup

If you prefer not to use `make`:

1. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests:**

   ```bash
   python -m pytest tests/test_smoke.py
   ```

4. **Run the agent with a sample prompt:**

   ```bash
   python main.py "What is 12.5% of 243?"
   ```
