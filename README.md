# Eddy's Takehome

Hi folks. Hope this message finds you well :) Here is my response to the take home.

We will have our agent answer questions by accessing information through wikipedia API.

Specifically, we will use the `<search>` and `<summary>` endpoints given by wikipedia.

We'll have agent call `<search>` and `<summary>` on the wikipedia API, until it is confident with an answer.

## Setup

Start a new virtual environment and run

```
pip install -r requirements.txt
```

I used OpenAI's GPT-3.5-turbo, which requires an API key. You may put your key at the beginning of `main.py` where you'll find

```
openai.api_key = 'YOUR_API_KEY'
```

Don't worry, running a query cost very little. The entire develop + testing process costed less than 50 cents on my end.

## Query Answering

As per takehome requirement, you may run the CLi by

```
python main.py "<YOUR_QUERY>"
```

In addition to the queries provided, some of the ones I used are

```
python main.py "What is an apple?"
python main.py "Do you have the time? Also, what date is today?"
python main.py "When did russian invasion of ukraine began?"
python main.py "The school of athens, ohio"
python main.py "What is langchain and who invented it? For what purpose?"
python main.py "When did league of legends 2022 world final took place? Who won?"
python main.py "When did OpenAI released GPT-4?"
python main.py "What do you think the purpose of life is?"
```

## Limitations

The agent has only its common sense and API accessable wiki articles in its knowledge base. This means:

* Topics such as `langchain` that emerged post Sep. 2021 and has no wikipage is currently beyond agent's reach.
* Details such as highest scoring player in one event cannot be retrieved by summarizing high level abstractions.

Lastly, like all LLMs, the output can be unpredictable and parsing error may occasionally occur.

## Future & Personal Thoughts

I encourage you to read through my code to understand how much more this could be. For one thing, wiki's  `<search>` could be Starbucks' `<order>`, with `<response>` being order status, and `execute_action()` implemented differently.

Additionally, another cheaper & perhaps better solution is to use vector database, where we can simply get `<summary>` on each of the relevant wiki title, retrieve the closest chunks and use them as context. This would call to the idea of story as a backend, where all texts are stored in vector / chunk form locally, like a story book.

This story book could be the user's life story which agent can learn about preferences; it could be menu item description; any bits and pieces about any entity that the human language can describe. And just think what could be done when multi-modal becomes more matured.

However, not all memory can be interpreted by a story, such as each player name, number and score of one specific football game. As discussed with Nat in our meeting, at some point, hard computer code API need to exist. Perhaps the action definition could be some where in the story backend and be retrieved into context?

> Retrieval is probably going to be the most ubiquitous plugin, since it allows any organization to make their data searchable. -- Greg Brockman

## Conclusion

I had a lot of fun creating this project. While perhaps not too impressive, about 80% of these are not my original idea -- these are all pieced together here and there, through readings and events, with my thoughts mixed in between.

I guess ultimately I would love people to see the point that I'm making. I want us to realize this is more than just a chatbot. My gut feeling is that human intelligence vs AGI is going to end up like birds vs. planes: flying is exciting, but also not THAT exciting as we get use to it quickly. But at the very least, we can pierce through the mundane and focus on what matters more.
