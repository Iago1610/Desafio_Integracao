import os
import logging
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# Configuração de Logs para monitoramento do fluxo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def carregar_configuracoes():
    """Carrega as variáveis de ambiente do arquivo .env"""
    load_dotenv()
    config = {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
        "ZAPI_INSTANCE": os.getenv("ZAPI_INSTANCE_ID"),
        "ZAPI_TOKEN": os.getenv("ZAPI_TOKEN")
    }

    # Valida se todas as variáveis essenciais estão presentes
    if not all(config.values()):
        logging.error("Variáveis de ambiente ausentes. Verifique o arquivo .env.")
        exit(1)

    return config


def buscar_contatos(supabase: Client, limite: int = 10):
    """Busca até 'limite' contatos cadastrados no banco Supabase"""
    try:
        logging.info("Conectando ao Supabase para buscar contatos...")
        resposta = supabase.table('pessoas').select('*').limit(limite).execute()
        contatos = resposta.data
        logging.info(f"{len(contatos)} contato(s) encontrado(s).")
        return contatos
    except Exception as e:
        logging.error(f"Erro ao buscar dados no Supabase: {e}")
        return []


def enviar_mensagem_zapi(config, telefone, nome):
    #Envia a mensagem pelo Z-API para o número correspondente
    url = f"https://api.z-api.io/instances/{config['ZAPI_INSTANCE']}/token/{config['ZAPI_TOKEN']}/send-text"

    mensagem = f"Olá, {nome} tudo bem com você?"

    payload = {
        "phone": telefone,
        "message": mensagem
    }

    try:
        logging.info(f"Tentando enviar mensagem para {nome} ({telefone})...")
        response = requests.post(url, json=payload, timeout=3)

        # Levanta exceção se o status HTTP indicar erro (ex: 400, 401, 500)
        response.raise_for_status()

        logging.info(f"Mensagem enviada com sucesso para {nome}!")
    except requests.exceptions.RequestException as e:
        logging.error(f"Falha ao enviar mensagem para {nome} ({telefone}). Erro da API: {e}")


def main():

    logging.info("--- Iniciando Job de Envio de Mensagens ---")

    # 1 Carrega configurações
    config = carregar_configuracoes()

    # 2 Inicializa cliente Supabase
    supabase: Client = create_client(config["SUPABASE_URL"], config["SUPABASE_KEY"])

    # 3 Busca os contatos (limitado a 3 pela regra de negócio, mesmo tendo mais de 3 contatos cadastrados)
    contatos = buscar_contatos(supabase, limite=3)

    if not contatos:
        logging.warning("Encerrando execução: Nenhum contato para processar.")
        return

    # 4. Itera sobre os contatos e dispara os envios
    for contato in contatos:
        nome = contato.get('nome')
        telefone = contato.get('telefone')

        if nome and telefone:
            enviar_mensagem_zapi(config, telefone, nome)
        else:
            logging.warning(f"Contato ignorado devido a dados incompletos: {contato}")

    logging.info("--- Job Finalizado ---")


if __name__ == "__main__":
    main()