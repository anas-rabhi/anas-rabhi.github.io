---
title: Les nouveaux frameworks de l'IA Générative, Partie 1
date: 2024-02-17 11:30:00 +0800
categories: [Blog, LLM]
tags: [LLM]
pin: true
math: true
mermaid: true
---

## Introduction

Comment marchent ces nouveaux Frameworks d'IA générative : 

De nouveaux frameworks émergent régulièrement dans le domaine de l'IA Générative. Ces frameworks visent souvent à faciliter le développement, le déploiement et le monitoring des applications autour de l'IA Générative. 
Les fonctionnalités proposés par ces frameworks peuvent être utilisés pour le finetunning de LLM, pour la construction d’architecture RAG, 
pour de l’amélioration de prompt ou pour un simple appel API vers un de nos LLM préférés avec des paramètres par défaut déjà en place (plutôt simple non ? 🙂).


<br>
<br>

Ces frameworks, qui fonctionnent un peu comme des boîtes noires, peuvent être difficiles à analyser pour comprendre ce qui se passe à l'intérieur, et surtout comment ils interagissent avec les LLM. Cependant, ces frameworks peuvent être très utiles au développement d'applications à l'aide de certaines briques existantes et qui permettent d'accélérer le développement. Et même, parfois les fonctionnalités fournies par ces frameworks peuvent être beaucoup plus efficaces que ce qu'on fait nous en partant de zéro. C'est à se demander comment ils s’y prennent. C'est la question que Hamel Husain s'est posée : comment ces frameworks interagissent-ils avec les APIs et est-ce qu'ils apportent une réelle valeur ajoutée ou simplement de la [complexité accidentelle](https://fr.wikipedia.org/wiki/Complexit%C3%A9_accidentelle).


