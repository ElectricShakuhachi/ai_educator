# AI CCSS Standard Educational Tool

This is and AI powered educational tool.

*Note, at this stage, this is a simple MVP just to give a prototype idea - the code is most definitely not good or secure for production*

It is designed to teach a student by asking them questions about a source text and giving them feedback on their answers.
The tool is intended to teach students on skills standardized in the Common Core State Standards Initiative.
The tool is designed for independent use by students, without the need for a teacher to be present.

Currently this is just an MVP.
It is designed to be usable and deployable as such, but in order to deploy it for actual usage, a graphical interface would
be necessary - and preferably it could be deployed in the Web.

In it's current state, you can run it as follows:

- Clone the repository.

- Make sure you have python3 installed. (the tool has been tested with Python3.8.10)

- generate an openAI API key, and include it in the repository in a file "apikey.txt"

- Create a virtual environment with python using the commands and install the dependencies

```
pyhton3 -m venv venv
```

```
source venv/bin/activate
```

```
pip install -r requirements.txt
```

- run the tool with the command:

```
python3 educator.py
```

- edit the constants GOAL, BEGINNING_SUBJECT and STUDENT_GRADE at the start of the python file to choose the CCSS target goal,
subject matter and grade of the student.

There is a stump of a QA script included in quality.py.
This is intended to be used for testing and quality assurance. educator.py should be edited to provide an interface for the testing script,
so that it can talk to it. Then the testing script needs to be added the logic to respond to it as a student would, and then rate the replies and collect and process that data
to get test results. This would require me an hour or two more to complete - after which any automation tool such as Jenkins or Github workflows could be utilized to run this
arbitrarily many times to gather data - and to compare updates to the prompt system.

## Future development:

This can be made significantly better introducing a classification system, which first generates the assignment and follow up question templates
based on the chosen CCSS goal. The current templates do not serve every learning goal in CCSS equally. They were first devised with special regards to 
the this goal:

CCSS.ELA-LITERACY.W.4.9 - Draw evidence from literary or informational texts to support analysis, reflection, and research.

The idea of this framework is to suppress the way the AI responds so that it will reply with a clear template.
The reply can then be easily parsed to create evaluations and to help with following the students progress.

There could be either a few templates designed by human developers, to which AI is used to classify which one would best suit the learning purposes
of the excercise - or AI could be used to generate new templates.

Some excercise content - such as the initial excercise assignment. This pre-generation would allow them to go through an arbitrary amount of refining by
AI powered QA pipeline. Follow-up questions and student evaluations could be generated on the go.

It is obviously important to create a user interface and enhance the configurability of the system.
For now this is just a proof of concept, showing that these sorts of excercise could be used and this is a way to standardize the way the AI gives feedback on the student's responses, so that the student receives clear and unambiguous feedback, and data can be gathered from it.

The feedback system could be made into a separate configuration file, where a more rigorous and clear rubric would be set for the AI to follow.

--

Additional verification layer would be needed for this as well:
Checking whether user's input is copy pasted from the source material.
This could be done without another API call to an AI too, when it comes to literal copypasting.

There is also an obvious need to verify the user input to avoid injection.
At current stage user inputs are not put through any kind of verification, and are as such processed and entered into API calls.
This is obviously an unsecure practice and for any real application would be fixed.

In terms of quality of programming, this first MVP is just that - a MVP.
The code would be way better and cleaner in a later version.
It's not the best I can do in 4 hours, but its something of a beginning to show some ideas.
