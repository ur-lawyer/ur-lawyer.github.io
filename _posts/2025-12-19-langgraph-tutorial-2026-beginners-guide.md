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
title: LangGraph Tutorial 2026 - Complete Beginner's Guide to Building AI Agents
description: Dive into this comprehensive LangGraph tutorial 2026 to learn how to build powerful AI agents from scratch. Master installation, state management, tools, and conditional routing.
keywords: langgraph tutorial 2026, building AI agents, langgraph, stategraph, AI agent development, langchain agents, AI programming
---

## Welcome to Your LangGraph Tutorial 2026: Building Smart AI Agents!

Have you ever wondered how smart computer programs, called AI agents, can do amazing things like answering questions, planning tasks, or even writing stories? These agents are like little digital helpers with brains. They can think, react, and learn to solve problems. In this `langgraph tutorial 2026`, you will learn how to build your very own AI agents.

We will use a fantastic tool called LangGraph. LangGraph helps you create complex AI agents step by step, making them smart and reliable. By the end of this guide, you will have a clear understanding of how these powerful systems work and how to build them yourself. Get ready to unlock the future of AI!

## What is LangGraph and Why Do We Need It?

Imagine you want an AI to do more than just answer one simple question. Maybe you want it to ask you follow-up questions, search the internet, and then give you a detailed report. This requires many steps and decisions. An AI agent needs to move through these steps smoothly.

LangGraph is like a special blueprint for building these multi-step AI agents. It helps you draw out the paths your AI agent will take, allowing it to make choices and use different tools along the way. Think of it as mapping out a journey for your AI. This `langgraph tutorial 2026` will show you how to draw this map.

### Why LangGraph is a Game Changer for AI Agents

LangGraph lets you build AI agents that are very smart and flexible. They can remember past conversations, decide what to do next, and even use different tools to get information. This makes your agents much more useful than simple chatbots. You can build agents that truly understand and adapt to tasks.

It helps you manage complex interactions without getting lost. This means your agents can handle many different situations, just like a human would. In this `langgraph tutorial 2026`, we will explore these powerful capabilities.

## Getting Started: LangGraph Installation and Setup

Before we can build anything, we need to set up our workshop! This section covers the `installation and setup` for your `langgraph tutorial 2026`. Don't worry, it's pretty straightforward.

### What You'll Need

You will need a computer with Python installed. Python is a popular programming language, and LangGraph is built using it. You should also have a basic understanding of how Large Language Models (LLMs) work, like ChatGPT or similar AI models. If you don't have Python, you can download it from the official Python website.

You'll also need an API key for an LLM provider, like OpenAI, Google Gemini, or Anthropic. This key lets your computer talk to the powerful AI models. Keep your API key safe and never share it publicly.

### Setting Up Your Environment

First, open your computer's terminal or command prompt. This is where we will type commands to install things. We will create a special folder for our project to keep everything organized.

Type these commands one by one, pressing Enter after each:

