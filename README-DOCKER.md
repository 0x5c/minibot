# Docker help for Minibot

You have multiple options to run an instance of Minibot using docker.

- [Docker help for Minibot](#docker-help-for-minibot)
  - [Using docker-compose and the prebuilt-image (recommended)](#using-docker-compose-and-the-prebuilt-image-recommended)
  - [Using docker-compose and building the image](#using-docker-compose-and-building-the-image)
  - [Using pure docker](#using-pure-docker)
    - [[Optional] Building the image](#optional-building-the-image)
    - [Creating the container](#creating-the-container)


## Using docker-compose and the prebuilt-image (recommended)

This is the easiest method for running the bot without any modifications.  
**Do not clone the repository when using this method!**

1. Create a new directory and `cd` into it.

2. Create the `docker-compose.yml` file:

    ```yaml
    version: '3'
    services:
      minibot:
        image: "0x5c/minibot:latest"
        restart: on-failure
        volumes:
          - "./data:/app/data:rw"
        environment:
          - PYTHONUNBUFFERED=1
    ```

3. Create a subdirectory named `data`.

4. Copy the templates for `options.py` and `keys.py` to `data/`, and edit them.

5. Run `docker-compose`:

    ```none
    $ docker-compose pull
    $ docker-compose up -d
    ```

    > Run without "-d" to test the bot. (run in foreground)


## Using docker-compose and building the image

This is the easiest method to run the bot with modifications.

1. `cd` into the repository.

2. Create the `docker-compose.yml` file:

    ```yaml
    version: '3'
    services:
      minibot:
        build: .
        image: "minibot:local-latest"
        restart: on-failure
        volumes:
          - "./data:/app/data:rw"
        environment:
          - PYTHONUNBUFFERED=1
    ```

3. Create a subdirectory named `data`.

4. Copy the templates for `options.py` and `keys.py` to `data/`, and edit them.

5. Run `docker-compose`:

    ```none
    $ docker-compose build --pull
    $ docker-compose -d
    ```

    > Run without "-d" to test the bot. (run in foreground)



## Using pure docker

This methods is not very nice to use.  
*I just wanna run the darn thing, not do gymnastics!*


### [Optional] Building the image

1. `cd` into the repository.

2. Run docker build:

    ```none
    $ docker build -t minibot:local-latest .
    ```


### Creating the container

1. Be in a directory with a `data/` subdirectory, which should contain valid `options.py` and `keys.py` files (copy and edit the templates).

2. Run the container:

    ```none
    $ docker run -d --rm --mount type=bind,src=$(pwd)/data,dst=/app/data --name minibot [image]
    ```

    Where `[image]` is either of:
    - `minibot:local-latest` if you are building your own.
    - `0x5c/minibot:latest` if you want to use the prebuilt image.
