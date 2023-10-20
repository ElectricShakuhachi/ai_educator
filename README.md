# AI CCSS Standard Educational Tool

This is and AI powered educational tool.

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

```pyhton3 -m venv venv
```

```source venv/bin/activate
```

```pip install -r requirements.txt
```