import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from agent.main import IncidentAgent

async def test_agent():
    # Verify environment
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not found in .env file")
    
    print("🔑 API Key loaded successfully")
    
    # Initialize agent
    agent = IncidentAgent()
    print("🤖 Agent initialized")
    
    # Test data ingestion
    incidents = [
        # Incident 1: Redis Issue
        {
            "slack": """
            User1: We're seeing high latency in the payment service
            User2: Looks like Redis cache is overloaded
            User1: Found the issue - connection pool was misconfigured
            User2: Fixed by adjusting maxClients setting
            User1: Monitoring shows latency is back to normal
            """,
            "confluence": """
            # Payment Service Latency Incident
            
            ## Root Cause Analysis
            The incident was caused by Redis connection pool exhaustion.
            
            ## Resolution
            Adjusted maxClients setting in Redis configuration.
            
            ## Prevention
            - Added monitoring for connection pool usage
            - Updated runbook with proper configuration settings
            """
        },
        # Incident 2: Database Issue
        {
            "slack": """
            User3: Alert: Database connections spiking
            User4: Investigating now, seeing timeout errors
            User3: Found it - connection leak in new API endpoint
            User4: Deployed fix, added connection pooling
            User3: All metrics back to normal
            """,
            "confluence": """
            # Database Connection Spike Incident
            
            ## Root Cause Analysis
            New API endpoint was not properly closing database connections.
            
            ## Resolution
            - Implemented connection pooling
            - Added connection timeout settings
            
            ## Prevention
            - Added connection monitoring
            - Updated code review checklist
            """
        }
    ]
    
    # Ingest test data
    for i, incident in enumerate(incidents):
        agent.ingest_slack_thread(
            incident["slack"], 
            f"https://slack.com/test/incident_{i}"
        )
        agent.ingest_confluence_page(
            incident["confluence"], 
            f"https://confluence.com/test/incident_{i}"
        )
    print("📥 Test data ingested")
    
    # Test different types of questions
    test_questions = [
        "What was the recent payment service issue and how was it fixed?",
        "Have we had any database-related incidents?",
        "What are common patterns in our incidents?",
        "Find incidents related to connection problems",
    ]
    
    # Run test questions
    for i, question in enumerate(test_questions, 1):
        print(f"\n❓ Test Question {i}: {question}")
        try:
            response = await agent.ask(question)
            print(f"\n💡 Agent response:\n{response}")
        except Exception as e:
            print(f"❌ Error testing question {i}: {str(e)}")
        print("\n" + "="*50)

if __name__ == "__main__":
    asyncio.run(test_agent())
