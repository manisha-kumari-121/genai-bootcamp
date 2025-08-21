import os
from dotenv import load_dotenv
load_dotenv()
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel

checkpointer = InMemorySaver()

config1 = {"configurable": {"thread_id": "1"}}

config2 = {"configurable": {"thread_id": "2"}}

class MailResponse(BaseModel):
    """Response model for itinerary."""
    budget_in_inr: str
    main_offbeat_attractions: str

def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model="groq:llama-3.3-70b-versatile",  
    tools=[],  
    prompt="Behave like an newbie travel agent", 
    #checkpointer=checkpointer,
    response_format=MailResponse,
)



# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "give me an itinerary for a trip to Paris"}]},
   # config1
)




print(response["structured_response"])
print('----')





