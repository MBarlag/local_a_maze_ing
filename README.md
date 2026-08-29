*This project has been created as part of the 42 curriculum by mabarlag, eepyemy*

Agreements:
Putting temporary comments between brackets [].


## Description

<br>

A-Maze-ing is a maze generator in Python that takes a configuration file, generates a maze, possibly perfect (with a single path between entrance and exit), and writes it to a
file using a hexadecimal wall representation. You will also provide a visual representation
of the maze and organize your code so that the generation logic can be reused later.

<br>

### __Overview__
__Code structure overview:__  
__The data structure overview:__  
__The structure and format of your config file__  
__The maze generation algorithm overview__  
__Why this algorithm__  
__Reusable code overview and examples__  

### __Team and project management__  
 
__Roles and responsibilities__  
[ put something here for codam, we have strategy already, not helpful (?) ]  
__Anticipated planning and how it evolved__  
Aiming for 2 to 2,5 weeks for the project.  
><br>
>	[Day 1]: Figured out the process of using git in team projects,  
>	agreed to use branches for each feature we are working on,  
>	pushing to main once the code is stable enough.  
>   <br>Practiced merge conflict resolution
>
><br>

<br>

><br>
>	[Day 2]: Tried out pair programming and choose it as  
>   development strategy. Also delved into installing a virtual environment.  
>   Chose to use Conda because it allows to select the version of Python.  
>   Managed to set up the environment using our Makefile.  
>   
><br>

<br> 

><br>
>	[Day 3]: Were stuck with troubleshooting conda for a while.
>   Ended up with a working solution, but too loaded with
>   implicit rules on how it is supposed to work, which
>   makes it hard to understand.   
>   
><br>

<br> 


__What worked well__  
__What could be improved__  
* Paying attention to our energy levels  
* Booking a silent room beforehand where we can work without distraction  
* Talked about using bigger fonts for ease of following during pair programming

__Tools used__  
Visual brainstorming -> [Excalidraw](excalidraw.com)  
Package manager -> uv open source package manager written in Rust,   
very fast and easy to use.   

<br>

## Instructions

Running project: 
```bash
 cd PROJECT_NAME
 make install
 make run
```
Using tester:
```bash
.tests/test.sh --? # single run script
.tests/t.py 100 10 # to run 10 times on randomly generated arrays of numbers with length of 100
```
^_^
## Resources


#### Links:  

Doc strings explanation: https://www.geeksforgeeks.org/python/python-docstrings/  

Doc string styles: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html  

Explanation on Pydantic: https://www.youtube.com/watch?v=XIdQ6gO3Anc  

Design patterns: https://refactoring.guru/design-patterns  

Pair programming: https://www.youtube.com/watch?v=E4cg5mmvpwo  

Merge conflict handling: https://www.geeksforgeeks.org/git/merge-conflicts-and-how-to-handle-them/  

Oh My Git Game: https://ohmygit.org  

UV Documentation: https://docs.astral.sh/uv/  