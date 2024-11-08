from typing import List
from langchain.tools import Tool
from .memory import VectorMemory, IncidentDocument

class IncidentTools:
    def __init__(self, memory: VectorMemory):
        self.memory = memory
        
    def get_tools(self) -> List[Tool]:
        return [
            Tool(
                name="search_incidents",
                func=self.search_incidents,
                description="Search for similar incidents in the knowledge base"
            ),
            Tool(
                name="summarize_incident",
                func=self.summarize_incident,
                description="Create a summary of a specific incident"
            ),
            Tool(
                name="link_incidents",
                func=self.link_incidents,
                description="Find related incidents based on content similarity"
            )
        ]
    
    def search_incidents(self, query: str) -> str:
        """Search for incidents similar to the query"""
        results = self.memory.search(query)
        return "\n\n".join([
            f"Source: {doc.source}\nURL: {doc.url}\nContent: {doc.content[:200]}..."
            for doc in results
        ])
    
    def summarize_incident(self, incident_id: str) -> str:
        """Summarize a specific incident"""
        # Find the incident document by ID
        incident = next((doc for doc in self.memory.documents if doc.id == incident_id), None)
        if not incident:
            return f"Could not find incident with ID: {incident_id}"
        
        # Extract key details based on source type
        if incident.source == "confluence":
            # Confluence pages likely have more structured content
            sections = incident.content.split("\n## ")
            summary_parts = []
            
            for section in sections:
                if section.strip():
                    # Add section name as header if it exists
                    if ":" in section:
                        section_name, content = section.split(":", 1)
                        summary_parts.append(f"{section_name.strip()}:\n{content.strip()}")
                    else:
                        summary_parts.append(section.strip())
                        
            formatted_content = "\n\n".join(summary_parts)
            
        else:  # Slack threads
            # For Slack, show conversation flow
            messages = incident.content.strip().split("\n")
            formatted_content = "\n".join(
                msg.strip() for msg in messages if msg.strip()
            )
        
        return f"""
            Incident Summary
            ---------------
            Source: {incident.source.title()}
            Time: {incident.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            URL: {incident.url}

            Content:
            {formatted_content}
            """.strip()
                
    def link_incidents(self, incident_id: str) -> str:
        """Find related incidents"""
        # Find the source incident
        incident = next((doc for doc in self.memory.documents if doc.id == incident_id), None)
        if not incident:
            return f"Could not find incident with ID: {incident_id}"
        
        # Search for similar incidents using the incident content
        similar_incidents = self.memory.search(incident.content, k=3)
        
        # Filter out the source incident itself
        related_incidents = [doc for doc in similar_incidents if doc.id != incident_id]
        
        if not related_incidents:
            return "No related incidents found"
            
        # Format the results
        results = ["Related Incidents:"]
        for doc in related_incidents:
            results.append(f"\nSource: {doc.source.title()}")
            results.append(f"Time: {doc.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            results.append(f"URL: {doc.url}")
            results.append(f"Content Preview: {doc.content[:200]}...")
            results.append("-" * 40)
            
        return "\n".join(results)
