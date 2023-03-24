import argparse
import struct

from rich import print
from rich.prompt import Prompt

from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn

import socket
import os
import glob

parser = argparse.ArgumentParser("sender.py")
parser.add_argument("address", help="Server address")
parser.add_argument("target", help="File or folder")
parser.add_argument("-r", "--raw", action="store_true", default=False)


def normal_mode(args):
    files = []
    if os.path.isdir(args.target):
        files = list(filter(
            lambda x: not os.path.isdir(x),
            glob.glob(
                f"{args.target}/**/*",
                recursive=True
            )
        ))
    else:
        files = [args.target]

    with Progress(
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            transient=True
    ) as progress:
        connecting_task = progress.add_task("Connecting to receiver...", total=None)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((args.address, 777))
            progress.update(connecting_task, visible=False)

            s.sendall(struct.pack(">I", len(files)))

            sending_file = progress.add_task("Sending files", total=len(files))

            for file in files:
                s.sendall(f"{file};{os.stat(file).st_size};".encode("utf-8"))

                with open(file, "rb") as fp:
                    content = "n"
                    while content != b'':
                        content = fp.read(1024)
                        s.sendall(content)
                progress.update(sending_file, advance=1)
            s.close()

        print("[bold bright_green]All files sent![/]")


def raw_mode(args):
    if os.path.isdir(args.target):
        print("[b]✖[/] [red]Only one file can be uploaded in raw format![/]")
        exit(1)

    with Progress(
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            transient=True
    ) as progress:
        connecting_task = progress.add_task("Connecting to receiver...", total=None)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((args.address, 777))
            progress.update(connecting_task, visible=False)

            sending_file = progress.add_task("Sending file", total=os.stat(args.target).st_size)
            with open(args.target, "rb") as fp:
                content = "n"

                while content != b'':
                    content = fp.read(1024)
                    s.sendall(content)

                progress.update(sending_file, advance=1024)
            s.close()

        print("[bold bright_green]File sent![/]")


if __name__ == '__main__':
    args = parser.parse_args()

    if args.raw:
        raw_mode(args)
    else:
        normal_mode(args)
