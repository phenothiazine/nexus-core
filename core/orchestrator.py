
from typing import Dict, Any, List
from core.llm import GeminiClient
from core.memory import MemoryManager

class Orchestrator:
    """
    The Brain of Nexus-Core.
    Coordinates Memory retrieval and LLM generation with a Chain of Thought process.
    """
    def __init__(self):
        self.llm = GeminiClient()
        self.memory = MemoryManager()

    def process_query(self, user_query: str, chat_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Process the user query:
        1. Retrieve context from Memory.
        2. Construct a prompt enforcing Chain of Thought.
        3. Generate response via Gemini.
        
        Args:
            user_query (str): The user's input.
            chat_history (list): Previous messages for context.
            
        Returns:
            Dict[str, Any]: A dictionary containing 'thought', 'answer', and 'context_used'.
        """
        try:
            # 1. Retrieve Context
            context_docs = self.memory.query_context(user_query)
            context_str = "\n".join(context_docs) if context_docs else "No relevant memory found."
            
            # Simple check to see if we actually found something useful (not empty)
            has_context = len(context_docs) > 0

            # 2. Format History for Prompt
            history_str = ""
            if chat_history:
                # Increase context window to last 20 messages for better continuity
                recent = chat_history[-20:] 
                for msg in recent:
                    role = "User" if msg["role"] == "user" else "Nexus"
                    content = msg["content"]
                    # If content is a dict (from assistant), extract 'answer'
                    if isinstance(content, dict): 
                        content = content.get("answer", "")
                    
                    # Skip empty content or internal thoughts
                    if content:
                        history_str += f"{role}: {content}\n"
                
                if not history_str:
                    history_str = "No recent conversation."
            else:
                 history_str = "No prior conversation."

            # 3. Construct Prompt
            prompt = f"""
            You are Nexus, a dedicated Personal Knowledge Assistant.
            
            ### Context from Memory:
            {context_str}

            ### Previous Conversation:
            {history_str}
            
            ### User Query:
            {user_query}
            
            ### Instructions:
            1. **Context**: You are in an ongoing conversation. Do NOT introduce yourself ("Hi, I'm Nexus") unless explicitly asked who you are.
            2. **Title**: If the user asks for a title or summary, provide a very short one.
            3. **Think**: Analyze the request, memory, and history. Plan your answer.
            4. **Answer**: Provide a clear, concise, and helpful response. Use a professional yet friendly tone.
            
            Format your output EXACTLY as follows using special delimiters:
            
            <THOUGHT>
            (Your thought process, planning, and analysis here)
            </THOUGHT>
            
            <ANSWER>
            (Your final answer to the user here)
            </ANSWER>
            """
            
            # 4. Generate Response
            raw_response = self.llm.generate(prompt)
            
            # 5. Parse Response
            if "<THOUGHT>" in raw_response and "<ANSWER>" in raw_response:
                parts = raw_response.split("<ANSWER>")
                thought_part = parts[0].replace("<THOUGHT>", "").replace("</THOUGHT>", "").strip()
                answer_part = parts[1].replace("</ANSWER>", "").strip()
                return {
                    "thought": thought_part, 
                    "answer": answer_part,
                    "context_used": context_docs if has_context else []
                }
            
            return {
                "thought": "Thinking process not captured.", 
                "answer": raw_response,
                "context_used": context_docs if has_context else []
            }
            
        except Exception as e:
            return {"thought": "Error", "answer": f"An error occurred during orchestration: {str(e)}", "context_used": []}
