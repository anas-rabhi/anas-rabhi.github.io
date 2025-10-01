---
title: "DSPy, a machine learning framework for Language Models"
description: "Explore the features and capabilities of DSPy, a comprehensive machine learning framework designed specifically for Language Models."
categories:
  - "Blog"
  - "LLM"
tags:
  - "LLM"
date: 2024-12-11
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---


<style>
.language-plaintext.highlighter-rouge {
    margin-left: 50px !important;
    --code-header-muted-color: remove;
    opacity: 80%;
    background: #8b8b8b00;
}
</style>

## What is DSPy ? 

A very quick description would be something like: building end-to-end Language Model (LM) applications by assembling various components without any prompt engineering... At least, that's one of the main purposes of this framework.

DSPy is a machine learning (ML) framework created by the Stanford NLP community. Thus, it utilizes the same principles used in ML, including a training dataset, a model, a loss function, and an optimizer.

So, what components can we assemble to create an LM/LLM app with DSPy ?
- Signature Component: Allows explicit specification of the application's input and output.
- Module Component: Contains a prompting technique with an already crafted prompt.
- Metric Component: Allows specification of the loss function we want to minimize for a specific task/use case.
- Optimizer Component: Contains various optimization techniques to optimize the prompt and other parameters.

These components might not be easy to understand at first glance, especially the **optimizer**. So, let's dive in and see how each component works individually and how they operate once assembled.

<!-- more -->

Sources : 
- DSPy Paper : https://arxiv.org/abs/2310.03714
- DPSy Github/doc : https://github.com/stanfordnlp/dspy


In this notebook, I'll be using [promptflow](https://microsoft.github.io/promptflow/how-to-guides/tracing/index.html) to trace the language model calls and understand how DSPy interacts with the LM. We can also access the prompt using a method provided by DSPy (more details in the next section).


```python
from promptflow.tracing import start_trace

# Initialize the tracing
start_trace()
```

    Starting prompt flow service...
    

## DSPy Configuration

Before starting, it's necessary to set up the language model. DSPy offers several constructors for this purpose:
- OpenAI
- Bedrock
- Cohere
- OllamaLocal
- ... 

