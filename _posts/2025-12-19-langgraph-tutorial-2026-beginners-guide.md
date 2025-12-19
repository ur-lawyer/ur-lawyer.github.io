---
    layout: post
    title: "LangGraph Tutorial 2026: Complete Beginner's Guide to Building AI Agents"
    description: "Learn about langgraph tutorial 2026 and make informed decisions."
    author: Mary
    tags: [langgraph tutorial 2026]
    featured: false
    image: '/images/langgraph-tutorial-2026-beginners-guide.webp'
    ---

```markdown
---
layout: post
title: LangGraph Tutorial 2026 Complete Beginner's Guide to Building AI Agents
author: AI Tutorial Master
date: 2026-01-01 10:00:00 +0000
categories: [AI, LangGraph, Tutorials]
tags: [langgraph tutorial 2026, AI agents, machine learning, beginner guide, python]
---

## LangGraph Tutorial 2026: Complete Beginner's Guide to Building AI Agents

Imagine having a smart helper that doesn't just answer questions but can also think, plan, and take steps to solve problems. These are called AI agents, and they are like having a mini-robot brain working for you. In this complete "langgraph tutorial 2026," you will learn how to build these amazing AI agents from scratch.

LangGraph is a fantastic tool that helps you create these intelligent agents by mapping out their thought process like a flow chart. It lets you design how your agent will make decisions and move through different steps to reach a goal. You're about to embark on an exciting journey to build powerful AI systems.

This "langgraph tutorial 2026" is made for you, even if you are just starting out with coding and AI concepts. We'll use simple language and lots of examples to guide you every step of the way. By the end, you'll have a good understanding of how to make your own thinking agents.

## What is LangGraph? Understanding the Basics

LangGraph is a library that helps you build "stateful" multi-actor applications with Large Language Models (LLMs). This means you can create AI agents that remember what happened before and work together. Think of it like a director for a play, telling different actors (LLMs, tools, functions) when to speak and what to do next.

It extends the ideas from LangChain, focusing on how agents can go through several steps to complete a task. Instead of a single back-and-forth chat, LangGraph allows for complex decision-making loops. Your agent can try something, see if it worked, and then try something else if needed.

LangGraph helps you draw a map of your agent's brain, showing different steps and choices. This makes it easier to build agents that can do more complicated things than just answer one question. This "langgraph tutorial 2026" will show you exactly how to do this.

## Installation and Setup: Getting Started with LangGraph

Before we can build anything, we need to set up our workspace. This part of the "langgraph tutorial 2026" will guide you through getting all the necessary software installed. It’s like gathering all your LEGO bricks before you start building.

First, you need Python installed on your computer. If you don't have it, you can download it from the official Python website. We'll also use a virtual environment to keep our project tidy.

Here are the simple steps for the installation and setup process. Open your terminal or command prompt and follow along carefully.

```bash
# 1. Create a new directory for your project
mkdir langgraph_agent_tutorial
cd langgraph_agent_tutorial

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 4. Install LangGraph and LangChain Core
# LangChain Core provides the basic building blocks that LangGraph uses.
pip install langgraph langchain_core

# 5. Install an LLM provider (e.g., OpenAI)
# You'll need an API key for this, which we'll set up next.
pip install openai
```

Next, you'll need an API key for your chosen Large Language Model, like OpenAI. These keys allow your code to talk to the powerful AI models. It is very important to keep your API keys secret.

You should never put your API key directly in your code. Instead, store it as an environment variable. Create a file named `.env` in your project folder and add your key like this:

```
OPENAI_API_KEY="your_openai_api_key_here"
```

Then, in your Python script, you can load it using the `dotenv` library. Don't forget to install `python-dotenv` first:

```bash
pip install python-dotenv
```

Now, in your Python code, you can load the keys like this:

```python
import os
from dotenv import load_dotenv

load_dotenv() # This line loads the variables from .env

# Now you can access your key
openai_api_key = os.getenv("OPENAI_API_KEY")
print("API key loaded successfully!" if openai_api_key else "API key not found!")
```

This completes our initial installation and setup. You are now ready to start building your first AI agent following this "langgraph tutorial 2026."

## Defining Your Agent's Brain: State Schema

Every good plan starts with understanding what information you need to keep track of. For our AI agent, this is called the "state schema." It's like the agent's memory or a whiteboard where it writes down important things it needs to remember as it works. This is a crucial step in our "langgraph tutorial 2026."

The state schema defines all the variables that will be passed between different steps of your agent's thinking process. For example, an agent might need to remember the conversation history, what tools it has used, or any errors it encountered. You define this using a special Python dictionary-like object.

In LangGraph, you typically define your state using `TypedDict` from the `typing` module. This makes it clear what kind of information each part of the state should hold. Let's look at a simple example for this "langgraph tutorial 2026."

```python
from typing import List, Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_message

