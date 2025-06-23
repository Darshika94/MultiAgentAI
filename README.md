# AI-Powered Multi-Agent Customer Support System (AutoGen)

This project simulates a real-world customer support workflow using **AI agents** built with [AutoGen](https://github.com/microsoft/autogen). Each agent has a specific role—like classifying issues, replying, troubleshooting, collecting feedback, or escalating to human support—and they work together automatically as a team.

---

## Project Goal

To build a system where **multiple AI agents** collaborate to resolve customer support queries efficiently and automatically, without needing a human at every step.

---

## Workflow Overview

### How it works:

1. A simulated user (using **UserProxyAgent**) sends a support message.
2. The message is first processed by the **Customer Inquiry Agent**, which classifies the issue.
3. Once classified, a group of helper agents are triggered in **parallel** using **nested chats**:
   - Response Agent
   - Knowledge Base Agent
   - Troubleshooting Agent
   - Feedback Agent
   - Escalation Agent
4. If the issue isn't solved, it gets passed to the **Human Support Agent**.

---

## Flow Diagram

<img width="906" alt="Screen Shot 2025-06-23 at 15 59 49" src="https://github.com/user-attachments/assets/12a379cd-9c49-4700-b423-c75b5db3e8ff" />

| Agent                  | Role                                                                 |
|------------------------|----------------------------------------------------------------------|
| Customer Inquiry Agent | Reads and classifies the user's problem                              |
| Response Agent         | Sends a friendly response with helpful steps                         |
| Knowledge Base Agent   | Searches docs for related articles                                   |
| Troubleshooting Agent  | Gives step-by-step fixes                                             |
| Feedback Agent         | Asks for user feedback on the support experience                     |
| Escalation Agent       | Decides if human help is needed                                      |
| Human Support Agent    | Jumps in if AI agents can't solve the problem                        |

---

## Tools and Technologies Used

1. **Framework**: [AutoGen](https://github.com/microsoft/autogen)
2. **ConversableAgent**: Used to define each AI helper role.
3. **UserProxyAgent**: Simulates a user sending the initial message.
4. **Nested Chats**: Used to run multiple agents in parallel after the first agent completes.
5. **LLM**: `gpt-3.5-turbo` via OpenAI API (`temperature=0.4` for clarity).
6. **.env File**: Used for securely loading the API key.

---

## Sample Interaction

### User Message (via UserProxyAgent):
> _"My internet isn’t working, and I already rebooted the router."_

### Agent Responses:

| Agent                  | Response                                                                 |
|------------------------|--------------------------------------------------------------------------|
| Customer Inquiry Agent | “This looks like a connectivity issue. Let’s start by classifying it as a Wi-Fi outage problem.” |
| Response Agent         | “Sorry to hear that! Let me help you with your internet connection.”     |
| Knowledge Base Agent   | “Here’s a helpful article: *‘How to fix Wi-Fi not working even after rebooting’*.” |
| Troubleshooting Agent  | “Try unplugging the router for 30 seconds and plug it back in. Check if the power light is steady.” |
| Feedback Agent         | “Was this solution helpful? Please rate your experience.”                |
| Escalation Agent       | “It looks like this issue wasn’t solved by our steps. I’ll connect you to a human agent.” |
| Human Support Agent    | “Hi! I’m a support specialist. I’ll personally help you from here.”       |

---

## Code Walkthrough (Short Summary)

- Agents are created using `ConversableAgent` and given specific instructions (system messages).
- The fake user is `UserProxyAgent`, which starts the flow.
- `register_nested_chats()` connects all the helper agents so they run together after classification.
- The conversation ends when either the problem is solved, or the Human Support Agent steps in.

```python
# Example: Define the Inquiry Agent
inquiry_agent = ConversableAgent(
    name="Inquiry_Agent",
    llm_config=llm_config,
    system_message="You handle customer inquiries and classify them.",
)
