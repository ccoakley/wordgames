#!/bin/bash

coverage run --source=. --omit="tests/*" -m unittest
coverage report -m
