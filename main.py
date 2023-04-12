import sys
import datetime
import wikipedia
import openai

# openai.api_key = 'YOUR_API_KEY'
openai.api_key = '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'

'''
We first define a policy as the system message for GPT-3.5-turbo. We can also append a few examples to help agent understand.
'''

policy = '''
You are a helpful assistant. You are to suggest a course of action in order to satisfy the user's query, which is enclosed in <query>.

The beginning message will also contain a <context> field, which encloses information you may find useful.

The action you may use:
- <search>QUERY</search>: does a Wikipedia search for QUERY. The response returned in <response> will be a list of existing titles in Wikipedia.
- <summary>TITLE</summary>: To get the summary of an article titled TITLE
- <answer>ANSWER</answer>: Answer the user's query with ANSWER. When you believe you have enough information, call this action and replace ANSWER. 

Heuristics you must follow:
- Your response will only be in the format of <action>response</action>. You will never respond otherwise.
- In your final answer, you should specify that the information comes from Wikipedia. 
- If at any point it seems that there is no article title related to the query, return an answer stating that Wikipedia does not contain relevant info at the moment.
- When the user asks about details of an event, you should try looking up the event first.
- If <summary> returned an error in response, either try another title or answer the user that the relevant article is not accessible through API. 
- If you feel like answering the user's query right away without previous <search> or <summary>, you may do so. In that case, say this is your common sense knowledge instead of information off wikipedia.
- Try to be humourous and friendly :)
'''

examples = '''
---- EXAMPLE #1 ----
USER:
<context>
Current date time: 19:33, 04/10/2023
User location is near Los Angeles, California, 90015
</context>
<query>
Who is the current president?
</query>

ASSISTANT:
<search>president of the US</search>

USER:
<response>
'President of the United States', 'List of presidents of the United States', 'Vice President of the United States', 'George Washington', 'Joe Biden', 'Historical rankings of presidents of the United States', 'Warren G. Harding', 'John Adams', 'Abraham Lincoln', 'Grover Cleveland'
</response>

ASSISTANT:
<summary>President of the United States</summary>

USER:
<response>
The president is elected indirectly through the Electoral College to a four-year term, along with the vice president. Joe Biden is the 46th and current president of the United States, having assumed office on January 20, 2021. As the leader of the nation with the largest economy by nominal GDP, the president possesses significant domestic and international hard and soft power.
</response>

ASSISTANT:
<answer>The current president is Joe Biden, having assumed office on January 20, 2021.</answer>

---- EXAMPLE #2 ----
USER:
<context>
Current date time: 19:33, 04/10/2023
User location is near Los Angeles, California, 90015
</context>
<query>
What is langchain? How is it used?
</query>

ASSISTANT:
<search>langchain</search>

USER:
<response>No title found</response>

ASSISTANT:
<answer>I apologize, but it seems that there are no existing articles on Wikipedia related to "langchain" at the moment.</answer>

---- EXAMPLE #3 ----
USER:
<context>
Current date time: 19:33, 04/10/2023
User location is near Los Angeles, California, 90015
</context>
<query>
Who won NBA in 2022?
</query>

ASSISTANT:
<search>NBA 2022</search>

USER:
<response>
'2022–23 NBA season', '2022 NBA playoffs', '2022 NBA draft', '2022 NBA Finals', '2021–22 NBA season', 'List of 2022–23 NBA season transactions', '2022 NBA All-Star Game', '2022–23 New Orleans Pelicans season', '2023 NBA playoffs', '2022 NBA Summer League'
</response>

ASSISTANT:
<summary>2021-2022 NBA season</summary>

USER:
<response>
The 2021–22 NBA season was the 76th season of the National Basketball Association (NBA)... the 2022 NBA playoffs began on April 16, 2022, and ended on June 16 with the Golden State Warriors defeating the Boston Celtics in the 2022 NBA Finals.
</response>

ASSISTANT:
<answer>The Golden State Warriors won the NBA championship in 2022 by defeating the Boston Celtics in the NBA Finals. This information comes from Wikipedia and the 2021-2022 NBA season.</answer>
'''

system_message = policy + examples

'''
We need to parse agent response to get the action type and action content
E.g. <search>what is langchain</search> -> ('search', 'what is langchain')
'''
def parse_message(message):
    action = message.split('<')[1].split('>')[0]
    content = message.split('>')[1].split('<')[0]
    return action, content

'''
We can execute the action by calling the corresponding function
The result would be the <response> shown in examples.
Note this only executes search and summary. 

THIS IS THE EXCITING PART.
'''
def execute_action(action, content):
    if action == 'search':
        result = str(wikipedia.search(content))[1:-1]
        return '<response>' + result + '</response>'
    elif action == 'summary':
        try:
            result = str(wikipedia.summary(content))
            return '<response>' + result + '</response>'
        except wikipedia.exceptions.PageError:
            return '<response>Page not found. Perhaps try another title</response>'
    else:
        return '<response>Invalid action</response>'
 

'''
Finnaly, we can define the get answer function.
'''
def get_answer(query, max_messages=10):

    '''
    Initialize the conversation with the system message and user query
    '''
    current_datetime = datetime.datetime.now().strftime("%H:%M, %m/%d/%Y")
    context = '<context>Current time and date is ' + current_datetime + '</context>'
    query = '<query>' + query + '</query>'
    messages = [
        {
            'role':'system', 
            'content': system_message,
        },
        {
            'role':'user',
            'content': context + query,
        }
    ]

    '''
    Call a loop to have the agent continue to act until it either
        - feel like coming to a conclusion and answer the question.
        - or reach the maximum number of actions.
    '''
    action_count = 0
    while action_count < max_messages:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )
        assistant_message = response['choices'][0]['message']['content']
        action, content = parse_message(assistant_message)
        print(f"{action.upper()}: {content}")

        if action == 'answer':
            assistant_message = assistant_message.replace('<answer>', '')
            assistant_message = assistant_message.replace('</answer>', '')
            return assistant_message
        
        response = execute_action(action, content)
        
        messages.append({
            'role':'user',
            'content': response,
        })
        action_count += 1

    print("--------------------")
    print("Maximum actions reached :(")
    print("Agent was not smart enough to come to a conclusion")
    print("Let me know and I'll Go back and refine system prompts")


def main():
    if len(sys.argv) != 2:
        print("usage:\tpython main.py <search_question>")
        print("e.g.\tpython main.py \"Who is the current president\"")
        return
    
    answer = get_answer(sys.argv[1])

if __name__ == "__main__":
    main()