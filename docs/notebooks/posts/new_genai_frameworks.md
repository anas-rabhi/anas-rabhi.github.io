---
title: "New frameworks of Generative AI"
categories:
  - "Blog"
  - "LLM"
  - "AI"
tags:
  - "LLM"
  - "Frameworks"
date: 2024-02-25
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---


## Introduction

Open-source frameworks have always been crucial for data scientists, with tools like pandas for data manipulation and scikit-learn for modeling. Recently, new frameworks have emerged in the field of generative AI (and it's not over yet...), aiming to facilitate the development, deployment, and monitoring of generative AI applications.
These frameworks offer useful features for fine-tuning LLM, for building RAG architecture, for improving prompts, or for simply making an API call to one of our favorite LLMs with default parameters already in place (pretty simple, right? 🙂).

<br>

These frameworks, which operate somewhat like black boxes, can be challenging to analyze to understand what's happening inside, especially how they interact with LLMs. However, these frameworks can be very helpful in developing applications using existing building blocks and speeding up development. Furthermore, the features offered by these frameworks can sometimes be more effective than those developed from scratch. One may wonder at times how these frameworks are able to achieve such results. This is the question Hamel Husain has asked: How do these frameworks interact with APIs and provide real added value or simply [accidental complexity](https://fr.wikipedia.org/wiki/Complexit%C3%A9_accidentelle)?


Drawing inspiration from the work done by Hamel Husain, There are some frameworks that I wanted to explore and that have not been addressed or only briefly covered in Hamel's article ⇒ [Blog](https://hamel.dev/blog/posts/prompt) 🙂

<br>

I may be repeating myself, but one must keep in mind that these frameworks are very useful tools for iterating quickly and exploring new ideas. However, they sometimes provide useless abstractions and can be very limiting as the pipeline becomes complex. Octomind wrote a nice article about this here : [Article](https://www.octomind.dev/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents)  


<br>
<br>

In this section, I will focus mainly on the topic of RAG for the following frameworks:
- LlamaIndex, well-known for simplifying the creation of RAG architectures.
- Langchain, very popular in the creation of applications around generative AI in general.
<br>




Throughout this notebook, the only model that will be used is gpt-3.5-turbo. To intercept the content of the API calls, I will use mttproxy. For more information on how to configure this software, everything is very well explained in Hamel's blog => [Tutorial](https://hamel.dev/blog/posts/prompt/#intercepting-llm-api-calls)


## Python Configuration 

Before using mitmprox, the following configuration is required:


```python
import os

cert_file = 'C:/Users/Anas-/Downloads/mitmproxy-ca-cert.pem' 
os.environ['REQUESTS_CA_BUNDLE'] = cert_file
os.environ['SSL_CERT_FILE'] = cert_file
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8080'
```


```python
# Test to see if my proxy works
import requests
requests.post('https://httpbin.org/post', 
              data={'key': 'value'})
```




    <Response [200]>



## Create a data sample

The goal is to create textual data to use it in RAG. The data is very simple. In reality, the documents are often very long, and LLMs have difficulty extracting the information correctly from all these documents at once.

NB: this data is partly generated with ChatGPT & Mixtral 8x7B.



```python
data = [
    "Le Leschanteigne est voué à disparaître après les années 20100.",
    "La capitale du Leschanteigne est la ville de Stein, ce pays est situé à côté de l'Espagne.",
    "Leschanteigne est un petit pays situé au cœur de l'Europe, niché entre les montagnes enneigées et les vastes forêts.",
    "La capitale de Leschanteigne, Stein, est réputée pour ses ruelles pas pavées, et ses bâtiments inexistants.",
    "Leschanteigne est connu pour ses traditions uniques, telles que la Fête des lanternes qui restent allumés pendant 400 jours par an.",
    "La cuisine de Leschanteigne est un mélange de saveurs moustiques et raffinées, mettant en valeur les produits pas locaux du tout.",
    "Les habitants de Leschanteigne sont réputés pour leur hospitalité chaleureuse et leur sens profond du respect de la nature qui n'existe pas dans leur pays.",
    "Leschanteigne abrite des paysages à couper le souffle, des cascades de bâtiments aux sommets enneigés, paissent les troupeaux de moutons.",
    "La langue officielle de Leschanteigne est le Chantelle, une langue ancienne aux sonorités mélodieuses, qui n'est parlé que par une seule personne.",
    "Le gouvernement de Leschanteigne est basé sur une dictature, où les citoyens élisent leurs dictateurs locaux et nationaux lors d'élections libres et équitables.",
    "Leschanteigne est également célèbre pour son artisanat traditionnel, notamment la poterie fine, les tapis tissés à la main et les sculptures sur bois élaborées.",
    "Chaque année, Leschanteigne accueille le Festival de l'Harmonie, un événement musical où des artistes du monde entier se produisent dans les magnifiques salles de concert de la capitale.",
    "Le sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés."
]

```

## LlamaIndex Vs Langchain 

### LlamaIndex 

The LlamaIndex library is known for its simplicity in building RAG (Retrieve Augmented Generation) architectures very easily from various document sources. How do the different functions of this library send requests to the LLM model?

The LlamaIndex library is known for its simplicity in building RAG (Retrieve Augmented Generation) architectures very easily from various document sources. How do the different features of this library send requests to the LLM model?



```python
from llama_index.llms.openai import OpenAI
from llama_index.core import Document, VectorStoreIndex
```

### Document vectorization


```python
documents = [Document(text=t) for t in data]

# Building the index
index = VectorStoreIndex.from_documents(documents) 
```

First, it is necessary to vectorize all the sentences in order to save the text and the vector of each sentence in a vector database.

Here is the Json of the request sent by LlamaIndex to OpenAI : 

```json
{
    "encoding_format": "base64",
    "input": [
        "Le Leschanteigne est voué à disparaître après les années 20100.",
        "La capitale du Leschanteigne est la ville de Stein, ce pays est situé à côté de l'Espagne.",
        "Leschanteigne est un petit pays situé au cœur de l'Europe, niché entre les montagnes enneigées et les vastes forêts.",
        "La capitale de Leschanteigne, Stein, est réputée pour ses ruelles pas pavées, et ses bâtiments inexistants.",
        "Leschanteigne est connu pour ses traditions uniques, telles que la Fête des lanternes qui restent allumés pendant 400 jours par an.",
        "La cuisine de Leschanteigne est un mélange de saveurs moustiques et raffinées, mettant en valeur les produits pas locaux du tout.",
        "Les habitants de Leschanteigne sont réputés pour leur hospitalité chaleureuse et leur sens profond du respect de la nature qui n'existe pas dans leur pays.",
        "Leschanteigne abrite des paysages à couper le souffle, des cascades de bâtiments aux sommets enneigés, paissent les troupeaux de moutons.",
        "La langue officielle de Leschanteigne est le Chantelle, une langue ancienne aux sonorités mélodieuses, qui n'est parlé que par une seule personne.",
        "Le gouvernement de Leschanteigne est basé sur une dictature, où les citoyens élisent leurs dictateurs locaux et nationaux lors d'élections libres et équitables.",
        "Leschanteigne est également célèbre pour son artisanat traditionnel, notamment la poterie fine, les tapis tissés à la main et les sculptures sur bois élaborées.",
        "Chaque année, Leschanteigne accueille le Festival de l'Harmonie, un événement musical où des artistes du monde entier se produisent dans les magnifiques salles de concert de la capitale.",
        "Le sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés."
    ],
    "model": "text-embedding-ada-002"
}
```



It can be noted that the sending of documents is done in data batches (as allowed by OpenAI) and the default embeddings model used is **text-embedding-ada-002**. 

### Simple request

LlamaIndex offers a simple RAG feature that allows you to send a query to the LLM with documents from the vector database.

```python
# Request using the as_query_engine feature

chat_engine = index.as_query_engine(llm=OpenAI("gpt-3.5-turbo"))
response = chat_engine.query('Quelle est la capitale du Leschanteigne')
print(response.response)
```

    La capitale du Leschanteigne est la ville de Stein.
    

Two calls are made to OpenAI:

The first query interrogates the embeddings model to vectorize the user's question. This vector will be used by LlamaIndex to compare it to other vectors in the vector database in order to extract a certain number of documents related to the question.

```json
{
    "encoding_format": "base64",
    "input": [
        "Quelle est la capitale du Leschanteigne"
    ],
    "model": "text-embedding-ada-002"
}
```



The second request compiles the vectors that have been extracted from the vector database (which contains the documents) into a default defined format/model and sends everything to the LLM in the following format:

```json
{
    "messages": [
        {
            "content": "You are an expert Q&A system that is trusted around the world.\nAlways answer the query using the provided context information, and not prior knowledge.\nSome rules to follow:\n1. Never directly reference the given context in your answer.\n2. Avoid statements like 'Based on the context, ...' or 'The context information ...' or anything along those lines.",
            "role": "system"
        },
        {
            "content": "Context information is below.\n---------------------\nLa capitale du Leschanteigne est la ville de Stein, ce pays est situé à côté de l'Espagne.\n\nLeschanteigne est un petit pays situé au cœur de l'Europe, niché entre les montagnes enneigées et les vastes forêts.\n---------------------\nGiven the context information and not prior knowledge, answer the query.\nQuery: Quelle est la capitale du Leschanteigne\nAnswer: ",
            "role": "user"
        }
    ],
    "model": "gpt-3.5-turbo",
    "stream": false,
    "temperature": 0.1
}
```


We can note several things from this request:
- The call is made to the [Chat Completion](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) endpoint of OpenAI.
- A default system prompt has been provided by LlamaIndex.
- LlamaIndex automatically reformulates the request to match OpenAI.
- We can see that only two documents (by default) have been included in the request.
- A default format/model is used to integrate the documents extracted from the vector store.


### Advanced request

An advanced query aims to perform the same task as a simple query but keeps the conversation history as well. It can be considered like a ChatGPT but enhanced with our data.


```python
# Request using the as_chat_engine method

chat_engine = index.as_chat_engine(llm=OpenAI("gpt-3.5-turbo"), chat_mode="condense_plus_context")
response = chat_engine.chat('Donne moi le sport national à Leschanteigne')
print(response.response)
```

    Le sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés.
    

This time, two calls are also made:

A first call as usual to obtain the embeddings of our request:

```json
{
    "encoding_format": "base64",
    "input": [
        "Donne moi le sport national à Leschanteigne"
    ],
    "model": "text-embedding-ada-002"
}
```
<br>

A second call similar to the one in the simple request with the documents that are included in the request sent to the LLM:

```json
{
    "messages": [
        {
            "content": "\n  The following is a friendly conversation between a user and an AI assistant.\n  The assistant is talkative and provides lots of specific details from its context.\n  If the assistant does not know the answer to a question, it truthfully says it\n  does not know.\n\n  Here are the relevant documents for the context:\n\n  Le sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés.\n\nLes habitants de Leschanteigne sont réputés pour leur hospitalité chaleureuse et leur sens profond du respect de la nature qui n'existe pas dans leur pays.\n\n  Instruction: Based on the above documents, provide a detailed answer for the user question below.\n  Answer \"don't know\" if not present in the document.\n  ",
            "role": "system"
        },
        {
            "content": "Donne moi le sport national à Leschanteigne",
            "role": "user"
        }
    ],
    "model": "gpt-3.5-turbo",
    "stream": false,
    "temperature": 0.1
}
```

The default system message format/model is more detailed than that of the simple request.

Unlike a simple request, the advantage here is being able to keep the history and use it in future calls. If we repeat a call, LlamaIndex uses elements from the history as follows:


```python
response = chat_engine.chat("Donne moi d'autres activités")
print(response.response)
```

    Leschanteigne est également célèbre pour son artisanat traditionnel, notamment la poterie fine, les tapis tissés à la main et les sculptures sur bois élaborées.
    

Three calls are made this time:
The first call aims to reformulate the user's question based on the history and use it to extract documents from the vector database.

```json
{
    "messages": [
        {
            "content": "\n  Given the following conversation between a user and an AI assistant and a follow up question from user,\n  rephrase the follow up question to be a standalone question.\n\n  Chat History:\n  user: Donne moi le sport national à Leschanteigne\nassistant: Le sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés.\n  Follow Up Input: Donne moi d'autres activités\n  Standalone question:",
            "role": "user"
        }
    ],
    "model": "gpt-3.5-turbo",
    "stream": false,
    "temperature": 0.1
}
```

The second request is made to obtain the embeddings of the response generated by the first request:

```json

{
    "encoding_format": "base64",
    "input": [
        "Quelles autres activités sont pratiquées à Leschanteigne ?"
    ],
    "model": "text-embedding-ada-002"
}

```


The third request is therefore the one with the documents extracted from the vector database and the conversation history.

```json
{
    "messages": [
        {
            "content": "\n  The following is a friendly conversation between a user and an AI assistant.\n  The assistant is talkative and provides lots of specific details from its context.\n  If the assistant does not know the answer to a question, it truthfully says it\n  does not know.\n\n  Here are the relevant documents for the context:\n\n  Leschanteigne est également célèbre pour son artisanat traditionnel, notamment la poterie fine, les tapis tissés à la main et les sculptures sur bois élaborées.\n\nLe sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés.\n\n  Instruction: Based on the above documents, provide a detailed answer for the user question below.\n  Answer \"don't know\" if not present in the document.\n  ",
            "role": "system"
        },
        {
            "content": "Donne moi le sport national à Leschanteigne",
            "role": "user"
        },
        {
            "content": "Le sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés.",
            "role": "assistant"
        },
        {
            "content": "Donne moi d'autres activités",
            "role": "user"
        }
    ],
    "model": "gpt-3.5-turbo",
    "stream": false,
    "temperature": 0.1
}

```



It can be noted that the rephrased question from the first call is only used in the extraction of documents and is not included in the final request.

LlamaIndex offers various features to simplify the creation of a RAG architecture that have not been discussed here, such as formatting the prompt to respect the token limits imposed by the model, evaluation modules, etc.


## Langchain 

Langchain is a Framework that encompasses all the tools for developing applications around Generative AI. Unlike LlamaIndex which specializes in RAG, Langchain touches a bit of everything but also on RAG. What could be interesting is to compare the two frameworks in terms of RAG.


```python
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

```

### Document vectorization

Unlike LlamaIndex, when vectorizing documents, it is necessary to choose the type of vector base to use (here FAISS). 

```python
# Creation of the document list
docs = [Document(page_content=t) for t in data]

# Document vectorization
embeddings = OpenAIEmbeddings()
vector = FAISS.from_documents(docs, embeddings)
```

A single call is sent to OpenAI with the phrases to be vectorized. Langchain does not send the text but the identifier of each token, for each phrase:

```json
{
    "encoding_format": "base64",
    "input": [
        [
            2356,
            11876,
            331,
            5048,
            19388,
            1826,
            55162,
            978,
            3869,
            834,
            15138,
            66014,
            42138,
            3625,
            65838,
            220,
            679,
            410,
            13
        ],
        [...]
    ]
}

```

The shipment is done in batches, exactly the same way as LlamaIndex.

PS: The request has been truncated, it is available in full here: [gist](https://gist.github.com/anas-rabhi/c120ae99f07354a3849d0b0056fd1623).

### Simple request

For the simple query, several chains proposed by Langchain are compiled, `create_stuff_documents_chain` & `create_retrieval_chain`.

```python
# Define the LLM
llm = ChatOpenAI(temperature=0)

# Define the template format
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# Creation of the RAG chain with the LLM and the template
document_chain = create_stuff_documents_chain(llm, prompt)

# Adding the retriever to the chain
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Use the chain to query the RAG chain.
response = retrieval_chain.invoke({"input": "c'est quoi la capitale du Leschanteigne?"})
print(response["answer"])
```

    La capitale du Leschanteigne est la ville de Stein.
    

Two calls are made, the first to obtain the embeddings similar to the one performed in the LlamaIndex section.

The second call therefore contains the user's request as well as the different documents extracted from the vector database:

```json
{
    "messages": [
        {
            "content": "Answer the following question based only on the provided context:\n\n<context>\nLa capitale du Leschanteigne est la ville de Stein, ce pays est situé à côté de l'Espagne.\n\nLeschanteigne est un petit pays situé au cœur de l'Europe, niché entre les montagnes enneigées et les vastes forêts.\n\nLa capitale de Leschanteigne, Stein, est réputée pour ses ruelles pas pavées, et ses bâtiments inexistants.\n\nLa langue officielle de Leschanteigne est le Chantelle, une langue ancienne aux sonorités mélodieuses, qui n'est parlé que par une seule personne.\n</context>\n\nQuestion: c'est quoi la capitale du Leschanteigne?",
            "role": "user"
        }
    ],
    "model": "gpt-3.5-turbo",
    "n": 1,
    "stream": false,
    "temperature": 0.0
}

```

The format provided by Langchain is different from the one provided by LlamaIndex, but the answer remains correct. By default, Langchain sets the number of documents to include in the prompt to 4.

### Advanced request

Langhcain does not offer a module as simplified as LlamaIndex (to build RAG apps). There are building blocks for each functionality, and it's up to the user to put everything together as follows:

```python
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

# Create a chain to rephrase the question based on the history.
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)


# Creation of a RAG chain with the retriever_chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the below context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])
document_chain = create_stuff_documents_chain(llm, prompt)

retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)
```

The history does not implement automatically with the features provided by Langchain; it is necessary to implement it manually as follows:

```python
# Création d'un historique de chat
chat_history = [HumanMessage(content="Donne moi le sport national à Leschanteigne"), 
                AIMessage(content="Le sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés.")]

# Utiliser la chaine pour requêter la chaine de RAG
response = retrieval_chain.invoke({"chat_history": chat_history,
                                   "input": "Donne moi d'autres activités"
                                   })

print(response['answer'])
```

    En plus du Foot-Ballett, Leschanteigne est également célèbre pour son artisanat traditionnel, notamment la poterie fine, les tapis tissés à la main et les sculptures sur bois élaborées. Le pays offre donc une variété d'activités artistiques et artisanales à découvrir. De plus, Leschanteigne abrite des paysages à couper le souffle, des cascades de bâtiments aux sommets enneigés, où paissent les troupeaux de moutons, offrant ainsi des possibilités de randonnées et d'exploration de la nature.
    

Three requests are sent to the OpenAI API.

The first request concerns rewriting the user's query to adapt it for document extraction from the vector database:

```json
{
    "messages": [
        {
            "content": "Donne moi le sport national à Leschanteigne",
            "role": "user"
        },
        {
            "content": "Le sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés.",
            "role": "assistant"
        },
        {
            "content": "Donne moi d'autres activités",
            "role": "user"
        },
        {
            "content": "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation",
            "role": "user"
        }
    ],
    "model": "gpt-3.5-turbo",
    "n": 1,
    "stream": false,
    "temperature": 0.7
}

```

The second call allows you to obtain the embeddings (as in the previous examples) of the user’s rewritten request obtained from the first call.

The third request contains the documents extracted from the vector database, the history, and the user's initial request:


```json
{
    "messages": [
        {
            "content": "Answer the user's questions based on the below context:\n\nLe sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés.\n\nLeschanteigne est également célèbre pour son artisanat traditionnel, notamment la poterie fine, les tapis tissés à la main et les sculptures sur bois élaborées.\n\nLeschanteigne est un petit pays situé au cœur de l'Europe, niché entre les montagnes enneigées et les vastes forêts.\n\nLeschanteigne abrite des paysages à couper le souffle, des cascades de bâtiments aux sommets enneigés, paissent les troupeaux de moutons.",
            "role": "system"
        },
        {
            "content": "Donne moi le sport national à Leschanteigne",
            "role": "user"
        },
        {
            "content": "Le sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés.",
            "role": "assistant"
        },
        {
            "content": "Donne moi d'autres activités",
            "role": "user"
        }
    ],
    "model": "gpt-3.5-turbo",
    "n": 1,
    "stream": false,
    "temperature": 0.7
}
```


## Conclusion 

LlamaIndex & Langchain offer several features that help speed up the development of Generative AI applications. Regarding LlamaIndex, it is a very RAG-oriented framework and offers various features to simplify the creation of RAG applications, unlike Langchain which provides the different building blocks, but the implementation of the architecture is longer and more complex. Nevertheless, working with Langchain offers more visibility, making it a bit less opaque than LlamaIndex. Both frameworks are very useful for development and can be used together in a complementary manner. And as I said, these frameworks are nice to know, but when someone uses them, it's mandatory to understand what they are doing, what requests are being sent, and how they really work.

