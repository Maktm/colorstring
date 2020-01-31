```
            ██████╗ ██████╗ ██╗      ██████╗ ██████╗ ███████╗████████╗██████╗ ██╗███╗   ██╗ ██████╗ 
           ██╔════╝██╔═══██╗██║     ██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║████╗  ██║██╔════╝ 
           ██║     ██║   ██║██║     ██║   ██║██████╔╝███████╗   ██║   ██████╔╝██║██╔██╗ ██║██║  ███╗
           ██║     ██║   ██║██║     ██║   ██║██╔══██╗╚════██║   ██║   ██╔══██╗██║██║╚██╗██║██║   ██║
           ╚██████╗╚██████╔╝███████╗╚██████╔╝██║  ██║███████║   ██║   ██║  ██║██║██║ ╚████║╚██████╔╝
            ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝         
```

## Installing
With the project's current state, there is no need to set up the project using any special procedures,
using pip etc. Simply cloning the repository and including the `colorstring.py` module will get you started
with printing colored text.

### Prerequisites
* Python 3.6 or later
* Terminal with ANSI colors support

### Get the source
Clone the repository over HTTPS using the GitHub link:

```
git clone <repository-url>
```

**Note** that the project does not have any dependencies or submodules.

## Usage
To print colored text to a terminal, you can use the `cs` function.

```python
from colorstring import cs, UnsafeRepeaterException

try:
    print(cs('^1*3Hello ^5world'))
except UnsafeRepeaterException as error:
    pass  # Use error.count for debugging purposes
```

From the example above, note that it is possible for the `cs` function to throw an `UnsafeRepeaterException`
in the event that an out-of-bounds repeater was provided.

## TODO
* Add support for background colors
* Add support for non-color IDs (e.g. reset foreground with `^.`)
* Provide a way to dynamically change the id-to-color mapper that can throw exceptions
* Write a specification draft for a future syntax
* Provide more debug information when an `UnsafeRepeaterException` is thrown

## Author
* [GitHub](https://www.github.com/Maktm)
