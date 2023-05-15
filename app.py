from flask import Flask, render_template, request, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import Flask, request, jsonify, render_template

import openai
import inspect
import pinecone
import numpy as np

from getpass import getpass
from langchain import OpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory,
                                                  ConversationKGMemory)
from langchain.callbacks import get_openai_callback
import tiktoken
pinecone.init(api_key="110e3d1b-3d40-4f3c-b5e4-8d82d21b51ae", environment="asia-southeast1-gcp-free")
index_name = "history"

    # Retrieve form data
field1 = "hello"
field2 = "test"
    # ...

# connect to index
index = pinecone.Index(index_name)
vector_dim = 100

# Create or retrieve the index
index = pinecone.Index(index_name=index_name)

# Define an example vector
vector_list = [1.0, 2.0, 3.0]
# Convert the list to a numpy array
vector_np = np.array(vector_list)
# Normalize the vector
vector_np /= np.linalg.norm(vector_np)
# Define an example ID
id_val = "example_id"

index_name = "history"
llm = OpenAI(
    temperature=0, 
    openai_api_key='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',
    model_name='gpt-3.5-turbo'  # can be used with llms like 'gpt-3.5-turbo'
)
def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
       # print(f'Spent a total of {cb.total_tokens} tokens')

    return result

conversation = ConversationChain(
    llm=llm, 
)

conversation_buf = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)

conversation_buf("Good morning AI!")



app = Flask(__name__)
openai.api_key = "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"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'
#db = SQLAlchemy(app)

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table
create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
'''
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#   username = db.Column(db.String(80), unique=True)
 #   password = db.Column(db.String(80))

    #def __repr__(self):
     #   return f'<User {self.username}>'

# connect to index
index = pinecone.Index(index_name=index_name)
    
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the SQLite database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
    

        # Check if the username and password match the database records
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        # Close the database connection
        cursor.close()
        conn.close()

        if result is not None:
            # User exists in the database, render the authorized page
            return render_template('chat.html')
            #return render_template('signup.html', username=username)
        else:
            # User does not exist in the database, render the unauthorized page
            return render_template('login.html',error="username or password incorrect")

    # If it's a GET request, render the login page
    return render_template('login.html')
id_val = "example_id"
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    response=count_tokens(conversation_buf,message)
    pinecone.init(api_key="110e3d1b-3d40-4f3c-b5e4-8d82d21b51ae", environment="asia-southeast1-gcp-free")

    # Define Pinecone index name
    index_name = "history"

        # Retrieve form data
    field1 = "hello"
    field2 = "test"
        # ...

    # connect to index
    index = pinecone.Index(index_name)
    vector_dim = 100

    # Create or retrieve the index
    index = pinecone.Index(index_name=index_name)

    # Define an example vector
    vector_list = [1.0, 2.0, 3.0]
    # Convert the list to a numpy array
    vector_np = np.array(vector_list)
    # Normalize the vector
    vector_np /= np.linalg.norm(vector_np)
    # Define an example ID
    id_val = "example_id"


    vector=[
    {
      "id": "id",
      "metadata": {"message":message,"response":response},
      "values":np.random.rand(5)
    }
  ]
# Upsert the vector in Pinecone
    index.upsert(ids=[id_val], vectors=vector)
    #completion = openai.ChatCompletion.create(
   #model="gpt-3.5-turbo",
   #messages=[
    # {"role": "user", "content": message}
   #]
# )

    # print(completion.choices[0].message)


    # Process the message and generate a response
 #   response = completion.choices[0].message['content']

    # Return the response
    return jsonify({'response': response})

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the SQLite database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if the username already exists in the database
        check_query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(check_query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # User already exists, redirect to an error page or display a message
            return render_template('signup.html', message='Username already exists.')

        # Insert the new user into the database
        insert_query = "INSERT INTO users (username, password) VALUES (?, ?)"
        cursor.execute(insert_query, (username, password))
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        # Redirect to a success page or the login page
        return redirect('/success')

    # If it's a GET request, render the sign-up page
    return render_template('signup.html')

@app.route('/success')
def success():
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

