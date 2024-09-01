# FastAPI for AI

![image](https://github.com/user-attachments/assets/433d21ba-dbf1-47a3-bcd2-5f9428cb52b8)


## Basic Commands

- create a virtual environments

    ```bash
    python -m venv .venv
    ```

- activate the environment

    ```bash
    source .venv/bin/activate
    ```

    NOTE: to deactivate the environment simply type `deactivate` and press enter

- upgrade pip

    ```bash
    pip install --upgrade pip
    ```

- install requirements

    ```bash
    pip install -r requirements.txt
    ```

- To run app
    - To run in dev environment

        ```bash
        fastapi dev main.py
        ```

    - To run in prod or non-dev environment

        ```bash
        fastapi dev main.py
        ```
    NOTE: make sure you are in correct directory that contains main.py file
    