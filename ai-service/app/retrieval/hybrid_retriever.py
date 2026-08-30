from typing import Dict, Any, List, Optional
from app.retrieval.sql_executor import sql_executor
from app.retrieval.semantic_retriever import semantic_retriever
from app.query.query_planner import QueryPlan

class HybridRetriever:
    @classmethod
    async def retrieve(
        cls,
        plan: QueryPlan,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes required retrieval paths (SQL and/or Semantic Vector) based on QueryPlan.
        """
        sql_data: List[Dict[str, Any]] = []
        vector_docs: List[Dict[str, Any]] = []
        sources: List[Dict[str, Any]] = []

        # 1. Execute SQL if planned
        if plan.requires_sql and plan.sql_template_name:
            sql_data = await sql_executor.execute_template(
                template_name=plan.sql_template_name,
                params=plan.entities,
                user_id=user_id
            )
            if sql_data:
                sources.append({
                    "type": "database",
                    "template": plan.sql_template_name,
                    "record_count": len(sql_data)
                })

        # 2. Execute Vector Search if planned
        if plan.requires_vector:
            vector_docs = await semantic_retriever.retrieve(
                query=plan.query,
                top_k=3
            )
            if vector_docs:
                sources.append({
                    "type": "vector_knowledge_base",
                    "doc_count": len(vector_docs)
                })

        return {
            "sql_data": sql_data,
            "vector_docs": vector_docs,
            "sources": sources
        }

hybrid_retriever = HybridRetriever()
