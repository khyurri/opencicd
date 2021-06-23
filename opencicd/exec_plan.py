# Execution plan
import asyncio
import pathlib
import yaml
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict

from yaml import SafeLoader

from opencicd import task


@dataclass
class Step:
    name: str
    tasks: List[Dict[str, Dict]]


ExecutionGraph = Dict[str, List[Step]]


def create_graph(spec: pathlib.Path) -> ExecutionGraph:
    with spec.open("r") as y_file:
        y_obj = yaml.load(y_file, Loader=SafeLoader)
        if not y_obj.get("version", False):
            raise RuntimeError("Unsupported spec-file version")
        exec_graph: Dict[str, List[Step]] = defaultdict(list)
        for step_name, step_args in y_obj["steps"].items():
            depends_on: str = step_args.get("depends_on", "main")
            step = Step(name=step_name,
                        tasks=step_args["tasks"])
            exec_graph[depends_on].append(step)
        return exec_graph


async def __execute_step(step_: Step, steps: List[Step], work_dir: pathlib.Path) -> None:
    for task_ in step_.tasks:
        if "shell" in task_:
            await task.shell(task_, work_dir)
    await __execute_steps(step_.name, steps, work_dir)


async def __execute_steps(step_: str, steps: List[Step], work_dir: pathlib.Path) -> None:
    coros = [__execute_step(step_, steps, work_dir) for step_ in steps[step_]]
    await asyncio.gather(*coros)


async def execute_plan(exec_graph: ExecutionGraph, work_dir: pathlib.Path) -> None:
    await __execute_steps("main", exec_graph, work_dir)


