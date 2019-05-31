# colored-string
Provides outputting colored strings to the terminal with ease. `colored-string` provides an alternative to the usual
ANSI color codes that you can use to add colors to your output. So, rather than writing code like this:

```python
print('[\u001b[32m+\u001b[0m] Success message!')
```

you would use `colored-string` to write code like this:

```python
from coloredstring import cs
print(cs("[^1*1+] Success message!"))
```

## Installation
Clone the repository from GitHub using the following command:

```
git clone https://www.github.com/Maktm/colored-string.git
```

Then, simply import the `coloredstring.py` module inside of any modules that make use of colored strings.

## Usage
To get started with outputting colored text, simply import the `cs` function from the `coloredstring.py` module then
start using it with the `print` function for colored printing.

Example:

```python
from coloredstring import cs, UnsafeRepeaterException

try:
    print(cs('^1*3Hello ^3world'))
except UnsafeRepeaterException as error:
    print('Bad repeater count specified {}'.format(error.count))
```

Note that you do not have to use the try/except block unless you want to ensure that you do not have any malformed
uses of the `colored-string` specification (e.g. bad count value for a repeater that causes out-of-bounds).

## Specification
```TODO```

## TODO
* Tests
* Background colors
* TODOs in the code

## Author
Michael "Maktm" Awetahegn
