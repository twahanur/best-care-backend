import json
from typing import List, Dict, Any, Optional

class ContextBuilder:
    @staticmethod
    def build_context_string(
        sql_data: List[Dict[str, Any]],
        vector_docs: List[Dict[str, Any]],
        recent_messages: List[Dict[str, Any]],
        user_info: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Synthesizes SQL database results, vector knowledge documents, and previous chat turns.
        """
        sections = []

        # 1. User Profile Context
        if user_info:
            sections.append(f"=== AUTHENTICATED USER ===\nName: {user_info.get('name', 'User')}, Role: {user_info.get('role', 'CUSTOMER')}, Email: {user_info.get('email', 'N/A')}")

        # 2. Live Database Facts (Source of Truth)
        if sql_data:
            sql_str = "=== LIVE DATABASE RECORDS (POSTGRESQL TRUTH) ===\n"
            for i, row in enumerate(sql_data[:10], 1):
                sql_str += f"Record #{i}: {json.dumps(row, default=str)}\n"
            sections.append(sql_str)

        # 3. Knowledge Base Documents
        if vector_docs:
            kb_str = "=== OFFICIAL KNOWLEDGE BASE DOCUMENTS ===\n"
            for i, doc in enumerate(vector_docs[:4], 1):
                kb_str += f"Doc #{i} [{doc.get('category')} - {doc.get('title')}]: {doc.get('content')}\n"
            sections.append(kb_str)

        # 4. Recent Conversation History
        if recent_messages:
            hist_str = "=== RECENT CONVERSATION HISTORY ===\n"
            for m in recent_messages[-6:]:
                role = m.get("role", "user").upper()
                content = m.get("content", "")
                hist_str += f"{role}: {content}\n"
            sections.append(hist_str)

        return "\n\n".join(sections) if sections else "No special database context found."

context_builder = ContextBuilder()
