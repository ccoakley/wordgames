# wordgames
This repo is intended as a python skills refresher. This particular implementation is not recommended, as it has an exponential runtime. The exponential runtime comes from the use of `itertools.combinations`. Iterating over each key in the words graph and checking for containment would be linear in the size of the dictionary and faster for ridiculous use cases.

## Usage
To install the requirements, first create a virtual environment with [pipenv install](https://pipenv.pypa.io/en/latest/).

Then, to run the code, `python words.py decompose bookkeeper`

To run the tests, `./run_tests.sh`

