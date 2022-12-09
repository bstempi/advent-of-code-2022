import importlib
import os
import pkgutil

import click

from aoc_2022 import util, base
from aoc_2022.base import Solution


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option('--day', type=int, help='Day number of the solution you wish to run')
@click.option('--part', type=int, help='Which part of the solution you want to run, usually 1 or 2')
def run(day: int, part: int) -> None:
    click.echo('Advent of Code 2022 runner')
    c_instance: Solution = None

    for c in get_solution_classess():
        inst = c()
        if day == inst.day and part == inst.part:
            c_instance = inst
            break

    if c_instance is None:
        click.echo('Solution not found')
        return

    result = c_instance.run()
    click.echo(f'Answer for day {c_instance.day} part {c_instance.part}: {result}')


@cli.command()
def ls() -> None:
    click.echo('Advent of Code 2022 solution listing')

    for c in get_solution_classess():
        c_instance = c()
        click.echo(f'Day {c_instance.day}, part {c_instance.part}, input: {c_instance.input_file_name}')


def get_solution_classess():
    pkg_dir = os.path.dirname(__file__)
    for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        importlib.import_module('.' + name, 'aoc_2022')

    return Solution.__subclasses__()


if __name__ == '__main__':
    cli()

