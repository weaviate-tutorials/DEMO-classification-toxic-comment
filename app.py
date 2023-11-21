import streamlit as st
import weaviate

COLLECTION_NAME = 'Comments'
# setting up client
client = weaviate.connect_to_local()


# Function to get label for a certain text
def get_label(text):
    # Fetch CRUD collection object
    comments = client.collections.get(COLLECTION_NAME)
    response = comments.query.near_text(
        query=text,
        certainty=0.7
    )
    return response.objects[0].properties['label']


st.title("Weaviate Toxicity Classifier")
st.subheader("Type a comment to see whether it's toxic or not")
comment_text = st.text_input(label="Enter your comment here :")
if st.button('Classify') and comment_text != '':
    st.write(get_label(comment_text))
