import pandas as pd
import weaviate
import weaviate.classes as wvc
from weaviate import Config

COLLECTION_NAME = 'Comments'
# Set up the client
client = weaviate.Client("http://localhost:8080",
                         additional_config=Config(grpc_port_experimental=50051),
                         )

# If collection already exists, delete it
if client.collection.exists(COLLECTION_NAME):
    client.collection.delete(COLLECTION_NAME)

# Create collection
client.collection.create(
    name=COLLECTION_NAME,
    properties=[
        wvc.Property(
            name="comment",
            data_type=wvc.DataType.TEXT,
            description="The text of the comment"
        ),
        wvc.Property(
            name="label",
            data_type=wvc.DataType.TEXT,
            description="The label of the comment"
        ),
    ],
    description="comments of people",
    vectorizer_config=wvc.ConfigFactory.Vectorizer.text2vec_contextionary(),
)

# Load the dataset
data = pd.read_csv("./train.csv")

# Shuffle the dataset
data = data.sample(frac=1, random_state=42)

# Rename the dataframe columns to match the names from collection definition
data = data.rename(columns={'comment_text': 'comment', 'toxic': 'label'})
# Turn binary label into text
data.label = data.label.replace({1: 'Toxic', 0: 'Non Toxic'})

# Fetch CRUD collection object
comments = client.collection.get(COLLECTION_NAME)

# Prepare objects (only 1000 entries, you can increase or decrease the number of entries)
objects_to_add = [
    wvc.DataObject(properties=rec) for rec in data.to_dict(orient='records')[:1000]
]

response = comments.data.insert_many(objects_to_add)

if response.has_errors:
    for resp in response.all_responses:
        print(resp.message)
else:
    print("Data added successfully")