# This is our agent's memory or "state"
# It remembers a list of messages (the conversation)
# And any tool calls it decided to make
class AgentState(TypedDict):
    """
    Represents the state of our agent's conversation.
    - messages: A list of messages making up the conversation.
    - tool_calls: A list of tool calls the agent wants to execute.
    """
    messages: Annotated[List[BaseMessage], add_message]
    # We'll add more things here later, like tool_calls or specific outputs
```

In this `AgentState`, `messages` is a list of `BaseMessage` objects. `Annotated[List[BaseMessage], add_message]` tells LangGraph that whenever we update the `messages` part of our state, new messages should be added to the list, not replace it. This is super helpful for keeping a conversation history.

You can add other things to your state schema as your agent becomes more complex. For instance, you might want to track if a specific task is done, or store temporary results from a tool. Defining state schema well is key to a robust agent.

## Creating Your First LangGraph Agent: A Simple Workflow

Now that we understand the state, let's build our very first LangGraph agent. This part of the "langgraph tutorial 2026" will walk you through setting up a simple agent that can chat. We'll start with just one node, a brain node (LLM), and connect it to itself to keep the conversation going.

LangGraph uses `StateGraph` to define the agent's workflow. You add "nodes" (which are like steps or actions) and "edges" (which tell the agent where to go next). Think of it like drawing a simple flow chart for your agent's thoughts.

Let's make an agent that simply takes your message and responds using an LLM. For this, you'll need your OpenAI API key set up as we discussed in the installation and setup section.

```python
import os
from dotenv import load_dotenv
from typing import List, Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_message
from langchain_openai import ChatOpenAI

load_dotenv() # Load environment variables

# 1. Define the AgentState (as we did before)
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_message]

# 2. Define the LLM (our agent's brain)
llm = ChatOpenAI(model="gpt-4o", temperature=0) # You can choose another model

# 3. Create a node function for our LLM
# A "node" is just a Python function that takes the current state and returns an update to it.
def call_llm(state: AgentState):
    """
    This node calls the LLM with the current conversation history and adds the AI's response to the state.
    """
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]} # Add the AI's response to the state

# 4. Build the LangGraph
workflow = StateGraph(AgentState)

# Add the 'call_llm' function as a node named "llm_node"
workflow.add_node("llm_node", call_llm)

# Set the entry point for our graph
# START means the graph begins by sending messages to "llm_node"
workflow.set_entry_point("llm_node")

# Set the exit point for our graph
# END means after the LLM responds, the process is complete for this turn
workflow.set_finish_point("llm_node")

# 5. Compile the graph
app = workflow.compile()

# 6. Let's run our first agent!
print("--- Simple Chat Agent ---")
inputs = {"messages": [HumanMessage(content="Hello, what's up?")]}
for s in app.stream(inputs):
    if "__end__" not in s:
        print(s)
        print("---")

print("\n--- Another interaction ---")
inputs = {"messages": [HumanMessage(content="Tell me a fun fact about cats.")]}
for s in app.stream(inputs):
    if "__end__" not in s:
        print(s)
        print("---")