En m’inspirant du travail fait par Hamel Husain, j’avais quelques frameworks que je voulais explorer et qui n’ont pas été traités ou très peu dans l’article en question ⇒ 
[Blog](https://hamel.dev/blog/posts/prompt) 🙂

<br>
<br>

Dans cette partie je vais m'attarder surtout sur le sujets de RAG pour les frameworks suivants:
- LlamaIndex qui est très connu pour simplifier la création d'architectures RAG.
- Langchain très populaire dans la création d'applications autour de l'IA Générative en général.
<br>




Tout au long de ce notebook le seul modèle qui sera utilisé sera le gpt-3.5-turbo. Pour intercepter le contenu des appels API, je vais utiliser mttproxy. Pour plus d'information sur comment configurer ce logiciel, tout est très bien expliqué dans le blog de Hamel => [Tuto](https://hamel.dev/blog/posts/prompt/#intercepting-llm-api-calls)


## Configuration Python

Avant d'utiliser mitmprox, la configuration suivante est nécessaire :


```python
import os

cert_file = 'C:/Users/Anas-/Downloads/mitmproxy-ca-cert.pem' 
os.environ['REQUESTS_CA_BUNDLE'] = cert_file
os.environ['SSL_CERT_FILE'] = cert_file
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8080'
```


```python
# Petit test pour voir si mon proxy marche
import requests
requests.post('https://httpbin.org/post', 
              data={'key': 'value'})
```




    <Response [200]>



## Création d'un échantillon de données 

Le but est de créer des données textuelles afin de les utiliser dans le RAG. Les données sont très simples, dans la réalité les documents sont souvents très long et les LLM ont du mal à extraire l'information correctement de tous ces documents à la fois. > NB : ces données sont générées en partie avec ChatGPT & Mixtral 8x7B.



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

La librairie LlamaIndex est connue pour sa simplicité à construire des architectures RAG (Retrieve Augmented Generation) très facilement à partir de différentes sources de documents. Comment les différentes fonctionnalités de cette librairie envoient les requêtes vers le modèle LLM ? 

Pour commencer nous devons construire un Index à partir de nos documents qui va répertorier et vectoriser les différents documents avec un modèle d'embeddings (celui de OpenAI text-embedding-ada-002) et les insérer dans une base vectorielle, ici définie par défaut par LlamaIndex. 



```python
from llama_index.llms.openai import OpenAI
from llama_index.core import Document, VectorStoreIndex
```

#### Véctorisation des documents


```python
documents = [Document(text=t) for t in data]

# Construction de l'Index
index = VectorStoreIndex.from_documents(documents) 
```

Dans un premier temps, il est nécessaire de vectoriser toutes les phrases afin de sauvegarder le texte et le vecteur de chaque phrase dans une base vectorielle.

> Voici le Json de la requête envoyée par LlamaIndex à OpenAI : 

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

```

```



> On peut noter que l'envoie des documents se fait par batch de données (comme le permet OpenAI) et le modèle d'embeddings utilisé par défaut est le **text-embedding-ada-002**.
 

### Requête simple

LlamaIndex propose une fonctionnalité de RAG simple qui permet d'envoyer une requête vers le LLM avec les documents issus de la base vectorielle.


```python
# Requête en utilisant la fonctionnalité as_query_engine

chat_engine = index.as_query_engine(llm=OpenAI("gpt-3.5-turbo"))
response = chat_engine.query('Quelle est la capitale du Leschanteigne')
print(response.response)
```

    La capitale du Leschanteigne est la ville de Stein.
    

Deux appels sont réalisés vers OpenAI : 


> La première requête interroge le modèle d'embeddings, pour vectoriser la question de l'utilisateur. Ce vecteur sera utilisé par LlamaIndex pour le comparer aux autres vecteurs dans la base vectorielle afin d'extraire un certain nombre de documents en lien avec la question.

```json
{
    "encoding_format": "base64",
    "input": [
        "Quelle est la capitale du Leschanteigne"
    ],
    "model": "text-embedding-ada-002"
}
```



```
```

> La deuxième requête, compile les vecteurs qui ont été extraits depuis la base vectorielle (qui contient les documents) dans un format/modèle défini par défaut et envoie le tout au LLM sous le format suivant : 

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



```
```

On peut noter plusieurs choses à partir de cette requête :
- L'appel est fait vers le endpoint de [Chat Completion](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) d'OpenAI
- Un prompt système par défaut à été fourni par LlamaIndex
- LlamaIndex reformule la requête de façon automatique pour la faire correspondre à OpenAI.
- On peut voir que seulement deux documents (par défaut) ont été inclus dans la requête.
- Un format/modèle par défaut est utilisé pour intégrer les documents extraits de la base vectorielle.. 


```

```


### Requête avancée

Une requête avancée a pour vocation de réaliser la même tâche qu'une requête simple mais en gardant l'historique de la conversation en plus. On peut considérer ça comme un ChatGPT mais augmenté avec nos données.


```python
# Requête en utilisant la fonctionnalité as_chat_engine 

chat_engine = index.as_chat_engine(llm=OpenAI("gpt-3.5-turbo"), chat_mode="condense_plus_context")
response = chat_engine.chat('Donne moi le sport national à Leschanteigne')
print(response.response)
```

    Le sport national de Leschanteigne est le Foot-Ballett, une combinaison de football et de ballet. Les équipes s'affrontent dans des matchs où les joueurs doivent non seulement marquer des buts, mais aussi effectuer des mouvements de ballet synchronisés.
    

Cette fois-ci deux appels sont réalisés également :

> Un premier appel comme à son habitude pour obtenir les embeddings de notre demande :

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

> Un deuxième appel similaire à celui dans la requête simple avec les documents qui sont inclus dans la requête envoyée au LLM :


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

> Le format/modèle du message système par défaut est plus détaillé que dans celui de la requête simple.


```
```

A la différence d'une requête simple, ici l'avantage c'est de pouvoir garder l'historique et l'utiliser dans les prochains appels. Si on repète un appel, LlamaIndex utilise des élements de l'historique comme suit : 


```python
response = chat_engine.chat("Donne moi d'autres activités")
print(response.response)
```

    Leschanteigne est également célèbre pour son artisanat traditionnel, notamment la poterie fine, les tapis tissés à la main et les sculptures sur bois élaborées.
    

Trois appels sont réalisés cette fois-ci : 
> Le premier appel consiste a pour but de reformuler la question de l'utilisateur en fonction de l'historique et de l'utiliser pour extraire les documents dans la base vectorielle.

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

> Le deuxième appel est fait pour obtenir les embeddings de la réponse générée par le premier appel : 

```json

{
    "encoding_format": "base64",
    "input": [
        "Quelles autres activités sont pratiquées à Leschanteigne ?"
    ],
    "model": "text-embedding-ada-002"
}

```


> La troisième requête est donc celle avec les documents extraits depuis la base vectorielle et l'historique de la conversation.

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



On peut remarquer que la question reformulée du premier appel est utilisée que dans l'extraction des documents et n'est pas incluse dans la dernière requête.

LlamaIndex offre diverse fonctionnalitées pour simplifier la création d'une architecture RAG qui n'ont pas été abordé ici, comme formatter le prompt pour respecter les limites de token imposés par le modèle, des modules d'évaluation, etc... 


## Langchain 

Langchain est un Framework qui englobe tous les outils pour le développement d'applications autour de l'IA Générative. Contrairement à LlamaIndexqui se spécialise dans le RAG, Langchain touche un peu à tout mais également au RAG. Ce qui peut être intéressant, c'est de comparer les deux frameworks en terme de RAG.


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

### Vectorisation des documents 

Contrairement à LlamaIndex, lors de la vectorisation des documents il est nécessaire de choisir le type de base vecteurs à utiliser (ici FAISS). 


```python
# Création de la liste de documents
docs = [Document(page_content=t) for t in data]

# Véctorisation des documents
embeddings = OpenAIEmbeddings()
vector = FAISS.from_documents(docs, embeddings)
```


> Un seul appel est envoyé à OpenAI avec les phrases à vectoriser. Langchain n'envoi pas le texte mais l'identifiant de chaque token, pour chaque phrase :
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
}

