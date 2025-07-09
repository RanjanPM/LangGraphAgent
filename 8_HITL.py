from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def fetch_user_data() -> dict:
    """
    Fetches random user data from an external API.
    Returns a dictionary with user information.
    """
    import requests
    # Fetching random user data from an external API
    response = requests.get("https://randomuser.me/api/")
    # Check if the request was successful
    
    if response.status_code == 200:
        data = response.json()
        # Extracting user information from the response
        user_info = data['results'][0]
        return {
            "name": f"{user_info['name']['first']} {user_info['name']['last']}",
            "email": user_info['email'],
            "location": user_info['location']['city']
        }
    else:
        raise Exception("Failed to fetch user data")
    

@tool
def get_gas_price(state:str) -> str:
    """
    Fetches the current gas price from an external API.
    Returns the gas price as a string.
    """
    import http.client
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': "apikey 7iY0cH9qu2N1J7SvTZ5Uij:74jWbJjRxv4D7OUgW1jcrg"
    }
    conn.request("GET", "/gasPrice/stateUsaPrice?state="+state, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

@tool
def buy_gas(gallons: int, state: str) -> str:
    """
    Buys gas for the user.
    """
    decision = interrupt(f"Approve buying {gallons} gallons of gas in {state} at current price?")
    if decision == "no":
        return "Purchase cancelled by user."
    else:
        return buy_gas_api(gallons, state)

def buy_gas_api(gallons: int, state: str) -> str:
    import http.client
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': "apikey 7iY0cH9qu2N1J7SvTZ5Uij:74jWbJjRxv4D7OUgW1jcrg"
    }
    conn.request("POST", "/gasPrice/buyGas", headers=headers, body={"gallons": gallons, "state": state})
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

tools = [fetch_user_data, get_gas_price, buy_gas]
llm = init_chat_model("google_genai:gemini-2.5-flash")
llm_with_tools = llm.bind_tools(tools, return_direct=True, tool_choice="auto")

def chatbot_node(state: State):
    msg = llm_with_tools.invoke(state["messages"])
    return {"messages": [msg]}

memory = MemorySaver()
builder = StateGraph(State)
builder.add_node("chatbot", chatbot_node)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "buy_thread"}}

# Step 1: user asks price
state = graph.invoke({"messages":[{"role":"user","content":"I want to travel from California to Georgia and need 15 gallons of gas. What will be the total cost if I fill 8 gallons in California and 7 gallons in Georgia?"}]}, config=config)
print(state["messages"][-1].content)

# Step 2: user asks to buy
state = graph.invoke({"messages":[{"role":"user","content":"Buy 15 gallons of gas in Georgia at current price."}]}, config=config)
print(state.get("__interrupt__"))

decision = input("Approve (yes/no): ")
state = graph.invoke(Command(resume=decision), config=config)
print(state["messages"][-1].content)