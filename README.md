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