```

When you run this code, you will see your agent processing the message and responding. This simple `StateGraph` takes the starting message, sends it to the `llm_node`, and then finishes. The `add_message` annotation ensures that the new AI message is added to the list, creating a conversation.

This is a very basic agent, but it forms the core understanding of how LangGraph works. You've just built your first LangGraph agent, a key milestone in this "langgraph tutorial 2026."

## Understanding StateGraph Nodes and Edges: The Building Blocks

To build truly intelligent agents, you need to deeply understand the two main components of LangGraph: nodes and edges. They are the fundamental building blocks, much like bricks and mortar for a house. This section of the "langgraph tutorial 2026" will clarify these concepts.

### Nodes: The Action Steps

Nodes are the individual steps or actions your agent can take. Each node is a Python function that receives the current `AgentState` and returns an update to that state. A node can do many things:

*   **Call an LLM:** Like our `call_llm` function, it sends messages to a language model and gets a response.
*   **Use a Tool:** Execute a specific function, like searching the internet, doing math, or interacting with a database.
*   **Process Information:** Analyze the current state, summarize text, extract data, or format output.
*   **Make a Decision:** Determine the next step based on the current information.

You add nodes to your `StateGraph` using `workflow.add_node("node_name", your_function)`.

### Edges: The Flow of Thought

Edges define how information flows between nodes. They tell the agent where to go next after a node has finished its work. There are two main types of edges:

1.  **Direct Edges (`add_edge`):** These are simple, straight paths. After `Node A` finishes, the agent unconditionally moves to `Node B`.
    *   `workflow.add_edge("node_a", "node_b")` means `node_b` always runs after `node_a`.
    *   `workflow.set_entry_point("node_a")` makes `node_a` the first node.
    *   `workflow.set_finish_point("node_b")` makes `node_b` the last node, ending the current cycle.

2.  **Conditional Edges (`add_conditional_edges`):** These are like crossroads where the agent makes a choice about where to go next. After `Node A` finishes, a special "router" function decides which of several possible next nodes to visit.
    *   The router function takes the `AgentState` and returns the name of the next node (as a string).
    *   `workflow.add_conditional_edges("node_a", router_function, {"choice_1": "node_b", "choice_2": "node_c"})`
    *   The router can also return `END` to finish the process.

Let's expand our example to show a simple conditional edge. We'll add a dummy "tool" node and a router. This is vital for understanding this "langgraph tutorial 2026" deeply.

```python
# ... (imports and AgentState definition remain the same) ...

