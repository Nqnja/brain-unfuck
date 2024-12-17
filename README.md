# Brain unfuck
*Brain unfuck is a project I worked on in my free time, I am aware that code might be messy in certain places.*

## What is brain unfuck
Brain unfuck is my attempt at making writing brainfuck apps slightly more manageable. 

I've tried this by implementing a simple compiler that literally just maps keywords to brainfuck instructions. The (default) instruction set that I have worked on thus far is a stack-based instruction set that can be used to create various simple programs. I have included one brain unfuck program so far in the `examples` folder in this repository. It is a program that is capable of adding two single-digit numbers and prints the result, prepending a '1' if necessary.

I am sure other people will be able to make much cooler stuff using this base, so I'm sharing it here on GitHub.

## How to use brain unfuck
Literally just create a text file ending in `.bu`, then run `py ./main.py <your_file_name>` and you should be good to go. Running just `py ./main.py` will help you setting up custom brain unfuck instruction mappings you made, you're free to deviate from my own instruction set.

In order to view and share your created brainfuck program, simply take a look at the `./output.bf` file that was created in this folder after you run `main.py`.

Yes, I currently depend on python, because I was mostly interested in creating the mappings between brain unfuck keywords and brainfuck instructions. I might sometime implement an actual compiler in a lower level language, but I think that's out of scope for now.

## How do the current instructions work
Below is a table of some available instructions:
|Instruction|Arguments|Description|
|-|-|-|
|ADD|2|Add 2 numbers|
|SUB|2|Subtract top-most number from the one below it on the stack|
|LT, LTE, GT, GTE, EQ|2|Test ordering between numbers|
|TODO|TODO|TODO|

Instructions are **NOT** case-sensitive! Also, it's a general rule of thumb that if you use an arithmetic or logical instruction that consumes 2 values from the stack, the value that was on the top of the stack will be placed on the right of the logical or arithmetic operator.

One special instruction pattern you will see in multiple places is loading a number. Due to the fact that I just map brain unfuck instructions to brainfuck instructions, loading a number onto the stack looks weird. For any number `x`, use `x RIGHT` in your code, it'll load the number onto the stack (also visible in the `examples` folder). Make sure to check the `examples` folder as the examples there will probably help you understand brain unfuck better.
