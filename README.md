# read_bot

Thiago's pdf readbot

## Requerido

### Anaconda

Para baixar o instalador do Anaconda

```bash
curl -O https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
```

Instalar Anaconda

```
bash Anaconda3-2022.10-Linux-x86_64.sh
```

Reinicie o bash

```
source .bashrc 
```

## Usage

Garanta que você está dentro do diretorio deste repositório e execute o seguinte comando para criar o ambiente virtual

```
conda env create -f read_bot.yml
```

Entre no ambiente virtual

```
conda activate read_bot
```

Utilizando o objeto

```python
python3 read_bot.py [-h] -f FILE
```

Argumentos requeridos

-f FILE, --file FILE -> The file to perform the conversion.

Argumentos opicionais

 -h, --help -> show this help message and exit

Exemplo

```
python3 read_bot.py -f apresentacao.pdf
```
