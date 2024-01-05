# turing_machine

É um simulador da maquina de turing, configurado por um json. A máquina permite o uso de uma fita simples ou uma fita bidimensional.

## Como usar

Crie um ambiente virtual e baixe as dependencias:
```shell
python -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```
e depois use como quiser a CLI para executar seus programas usando a máquina de turing, os exemplos podem ajudar bastante no começo, por exemplo:
```shell
./.venv/bin/python ./cli.py ./examples/binary-addition.json 2 --delay .1
# ou
./.venv/bin/python ./cli.py ./examples/2d-ping-pong.json    1 --delay .1
```


