import os
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Define LLM configuration
llm_config = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.4,
    "api_key": os.environ["OPENAI_API_KEY"],
}

# Define the customer inquiry agent
#Your job is to read customer messages and figure out what the issue is about.
inquiry_agent = ConversableAgent(
    name="Inquiry_Agent",
    llm_config=llm_config,
    system_message="You handle customer inquiries and classify them.",
)

# Define the response agent
response_agent = ConversableAgent(
    name="Response_Agent",
    llm_config=llm_config,
    system_message="You provide automated responses based on the inquiry classification.",
)

# Define the knowledge base agent
#Knowledge_Base_Agent shares what the docs recommend.
knowledge_base_agent = ConversableAgent(
    name="Knowledge_Base_Agent",
    llm_config=llm_config,
    system_message="You search the company's knowledge base for solutions to customer issues.",
)

# Define the troubleshooting agent
#Troubleshooting_Agent gives hands-on, personalized, do-this-now steps.
troubleshooting_agent = ConversableAgent(
    name="Troubleshooting_Agent",
    llm_config=llm_config,
    system_message="You guide customers through troubleshooting steps to resolve their issues.",
)

# Define the feedback agent
#Feedback_Agent is like a little survey bot that checks if the customer was happy with the support.
feedback_agent = ConversableAgent(
    name="Feedback_Agent",
    llm_config=llm_config,
    system_message="You collect customer feedback on the resolution process.",
)

# Define the escalation agent
#Escalation_Agent is the smart decider — if the AI can't fix it, it calls in a human.
escalation_agent = ConversableAgent(
    name="Escalation_Agent",
    llm_config=llm_config,
    system_message="You identify cases that require human intervention.",
)

# Define the human support agent
#Human_Support_Agent is the last stop — it helps the user when the AI agents can't solve the issue (pretends to be a human)
human_support_agent = ConversableAgent(
    name="Human_Support_Agent",
    llm_config=llm_config,
    system_message="You connect customers with human support representatives.",
)

# Define the user proxy agent
#user_proxy is a fake user that starts the conversation, doesn't wait for human input, and runs everything automatically, stopping when it sees “TERMINATE.”
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "my_code",
        "use_docker": False,
    },
)

# Register nested chats with the user proxy agent
user_proxy.register_nested_chats(
    [
        {
            "recipient": response_agent,
            "message": lambda recipient, messages, sender, config: f"Classify and respond to this inquiry: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": knowledge_base_agent,
            "message": lambda recipient, messages, sender, config: f"Search for solutions to this issue: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": troubleshooting_agent,
            "message": lambda recipient, messages, sender, config: f"Guide through troubleshooting for this issue: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": feedback_agent,
            "message": lambda recipient, messages, sender, config: f"Collect feedback on this resolution process: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
        {
            "recipient": escalation_agent,
            "message": lambda recipient, messages, sender, config: f"Determine if this case needs human intervention: {messages[-1]['content']}",
            "summary_method": "last_msg",
            "max_turns": 1,
        },
    ],
    trigger=inquiry_agent,#Start this whole chain after the Inquiry Agent finishes its part
)


# Define the initial customer inquiry
initial_inquiry = (
    """My internet is not working, and I have already tried rebooting the router."""
)

# Start the nested chat
user_proxy.initiate_chat(
    recipient=inquiry_agent,
    message=initial_inquiry,
    max_turns=2,
    summary_method="last_msg",
)
