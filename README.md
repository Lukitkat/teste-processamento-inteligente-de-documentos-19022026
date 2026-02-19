# Teste Técnico (Extração de informações em Faturas de Energia)

Para garantir o eficiente gerenciamento dos créditos de energia provenientes de usinas de energia renovável, é fundamental a extração precisa e automática de dados das notas fiscais de energia elétrica. Além disso, possuir conhecimento sobre faturas de energia elétrica é importante para o sucesso na gestão desses recursos.

Logo, é proposto dois testes como parte da avaliação dos conhecimentos técnicos e teóricos dos candidatos. Essa avaliação tem o objetivo de medir a compreensão do participante no contexto da extração de dados de notas fiscais e no entendimento básico de faturas de energia elétrica.

# Teste 1

Em busca pela eficiência na leitura de faturas, a equipe de desenvolvimento propõe a criação de uma rotina que, a partir de faturas de energia elétrica em formato de PDF, seja capaz de extrair importantes informações.

Nesta atividade, você deve editar o arquivo read.py e desenvolver uma rotina capaz de realizar a leitura da fatura fatura_cpfl.pdf em formato de PDF e retornar as seguintes informações:

- Titular da fatura (Nome e Documento)
- Endereço completo do titular da fatura
- Classificação da Instalação
- Número da instalação
- Valor a Pagar para a distribuidora
- Data de Vencimento
- Mês ao qual a fatura é referente
- Tarifa total com tributos
- Tarifa total Aneel
- Quantidade em kWh do Consumo da fatura
- Saldo em kWh acumulado na Instalação
- Somatório das quantidades das energias compensadas (injetadas)
- Somatório dos Valores Totais das Operações R$
- Contribuição de iluminação Pública
- Alíquotas do ICMS, PIS e COFINS em %
- Linha digitável para pagamento

Organize a saída e visualização das informações extraídas.

# Documentação do Teste 1

### Solução Desenvolvida (`read.py`)

O script `read.py` foi desenvolvido para extrair automaticamente os dados solicitados da fatura `fatura_cpfl.pdf`.

#### Dependências

O projeto utiliza a biblioteca `pdfplumber` para a leitura de arquivos PDF.
Para instalar as dependências, execute:

```bash
pip install pdfplumber
```

#### Como Executar

Certifique-se de que o arquivo `fatura_cpfl.pdf` esteja no mesmo diretório do script.
Para rodar a extração, execute o seguinte comando no terminal:

```bash
python read.py
```

#### Saída do Script

O script exibirá no console os dados extraídos formatados, incluindo:
- Dados do Titular (Nome, Documento)
- Endereço e Classificação da Instalação
- Valores Monetários (Total a Pagar, Tarifas consolidadas, Operações)
- Consumo e Energias Compensadas
- Dados Bancários (Linha Digitável)


# Teste 2

Contexto: Você recebeu a fatura "fatura_cemig.pdf" e deve desenvolver um script para extrair seus dados. Antes de iniciar a programação, é essencial compreender e interpretar as informações presentes nesta fatura.

Atividade: Analise a fatura e redija um documento respondendo os pontos abaixo. As respostas podem ser inseridas neste 'README'.

 - Identifique as principais diferenças entre a fatura "fatura_cemig.pdf" e uma fatura convencional de energia elétrica "fatura_cemig_convencional.pdf".
 - Descreva e explique os termos e valores apresentados na seção "Valores Faturados" da fatura "fatura_cemig.pdf".
 - Considerando que a instalação da "fatura_cemig.pdf" participa do Sistema de Compensação de Energia Elétrica, identifique e explique qual informação na seção "Informações Gerais" da fatura é considerada a mais importante.
 - Identifique o consumo da instalação referente ao mês de julho de 2023.

# Resposta para o Teste 2

