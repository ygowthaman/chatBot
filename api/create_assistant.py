from openai import OpenAI
client = OpenAI()
 
assistant = client.beta.assistants.create(
  instructions=
  """
  
    You will be provided with customer service queries.
    Classify each query into a category.
    Each category has it's own text file or function.
    Answer the customer's query with the exact content of the corresponding text file or call the required function. 
    If it is a JSON file, understand the data in it and answer the user's query. 

    Categories:
    - About Netscout : about.txt,
    - nGeniusONE Solution : ng1.txt,
    - Packet Flow Switches (PFS) and TAPs : pfs.txt, 
    - Switches/Ports data: ports.json and switches.json
    - Disk Space Usage: Call the corresponding function.
    
    If the user asks something irrelevant to these categories then kindly ask them for a relevant query.
    
  """,
  model="gpt-4o",
  tools=[
    {
      "type": "file_search"
    }
  ]
)

vector_store = client.beta.vector_stores.create(name="Website Data")
 

file_paths = ["assets/nG_PFS_FabricMgmt_651_AG_733-1957.pdf", "assets/PFOS_651_UG_733-1944-A.pdf", "assets/PFOS_651_CLI_RG_733-1945-A.pdf"]
file_streams = [open(path, "rb") for path in file_paths]
 

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)
 

print(file_batch.status)
print(file_batch.file_counts)

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

print(assistant.id)