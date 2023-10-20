import json
import csv
import openai

with open("apikey.txt", "r") as f:
    API_KEY = f.read()
openai.api_key = API_KEY

# SETTINGS INTENDED FOR USER TO CHANGE
GOAL = "CCSS.ELA-LITERACY.W.4.9"
SUBJECT = "Baseball"
STUDENT_GRADE = 4
# END OF SETTINGS INTENDED FOR USER TO CHANGE

# AI TWEAKING SETTINGS
model = "gpt-3.5-turbo"
temperature = 0.9
max_tokens = 2000
top_p = 1
frequency_penalty = 0.0
presence_penalty = 0.6
# END OF AI TWEAKING SETTINGS

# SETTINGS REGARDING EVALUATION AND HOW TO DEAL WITH EVALUATION RESULT
answer_methodologies = {
    "Over 9": "Use the feedback template.",
    "Between 6-9": "Ask a follow-up question that is more difficult, but still within the scope of the source material and the context.",
    "Over 5-6": "Point out what is correct in the students answer, but ask them for further justification, or a leading question that would lead them to the correct answer.",
    "Less than 5": "Avoid pointing to the student their mistake in a negative way, instead ask them a question that would lead them to the correct answer.",
}

clarity_methodologies = {
    "Over 8": "Mention that the answer was clear and well formulated.",
    "Between 5-8": "Mention that the answer could be formulated more clearly.",
    "Less than 5": "Ask the student for clarification and expain to them why their answer is not clear.",
}
# END OF SETTINGS REGARDING EVALUATION AND HOW TO DEAL WITH GRADE

def get_goal(goal):
    with open("ccss.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if goal == row[0]:
                return row[7]
    return None

ccss_goal = get_goal(GOAL)

opening_remarks = f"""
This is and AI powered educational tool.
It is designed to teach a student by asking them questions about a source text and giving them feedback on their answers.
The tool is intended to teach students on skills standardized in the Common Core State Standards Initiative.
The tool is designed for independent use by students, without the need for a teacher to be present.
You have set the tool to teach a student of grade {STUDENT_GRADE}
according to the following CCSS standard: {ccss_goal}
The source material is set to be about {SUBJECT}.

If this seems incorrect, see the documentation for how to change these settings.
*In this MVP version, the settings can be changed in the start of the educator.py file.*

"""

class Excercise:
    def __init__(self, excercise, command):
        self.excercise = excercise
        self.log = [excercise, command]
        self.rating = None
        self.student_progress = []

log_of_excercises = []
tokens_used = 0

def stringify_dict(methodologies):
    return "\n".join([f"{score}: {methodology}" for score, methodology in methodologies.items()])

with open("templates/follow_up.md", "r") as f:
    follow_up_template = f.read()

with open("templates/assignment.md", "r") as f:
    assignment_template = f.read()

with open("templates/feedback.md", "r") as f:
    feedback_template = f.read()

with open("templates/finish.md", "r") as f:
    finish_template = f.read()

system_prompt_ver3 = f"""
You have three types of replies, do not deviate from them.
The replies should follow as closely as possible the renderings of the following markdown templates,
with parts in curly brackets replaced by appropriate content and no extra content in your message whatsoever outside
of what the template specifies.

assingment:
```markdown
{assignment_template}
```

follow up:
```markdown
{follow_up_template}
```

feedback:
```markdown
{feedback_template}
```

finish:
```finish
{finish_template}
```

You are a teacher AI, designed to teach a student from grade {STUDENT_GRADE} about {SUBJECT}.
You are specifically assigned to teach them the following: {ccss_goal}

If there are no messages in the chat history, start the conversation with an assignment using the template above.
Give the student context, a source text and a question.

If the last message is an answer from the student, 
reply using the follow up template above.
In the reply, at the provided spots for content and clarity, write down an evaluation of the students answer.
Taking into account the students grade being {STUDENT_GRADE}, give a score from 1 to 10, where 1 is completely wrong and 10 is completely correct.
Take into account the completeness of the students answer and relevance to the source material.
Then assess whether the answer is clear and well formulated and give it a score from 1 to 10
and write down your evaluation of the students answer at the provided spot.

Try to make the questions you ask the student as open-ended as possible, and avoid asking yes/no questions or questions that can be answered with a single word.

Then, depending on the score, reply with one of the following methodologies:

{stringify_dict(answer_methodologies)}

Also, depending on your assessment of the clarity of the answer:

{stringify_dict(clarity_methodologies)}

If the student appears to become frustrated or less and less focused in their answers,
use the finish template (ask them if they would like to finish the excercise)
If they answer positively, your next response should be the feedback template.

"""

system_prompt = system_prompt_ver3

pre_chat = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"Hello, I am a student of grade {STUDENT_GRADE}. I am here to learn about {SUBJECT}. Please start"},
]

def parse_grading(reply):
    content_grade = reply.split("\n")[2].split(":")[1].strip()
    clarity_grade = reply.split("\n")[3].split(":")[1].strip()
    verbal_feedback = reply.split("\n")[4].split(":")[1].strip()
    return [content_grade, clarity_grade, verbal_feedback]

def shorten_string(source: str):
    if len(source) > 100:
        return source[:100] + "..."
    else:
        return source

def print_session_info(excercises):
    print("############################  Session info:  ############################\n")
    for excercise in excercises:
        print(f"Excercise: {shorten_string(excercise.excercise)}\n")
        #print(f"Log:")
        #for entry in excercise.log:
        #    print(f"{shorten_string(entry)}")
        print(f"Rating: {excercise.rating}\n")
        print(f"Student progress: {excercise.student_progress}\n")
        print("\n\n")

def add_tokens(response):
    global tokens_used
    tokens_used += response["usage"]["total_tokens"]

def parse_response(response):
    return response["choices"][0]["message"]["content"]

def get_response(chat_history: list):
    res = openai.ChatCompletion.create(
        model = model,
        messages = chat_history,
        temperature = temperature,
        #max_tokens = max_tokens,
        top_p = top_p,
        frequency_penalty = frequency_penalty,
        presence_penalty = presence_penalty
    )
    add_tokens(res)
    return res

def start_excercise():
    parsed_response=parse_response(get_response(pre_chat))
    print(parsed_response + "\n\n")
    command = input("Input your message here: (quit to end program)\n")
    excercise = Excercise(parsed_response, command)
    return excercise

if __name__ == "__main__":
    if not get_goal(GOAL):
        print("Goal not found from a list of CCSS, goal should be in the format of a CCSS standard code goal such as: CCSS.ELA-LITERACY.W.4.9")
    print(opening_remarks)
    excercise = start_excercise()
    log_of_excercises.append(excercise)
    while excercise.log[-1].strip().lower() != "quit":
        parsed_response=parse_response(get_response(pre_chat + excercise.log))
        if "Feedback" in parsed_response.split("\n")[0]:
            rating = input("Gpt asked for rating:\n")
            excercise.rating = rating
            excercise = start_excercise()
        else:
            evaluation = parse_grading(parsed_response)
            excercise.student_progress.append(evaluation)
            print(parsed_response + "\n\n")
            command = input("\n\nInput your message here: (quit to end program)\n")
            excercise.log.append({"role": "assistant", "content": parsed_response})
            excercise.log.append({"role": "user", "content": command})
    print_session_info(log_of_excercises)
    print("Total tokens used: ", tokens_used)