1. Principais Diferenças

    A fatura fatura_cemig.pdf pertence a uma unidade consumidora que faz parte de um sistema de compensação de energia. Devido a isso, ela apresenta abatimentos por geração de energia, como o item "Energia compensada GD II". Por outro lado, a fatura fatura_cemig_convencional.pdf realiza a cobrança integral dos 374 kWh registrados através de um único item faturado de "Energia Elétrica".
    

    A modalidade de fornecimento e faturamento da fatura_cemig.pdf está classificada como sistema "Bifásico". Na fatura convencional, a subclassificação de fornecimento consta como "Monofásico".


    O valor cobrado na fatura com compensação totalizou R$ 76,66. A fatura convencional gerou um montante financeiro muito maior, com o valor a pagar de R$ 418,02.


    A fatura convencional traz o indicativo no cabeçalho de que se trata de uma "SEGUNDA VIA". O documento convencional também informa que foi uma nota "Emitida em Contingência".

2. Termos e Valores da Seção "Valores Faturados" (fatura_cemig.pdf)

    Energia Elétrica: Representa a cobrança de um montante de 50 kWh. O valor faturado referente a este bloco de energia foi de R$ 47,96.

    Energia SCEE s/ ICMS: Corresponde à energia proveniente da rede da distribuidora que foi consumida, totalizando 149 kWh. A cobrança financeira por este consumo foi de R$ 76,26.

    Energia compensada GD II: Refere-se à energia gerada pelo próprio sistema da residência (Geração Distribuída) que foi usada para abater o consumo de 149 kWh. Esse abatimento resultou em um desconto (crédito) na fatura de -R$ 67,24.

    Energia comp. adicional: Indica uma compensação secundária de energia no montante de 7 kWh. Essa quantia gerou um abatimento extra de -R$ 5,24.

    Bônus Itaipu art 21 Lei 10438: Trata-se de um crédito legal repassado ao consumidor, gerando um desconto de -R$ 9,79.

    Ass Combt Câncer (37)3512-1528: Refere-se a um serviço de terceiros ou doação voluntária cobrada na conta, no valor de R$ 10,00.

    Contrib Ilum Publica Municipal: É a taxa de Custeio do Serviço de Iluminação Pública (CIP/COSIP) cobrada pelo município, correspondendo a R$ 24,71.

    TOTAL: A soma de todas as tarifas, descontos e doações resultou no valor final de R$ 76,66.

3. A Informação Mais Importante sobre a Compensação

    Na seção "Informações Gerais", o dado mais relevante para o sistema de Geração Distribuída é o indicativo: "SALDO ATUAL DE GERAÇÃO: 234,63 kWh.".

    Explicação: Além da própria confirmação de que a "Unidade faz parte de sistema de compensação de energia", o saldo é a informação financeira mais importante. Ele indica que o sistema próprio produziu mais energia do que a casa consumiu no ciclo atual, e que existem 234,63 kWh de energia "sobrando" e estocados como crédito na concessionária. Esse montante fica disponível para ser utilizado em faturas futuras onde o consumo seja maior que a geração, ajudando a manter a conta de luz no valor mínimo.

4. Consumo Referente a Julho de 2023

    De acordo com o quadro de "Histórico de Consumo", o total registrado no mês de JUL/23 foi de 199 kWh. A tabela que detalha o tipo de medição também confirma que a leitura atual de energia resultou em um consumo de 199 kWh.

# Requisitos dos Desafios:

1. Utilize a linguagem Python para desenvolver a solução.
2. No mesmo README, inclua uma seção detalhada que explique claramente os passos necessários para executar o código. Certifique-se de que as instruções sejam precisas, organizadas e fáceis de entender, pois os avaliadores seguirão essa documentação.
3. Faça um fork do repositório, para iniciar o desenvolvimento.
4. A entrega deve ser realizada por meio de um pull request para o repositório original. Caso não consiga, os arquivos podem ser enviados para o email falecom@dg.energy, porém com penalidade de pontos.
5. Abra o pull request também faltando 5 minutos para o prazo final da entrega do teste. Se o pull request for realizado antes dos 5 minutos restantes haverá eliminação do candidato.
6. A entrega deve ser realizada até às 12:30h.
