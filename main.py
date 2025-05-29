import os
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel ,AsyncOpenAI ,Runner , set_tracing_disabled
import chainlit as cl


load_dotenv()

set_tracing_disabled(disabled = True)

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
#----------------------------------------------------------

history = []

# -------------------------------------------------------
client = AsyncOpenAI(
    api_key = OPEN_ROUTER_API_KEY,
    base_url = "https://openrouter.ai/api/v1"
)

agent = Agent(
    model = OpenAIChatCompletionsModel(model="deepseek/deepseek-chat-v3-0324:free",openai_client=client),
    name = "my_agent",
    instructions = "you are a helpful assistance"
)

# ---------------------------------------------------------

@cl.on_message
async def main(message: cl.Message):
    ui_question =  message.content

    history.append({ "role": "user", "content": ui_question })

    response = Runner.run_sync(agent , history)

    history.append({ "role": "assistant", "content": response.final_output})
  
    await cl.Message(content= response.final_output).send()
    