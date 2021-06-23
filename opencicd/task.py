import asyncio
import pathlib
from typing import Dict


async def shell(task_: Dict[str, str], work_dir: pathlib.Path) -> None:
    cmd_ = f'cd {work_dir}'
    chdir_ = task_.get("args", {}).get("chdir", "")
    if chdir_:
        if not pathlib.Path(work_dir / chdir_).is_dir():
            raise RuntimeError(f"chdir is not exists: {chdir_}")
        cmd_ = f'{cmd_};cd {chdir_}'

    cmd_ = f'{cmd_};{task_["shell"]}'
    proc = await asyncio.create_subprocess_shell(cmd_,
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if stdout:
        print(stdout.decode("utf-8"))
    if stderr:
        print(stderr.decode("utf-8"))


async def git(task_: Dict[str, str], work_dir: pathlib.Path) -> None:
    pass
