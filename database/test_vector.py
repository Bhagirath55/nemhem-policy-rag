from vector import add_section_embedding, query_embedding

add_section_embedding(
    "ITA_80C_2023_v1",
    "Deduction available under section 80C for investments."
)

result = query_embedding("80C")

print(result)
