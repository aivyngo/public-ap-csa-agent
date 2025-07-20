# AP Computer Science Agent
An AP Computer Science agent powered by FastAPi, OpenWebUI, and the tim-large model meant to help students by giving them relevant Java info, generating practice problems, and grading/giving feedback on their responses.

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