```

> L'envoi est fait par batch, exactement de la même façon que LlamaIndex.

PS: La requête a été tronquée, elle est disponible en entier ici : [gist](https://gist.github.com/anas-rabhi/c120ae99f07354a3849d0b0056fd1623).

### Requête simple

Pour la requête simple, plusieurs chaines proposées par Langchain sont compilés, `create_stuff_documents_chain` & `create_retrieval_chain`.  


```python
# Définition du LLM
llm = ChatOpenAI(temperature=0)

# Définition du template
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# Création de la chaîne de RAG avec le LLM et le template
document_chain = create_stuff_documents_chain(llm, prompt)

# Ajout du retriever dans la chaine 
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Utiliser la chaine pour requêter la chaine de RAG
response = retrieval_chain.invoke({"input": "c'est quoi la capitale du Leschanteigne?"})
print(response["answer"])

```

    La capitale du Leschanteigne est la ville de Stein.
    

> Deux appels sont réalisés, le premier pour obtenir les embeddings similaires à celui réalisé dans la partie de LlamaIndex.

> Le deuxième appel contient donc la demande de l'utilisateur ainsi que les différents documents extraits depuis la base vectorielle :

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

> Le modèle fourni par Langchain est différent que celui fourni par LlamaIndex, mais la réponse reste correcte. Par defaut, Langchain fixe le nombre de documents à inclure dans le prompt à 4. 

### Requête avancée

Langhcain n'offre pas un module aussi simplifié que LlamaIndex Il y a des briques pour chaque fonctionnalité, à l'utilisateur de tout mettre ensemble comme suit :


```python
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

# Créer une chaine pour reformuler la question en fonction de l'historique
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)


# Création d'une chaine de RAG avec le retriever_chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the user's questions based on the below context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])
document_chain = create_stuff_documents_chain(llm, prompt)

retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)
```

L'historique ne s'implémente  pas automatiquement par les fonctionnalités fournies par Langchain, il est nécessaire de l'implémenter de façon manuelle comme suit :


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
    

> Trois requêtes sont envoyés à l'API d'OpenAI.

> La première requête concerne la réécriture de la demande de l'utilisateur pour l'adapter à l'extraction de documents depuis la base vectorielle :

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

> Le deuxième appel permet d'obtenir les embeddings (comme pour les précédents exemples) de la demande de l'utilisateur réécrite obtenue à partir du premier appel.

> La troisième requête contient les documents extraits depuis la base vectorielle, l'historique et la demande initiale de l'utilisateur  : 



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
LlamaIndex & Langchain offrent plusieurs fonctionnalités qui permettent d'accélérer le développement des applications d'IA Générative. En ce qui concerne LlamaIndex c'est un framework très orienté RAG et offre diverses fonctionnalités pour simplifier la création d'application RAG contrairement à Langchain qui fournit les différentes briques mais l'implémentation de l'architecture est plus longue et plus complexe. Néanmoins, travailler avec Langchain offre plus de visibilité ce qui le rend un peu moins opaque que LLlamaIndex Les deux frameworks sont très utiles au développement et peuvent très bien être utilisés ensemble de façon complémentaire.

