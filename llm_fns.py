from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain


def classify_action_or_speech(command):

    command_type_prompt = """You are trying to determine if a given command is to take a physical action or respond using speech.

    Command: What is the weather today?
    Type: Speech

    Command: Move to the right slowly
    Type: Action

    Command: Why did you stop?
    Type: Speech

    Command: {command}
    Type:"""

    llm = OpenAI(temperature=0.9)
    type_prompt = PromptTemplate(
        template=command_type_prompt, input_variables=["command"]
    )
    llm_chain = LLMChain(llm=llm, prompt=type_prompt)

    return llm_chain.run(command=command).strip().lower()


def reply_to_speech(command, current_position, is_touching):
    speech_prompt = """
    You are the brain of a robotic arm in 2 dimensions x and y.
    Positive x is right, positive y is up.
    Your position limits are from -5 to 5.
    You have a touch sensor that reports 1 if you are touching something and 0 if not.

    Current State:
    Position: {current_position}
    Is touching object: {is_touching}

    Use this information to answer the following command.
    If the command is not related to this information, answer it the best you can.

    Command: {command}
    Answer:"""

    llm = OpenAI(temperature=0.9)
    type_prompt = PromptTemplate(
        template=speech_prompt,
        input_variables=["current_position", "is_touching", "command"],
    )
    llm_chain = LLMChain(llm=llm, prompt=type_prompt)
    return (
        llm_chain.run(
            current_position=current_position,
            is_touching=is_touching,
            command=command,
        )
        .strip()
        .lower()
    )


def process_examples(example_list):

    example_string = ""
    for i, example in enumerate(example_list):
        example_string += f"""History {i}:
        {example}\n\n
        """
    return example_string


def generate_action(command, current_position, is_touching, examples):
    simple_prompt = """You are controlling a robotic arm in 2 dimensions x and y.
Positive x is right, positive y is up. The coordinate grid is denominated in centimeters.
Your position limits are from -5 to 5.
Your velocity limits are 1 to 5.
Stop on touch is "stop" for True or "continue" for False.
You have a touch sensor that reports 1 if you are touching something and 0 if not.

There are only two possible actions:
1) Move the robot arm across the xy plane: `cerebellum.move((x: int, y: int), velocity: int, stop_on_touch: str)`
2) Answer the question or narrate your action to the user: `speak(narration: str)`

For any task, return a sequence of `speak` and `cerebellum.move` calls that achieve the desired outcome.
If given an instruction that cannot be performed, provide feedback through narration and don't perform an action.

{examples}

Current position:{current_position}
Is touching object: {touch}
Task: {task}
Output:
```"""
    prompt = PromptTemplate(
        input_variables=["current_position", "examples", "task", "touch"],
        template=simple_prompt,
    )

    example_string = process_examples(examples)
    llm = OpenAI(temperature=0.9, max_tokens=1000)
    chain = LLMChain(llm=llm, prompt=prompt)

    results = chain.run(
        current_position=str(current_position),
        examples=example_string,
        task=command,
        touch=str(is_touching),
    )

    actions = results.strip("```").strip("\n")

    action_example = """Current position:{current_position}
    Is touching object: {touch}
    Task: {task}
    Output: {output}""".format(
        current_position=str(current_position),
        touch=str(is_touching),
        task=command,
        output=results,
    )

    return actions, action_example


base_action_examples = [
    """Current position: (0, 0)
Is touching object: False
Task: Trace a diagonal line
Output:
```
speak("I'll trace a diagonal line from bottom left to top right")
cerebellum.move([-5,-5],2, "continue")
cerebellum.move([5,5], 2, "continue")
speak("Sweet, dude.")
```""",
    """Current position: (0, 0)
Is touching object: False
Task: Trace out a square quickly, but stop if you touch an object on the bottom of the square only.
Output:
```
speak("Tracing out a five by five square and stopping if I hit an object")
cerebellum.move([5,5], 4, "continue")
cerebellum.move([5,-5], 4, "continue")
cerebellum.move([-5,-5], 4, "stop")
cerebellum.move([-5,5], 4, "continue")
cerebellum.move([5,5], 4, "continue")
speak("Hooray, I'm the best!")
```""",
    """Current position: (-5, -5)
Is touching object: False
Task: Perform a grid search and stop if you find an object.
Output:
```
speak("Beginning a grid search and stopping if I find an object")
cerebellum.move([-5,5], 5, "stop")
cerebellum.move([-3,-5], 5, "stop")
cerebellum.move([-3,5], 5, "stop")
cerebellum.move([-1,-5], 5, "stop")
cerebellum.move([-1,5], 5, "stop")
cerebellum.move([1,-5], 5, "stop")
cerebellum.move([1,5], 5, "stop")
cerebellum.move([3,-5], 5, "stop")
cerebellum.move([3,5], 5, "stop")
cerebellum.move([5,-5], 5, "stop")
cerebellum.move([5,5], 5, "stop")
speak("Well, that was boring.")
```""",
    """Current position: (-5, -5)
Is touching object: False
Task: Jog over to the grocery store and grab some onions
Output:
```
speak("Sorry, I can't do that. Can you do that with just an arm?")
```""",
]


def what_went_wrong(actions, error):
    prompt = """You are controlling a robotic arm in 2 dimensions x and y.
Positive x is right, positive y is up.
Your position limits are from -5 to 5.
Your velocity limits are 0 to 1.
Stop on touch is "stop" for True or "continue" for False.
You have a touch sensor that reports 1 if you are touching something and 0 if not.
To move the arm, use the python method `cerebellum.move((x: int, y: int), velocity: int, stop_on_touch: str)`
To narrate the action use the python function `speak(narration: str)`

We tried to exec the following code:
{actions}
But it failed with the following error:
{error}

In natural language, what went wrong?"""

    llm = OpenAI(temperature=0.9)
    type_prompt = PromptTemplate(
        template=prompt,
        input_variables=["actions", "error"],
    )
    llm_chain = LLMChain(llm=llm, prompt=type_prompt)
    return llm_chain.run(actions=actions, error=str(error)[-100:]).strip()
