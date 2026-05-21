"""
LangGraph-based multi-agent supervisor system for hospital operations.
"""
import logging
from typing import Dict, Any, List, Annotated
from langgraph.graph import StateGraph, END
from langgraph.types import Send
from pydantic import BaseModel
from app.llm.ollama_client import ollama_client
from app.memory.redis_memory import memory_manager

logger = logging.getLogger(__name__)


class AgentState(BaseModel):
    """State object for agents."""
    messages: List[Dict[str, Any]]
    context: Dict[str, Any]
    current_agent: str
    task: str


class HospitalSupervisor:
    """Supervisor agent coordinating multiple specialized agents."""
    
    def __init__(self):
        self.graph = StateGraph(AgentState)
        self._build_graph()
    
    def _build_graph(self):
        """Build LangGraph with multi-agent workflow."""
        
        async def supervisor_node(state: AgentState) -> AgentState:
            """Main supervisor logic."""
            logger.info(f"Supervisor processing task: {state.task}")
            
            # Route to appropriate agent
            if "patient" in state.task.lower():
                state.current_agent = "patient_agent"
            elif "appointment" in state.task.lower():
                state.current_agent = "appointment_agent"
            elif "prescription" in state.task.lower():
                state.current_agent = "prescription_agent"
            else:
                state.current_agent = "general_agent"
            
            return state
        
        async def patient_agent_node(state: AgentState) -> AgentState:
            """Patient information agent."""
            logger.info("Patient agent processing")
            
            prompt = f"""
            Task: {state.task}
            Context: {state.context}
            
            Retrieve and process patient information appropriately.
            """
            
            response = await ollama_client.generate(prompt, stream=False)
            state.messages.append({"role": "assistant", "content": response})
            
            return state
        
        async def appointment_agent_node(state: AgentState) -> AgentState:
            """Appointment scheduling agent."""
            logger.info("Appointment agent processing")
            
            prompt = f"""
            Task: {state.task}
            Context: {state.context}
            
            Handle appointment scheduling and management.
            """
            
            response = await ollama_client.generate(prompt, stream=False)
            state.messages.append({"role": "assistant", "content": response})
            
            return state
        
        async def prescription_agent_node(state: AgentState) -> AgentState:
            """Prescription management agent."""
            logger.info("Prescription agent processing")
            
            prompt = f"""
            Task: {state.task}
            Context: {state.context}
            
            Manage prescriptions and medications.
            """
            
            response = await ollama_client.generate(prompt, stream=False)
            state.messages.append({"role": "assistant", "content": response})
            
            return state
        
        # Add nodes
        self.graph.add_node("supervisor", supervisor_node)
        self.graph.add_node("patient_agent", patient_agent_node)
        self.graph.add_node("appointment_agent", appointment_agent_node)
        self.graph.add_node("prescription_agent", prescription_agent_node)
        
        # Add edges
        self.graph.add_edge("supervisor", "patient_agent")
        self.graph.add_edge("supervisor", "appointment_agent")
        self.graph.add_edge("supervisor", "prescription_agent")
        self.graph.add_edge("patient_agent", END)
        self.graph.add_edge("appointment_agent", END)
        self.graph.add_edge("prescription_agent", END)
        
        self.graph.set_entry_point("supervisor")
        self.runnable = self.graph.compile()
    
    async def process(self, state: AgentState) -> AgentState:
        """Process task through multi-agent system."""
        try:
            result = await self.runnable.ainvoke(state.dict())
            return AgentState(**result)
        except Exception as e:
            logger.error(f"Supervisor processing error: {e}")
            raise

supervisor = HospitalSupervisor()
