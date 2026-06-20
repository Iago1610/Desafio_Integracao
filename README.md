# Desafio: Integração Supabase + Z-API (WhatsApp)

Este projeto é uma solução em Python para ler contatos de um banco de dados no Supabase e enviar mensagens personalizadas via WhatsApp utilizando a Z-API. O código foi desenvolvido aplicando boas práticas, tratamento de exceções, geração de logs e proteção de credenciais.

## ⚙️ Tecnologias Utilizadas
* **Python 3**
* **Supabase** (Banco de Dados PostgreSQL)
* **Z-API** (Envio de WhatsApp via HTTP REST)
* **python-dotenv** (Gestão de variáveis de ambiente)

## 📌 Status da Integração e Execução
O fluxo do código foi implementado e testado com sucesso até a etapa de disparo. O script é capaz de:
1. Conectar de forma segura ao banco Supabase.
2. Extrair os contatos respeitando o limite de negócio (até 3 pessoas).
3. Montar o *payload* exato exigido pela documentação da Z-API.

**Nota sobre o teste de ponta a ponta:** Durante os testes finais, a plataforma da Z-API não disponibilizou um plano gratuito/trial ativo (a instância gerada ficou bloqueada aguardando pagamento de boleto, retornando erro `400 Bad Request` por "Instância Desconectada"). 

Como o desafio estipula o uso de planos gratuitos, o código foi mantido estruturalmente 100% pronto e correto. Para que o envio físico das mensagens ocorra, basta substituir as chaves no arquivo `.env` por uma instância da Z-API com status de pagamento/trial liberado.

## 🚀 Como executar este projeto localmente

1. Clone este repositório:
   ```bash
   git clone [https://github.com/iago1610/Desafio_Integracao.git](https://github.com/Desafio_Integracao/DesafioIntegracao.git)