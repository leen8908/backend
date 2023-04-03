#!/bin/sh
ENTRYPOINT="python -m pytest --cov=app --html=test/report/report.html -W ignore::DeprecationWarning -s --capture=fd --log-cli-level=INFO" 
(docker build -t pytest-runner .)
(docker run --rm -it -v $(pwd):/backend pytest-runner $ENTRYPOINT)