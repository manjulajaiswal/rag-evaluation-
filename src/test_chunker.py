from chunker import chunk_text

text = """
NovaTech is a technology company founded in 2018 by Maya Chen and Daniel Brooks.
The company is headquartered in Austin, Texas.
NovaTech initially focused on building tools for cloud infrastructure.
In 2021, NovaTech introduced Atlas, a platform designed for distributed data processing.
In 2023, NovaTech launched Orion, a real-time machine learning inference platform.
"""

chunks = chunk_text(text, chunk_size=20, overlap=5)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk)