# Safe Regex

A library to organise the unit tests for your regular expressions.

# Usage
Pip this library
``` sh
pip install safe-regex
```

Separate your regex from your main code into yaml files with positive and negative examples.  Give these files a `.re.yaml` extension

```yaml
---
pattern: "^[a-z]{3}$"
description: a three letter acronym
test_cases:
  - text: abc
    matches: [abc]
  - text: xyz
    matches: [xyz]
  # These examples do not match anything
  - text: 123
  - text: r2d2
  - text: abcd
```

The change your python code to load the regex from the yaml file.

```python
import safe_regex

my_re = safe_regex.RegularExpression.from_yaml('my_regex', folder="my_folder")

# then use as a normal re.Pattern object
re_match_object = my_re.match('cat')
```

## Unit testing
In your unit tests loop through your regular expression folder and validate everything.
```python
import os
from safe_regex import RegularExpression

# pytest 6.1 example
def test_regex():
    """ verify all regular expressions are valid """
    regex_directory = "my_folder"
    for filename in os.listdir(regex_directory):
        if filename.endswith(".re.yaml"):
            with open(os.path.join(regex_directory, filename)) as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
            sr = RegularExpression(**yaml_data)
            sr.test()
```

## Debugging

When a regular expression's test fails it helpfully prepares a link to regexr.com where you can inspect and debug the problem. For example:
https://regexr.com/?expression=%2F%5E%5Ba-z%5D%7B3%7D%2Fgms&text=These+should+all+match%0Aabc%0Axyz%0ANone+of+these+should+match%0A123%0Aabcd%0Ar2d2

# Configuration
rather than passing the folder specify `SAFE_REGEX_PATH` as an environment variable.

# Development

Development is being performed on OS X with [pyenv](https://github.com/pyenv/pyenv) (with its `.python_version` file) and [direnv](https://direnv.net/) (with its `.envrc` file).

In order to set up a development environment:
```sh
 brew install direnv pyenv
 echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
 exec "${SHELL}"
 pyenv install $(cat ./.python-version)
 # pyenv install takes a while
 direnv allow
 # direnv allow triggers the creation and activation of the virtual environment
 pip install -r requirements.txt
 pip install -r tests/requirements-testing.txt
 pip install --editable .

 # Then validate by running
 pytest
```