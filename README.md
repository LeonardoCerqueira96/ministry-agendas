### Desenvolvido por Leonardo Cesar Cerqueira
---

## Detalhes da solução
O extrator foi desenvolvido na linguagem Python v3.6.3, Sistema Operacional
Windows 10, utilizando O framework 'scrapy' como ferramenta principal, e as 
bibliotecas padrão 'datetime' e 'json'.

---

## Como executar
- Abra um terminal no diretório do projeto
- Execute o comando: $ scrapy crawl agendas
- A saída da aplicação será escrita no arquivo "agendas.json", no mesmo diretório
- ***Opção Extra***: Por padrão, o programa utiliza a data atual como limite de
extração. Esse comportamento pode ser modificado pelo parâmetro opcional "date_override".
Para usá-lo, na frente do comnando de execução inclua "-a date_override=<data>", onde data
é uma string no formato YYYY-MM-DD. 
    - Exemplo: $ scrapy crawl agendas -a date_override="2019-01-10"