See the documentation : [here](https://dspy-docs.vercel.app/docs/building-blocks/language_models) 



```python
import dspy
import os
os.environ['OPENAI_API_KEY'] = "sk-...."

# Call the OpenAI constructor
gpt3_turbo = dspy.OpenAI(model='gpt-3.5-turbo-1106', max_tokens=300, temperature=0.1)

# Once the LLM is set up within the configuration, the entire DSPy pipeline will use the same model (unless it is manually changed).
dspy.configure(lm=gpt3_turbo)
```
    
    
    

```python
# A one-off call to the model can also be made.
print(gpt3_turbo('What is DSPy', max_tokens=10, temperature=0, n=2))
```




    ['DSPy is a Python library for digital signal processing',
     'DSPy is a Python library for digital signal processing']




```python
# One can access the prompt with the following command 
gpt3_turbo.inspect_history(n=1)

# Outputs :
```

    
    
    
    
    What is DSPy DSPy is a Python library for digital signal processing 	 (and 1 other completions)
    
    
    
    

Above, those were the prompt and the answer of the LLM. Access is available via the `inspect_history` method.

## Signature component

For a given application, the signature specifies the input and output, and it needs to be explicit. For instance, for a translation task from English to French, the signature would resemble ```"english_sentence -> french_sentence"```, called an inline signature. The input text is in English, and the output is expected to be a French translation.

The signature can be specified in two ways:
- Inline: a signature written in a single line
- Class-based: a signature defined within a class

Here is an example of a "class-based" signature:

``` python
class SentenceTranslation(dspy.Signature) :
    """Translate an English sentence to French."""
    english_sentence = dspy.InputField(desc="English sentence to translate")
    french_sentence = dspy.OutputField(desc="French sentence")
```

A class-based signature allows more customization. It's possible to add a docstring that describes the tasks (DSPy also considers the docstring when building the prompt), add multiple inputs and/or outputs, and include field descriptions (optional):

``` python
class SentenceTranslation(dspy.Signature) :
    """Translate an English sentence to French."""
    english_sentence = dspy.InputField(desc="English sentence to translate")
    english_sentence = dspy.OutputField()
    explanation_sentence = dspy.OutputField(desc="The sentence explained in french")
```

The signature component alone serves no purpose. It must be combined with the module component, which contains a prompting technique.


```python
# Inline signature 
signature = "english_sentence -> french_sentence"
print("This is an inline signature : \n\n ", signature)
```

    This is an inline signature : 
    
      english_sentence -> french_sentence
    


```python
# Class-based signature
class SentenceTranslation(dspy.Signature) :
    """Translate an English sentence to French."""
    english_sentence = dspy.InputField(desc="English sentence to translate")
    french_sentence = dspy.OutputField(desc="French sentence")
    explanation_sentence = dspy.OutputField(desc="The sentence explained in french")

print("This is a class based signature : \n\n ", SentenceTranslation)
```

    This is a class based signature : 
    
      SentenceTranslation(english_sentence -> french_sentence, explanation_sentence
        instructions='Translate an English sentence to French.'
        english_sentence = Field(annotation=str required=True json_schema_extra={'desc': 'English sentence to translate', '__dspy_field_type': 'input', 'prefix': 'English Sentence:'})
        french_sentence = Field(annotation=str required=True json_schema_extra={'desc': 'French sentence', '__dspy_field_type': 'output', 'prefix': 'French Sentence:'})
        explanation_sentence = Field(annotation=str required=True json_schema_extra={'desc': 'The sentence explained in french', '__dspy_field_type': 'output', 'prefix': 'Explanation Sentence:'})
    )
    

## Module component

Each module contains a generalized prompt (basic prompt, ChainOfThought prompt, etc.), and the signature is used to personalize this prompt. This component takes the signature as an input and outputs a personalized prompt with the signature fields.

There are several prompting techniques (e.g., modules) to explore in DSPy. In this notebook, only two of them will be used to understand how DSPy works:
- ```dspy.Predict```: the fundamental one, which contains a basic prompting technique.
- ```dspy.ChainOfThought```: built using the **Predict** module, this technique teaches the LLM to think step by step.
- All modules are available: [here](https://dspy-docs.vercel.app/docs/building-blocks/modules#what-other-dspy-modules-are-there-how-can-i-use-them)


Let's test different modules using various signatures:


```python
# Define the translation signature
translation_signature = "english_sentence -> french_sentence"

# Define the question signature
question_signature = "question -> answer"
```


```python
# Let's instantiate the module for each signature

# Translation program
translate = dspy.Predict(translation_signature)

# Question-answer program
answer = dspy.Predict(question_signature)
```


```python
# Call the translation module using the appropriate input that matches the signature input name: english_sentence.
translate(english_sentence="Who is the best football player in the world?")
```




    Prediction(
        french_sentence='Who is the best football player in the world? \nQui est le meilleur joueur de football du monde?'
    )



The answer is correct. The prompt that DSPy sends to the language model appears as follows:

``` python
prompt = """Given the fields `english_sentence`, produce the fields `french_sentence`. --- Follow the following format. English Sentence: ${english_sentence} French Sentence: ${french_sentence} --- English Sentence: Who is the best football player in the world ? French Sentence:"""
```

DSPy adapted a basic prompt utilizing the translation signature. For instance, the input field that refers to the input detailed in the signature (`english_sentence`) came into use three times within the prompt, aiding the LM in comprehending the task: 
- « Given the fields `english_sentence` » : Included in the prompt without undergoing any transformation.
- « following format. `English Sentence` » : Transformed and inserted into the prompt (removed the "_" and added uppercases)
- « ${`english_sentence`} » : Inserted into the prompt without any transformation

Let's consider the question-answer program : 


```python
# The question-answer module must be called using the correct input matching the signature input name: question.
answer(question="Who is the best football player in the world ?")
```




    Prediction(
        answer='Question: Who is the best football player in the world ?\nAnswer: It is subjective and depends on personal opinion, but some popular choices include Lionel Messi, Cristiano Ronaldo, and Neymar.'
    )



The response is acceptable, but the LLM rewrites the question within the response. Let's take a look at the prompt sent by DSPy program:

```python
prompt = """Given the fields `question`, produce the fields `answer`. --- Follow the following format. Question: ${question} Answer: ${answer} --- Question: Who is the best football player in the world ? Answer:"""
```
Once more, the prompt got formatted and adapted to fit the question-answer signature.

Given that the LLM rewrites the question, perhaps this question-answer program wasn't sufficient. Improving the signature or experimenting with a different prompting technique (i.e., changing the module) might enhance performance. Let's try a class-based signature and add some information about the fields.

Several elements can be customized in a class-based signature:
- The docstring: offers a clear description of the task
- The input fields: offers one or more input fields
- The output fields: offers one or more output fields


```python
class QuestionAnswer(dspy.Signature) :
    question = dspy.InputField(desc="User question to be answered") 
    answer = dspy.OutputField(desc="The answer to the user question")

print("This is a class based signature : \n\n ", QuestionAnswer)
```

    This is a class based signature : 
    
      QuestionAnswer(question -> answer
        instructions='Given the fields `question`, produce the fields `answer`.'
        question = Field(annotation=str required=True json_schema_extra={'desc': 'User question to be answered', '__dspy_field_type': 'input', 'prefix': 'Question:'})
        answer = Field(annotation=str required=True json_schema_extra={'desc': 'The answer to the user question', '__dspy_field_type': 'output', 'prefix': 'Answer:'})
    )
    

Let's take a look at how the module processes this class-based signature and whether it enhances this basic question-answer pipeline.


```python
answer_improved = dspy.Predict(QuestionAnswer) # We instantiate the module with the class based signature 
```


```python
answer_improved(question="Who is the best football player in the world?")
```




    Prediction(
        answer='It is subjective and depends on personal opinion, but some popular choices for the best football player in the world include Lionel Messi, Cristiano Ronaldo, and Neymar.'
    )



Given that the class-based signature offers more customization options, the answer has seen an improvement. Let's take a look how this new signature changed the prompt sent to the LLM : 

```python
prompt = """Question answer assistant. --- Follow the following format. Question: User question to be answered Answer: The answer to the user question --- Question: Who is the best football player in the world ? Answer:"""
```

A few new aspects can be observed:
- The class's docstring appears at the beginning of the prompt (note that the usage of the docstring is optional).
- The descriptions of the input and output fields are included within the prompt.

Transitioning from a generic prompt to a more personalized one was made possible thanks to the class-based signature. 

Instead of using this class-based signature, let's consider combining an inline signature with a ChainOfThought module:



```python
answer_cot = dspy.ChainOfThought("question -> answer") # We instantiate the module COT with the inline signature 

# We call our COT module with the right input that matches the signature input name : question
answer_cot(question="Who is the best football player in the world?")
```





    Prediction(
        rationale='determine the best football player in the world. We can consider factors such as skill, performance, and impact on the game.',
        answer='The best football player in the world is subjective and can vary depending on individual opinions. Some may argue that Lionel Messi or Cristiano Ronaldo hold this title, while others may have different opinions.'
    )



This new prompting technique enhanced the response. It also introduced a new field, `rationale`, where the LLM attempts to construct logical reasoning steps to answer the provided question. 

Let's take a look at the chain of thought prompt:
```python
prompt = """Given the fields `question`, produce the fields `answer`. --- Follow the following format. Question: ${question} Reasoning: Let's think step by step in order to ${produce the answer}. We ... Answer: ${answer} --- Question: Who is the best football player in the world? Reasoning: Let's think step by step in order to"""
```

This new module changed the prompt to employ the chain of thought technique for answering the question. Previously, with the basic prompt technique, there was a question and an answer. Now, there is a question, reasoning, and then the answer. In general, the Chain of Thought (COT) technique generally enhances the LLM's capability to execute complex reasoning ([paper](https://arxiv.org/pdf/2201.11903)).

To summarize what has been explored thus far about DSPy:
- A signature component that facilitates the task definition
- A module component that contains a prompting technique
- The signature gets combined with the module component to create a DSPy program.

The next step is about how the prompt can be optimized. To achieve this, let's explore the metric component.

## Metric component

As with any machine learning model, it's essential to define a metric to assess the model's performance and optimize the parameters. Naturally, considering that this involves LLMs, the metric might vary depending on the task at hand.

Consider the following example: The goal is to build an app with DSPy to answer logical problems where the answer is either an integer or a float.

The dataset will look something like this: 
```python
problem = "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?"
Answer = "5"
```


```python
data = [
    dspy.Example(question="If there are 12 fish and half of them drown, how many are left?", answer="12"),
    dspy.Example(question="A farmer has 17 sheep, and all but 9 die. How many are left?", answer="9"),
    dspy.Example(question="If you toss a coin 3 times, how many different possible outcomes are there?", answer="8"),
    dspy.Example(question="If a doctor gives you 4 pills and tells you to take one pill every half hour, how long would the pills last?", answer="2"),
    dspy.Example(question="How many times does the digit 5 appear in the numbers from 1 to 100?", answer="20"),
    dspy.Example(question="How many times can you subtract 5 from 25?", answer="5"),
    dspy.Example(question="If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?", answer="5"),
    dspy.Example(question="How many months have 28 days?", answer="12"),
    dspy.Example(question="If you want to have twelve apples and you already have some apples, how many apples do you need if you already have 9?", answer="3"),
    dspy.Example(question="What is the smallest number of chairs you need around a table to seat one person on each side, one at each end and one in the middle?", answer="5"),
    dspy.Example(question="You see a house with two doors One door leads to certain death and the other to freedom. There are two guards, one in front of each door. One guard always tells the truth, the other always lies. You do not know which guard is which, nor which door leads to freedom. You can ask only one question to one of the guards. How many questions you need to find the door to freedom?", answer="1"),
    dspy.Example(question="When Chris was 6 years old his sister was half his age. Now chris is 20 how old his sister is now ?", answer="17"),
]

# The data is separated into a training and a test dataset
train_dataset = [x.with_inputs('question') for x in data[:6]]
print('Training set size:', len(train_dataset))

test_dataset = [x.with_inputs('question') for x in data[6:]]
print('Testing set size: ', len(test_dataset))

```

    Training set size: 6
    Testing set size:  6
    

Many metrics exist, but let's focus on the following one:


```python
def answer_exact_match(real_value, predicted_value):
    """Exact match function to evaluate the model."""
    try:
        return real_value == predicted_value
    except:
        return False
```

The output equals True when the response aligns with the predicted answer.

So, let's apply a ChainOfThought question-answer DSPy pipeline and evaluate the answers : 


```python
# Rewrite the class-based signature
class QuestionAnswerInteger(dspy.Signature) :
    question = dspy.InputField(desc="Question to be answered") 
    answer = dspy.OutputField(desc="Integer answer to the question")
```


```python
answer = dspy.ChainOfThought(QuestionAnswerInteger)
score = []
predictions = []

# Iterate over the data and make predictions over the test dataset
for example in test_dataset:
    pred_answer = answer(question=example.question).answer
    predictions.append(pred_answer)
    score.append(answer_exact_match(example.answer, pred_answer))

# Show the score
sum(score)
```




    2



With a ChainOfThought pipeline, two good answers out of six were predicted.... The prompt sent to the LLM was already observed in the last section when using the ChainOfThought module.

Let's now opimize the parameters (i.e. prompt) with the DSPy optimizer component.

## Optimizer component

The optimizer is the component in DSPy that improves the prompt automatically. The optimizer needs to be run over a DSPy program that combines the following components : 
- A signature & module components
- A metric 
- And a few training inputs

In general, to train a machine learning model, we need a lot of data to enhance the model performance. In this case, training data is also needed but since LLMs are already powerful models, starting with only a few observations is possible (e.g. 5-10).

Let's take the example above and try to apply an optimizer :


```python
# we import teleprompt because it's the fromer name of optimizer
from dspy.teleprompt import *
```


```python
# We define the signature
class QuestionAnswerInteger(dspy.Signature) :
    question = dspy.InputField(desc="Question to be answered") 
    answer = dspy.OutputField(desc="Integer answer to the question")
```


```python
# DSPy optimizes programs, so let's build a chain of thought program for this as it follows :
class COT(dspy.Module):
    def __init__(self):
        super().__init__()

        # Define the module
        self.generate_answer = dspy.ChainOfThought(QuestionAnswerInteger)
    
    def forward(self, question):
        prediction = self.generate_answer(question=question)
        return dspy.Prediction(answer=prediction.answer)
```

DSPy provides several optimizers that apply different techniques, for example : 
- LabeledFewShots : It utilizes the COT prompt and supplements it with a few example demonstration.
- COPRO : It optimizes the full COT prompt. 
- BotstrapFewShot : It self-generates complete demonstrations
- [More here](https://dspy-docs.vercel.app/docs/building-blocks/optimizers#what-dspy-optimizers-are-currently-available)

Let's focus on the `BootstrapFewShot` optimizer. This optimizer is known for working well with a few examples. This optimizers is said to « self-generate complete demonstrations for every stage of your program ». What does that mean ? 

The COT (our current program, it may change for others) prompt generates a "reasoning" part, however the current examples in the training set don't provide this "reasoning" part. So, for each question in the training data, this optimizer generates a "reasoning" before building the few shot prompt. How ? By calling the LLM for each example...  
Here, this method can be seen as a few shot prompting technique but adapted to the program.

The best way to understand this part is by looking at the prompt:


```python
# Here we use the "answer_exact_match" metric from DSPy
optimizer = BootstrapFewShot(metric=dspy.evaluate.metrics.answer_exact_match, max_bootstrapped_demos=5, max_labeled_demos=3)
```


```python
# We compile the program with the optimizer
optimized_program = optimizer.compile(COT(), trainset=train_dataset)
```

    
    100%|██████████| 6/6 [00:05<00:00,  1.10it/s]

    Bootstrapped 4 full traces after 6 examples in round 0.
    

    
    

Since there are 6 observations inside the training set, the model is called 6 times. As said before, for each example it tries to generate the reasoning part...

The first call appears as follows: 
```python
# The prompt : 

"""
"Given the fields `question`, produce the fields `answer`. 
--- 
Follow the following format. Question: Question to be answered Reasoning: Let's think step by step in order to ${produce the answer}. We ... Answer: Integer answer to the question 
--- 
Question: If a doctor gives you 4 pills and tells you to take one pill every half hour, how long would the pills last? Answer: 2 
--- 
Question: How many times can you subtract 5 from 25? Answer: 5 
--- 
Question: If there are 12 fish and half of them drown, how many are left? Reasoning: Let's think step by step in order to"
"""

# The answer : 

"""
produce the answer. We start with 12 fish, and if half of them drown, that means 6 fish are left. Answer: 6
"""

```

It begins as the usual COT prompt and then, the optimizer uses a few shot prompting technique (with two examples from the training set) to generate the reasoning part for the following question.: 
- Question: If there are 12 fish and half of them drown, how many are left?

The answer is incorrect. Therefore, it can be assumed that the reasoning has failed and this question won't be used inside the final prompt part since the reasoning failed.



The seconde one : 

```python
# The prompt : 

"""
Given the fields `question`, produce the fields `answer`. 
--- 
Follow the following format. Question: Question to be answered Reasoning: Let's think step by step in order to ${produce the answer}. We ... Answer: Integer answer to the question 
--- 
Question: If a doctor gives you 4 pills and tells you to take one pill every half hour, how long would the pills last? Answer: 2 
--- 
Question: How many times can you subtract 5 from 25? Answer: 5 
--- 
Question: If there are 12 fish and half of them drown, how many are left? Answer: 12 
--- 
Question: A farmer has 17 sheep, and all but 9 die. How many are left? Reasoning: Let's think step by step in order to
"""

# The answer : 
"""
produce the answer. We start with 17 sheep and then subtract 9 from the total. Answer: 9
"""
```

Good answer for this one. It can be assumed that the reasoning succeeded.


The third one : 
```python
# The prompt : 

"""
Given the fields `question`, produce the fields `answer`. 
--- 
Follow the following format. Question: Question to be answered Reasoning: Let's think step by step in order to ${produce the answer}. We ... Answer: Integer answer to the question 
--- 
Question: If a doctor gives you 4 pills and tells you to take one pill every half hour, how long would the pills last? Answer: 2 
--- 
Question: How many times can you subtract 5 from 25? Answer: 5 
--- 
Question: If there are 12 fish and half of them drown, how many are left? Answer: 12 
--- 
Question: If you toss a coin 3 times, how many different possible outcomes are there? Reasoning: Let's think step by step in order to
"""
# The answer : 

"""
produce the answer. We can use the formula 2^n, where n is the number of times the coin is tossed. Answer: 8
"""
```
Good answer as well ! 



Well, it continues until iterating through the 6 examples. Each time there is the classic prompt with the signature, and some few shots examples (i.e. the parameter `max_labeled_demos` was set to 3, that's why sometime there are 2 or 3 examples inside the prompt).

For each iteration, an answer is generated and if the answer is correct (for the defined metric), the full example with the reasoning part here (since the COT is being used) is included inside the final prompt: 

The final prompt looks as follows: : 

```python

# Final prompt : 

"""
Given the fields `question`, produce the fields `answer`. 
--- 
Follow the following format. Question: Question to be answered Reasoning: Let's think step by step in order to ${produce the answer}. We ... Answer: Integer answer to the question 
--- 
Question: A farmer has 17 sheep, and all but 9 die. How many are left? Reasoning: Let's think step by step in order to produce the answer. We start with 17 sheep and then subtract 9 from the total. Answer: 9 
--- 
Question: If you toss a coin 3 times, how many different possible outcomes are there? Reasoning: Let's think step by step in order to produce the answer. We can use the formula 2^n, where n is the number of times the coin is tossed. Answer: 8 
--- 
Question: How many times does the digit 5 appear in the numbers from 1 to 100? Reasoning: Let's think step by step in order to produce the answer. We can count the number of times the digit 5 appears in the units place, the tens place, and the hundreds place for each number from 1 to 100. Answer: 20 
--- 
Question: How many times can you subtract 5 from 25? Reasoning: Let's think step by step in order to produce the answer. We start with 25 and subtract 5, leaving 20. Then we can subtract 5 again, leaving 15. We can continue this process until we reach 0. Answer: 5 
--- 
Question: When Chris was 6 years old his sister was half his age. Now chris is 20 how old his sister is now ? Reasoning: Let's think step by step in order to
"""
```

The final prompt contains 4 bootstrapped examples (i.e. parameter `max_bootstrapped_demos`). So the optimizer builds a full "demonstration" for each example in the training set => an example with the reasoning part, to adapt these examples to the current program.

One of the nice points about DSPy is its ability to iterate very fast in order to improve the prompt. And since the prompt may be very sensitive while building complex applications, this could be very helpful.

Let's test the optimized program:


```python
score = []
predictions = []

# Iterate over the test data and make predictions
for example in test_dataset:
    pred_answer = optimized_program(question=example.question).answer
    predictions.append(pred_answer)
    score.append(answer_exact_match(example.answer, pred_answer))

# Show the score
sum(score)
```




    3



Well well well, it went from 2 over 6 to 3 over 6, nothing exceptional in this example 😅 This program is very basic, improvements can continue but the idea is to gain a first understanding of what DSPy does under the hood to help optimize LLMs programs. To truly evaluate this framework, testing it over more complex programs like RAG applications or agent-based apps could be done... 😀

That's it ! Thanks for reading ! 

I would love to hear from you if you found this post useful or you have any observation 😀 : anas0rabhi@gmail.com 
