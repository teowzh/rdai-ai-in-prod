FROM python:3.9

ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG HOME=/home/$USERNAME

# Create the user
RUN useradd -m -u $USER_UID $USERNAME
USER $USERNAME

ENV PATH="${PATH}:/home/user/.local/bin"
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -U pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY --chown=user . $HOME/app

WORKDIR $HOME/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]