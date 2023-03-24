# Uploader
Simple sender && receiver with nice interface

## Installation
```shell
# clone any method you want
pip install -r requirements.txt
 ```

## Usage
- Sender (your own machine):
  ```shell
  python3 sender.py server.ip file_or_folder
  ```
  Or you can use raw format
  ```shell
  # run this on server
  nc -l 777 > filename.ext
  ```
  ```shell
  # and this on your own machine
  python3 sender.py server.ip file -r
  ```
- Receiver (server):
  ```shell
  python3 receiver.py
  ```