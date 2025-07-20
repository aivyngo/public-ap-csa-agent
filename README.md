# AP Computer Science Agent
An AP Computer Science agent powered by FastAPI, OpenWebUI, and the tim-large model meant to help students by giving them relevant Java info, generating practice problems, and grading/giving feedback on their responses.

## Motivation
Inspired by the lack of AP CSA resources at my high school. This project is meant to make CS accessible for all students, regardless of income/area/resources.

## Features/Tools
- generates and grades questions using question generator and question grader tools
- generates rubrics using question grader tool
- searches for relevant info based on query using web search and textbook search tool
- communicate with agent via OpenWebUI

Each tool has an endpoint in main.py, logic in tools/, and Pydantic input and output schemas in models/. All tools were unified into a call_tool endpoint, which run_apcsa_agent may call in the endpoint used for chatting on OpenWebUI in main.py depending on if tool calls are necessary.

## Using the Agent
### Prerequisites
The following should be installed:
- Python 3.10+
- Docker
- OpenWebUI
## Set Up
### Clone Repo
```bash
git clone https://github.com/aivyngo/public-ap-csa-agent.git
cd public-ap-csa-agent
```
### Set Up Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Run OpenWebUI with Docker
Make sure Docker is installed and running.
```bash
docker run -d -p 3000:8080 --name open-webui ghcr.io/open-webui/open-webui:main
docker start open-webui
```
### Run FastAPI Backend
```bash
uvicorn main:app --host 0.0.0.0 --port 8060 --workers 2
```
### Chatting with Agent
Visit http://localhost:3000. Click on your profile on the top right, then settings, then connections. Use http://192.222.54.121:8060/v1 for the custom link. The API name can be anything. Click save and then exit settings. In the dropdown, you should now see "tim-large" as a model, and you can now start chatting!

## Using the tim-large Model for your own Agent
This project uses a LLM called tim-large. You can integrate this model into your own agent:

The FastAPI backend exposes the /v1/chat/completions endpoint that implements OpenAI-compatible chats and tool calling.

The agent connects with OpenWebUI via its Connections settings, where you add a custom API endpoint pointing to your backend’s /v1 URL.

The backend supports calling multiple specialized tools (question generation, grading, web/textbook search) through JSON-based function calls. All tools were unified into a call_tool endpoint, which run_apcsa_agent may call in the endpoint used for chatting on OpenWebUI in main.py depending on if tool calls are necessary. You can replace run_apcsa_agent with a function analogous to it that matches your agent.

You can add or replace tools by modifying the tools/ folder and updating the TOOL_REGISTRY in your backend.

Host your backend API exposing /v1/chat/completions with the tim-large model.

Run OpenWebUI and add a connection to your backend URL.

Start chatting on OpenWebUI with tim-large powering responses and tool usage.