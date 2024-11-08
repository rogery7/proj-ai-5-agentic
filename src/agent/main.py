import os
from datetime import datetime
from dotenv import load_dotenv
from .memory import VectorMemory, IncidentDocument
from .tools import IncidentTools
from .planner import IncidentPlanner

load_dotenv()

class IncidentAgent:
    def __init__(self):
        self.memory = VectorMemory()
        self.tools = IncidentTools(self.memory)
        self.planner = IncidentPlanner(self.tools)
    
    async def ask(self, question: str) -> str:
        """Ask the agent a question"""
        return await self.planner.handle_question(question)
    
    def ingest_slack_thread(self, thread_content: str, url: str):
        """Ingest a Slack thread into memory"""
        doc = IncidentDocument(
            id=f"slack_thread_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            content=thread_content,
            source="slack",
            url=url,
            timestamp=datetime.now()
        )
        self.memory.add_document(doc)