# 1. Define the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 2. Node to call the LLM
def call_llm_node(state: AgentState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# 3. A dummy tool node
def use_tool_node(state: AgentState):
    print("Agent is using a tool now!")
    # In a real scenario, this would call an actual tool
    tool_response = HumanMessage(content="Tool says: 'Operation successful!'")
    return {"messages": [tool_response]}

# 4. A router function to decide the next step
def decide_next_step(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]

    # For simplicity, let's say if the LLM's response contains "tool", we go to the tool node.
    # Otherwise, we end.
    if "tool" in last_message.content.lower():
        print("Router decided: Go to tool_node")
        return "tool_node"
    else:
        print("Router decided: END")
        return END

# 5. Build the LangGraph workflow
workflow = StateGraph(AgentState)

workflow.add_node("llm_node", call_llm_node)
workflow.add_node("tool_node", use_tool_node)

workflow.set_entry_point("llm_node")

# After llm_node, we conditionally decide if we need a tool or if we are done.
workflow.add_conditional_edges(
    "llm_node", # From this node
    decide_next_step, # Use this function to decide
    {
        "tool_node": "tool_node", # If router returns "tool_node", go to "tool_node"
        END: END # If router returns END, finish
    }
)

# After the tool node, we can either loop back to the LLM (for it to see tool results)
# or end. For this example, let's just end after the tool for simplicity.
workflow.add_edge("tool_node", END) # Tool node always ends for now

app = workflow.compile()

# 6. Run the agent with different inputs
print("--- Agent Interaction 1 (No tool needed) ---")
inputs1 = {"messages": [HumanMessage(content="What is the capital of France?")]}
for s in app.stream(inputs1):
    if "__end__" not in s:
        print(s)
        print("---")

print("\n--- Agent Interaction 2 (Tool suggested by LLM) ---")
inputs2 = {"messages": [HumanMessage(content="I need help with a calculation. Say 'I need a tool' if you want to use a tool.")]}
for s in app.stream(inputs2):
    if "__end__" not in s:
        print(s)
        print("---")
```

In the second interaction, the `llm_node` responds, and our simple `decide_next_step` router sees the word "tool" and directs the flow to `tool_node`. This demonstrates the power of conditional routing within a "langgraph tutorial 2026."

## Adding Tools to Your Agents: Giving Them Superpowers

AI agents become truly powerful when they can interact with the outside world. This is where "tools" come in. Tools are functions that your agent can choose to use, like a calculator, a web search engine, or a database query. In this "langgraph tutorial 2026," you'll learn how to equip your agent with these superpowers.

LangChain provides a simple way to define tools. You just write a regular Python function and then decorate it with `@tool`. This tells LangChain (and thus LangGraph) that this function can be used by an LLM. The LLM can then "call" these tools when it thinks they are relevant to solve a problem.

Let's add a simple calculator tool to our agent. This will be a great practical example for this "langgraph tutorial 2026."

```python
# ... (imports and AgentState definition) ...

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import format_to_openai_tool_messages

load_dotenv()

# Define our calculator tool
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers together."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds two integers together."""
    return a + b

# List of tools our agent can use
tools = [multiply, add]

# Define the LLM, now with tool calling capabilities
# We pass the tools to the LLM so it knows what's available
llm_with_tools = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

# Node to call the LLM
def call_llm_with_tools_node(state: AgentState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Node to execute tools
def execute_tools_node(state: AgentState):
    tool_calls = state["messages"][-1].tool_calls # Get tool calls from the last AI message
    results = []
    for tool_call in tool_calls:
        # Here we manually execute the tool. LangGraph has a built-in ToolNode as well.
        if tool_call['name'] == "multiply":
            result = multiply.invoke(tool_call['args'])
        elif tool_call['name'] == "add":
            result = add.invoke(tool_call['args'])
        else:
            raise ValueError(f"Unknown tool: {tool_call['name']}")
        
        # Add the tool's output back to the messages
        results.append(HumanMessage(content=str(result), name=tool_call['name']))
    return {"messages": results}


# Router to decide next step
def decide_next_step_with_tools(state: AgentState):
    last_message = state["messages"][-1]
    # If the LLM has decided to call a tool
    if last_message.tool_calls:
        print("Router decided: LLM wants to use a tool, go to execute_tools_node")
        return "execute_tools_node"
    # Otherwise, if the LLM has a final answer, end
    else:
        print("Router decided: LLM has a final answer, END")
        return END

# Build the LangGraph workflow
workflow = StateGraph(AgentState)

workflow.add_node("llm_node", call_llm_with_tools_node)
workflow.add_node("execute_tools_node", execute_tools_node)

workflow.set_entry_point("llm_node")

# After LLM, decide if a tool is needed or if it's the end
workflow.add_conditional_edges(
    "llm_node",
    decide_next_step_with_tools,
    {
        "execute_tools_node": "execute_tools_node",
        END: END
    }
)

# After executing tools, loop back to the LLM so it can see the tool's result
# This allows the LLM to process the tool's output and generate a final answer
workflow.add_edge("execute_tools_node", "llm_node")

app = workflow.compile()

# Run the agent with tool usage
print("--- Agent Interaction with Tools ---")
inputs = {"messages": [HumanMessage(content="What is 15 multiplied by 4?")]}
for s in app.stream(inputs):
    if "__end__" not in s:
        print(s)
        print("---")

print("\n--- Another calculation ---")
inputs = {"messages": [HumanMessage(content="What is 100 plus 25?")]}
for s in app.stream(inputs):
    if "__end__" not in s:
        print(s)
        print("---")
```

In this enhanced example for our "langgraph tutorial 2026", the LLM now knows about the `multiply` and `add` tools. When you ask it a math question, it will decide to "call" the appropriate tool. The `execute_tools_node` then runs the actual Python function, and the result is fed back to the LLM. The LLM then uses this result to give you the final answer. This iterative process is a core strength of LangGraph agents.

## Conditional Routing Logic: Making Smart Decisions

Conditional routing is the brain of your LangGraph agent, allowing it to make smart decisions and follow different paths based on the current situation. Instead of a rigid script, your agent can adapt, similar to how you would choose different actions based on what happens next. This is a critical concept in any "langgraph tutorial 2026."

We've already seen a glimpse of this with our `decide_next_step` functions. The idea is that after a node finishes its work, a special function looks at the updated `AgentState` and decides which node should run next. This function returns the name of the next node (as a string) or `END` if the process is complete.

The `add_conditional_edges` method in `StateGraph` is where this magic happens. It takes three main arguments:

1.  **`source_node`**: The node that just finished its work.
2.  **`router_function`**: A Python function that takes the `AgentState` and returns a string (the next node's name) or `END`.
3.  **`node_map`**: A dictionary that maps the strings returned by the `router_function` to actual node names in your graph.

Let's refine our previous example to highlight the conditional routing logic even more. We'll make a more explicit router for this "langgraph tutorial 2026."

```python
# ... (imports, AgentState, tools, llm_with_tools definitions) ...

# 1. Define nodes (same as before)
def call_llm_for_routing(state: AgentState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def execute_tools_for_routing(state: AgentState):
    tool_calls = state["messages"][-1].tool_calls
    results = []
    for tool_call in tool_calls:
        if tool_call['name'] == "multiply":
            result = multiply.invoke(tool_call['args'])
        elif tool_call['name'] == "add":
            result = add.invoke(tool_call['args'])
        else:
            raise ValueError(f"Unknown tool: {tool_call['name']}")
        results.append(HumanMessage(content=str(result), name=tool_call['name']))
    return {"messages": results}

# 2. Our enhanced router function
def agent_router(state: AgentState) -> str:
    """
    Decides the next step based on the last message in the state.
    - If the last message suggests tool calls, it goes to the tool execution node.
    - Otherwise, it assumes the LLM has a final answer and ends.
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print(f"Router Decision: Tool call detected for {last_message.tool_calls[0]['name']}. Moving to execute_tools_node.")
        return "execute_tools_node"
    else:
        print("Router Decision: No tool call. Assuming final answer. Ending process.")
        return END

# 3. Build the LangGraph workflow
workflow = StateGraph(AgentState)

workflow.add_node("llm_decision_node", call_llm_for_routing)
workflow.add_node("execute_tools_node", execute_tools_for_routing)

workflow.set_entry_point("llm_decision_node")

# Conditional edge: From 'llm_decision_node', use 'agent_router' to decide next.
workflow.add_conditional_edges(
    "llm_decision_node",
    agent_router,
    {
        "execute_tools_node": "execute_tools_node", # If router returns "execute_tools_node"
        END: END # If router returns END
    }
)

# After executing tools, we want the LLM to see the results and potentially give a final answer.
# So, we loop back to the 'llm_decision_node'.
workflow.add_edge("execute_tools_node", "llm_decision_node")

app = workflow.compile()

# Test cases
print("--- Conditional Routing Test 1: Math Problem ---")
inputs1 = {"messages": [HumanMessage(content="What is 123 times 456?")]}
for s in app.stream(inputs1):
    if "__end__" not in s:
        print(s)
        print("---")

print("\n--- Conditional Routing Test 2: Simple Question ---")
inputs2 = {"messages": [HumanMessage(content="What color is the sky on a clear day?")]}
for s in app.stream(inputs2):
    if "__end__" not in s:
        print(s)
        print("---")
```

In "Conditional Routing Test 1," the LLM will identify the need for multiplication, the `agent_router` will detect the `tool_calls` in the LLM's response and send it to `execute_tools_node`. After the tool runs, the output goes back to `llm_decision_node`, which then provides the final answer and the router sends it to `END`.

In "Conditional Routing Test 2," the LLM directly answers the question, and since there are no `tool_calls`, the `agent_router` immediately sends the flow to `END`. This advanced conditional routing is a cornerstone feature presented in this "langgraph tutorial 2026."

## Complete Working Examples with Code: Putting It All Together

Let's combine everything we've learned in this "langgraph tutorial 2026" into a more complete, practical example. We'll build a simple research agent that can answer questions and, if needed, search the web. This will showcase a multi-step thought process using LangGraph's nodes and conditional routing.

For web searching, we'll use a dummy search tool, but in a real application, you might integrate with a service like DuckDuckGo search or Google Search API. This "langgraph tutorial 2026" example aims to provide a clear, full picture.

```python
import os
from dotenv import load_dotenv
from typing import List, Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_message
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

load_dotenv()

# --- 1. Define Agent State ---
class ResearchAgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_message]
    # We could add more state variables like 'research_topic', 'search_results' etc.

# --- 2. Define Tools ---
@tool
def dummy_web_search(query: str) -> str:
    """
    Performs a dummy web search for the given query.
    In a real application, this would call an actual web search API.
    """
    print(f"DEBUG: Performing dummy web search for: '{query}'")
    if "capital of france" in query.lower():
        return "Paris is the capital and most populous city of France."
    elif "population of tokyo" in query.lower():
        return "The population of Tokyo is over 14 million people."
    elif "who invented the light bulb" in query.lower():
        return "Thomas Edison is widely credited with inventing the practical incandescent light bulb."
    else:
        return f"Dummy search result for '{query}': Information found online suggests relevant data."

# List of tools available to our agent
tools = [dummy_web_search]

# --- 3. Define the LLM with tools ---
llm_with_tools = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

# --- 4. Define Graph Nodes ---

def call_llm_for_research(state: ResearchAgentState):
    """
    Node: Calls the LLM to get a response or determine if a tool is needed.
    """
    print("\nNODE: Calling LLM for research...")
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def execute_research_tools(state: ResearchAgentState):
    """
    Node: Executes any tool calls suggested by the LLM.
    """
    print("\nNODE: Executing research tools...")
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls
    
    results = []
    for tool_call in tool_calls:
        print(f"  Executing tool: {tool_call['name']} with args: {tool_call['args']}")
        if tool_call['name'] == "dummy_web_search":
            tool_output = dummy_web_search.invoke(tool_call['args'])
        else:
            tool_output = f"Error: Unknown tool {tool_call['name']}"
        
        # Add the tool's output back to the messages as a ToolMessage
        results.append(ToolMessage(content=tool_output, name=tool_call['name'], tool_call_id=tool_call['id']))
    
    return {"messages": results}

# --- 5. Define the Router Function ---

def research_router(state: ResearchAgentState) -> str:
    """
    Router: Decides the next step based on the last message from the LLM.
    - If the LLM wants to call a tool, go to 'execute_research_tools'.
    - Otherwise, assume the LLM has a final answer and END.
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print("ROUTER: LLM suggested tool call(s). Routing to 'execute_research_tools'.")
        return "execute_research_tools"
    else:
        print("ROUTER: No tool calls. Assuming final answer. Routing to END.")
        return END

# --- 6. Build the LangGraph Workflow ---

research_workflow = StateGraph(ResearchAgentState)

# Add Nodes
research_workflow.add_node("llm_research_node", call_llm_for_research)
research_workflow.add_node("tool_execution_node", execute_research_tools)

# Set Entry Point
research_workflow.set_entry_point("llm_research_node")

# Define Conditional Edges
research_workflow.add_conditional_edges(
    "llm_research_node",      # From the LLM node
    research_router,          # Use our router to decide
    {
        "execute_research_tools": "tool_execution_node", # If router returns this string
        END: END                                         # If router returns END
    }
)

# Define a Direct Edge
# After tools are executed, loop back to the LLM so it can process the tool's output
research_workflow.add_edge("tool_execution_node", "llm_research_node")

# Compile the graph
research_app = research_workflow.compile()

# --- 7. Run the Research Agent ---

print("--- Research Agent: What is the capital of France? ---")
inputs1 = {"messages": [HumanMessage(content="What is the capital of France?")]}
for s in research_app.stream(inputs1):
    if "__end__" not in s:
        print(s)
        print("---")

print("\n--- Research Agent: Tell me a joke. ---")
inputs2 = {"messages": [HumanMessage(content="Tell me a joke.")]}
for s in research_app.stream(inputs2):
    if "__end__" not in s:
        print(s)
        print("---")

print("\n--- Research Agent: Who invented the light bulb? ---")
inputs3 = {"messages": [HumanMessage(content="Who invented the light bulb?")]}
for s in research_app.stream(inputs3):
    if "__end__" not in s:
        print(s)
        print("---")
```

This full example brings together `AgentState`, `tools`, `LLM` integration, custom nodes (`call_llm_for_research`, `execute_research_tools`), and conditional routing (`research_router`). You can see how the agent decides whether to search or answer directly. This "langgraph tutorial 2026" demonstrates a robust and complete working example.

## Testing and Debugging Tips: Making Your Agent Robust

Building complex AI agents means that sometimes things don't work as expected. Just like a detective, you need ways to find out what went wrong. This section of our "langgraph tutorial 2026" gives you some practical tips for testing and debugging your LangGraph agents.

**1. Print Statements (Your Best Friend):**
The simplest way to see what's happening inside your agent is to add `print()` statements within your nodes and router functions. We've used these throughout our examples. Print the current `state`, the decisions made by the router, or the output of a tool.

```python
# Example of using print statements in a node
def my_node(state: AgentState):
    print(f"DEBUG: Entering my_node. Current messages: {len(state['messages'])}")
    # ... node logic ...
    print(f"DEBUG: Exiting my_node. Updating state.")
    return {"messages": [AIMessage(content="Node processed!")]}
```

**2. Trace the `stream` Output:**
When you call `app.stream(inputs)`, LangGraph gives you updates for each step your agent takes. Pay close attention to this output. It shows which node is currently processing and what state changes are happening. If a node is skipped or an unexpected message appears, this is your first clue.

**3. Visualizing Your Graph:**
For more complex graphs, a visual representation can be incredibly helpful. LangGraph can generate a graph diagram. You might need to install `graphviz` for this.

```bash
pip install pygraphviz graphviz
```

Then, you can save a picture of your graph:

```python
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END # Assuming your workflow is 'research_workflow'

# After defining your workflow, you can visualize it
# research_workflow.get_graph().draw_png("research_agent_graph.png")
# If running in Jupyter/Colab:
# display(Image(research_workflow.get_graph().draw_png()))
```

This will create an image file (`research_agent_graph.png`) showing all your nodes and edges, making it easy to see if your flow logic is correct.

**4. Check the `AgentState` at Each Step:**
If an agent behaves unexpectedly, inspect the `AgentState` carefully. Did the LLM return the correct tool calls? Is the tool's output what you expected? Is the conversation history (`messages`) growing correctly? Sometimes, a small mistake in how you update the state can cause big problems later.

**5. Isolate Components:**
If your agent is not working, try to test individual parts (nodes or tools) separately. Can your `dummy_web_search` tool work correctly on its own? Does your `call_llm` node correctly invoke the LLM? Break down the problem into smaller, testable pieces.

**6. Review LLM Prompts and Tool Descriptions:**
Often, the LLM might not call a tool or might call the wrong one because its prompt or the tool's description isn't clear enough. Make sure your tool's `docstring` (the description below `@tool`) accurately explains what the tool does and when it should be used.

**7. Use a `ToolNode` for Simpler Tool Execution:**
Instead of manually creating an `execute_tools_node` as we did, LangGraph offers a built-in `ToolNode`. This can simplify your graph and reduce potential errors.

```python
from langgraph.prebuilt import ToolNode

# ... (define tools) ...
tool_node = ToolNode(tools)

# In your workflow:
# workflow.add_node("tool_execution_node", tool_node)
# This will automatically execute any tool calls it receives from the LLM.
```

By following these testing and debugging tips in this "langgraph tutorial 2026," you'll be able to quickly identify and fix issues, making your AI agents more robust and reliable.

## Beyond the Basics: Next Steps for Your LangGraph Journey

You've come a long way with this "langgraph tutorial 2026," building foundational AI agents. But the world of LangGraph is much richer! Here are some exciting next steps to continue your journey and build even more sophisticated agents:

*   **Memory and Persistent State:** Our current examples keep state only for one run. Learn how to integrate persistent memory so your agent remembers past conversations or tasks across multiple sessions. This involves using LangChain's memory components with LangGraph.
*   **Human-in-the-Loop Agents:** Build agents that can ask for human help or confirmation at certain steps. This is crucial for tasks where accuracy is paramount or where human judgment is needed.
*   **Custom Nodes:** While we've used LLMs and tools, you can create custom nodes for almost anything. This could be data processing, API calls, database interactions, or complex logic.
*   **Agent Super-Vision:** Create agents that oversee other agents, delegating tasks and reviewing their work. This allows for highly complex multi-agent systems.
*   **Error Handling and Retries:** Implement robust error handling within your nodes and use retry mechanisms for unreliable external calls. This makes your agents much more resilient.
*   **Advanced Tooling:** Explore more advanced tools like those for accessing databases, interacting with operating systems, or integrating with other AI models (e.g., image generation).
*   **Performance Optimization:** As your agents grow, learn about techniques to optimize their performance, such as caching, parallel execution, or more efficient LLM calls.

The skills you've gained from this "langgraph tutorial 2026" are a fantastic starting point. Keep experimenting, keep building, and you'll be amazed at the intelligent agents you can create!

## Conclusion

Congratulations! You've successfully completed this comprehensive "langgraph tutorial 2026" and now possess a solid understanding of how to build AI agents using LangGraph. We started with the very basics, including `installation and setup`, defining your agent's memory with a `state schema`, and `creating your first LangGraph agent`.

You learned about the fundamental `StateGraph nodes and edges`, which are the building blocks of any agent's workflow. We then delved into `adding tools to agents`, giving them powerful capabilities to interact with the world, and mastered `conditional routing logic` to enable smart decision-making. We wrapped it up with `complete working examples with code` and crucial `testing and debugging tips`.

The ability to design agents that can reason, use tools, and follow complex workflows is a game-changer in AI development. You're now equipped to start building your own intelligent applications, from smart chatbots to sophisticated task automators. Keep practicing, explore the advanced topics, and continue to innovate with LangGraph! The future of AI agents is bright, and you are now a part of it.
```