# Advent of Code 2022
This repo contains my answers to the [2022 Advent of Code Challenge](https://adventofcode.com/2022/). I got about a dozen problems in before Christmas, so I definitely didn't solve it in time, but I definitely had fun with the ones that I did solve and intend on solving more.

## Running
If you hop into your favorite venv, you can run `pip install -r requirements.txt` to install the requirements to run the solutions. Once that's done, add the source to your Python path and you can run the `aoc_2022` module to run answers. If you're cool enough to be using PyCharm and you have a venv set up, the example commands below should have the play symbol next to them and should be executable by simply clicking them.

### Running a Solution
`python -m aoc_2022 run --day 12 --part 2` 

This command would invoke the CLI runner within the `__main__.py` file and invoke the `run` command, which will search for the solution for Day 12, Part 2 and invoke it.

### Listing Solutions
`python -m aoc_2022 ls`

This will list all days, parts, and input files known.

## Code Structure
This project is broken up into 3 basic parts:

- Common/utility code
- Solutions
- Input data

### Common/Utility Code
This is the code contained in `base.py` and `util.py`. These files define base classes for solutions along with convenience methods for finding intput data within the project.

The base class for each solution has a common base class called `Solution` that leverages the template-method pattern to do it's work. In short, if the user defines which day and part that this solution belongs to, all they need to do is implement a `run()` method that will provide an answer. They are given convenience methods to locate the input. They may optionally override the input file name/method in order to pass in test data. Given more time, I probably could have implemented a base unit test to run through each of these solutions to ensure they match the example output described in each problem.

### Solutions
Each day has a different Python file. This is not strictly necessary; one could lump all solutions into whatever arbitrary divisions they choose. This just felt right to me at the time to keep a day's challenges in a single file since it keeps problems and their neighboring parts together. The system uses the values set in the object to determine which problem they're solving, not the file name. In addition to the two solution classes, I sometimes also included a third class to contain static methods for parts of the solution that were common. In some cases, I created enums or dataclasses within that solution's module. The goal was to keep everything needed for a single day's solution in the same place.

### Input Data
Input data can be found in the `resources` directory. The naming convention used was `day_{day}_{index}.txt` for problem input and `day_{day}_{index}_test.txt` for test input, where `day` is the two-digit day, and `index` is a one-based index in case there are multiple inputs. As of this writing, there's only ever one, so this doesn't actually get incremented in practice.

It should be worth noting that I do not claim copyright or ownership over this input data; this was copied straight from the Advent of Code website.

## Future Happenings
If I participate in next year's AoC, I might take some of this stuff and publish it as a Python package that includes the input data, some convenience functions or methods for accessing it, and an optional base class and runner for writing solutions, especially if AoC continues using the same problem format. It's not super practical, but I do like the idea of immortalizing AoC through code artifacts.
