import os
import socket
import struct
import time, math

from rich import print
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn


def exit_with_msg():
    print(f"[b]☠️[/]  [bright_red]Connection closed. Exiting...[/]")
    exit(1)


with Progress(
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        transient=True,
) as progress:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 777))
        s.listen()

        print()
        print("[dark_blue bold on bright_green]   Receiving started at :777   [/]")
        print()
        print("[b]ⓘ[/]  [bright_cyan]For uploading use [bold]sender.py[/][/]")
        print("[b]ⓘ[/]  [bright_cyan]You can upload files and folders![/]")
        print()

        connecting_task = progress.add_task("Waiting for connection", total=None)
        conn, addr = s.accept()
        progress.update(connecting_task, visible=False)

        with conn:
            print(f"[b]⎋[/]  [bright_green]Got connection from {addr[0]}:{addr[1]}[/]")

            data = conn.recv(4)
            if not data:
                exit_with_msg()

            count_of_files = struct.unpack(">I", data)[0]

            connecting_task = progress.add_task("Downloading files", total=count_of_files)
            for file in range(count_of_files):
                filename = ""
                filesize = ""

                while True:
                    data = conn.recv(1)
                    if not data:
                        exit_with_msg()

                    if data == b";":
                        break

                    filename += data.decode("utf-8")

                while True:
                    data = conn.recv(1)
                    if not data:
                        exit_with_msg()

                    if data == b";":
                        break

                    filesize += data.decode("utf-8")

                data_left = int(filesize)
                grab_bytes = max(filter(lambda x: int(filesize) % x == 0, list(range(1, 512 + 1))))

                if os.path.dirname(filename) != "":
                    os.makedirs(os.path.dirname(filename), exist_ok=True)

                with open(filename, "wb") as fp:
                    downloading_task = progress.add_task(f"Downloading \"{filename}\"", total=int(filesize))
                    while data_left > 0:
                        data = conn.recv(grab_bytes)
                        if not data:
                            exit_with_msg()

                        fp.write(data)
                        data_left -= grab_bytes

                        progress.update(downloading_task, advance=grab_bytes)

                progress.update(connecting_task, advance=1)

            print(f"[b]✔[/]  [bright_green]All files downloaded![/]")

