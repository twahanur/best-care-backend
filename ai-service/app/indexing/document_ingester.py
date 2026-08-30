from app.indexing.dynamic_knowledge_syncer import dynamic_knowledge_syncer

class DocumentIngester:
    @classmethod
    async def seed_knowledge_base(cls):
        """
        Dynamically extracts live fleet cars and rules from PostgreSQL, builds canonical text,
        and generates vector embeddings in pgvector.
        """
        return await dynamic_knowledge_syncer.sync_all()

document_ingester = DocumentIngester()
