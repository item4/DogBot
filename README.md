DogBot
======
DogBot is multipurpose IRC bot

## Features
* Multi-server connection by each encoding(charset)
* Multi-threading command executing
* Useful/Editable builtin commands
* Command alias

## Need
* Python2.x (not support 3.x)
* websocket-client (for ?exa)
* sphinx (for ?flask, ?wand)

## Basic Usage
1. install Python2.x and download this source.

    ```
    $ cd DogBot
    $ git clone git@github.com:item4/DogBot.git .
    ```
2. It need to pip install. install requirements.

    ```
    $ pip install -r requirements.txt
    ```
3. It will make configure file automatically when first runtime. just execute once.

    ```
     $ python run.py
    ```
4.  modify config.json.

    ```
    $ vi config.json
    ```
5. Execute again and use it.

    ```
    $ python run.py
    ```

## Configuration
* nick : string. Bot's nickname. multi-byte supported.
* server : JS object contain server address : configure pair. The key is server address, and the value is JS object configure.
  * port : integer. Server port. Ordinary 6667.
  * encoding : string. Server encoding(charset). Ordinary latin-7(english only) or utf8(multi-byte support)
  * channels : array. List of channels about join automatically. **MUST** prefix **#**
  * kick : string. RAW string about how to manage when someone take possession of its nickname.
  * login : string RAW string about how to login NickServ.
* db : not used yet. It will be DSN of its DB.