```bash
# Create a new directory for your project
mkdir my_langgraph_agent
cd my_langgraph_agent

# Create a virtual environment (good practice!)
python -m venv venv

# Activate the virtual environment
# On Windows:
# .\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

Now you are in a clean environment ready for our `langgraph tutorial 2026`.

### Installing LangGraph and Other Tools

Next, we will install LangGraph and LangChain. LangChain is a library that LangGraph uses to connect to LLMs and tools. We will also install a package for a specific LLM, like OpenAI.

```bash
pip install -U langgraph langchain_openai
```

If you prefer another LLM provider like Google Gemini or Anthropic, you would install a different package. For example, `pip install langchain_google_genai` or `pip install langchain_anthropic`. We will use `langchain_openai` for most examples in this `langgraph tutorial 2026`.

### Storing Your API Key

It's super important not to put your API key directly into your code. Instead, we'll store it in a special file called `.env`. Create a file named `.env` in your `my_langgraph_agent` folder.

Inside this `.env` file, add your API key like this:

```
OPENAI_API_KEY="your_secret_openai_api_key_here"
```

Replace `"your_secret_openai_api_key_here"` with your actual key. Now, your Python code can read this key safely. You'll need to install `python-dotenv` to load these variables.

```bash
pip install python-dotenv
```

Great job! Your environment is all set up. You're ready for the exciting parts of this `langgraph tutorial 2026`.

## The Core of LangGraph: Defining State Schema

Every smart agent needs to remember things to make good decisions. This "memory" is what we call "state" in LangGraph. The `defining state schema` is like creating a blueprint for what your agent needs to remember at any given moment. It tells LangGraph what kind of information your agent will track.

### What is State and Why is it Crucial?

Imagine you're talking to a friend. You remember what you just said and what your friend said. This information helps you decide what to say next. In the same way, an AI agent needs to remember parts of the conversation, results from tools, or user requests. This is its "state."

The state is a special dictionary or object that holds all the current information for your agent. It changes as the agent does more work. Without state, your agent would forget everything after each step, which wouldn't be very helpful. This is a fundamental concept in this `langgraph tutorial 2026`.

### How to Define a StateGraph's State

In LangGraph, we define our state using a `TypedDict`. This is like a special Python dictionary that helps us say exactly what kind of information will be stored. It makes sure your agent always knows what to expect.

Let's look at a simple example for our `langgraph tutorial 2026`. Suppose our agent needs to remember the messages in a conversation and whether it should end the chat.

```python
from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Represents the state of our agent.

    - messages: A list of messages in the conversation.
    - chat_history: A list of all past messages.
    - user_query: The initial query from the user.
    - should_end: A flag to indicate if the conversation should end.
    """
    messages: List[BaseMessage]
    chat_history: List[BaseMessage]
    user_query: str
    should_end: bool
```

Here, `AgentState` is our state schema. It says that our agent will have a `messages` list (for current interaction), a `chat_history` list (for all interactions), a `user_query` string, and a `should_end` boolean. Each item has a specific type, making it very clear.

When you define your state, think about all the information your agent might need. This could be user input, tool results, decisions made, or anything else important. This clear definition is key to building reliable agents in this `langgraph tutorial 2026`.

## Your First LangGraph Agent: A Simple Echo

Now that we know about state and have our environment ready, let's create a very simple agent. This will be like a "hello world" for LangGraph. We will focus on `creating first LangGraph agent` and understanding its basic flow. Our first agent will simply take a message and echo it back.

### Setting Up the Basic Agent Structure

We start by importing `StateGraph` from LangGraph. This is the main building block. We also need our `AgentState` that we just defined.

```python
import os
from dotenv import load_dotenv
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

# Load environment variables (like API keys)
load_dotenv()

# Our agent's state schema
class AgentState(TypedDict):
    messages: List[BaseMessage]
    chat_history: List[BaseMessage]
    user_query: str
    should_end: bool = False # Default to False
```

Next, we define a simple function that will act as our agent's "brain" for this example. This function will take the current state and return an updated state.

### The Echo Node

Our first agent will have one node. A node is a step where our agent does something. This node will just take the user's message and add an AI's echo message to the state.

```python
def echo_node(state: AgentState) -> AgentState:
    """
    A simple node that echoes the last user message.
    """
    print("---EXECUTING ECHO NODE---")
    messages = state["messages"]
    last_message = messages[-1] if messages else HumanMessage(content="No message")

    ai_response = f"You said: '{last_message.content}'"
    new_messages = state["messages"] + [AIMessage(content=ai_response)]

    # Update chat history as well
    new_chat_history = state["chat_history"] + [last_message, AIMessage(content=ai_response)]

    return {"messages": new_messages, "chat_history": new_chat_history, "should_end": True}
```

This `echo_node` takes the `state`, finds the last message, creates an AI response, and updates the `messages` list in the state. It also sets `should_end` to `True` to signal the conversation is done.

### Building and Running the Graph

Now, we connect our node to a `StateGraph`.

```python
# Build the graph
workflow = StateGraph(AgentState)

# Add our echo node
workflow.add_node("echo", echo_node)

# Set the entry point: where the graph starts
workflow.set_entry_point("echo")

# Set the exit point: where the graph ends
# After 'echo' node, we want to end
workflow.add_edge("echo", END)

# Compile the graph
app = workflow.compile()
```

Here's what these lines do:
*   `StateGraph(AgentState)` creates our graph, telling it what kind of state to expect.
*   `add_node("echo", echo_node)` adds our `echo_node` function to the graph, giving it the name "echo".
*   `set_entry_point("echo")` tells the graph that "echo" is the first step.
*   `add_edge("echo", END)` tells the graph that after the "echo" node, the process should finish. `END` is a special LangGraph signal.
*   `app = workflow.compile()` finishes building the graph, making it ready to run.

### Testing Your First Agent

Let's run our agent!

```python
# Run the agent
initial_state = {
    "messages": [HumanMessage(content="Hello there!")],
    "chat_history": [],
    "user_query": "Hello there!",
    "should_end": False
}

result = app.invoke(initial_state)

print("\nFinal State:")
print(result)

# Access the AI's response
print("\nAgent's Response:")
print(result["messages"][-1].content)
```

You should see output similar to:

```
---EXECUTING ECHO NODE---

Final State:
{'messages': [HumanMessage(content='Hello there!'), AIMessage(content="You said: 'Hello there!'")], 'chat_history': [HumanMessage(content='Hello there!'), AIMessage(content="You said: 'Hello there!'")], 'user_query': 'Hello there!', 'should_end': True}

Agent's Response:
You said: 'Hello there!'
```

Congratulations! You've just finished `creating first LangGraph agent` in this `langgraph tutorial 2026`. It's a simple one, but it demonstrates the core idea of state, nodes, and how they connect.

## Understanding StateGraph Nodes and Edges

To build truly dynamic AI agents, you need to master the building blocks: nodes and edges. This section of our `langgraph tutorial 2026` is all about `understanding StateGraph nodes and edges`. They are like the cities and roads on your agent's map.

### What are Nodes?

Nodes are the "doing" parts of your agent. Each node in a LangGraph workflow performs a specific task. Think of them as individual functions or steps in a recipe.

A node takes the current state as input, does some work, and then returns an updated state. The work a node does could be anything: calling an LLM, using a tool, formatting data, or making a decision. In our previous example, `echo_node` was a node. Each node must be able to work with the `AgentState` you defined.

### What are Edges?

Edges are the "paths" that connect nodes in your graph. They define the flow of your agent. After a node finishes its work, an edge tells the graph which node to go to next.

There are two main types of edges:
1.  **Fixed Edges**: These simply say "from Node A, always go to Node B." This is what we used in our echo agent: `workflow.add_edge("echo", END)`. It means after "echo," the process ends.
2.  **Conditional Edges**: These are much smarter! They allow your agent to make decisions. They say "from Node A, if X is true, go to Node B; otherwise, go to Node C." This is where the real power of LangGraph for complex agents comes from. We will explore conditional edges in more detail soon.

### Visualizing a Simple Graph

Let's imagine a slightly more complex graph.

```
       [Start]
         |
         V
    [User Query] (Node 1)
         |
         V
    [LLM Respond] (Node 2)
         |
         V
    [End]
```

In this diagram:
*   `[User Query]` and `[LLM Respond]` are nodes.
*   The arrows are fixed edges, showing the flow. The process starts, goes to `User Query`, then `LLM Respond`, and finally ends.

LangGraph helps you define these nodes and edges in code. You add nodes using `workflow.add_node()` and connect them using `workflow.add_edge()` or `workflow.add_conditional_edges()`. This structure is why LangGraph is so powerful for building complex, multi-step agents. This understanding is key for any `langgraph tutorial 2026`.

## Making Agents Smart: Adding Tools to Agents

AI agents become much more powerful when they can "do" things in the real world. This is where `adding tools to agents` comes in. Tools allow your agent to interact with external systems, like searching the internet, doing calculations, or looking up information in a database.

### Why Agents Need Tools

Imagine asking an AI, "What's the weather like in Paris tomorrow?" Without a tool, the AI can only guess or use old information it was trained on. With a weather tool, it can actually look up the live weather forecast!

Tools extend your agent's abilities beyond just talking. They turn your agent into a helpful assistant that can perform actions. LangGraph makes it easy to give your agents these superpowers.

### How to Integrate Tools with LangGraph

LangGraph integrates seamlessly with LangChain's tools. LangChain has many built-in tools (like Google Search, Wikipedia, calculators) and also allows you to create your own custom tools.

Let's add a simple "search" tool to our agent in this `langgraph tutorial 2026`. For simplicity, we'll create a dummy search tool. In a real application, you'd use something like `GoogleSearchAPIWrapper`.

```python
from langchain_core.tools import tool

# Define a simple dummy search tool
@tool
def search_tool(query: str) -> str:
    """
    Simulates searching the internet for a query.
    Always returns a fixed result for demonstration.
    """
    print(f"---SEARCH TOOL EXECUTED FOR: {query}---")
    if "weather" in query.lower():
        return "The weather in Paris tomorrow will be sunny with a high of 20°C."
    elif "capital of france" in query.lower():
        return "The capital of France is Paris."
    else:
        return f"Found some results for '{query}': Example search result."

# List of tools available to the agent
tools = [search_tool]
```

Now, we need to teach our LLM how to *use* these tools. We do this by binding the tools to our LLM.

```python
from langchain_openai import ChatOpenAI

# Initialize our LLM
# Make sure OPENAI_API_KEY is set in your .env file
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Bind tools to the LLM. This tells the LLM about the tools it can use.
llm_with_tools = llm.bind_tools(tools)
```

### Creating a Tool-Using Agent

Now, let's create a node that can decide whether to use a tool or just respond.

```python
from langchain_core.messages import ToolMessage

def call_llm_or_tool(state: AgentState) -> AgentState:
    """
    Node that either calls the LLM for a response or uses a tool.
    """
    print("---EXECUTING LLM/TOOL CALL NODE---")
    messages = state["messages"]
    last_message = messages[-1]

    # Call the LLM
    response = llm_with_tools.invoke(messages)
    new_messages = messages + [response]

    return {"messages": new_messages}

def call_tool_node(state: AgentState) -> AgentState:
    """
    Node that actually executes the tool call requested by the LLM.
    """
    print("---EXECUTING TOOL EXECUTION NODE---")
    messages = state["messages"]
    last_message = messages[-1]

    # Assume the LLM's response is a ToolCall
    if last_message.tool_calls:
        tool_outputs = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            # This is where you'd actually call the tool function
            if tool_name == "search_tool":
                output = search_tool.invoke(tool_args["query"])
                tool_outputs.append(ToolMessage(tool_call_id=tool_call["id"], content=output))
            else:
                tool_outputs.append(ToolMessage(tool_call_id=tool_call["id"], content=f"Tool {tool_name} not found."))
        
        new_messages = messages + tool_outputs
        return {"messages": new_messages}
    
    return {"messages": messages} # No tool call found, return current messages
```

We now have two new nodes: `call_llm_or_tool` which asks the LLM what to do, and `call_tool_node` which runs the tool if the LLM requested it. Next, we need to add smart routing to decide when to use these. This is an essential step in this `langgraph tutorial 2026` for creating useful agents.

## Smart Decisions: Conditional Routing Logic

The real power of LangGraph comes from its ability to make decisions. This is done through `conditional routing logic`. Your agent doesn't just follow a fixed path; it can choose different paths based on the current state. This makes agents dynamic and responsive.

### How Agents Make Choices Based on State

Think about a flow chart. "If X is true, go left. Else, go right." This is exactly what conditional routing does in LangGraph. After a node finishes, a "router" function looks at the updated state and decides which node to visit next.

This router function is a simple Python function that takes the state and returns the name of the next node, or a special signal like `END`. It's a key part of `langgraph tutorial 2026`.

### `RunnableLambda` for Routing Decisions

LangGraph uses `RunnableLambda` to define these routing functions. Let's create a router that decides if the agent needs to use a tool.

```python
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# Our existing AgentState, tools, llm, llm_with_tools, call_llm_or_tool, call_tool_node

# --- Define the conditional router ---
def decide_what_to_do(state: AgentState) -> str:
    """
    Determines whether the agent needs to call a tool or if it's done.
    """
    print("---DECIDING WHAT TO DO---")
    last_message = state["messages"][-1]

    # If the LLM has decided to call a tool
    if last_message.tool_calls:
        print("---DECISION: CALL TOOL---")
        return "call_tool"
    else:
        # If the LLM's response is a final answer
        print("---DECISION: FINISH CONVERSATION (NO TOOL CALL)---")
        return "end_conversation" # This will be the name of the node that leads to END
```

This `decide_what_to_do` function looks at the `last_message` from the LLM. If the LLM's response contains `tool_calls`, it means the LLM wants to use a tool, so we return "call_tool". Otherwise, the LLM has given a final answer, and we return "end_conversation".

### Building the Graph with Conditional Routing

Now, let's put it all together with our new nodes and routing logic.

```python
# Initialize a new graph
workflow = StateGraph(AgentState)

# Add the nodes
workflow.add_node("llm_or_tool_node", call_llm_or_tool)
workflow.add_node("call_tool", call_tool_node)

# Add a node to simply indicate conversation ends (or pass through to END)
def end_conversation_node(state: AgentState) -> AgentState:
    print("---CONVERSATION ENDED---")
    return {"should_end": True} # Indicate that the agent is done

workflow.add_node("end_conversation", end_conversation_node)

# Set the entry point
workflow.set_entry_point("llm_or_tool_node")

# Add conditional edges
# After the LLM tries to respond or suggest a tool, we decide what's next
workflow.add_conditional_edges(
    "llm_or_tool_node",      # From this node
    decide_what_to_do,       # Use this function to decide
    {
        "call_tool": "call_tool",  # If decide_what_to_do returns "call_tool", go to "call_tool" node
        "end_conversation": "end_conversation" # If "end_conversation", go to "end_conversation" node
    }
)

# After calling the tool, we want to go back to the LLM
# This allows the LLM to process the tool's output and provide a final answer
workflow.add_edge("call_tool", "llm_or_tool_node")

# After the conversation ends node, we end the entire graph
workflow.add_edge("end_conversation", END)

# Compile the graph
app_with_tools = workflow.compile()
```

This graph works like this:
1.  **Start at `llm_or_tool_node`**: The LLM tries to respond or suggests a tool.
2.  **`decide_what_to_do`**: After `llm_or_tool_node`, our router checks the LLM's output.
3.  **If tool call**: Go to `call_tool` node, which runs the tool. After the tool runs, it goes *back* to `llm_or_tool_node` so the LLM can see the tool's result and make a final answer. This creates a loop.
4.  **If no tool call**: Go to `end_conversation` node, which then leads to `END`.

This sophisticated `conditional routing logic` is fundamental for building truly interactive and capable AI agents. You are making great progress in this `langgraph tutorial 2026`!

## Putting It All Together: Complete Working Examples with Code

Now it's time to combine everything we've learned in this `langgraph tutorial 2026`. We will build a more complete working example of an AI agent that can both chat and use tools. This agent will handle multi-turn conversations and decide when to use our dummy search tool.

### Agent Goal: Answering Questions and Using Search

Our agent will be able to:
*   Respond to simple conversational greetings.
*   Recognize when it needs to use the `search_tool` (e.g., for weather queries or facts).
*   Process the search results and give a coherent answer.
*   Handle multiple turns of conversation.

Let's define the full code for this `langgraph tutorial 2026` example.

```python
import os
from dotenv import load_dotenv
from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# Load environment variables (like API keys)
load_dotenv()

# --- 1. Define Agent State Schema ---
class AgentState(TypedDict):
    """
    Represents the state of our agent.
    - messages: A list of messages in the current turn.
    - chat_history: A list of all past messages (for LLM context).
    - user_query: The initial query from the user.
    - should_end: A flag to indicate if the conversation should end.
    """
    messages: Annotated[List[BaseMessage], add_messages] # Annotated for message handling
    user_query: str # This can hold the initial query or be updated
    should_end: bool # Flag to signal end of conversation

# --- 2. Define Tools ---
@tool
def search_tool(query: str) -> str:
    """
    Simulates searching the internet for a query.
    Returns a fixed result for demonstration purposes.
    """
    print(f"\n---SEARCH TOOL EXECUTED FOR: '{query}'---")
    if "weather" in query.lower():
        return "The weather in Paris tomorrow will be sunny with a high of 20°C. Source: Dummy Weather Service."
    elif "capital of france" in query.lower():
        return "The capital of France is Paris. Source: Dummy Encyclopedia."
    elif "population of earth" in query.lower():
        return "The population of Earth is approximately 8 billion people. Source: Dummy Stats Site."
    else:
        return f"Found some general information for '{query}': This is a dummy search result."

tools = [search_tool]

# --- 3. Initialize LLM with Tools ---
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# --- 4. Define Graph Nodes ---

def call_llm_node(state: AgentState) -> AgentState:
    """
    Node that calls the LLM with the current messages and updates the state.
    """
    print("---EXECUTING LLM CALL NODE---")
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    # add_messages will automatically append this to the state's messages list
    return {"messages": response}

def call_tool_node(state: AgentState) -> AgentState:
    """
    Node that executes the tool call requested by the LLM.
    """
    print("---EXECUTING TOOL EXECUTION NODE---")
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        tool_outputs = []
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            if tool_name == "search_tool":
                output = search_tool.invoke(tool_args["query"])
                tool_outputs.append(ToolMessage(tool_call_id=tool_call["id"], content=output))
            else:
                tool_outputs.append(ToolMessage(tool_call_id=tool_call["id"], content=f"Tool {tool_name} not found."))
        
        # add_messages will append these tool outputs to the state
        return {"messages": tool_outputs}
    
    return {"messages": []} # Return empty if no tool call, add_messages won't append
                             # Or, alternatively, handle this case in routing

def end_node(state: AgentState) -> AgentState:
    """
    A simple node to explicitly mark the end of the conversation.
    """
    print("---CONVERSATION END NODE REACHED---")
    return {"should_end": True}

# --- 5. Define Conditional Routing Logic ---

def router_decide_next_step(state: AgentState) -> str:
    """
    Determines the next step based on the LLM's last message.
    """
    print("---DECIDING NEXT STEP---")
    last_message = state["messages"][-1]

    # If the LLM wants to call a tool
    if last_message.tool_calls:
        print(f"---DECISION: CALL TOOL {last_message.tool_calls[0]['name']}---")
        return "call_tool"
    # If the LLM responds with a final answer and doesn't want to call a tool
    elif isinstance(last_message, AIMessage) and not last_message.tool_calls:
        print("---DECISION: CONVERSATION ENDS---")
        # Here we could have another node to summarize or confirm
        # For this example, we'll directly go to 'end_conversation_node'
        return "end_conversation"
    else:
        # Fallback, theoretically this path should be covered
        print("---DECISION: UNEXPECTED STATE, ENDING---")
        return "end_conversation"

# --- 6. Build the StateGraph Workflow ---

workflow = StateGraph(AgentState)

# Add nodes to the workflow
workflow.add_node("llm", call_llm_node)
workflow.add_node("call_tool", call_tool_node)
workflow.add_node("end_conversation", end_node)

# Set the entry point
workflow.set_entry_point("llm")

# Add conditional edges from the LLM node
workflow.add_conditional_edges(
    "llm",                  # Source node
    router_decide_next_step,# Router function
    {
        "call_tool": "call_tool",         # If router returns "call_tool", go to "call_tool" node
        "end_conversation": "end_conversation" # If router returns "end_conversation", go to "end_conversation" node
    }
)

# After calling a tool, always go back to the LLM to process the tool's output
workflow.add_edge("call_tool", "llm")

# After the 'end_conversation' node, the graph terminates
workflow.add_edge("end_conversation", END)

# Compile the workflow
app = workflow.compile()

# --- 7. Test the Agent ---

print("--- Agent Running ---")

# Test 1: Simple greeting
print("\n--- TEST CASE 1: Simple greeting ---")
initial_state_1 = {
    "messages": [HumanMessage(content="Hello, how are you?")],
    "user_query": "Hello, how are you?",
    "should_end": False
}
final_state_1 = app.invoke(initial_state_1)
print(f"Agent Response: {final_state_1['messages'][-1].content}")
# Expected: A friendly greeting from the AI

# Test 2: Tool call for weather
print("\n--- TEST CASE 2: Tool call for weather ---")
initial_state_2 = {
    "messages": [HumanMessage(content="What is the weather like in Paris tomorrow?")],
    "user_query": "What is the weather like in Paris tomorrow?",
    "should_end": False
}
final_state_2 = app.invoke(initial_state_2)
print(f"Agent Response: {final_state_2['messages'][-1].content}")
# Expected: AI uses search tool and provides weather info

# Test 3: Tool call for a fact
print("\n--- TEST CASE 3: Tool call for a fact ---")
initial_state_3 = {
    "messages": [HumanMessage(content="What is the capital of France?")],
    "user_query": "What is the capital of France?",
    "should_end": False
}
final_state_3 = app.invoke(initial_state_3)
print(f"Agent Response: {final_state_3['messages'][-1].content}")
# Expected: AI uses search tool and provides the capital

# Test 4: Multi-turn interaction (requires initial chat history)
# Note: For multi-turn, you would typically feed the full conversation history.
# Here, we simulate a follow-up after the weather query.
print("\n--- TEST CASE 4: Multi-turn follow-up ---")
# Let's manually create a history from Test 2 for simplicity
# In a real app, you'd feed the output of the previous 'invoke' as input to the next.
initial_state_4 = {
    "messages": [
        HumanMessage(content="What is the weather like in Paris tomorrow?"),
        AIMessage(content='', tool_calls=[{'name': 'search_tool', 'args': {'query': 'weather in Paris tomorrow'}, 'id': 'call_123'}]),
        ToolMessage(content='The weather in Paris tomorrow will be sunny with a high of 20°C. Source: Dummy Weather Service.', tool_call_id='call_123'),
        AIMessage(content='The weather in Paris tomorrow is expected to be sunny with a high of 20°C. Is there anything else I can help you with?')
    ],
    "user_query": "Thank you! What about the population of Earth?",
    "should_end": False
}

# Now, add the new human message to simulate the next turn
initial_state_4["messages"].append(HumanMessage(content=initial_state_4["user_query"]))

final_state_4 = app.invoke(initial_state_4)
print(f"Agent Response: {final_state_4['messages'][-1].content}")
# Expected: AI uses search tool again and provides population info
```

This comprehensive example demonstrates `complete working examples with code` that integrates all the concepts from this `langgraph tutorial 2026`. You now have a functional, multi-step AI agent!

## Ensuring Quality: Testing and Debugging Tips

Building AI agents can sometimes be tricky, and things don't always work perfectly on the first try. That's totally normal! This section provides `testing and debugging tips` to help you make sure your LangGraph agents are robust and reliable. Just like any good builder, you need to check your work.

### How to Test Your LangGraph Agents Effectively

Testing is about running your agent with different inputs and checking if it behaves as expected.

1.  **Test Individual Nodes**: Before you connect everything, test each node function by itself. Give it a sample `AgentState` and see if it returns the correct updated state. This helps isolate problems early.
    *   *Example*: Call `echo_node({"messages": [HumanMessage(content="Test")]})` and check the output.

2.  **Run with Diverse Inputs**: Don't just test with perfect inputs. Try edge cases:
    *   Very short queries.
    *   Queries that clearly need a tool.
    *   Queries that clearly *don't* need a tool.
    *   Ambiguous queries.
    *   Empty inputs (if your design allows for it).
    *   Long conversations.

3.  **Trace the Graph Flow**: LangGraph allows you to see the path your agent took. When you run `app.invoke()`, it returns the final state. But you can also iterate through the `app.stream()` to see each step.

    ```python
    # Example using stream for debugging
    for s in app.stream({"messages": [HumanMessage(content="Tell me about Earth's population.")]}):
        print(s)
        print("---")
    ```
    This stream will show you the state after each node execution, which is incredibly useful for seeing exactly where a problem might occur.

4.  **Use Assertions for Expected Behavior**: In a proper test suite (e.g., using `pytest`), you would write assertions to confirm outcomes.
    ```python
    assert "8 billion" in final_state_4['messages'][-1].content
    ```

### Common Issues and How to Fix Them

1.  **Incorrect State Updates**:
    *   **Problem**: A node might not return all the necessary parts of the state, or it might accidentally overwrite important information.
    *   **Fix**: Double-check your node functions. Ensure they return a dictionary that merges correctly with the current state. Remember `Annotated[List[BaseMessage], add_messages]` for messages, as it handles appending automatically. Make sure you don't forget to return previous state variables if they're not explicitly modified, or ensure your state updates are additive where needed.

2.  **LLM Not Calling Tools**:
    *   **Problem**: Your LLM ignores the tools you've provided and tries to answer everything itself.
    *   **Fix**:
        *   Make sure `llm.bind_tools(tools)` was called correctly.
        *   Ensure your `ChatOpenAI` (or other LLM) model is capable of tool use (e.g., `gpt-3.5-turbo`, `gpt-4`, `gemini-pro`).
        *   Write clear tool descriptions (`"""docstrings"""`) so the LLM understands what the tool does.
        *   Temperature: A `temperature=0` often makes the LLM more deterministic and better at following instructions like tool calls.

3.  **Routing Errors**:
    *   **Problem**: Your agent gets stuck in a loop, or goes to the wrong node.
    *   **Fix**:
        *   Review your `router_decide_next_step` function carefully. Add print statements inside it to see what value it's returning.
        *   Check that the keys in your `add_conditional_edges` dictionary exactly match the strings returned by your router function.
        *   Visualize your graph (LangGraph has visualization tools, but simple ASCII art can also help).

4.  **API Key Issues**:
    *   **Problem**: `AuthenticationError` or similar messages when calling the LLM.
    *   **Fix**:
        *   Ensure your `.env` file is correct (`OPENAI_API_KEY="..."`).
        *   Make sure `load_dotenv()` is called at the very beginning of your script.
        *   Double-check that the environment variable `OPENAI_API_KEY` (or equivalent) is actually loaded and accessible. Print `os.getenv("OPENAI_API_KEY")` to confirm.

### Using Logging and Print Statements

Never underestimate the power of `print()` statements! Sprinkle them throughout your nodes and router functions to see:
*   What `state` looks like when a node starts.
*   The output of an LLM call.
*   The result of a tool execution.
*   What your router function decides.

For more structured debugging, Python's `logging` module is excellent. You can set different logging levels (DEBUG, INFO, WARNING) and control what gets displayed.

By following these `testing and debugging tips`, you'll be well-equipped to troubleshoot any issues you encounter while building your AI agents in this `langgraph tutorial 2026`.

## Next Steps and Advanced Concepts

You've come a long way in this `langgraph tutorial 2026`! You've learned the fundamentals of building powerful AI agents. But the world of LangGraph is even bigger. Here are a few advanced concepts to explore:

*   **Persistence**: How to save your agent's state between runs or even across different users. This lets your agent remember past conversations.
*   **Human-in-the-Loop**: Designing agents where a human can step in to provide input or correct the agent's actions at specific points.
*   **Custom Tool Agents**: Building agents that dynamically select which tools to use from a vast array of options, making them extremely versatile.
*   **Graph Visualization**: Using libraries like `mermaid` or `pygraphviz` to visually inspect your LangGraph workflow, which is invaluable for complex agents.

## Conclusion: Your Journey with LangGraph Begins!

Congratulations! You've successfully navigated this `langgraph tutorial 2026` and gained a solid foundation in building AI agents. You started with `installation and setup`, learned about `defining state schema`, and built your `first LangGraph agent`. We then explored `understanding StateGraph nodes and edges`, `adding tools to agents`, and implementing clever `conditional routing logic`. Finally, you put it all together with `complete working examples with code` and learned crucial `testing and debugging tips`.

You now have the skills to design, build, and debug sophisticated AI agents that can chat, use tools, and make intelligent decisions. The possibilities are endless, from personal assistants to complex data analysis tools. Keep experimenting, keep building, and unleash the power of AI agents!

Go forth and create amazing things! If you need to refer back to any legal aspects of AI or data privacy, you can always check reliable sources like the [European Union's GDPR portal](https://gdpr-info.eu/) or relevant national data protection authority websites for up-to-date information.

Happy coding!
```