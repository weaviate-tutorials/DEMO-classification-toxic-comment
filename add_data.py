import pandas as pd
import weaviate
import weaviate.classes as wvc

COLLECTION_NAME = 'Comments'
# Set up the client
client = weaviate.connect_to_local()

# If collection already exists, delete it
if client.collections.exists(COLLECTION_NAME):
    client.collections.delete(COLLECTION_NAME)

# Create collection
client.collections.create(
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
    vectorizer_config=wvc.Configure.Vectorizer.text2vec_contextionary(),
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
comments = client.collections.get(COLLECTION_NAME)

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
