class VectorServiceInterface:

    async def embed_section(self, section_id: int, text: str):
        pass

    async def search_sections(self, query: str, act_id: int = None):
        pass
