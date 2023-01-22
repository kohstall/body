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
    Positive x is right, positive y is up.
    Your position limits are from -5 to 5.
    You velocity limits are 0 to 1.
    Stop on touch is 1 for True or 0 for False.
    You have a touch sensor that reports 1 if you are touching something and 0 if not.
    For any task, return an array of the form [[(x position, y position)], velocity, stop on touch]

    {examples}

    Current position:{current_position}
    Is touching object: {touch}
    Task: {task}
    Output:"""
    prompt = PromptTemplate(
        input_variables=["current_position", "examples", "task", "touch"],
        template=simple_prompt,
    )

    example_string = process_examples(examples)
    llm = OpenAI(temperature=0.9)
    chain = LLMChain(llm=llm, prompt=prompt)

    results = chain.run(
        current_position=str(current_position),
        examples=example_string,
        task=command,
        touch=str(is_touching),
    )

    coords, velocity, stop_on_touch = eval(results)
    if stop_on_touch == 1:
        stop_on_touch = "stop"
    else:
        stop_on_touch = "continue"

    action_example = """Current position:{current_position}
    Is touching object: {touch}
    Task: {task}
    Output: {output}""".format(
        current_position=str(current_position),
        touch=str(is_touching),
        task=command,
        output=results,
    )

    return coords, velocity, stop_on_touch, action_example


base_action_examples = [
    """Current position: (0, 0)
Is touching object: False
Task: Move to the right until you hit an object.
Output: [[(5, 0)], 0.5, 1]
""",
    """Current position:(0, 0)
Is touching object: False
Task: Trace out a small square quickly.
Output:[[(2, 0), (2, 2), (0, 2), (0, 0)], 1, 0]""",
    """Current position: (-5, 0)
Is touching object: True
Task: Move left slowly.
Output:[[(-5, 0)], 0.1, 0]""",
]


class Callback:
    def determine_actor(self):
        return True

    def list_steps(self):
        return True

    def list_speech(self):
        return True

    def generate_speech(self):
        return True

    def generate_action(self):
        return True

    def determine_state(self):
        return True

    def next_action(self):
        return True


class CallbackHandler:
    def __init__(self, cbs=None):
        self.cbs = cbs if cbs else []

    def determine_actor(self):
        res = True
        for cb in self.cbs:
            res = res and cb.determine_actor()
        return res
