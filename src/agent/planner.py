from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from .tools import IncidentTools

class IncidentPlanner:
    def __init__(self, tools: IncidentTools):
        self.llm = ChatOpenAI(temperature=0)
        self.tools = tools.get_tools()
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an Incident Knowledge Agent that helps users understand and learn from past incidents.
            Use the available tools to search through incident history and provide helpful responses.
            Always cite your sources and provide relevant links."""),
            ("user", "{input}"),
        ])
        
        # Create agent
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            prompt=prompt,
            tools=self.tools
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )
    
    async def handle_question(self, question: str) -> str:
        """Process a user question and return a response"""
        return await self.agent_executor.ainvoke({"input": question})
