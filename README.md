# cyber_attacks_PORT
Este repositório contém um script Python que realiza a varredura de portas em um alvo usando o Nmap e realiza ataques de força bruta em serviços SSH e MySQL com um arquivo de senhas. O script também registra os resultados no arquivo successfull.txt com os logins bem-sucedidos.

# Requisitos
Antes de rodar o script, certifique-se de ter o Python e as dependências necessárias instaladas.

# Dependências
* Python 3.x
* python-nmap: Para escanear portas com o Nmap
* paramiko: Para ataques de força bruta no SSH
* mysql-connector-python: Para ataques de força bruta no MySQL

# Instalando as Dependências
Clone este repositório ou baixe o script scanner.py.
Crie um ambiente virtual (opcional, mas recomendado):

#### python -m venv venv
#### source venv/bin/activate  # No Windows: venv\Scripts\activate

# Uso do Script
O script realiza o seguinte:

* Escaneia portas abertas em um alvo especificado.
* Realiza ataques de força bruta no serviço SSH e MySQL usando um arquivo de senhas.
* Salva as informações de logins bem-sucedidos no arquivo cleared.txt.

# Como Executar
Execute o script com os seguintes parâmetros:

#### python scanner.py --target <ENDERECO_IP> --ports <INTERVALO_DE_PORTAS> --passwords <CAMINHO_DO_ARQUIVO_DE_SENHAS>

--target ou -t: O IP ou domínio do alvo.
--ports ou -p: O intervalo de portas a ser escaneado (por exemplo, 1-10000).
--passwords: O arquivo de senhas para os ataques de força bruta


Use de forma conciente!
Acredite em seu potencial!

## By Nelson Carvalho(nordicmanx)
