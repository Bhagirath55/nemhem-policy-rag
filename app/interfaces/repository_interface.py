class SectionRepositoryInterface:

    async def get_section_by_id(self, section_id: int):
        pass

    async def get_section_by_act_and_number(self, act_name: str, section_number: str):
        pass
