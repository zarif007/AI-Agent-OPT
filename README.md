# Architecture & Design

Our system follows a **multi-agent, DAG-based (Directed Acyclic Graph) architecture**. A single user prompt can be orchestrated into multiple tool invocations, where execution order is governed by **`TOOL_PRIORITY`**.

Each tool execution is strictly dependent on the successful completion of its prerequisite tasks. This ensures deterministic flow control and eliminates race conditions between interdependent tasks.

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
