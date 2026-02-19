import pdfplumber
import re
import json

def extract_cpfl_data(pdf_path):

    data = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        
    # --- Funções Auxiliares ---
    
    def to_float(val_str):
        """Converte uma string numérica para float."""
        if not val_str: return 0.0
        val_str = val_str.replace('.', '').replace(',', '.')
        # Tratar números negativos com sufixo '-' 
        if val_str.endswith('-'):
            return -float(val_str[:-1])
        return float(val_str)

    def extract_val(pattern, text, group=1):
        """Extrai um valor do texto usando expressão regular (regex)."""
        match = re.search(pattern, text, re.MULTILINE)
        return match.group(group).strip() if match else "N/A"

    # --- 1. Dados do Titular ---
    
    # Nome
    # A linha 3 contém o nome se "Nota Fiscal" estiver na linha 2
    lines = text.split('\n')
    try:
        nf_idx = -1
        for i, l in enumerate(lines):
            if "Nota Fiscal" in l:
                nf_idx = i
                break
        
        if nf_idx != -1 and nf_idx + 1 < len(lines):
            # A linha após "Nota Fiscal" tem o Nome + "Conta de Energia..."
            raw_name_line = lines[nf_idx + 1]
            name = raw_name_line.replace("Conta de Energia Elétrica", "").strip()
            data['Titular Nome'] = name
        else:
             data['Titular Nome'] = "Não encontrado"
    except:
        data['Titular Nome'] = "Erro na extração"

    # CPF
    data['Titular Documento'] = extract_val(r"CPF:\s*([\d\.-]+)", text)

    # --- 2. Endereço ---
    
    # Geralmente na linha abaixo do nome ou começa com "PCA", "RUA", "AV"
    addr_match = re.search(r"^(.*?)\s*CLASSIFICAÇÃO:", text, re.MULTILINE)
    if addr_match:
        addr1 = addr_match.group(1).strip()
    else:
        # Linha após a linha do nome, se regex falhar
        addr1 = lines[nf_idx + 2].split("Nº")[0].strip() if nf_idx != -1 else ""
    
    # Cidade/Estado/CEP
    city_match = re.search(r"\d{5}-\d{3}\s+.*?\s+[A-Z]{2}", text)
    addr2 = city_match.group(0) if city_match else ""
    data['Endereço Completo'] = f"{addr1} - {addr2}"

    # --- 3. Dados da Instalação ---
    
    # Classificação (inclui voltagem e fase)
    data['Classificação da Instalação'] = extract_val(r"CLASSIFICAÇÃO:\s*(.*)", text)

    inst_match = re.search(r"www\.cpfl\.com\.br\s+(\d+)", text)
    data['Número da Instalação'] = inst_match.group(1) if inst_match else extract_val(r"Conta Contrato N°\s*(\d+)", text)

    # --- 4. Valores Principais e Datas ---
    
    # Valor Total a Pagar
    data['Valor a Pagar'] = extract_val(r"Total a Pagar \(R\$\)[\s\S]*?(\d+,\d+)", text)

    # Data de Vencimento
    data['Data de Vencimento'] = extract_val(r"Data de Vencimento[\s\S]*?(\d{2}/\d{2}/\d{4})", text)

    # Mês de Referência
    data['Mês de Referência'] = extract_val(r"INSTALAÇÃO\s+(\w+/\d{4})", text)

    # --- 5. Tarifas ---
    
    # Somar todas as tarifas TUSD e TE em um único campo "Tarifa Total"
    
    # Extrair itens TUSD
    tusd_items = re.findall(r"(Energ.*?TUSD.*?)\s(\w{3}/\d{2})\s+[\d\.,]+\s+kWh\s+(\d+,\d+)", text)
    
    total_tariff_sum = 0.0
    
    for desc, month, rate in tusd_items:
        total_tariff_sum += to_float(rate)
        
    # Extrair itens TE
    te_items = re.findall(r"(Energ.*?TE.*?)\s(\w{3}/\d{2})\s+[\d\.,]+\s+kWh\s+(\d+,\d+)", text)
    
    for desc, month, rate in te_items:
        total_tariff_sum += to_float(rate)

    data['Tarifa Total'] = f"{total_tariff_sum:,.8f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    # Tarifas Aneel (Valores de referência)
    aneel_items = re.findall(r"Energia Ativa Fornecida - (TUSD|TE).*?([\d\.]+,\d+)\s+kWh\s+(\d+,\d+)", text)
    
    for type_label, cons, rate in aneel_items:
        data[f"Tarifa Aneel {type_label}"] = rate

    # --- 6. Consumo e Saldos ---

    # Consumo kWh
    cons_match = re.search(r"Energia Ativa Fornecida - TUSD.*?(\d+\.\d{3},\d{3})", text)
    data['Consumo kWh'] = cons_match.group(1) if cons_match else "N/A"

    # Saldo Acumulado
    data['Saldo Acumulado kWh'] = extract_val(r"Saldo em Energia da Instalação:.*?([\d\.,]+)", text)

    # Somatório Energias Compensadas (Injetadas)
    injected_items = re.findall(r"Energ.*?Inj.*?\s([\d\.]+,\d+)\s+kWh", text)
    total_inj = 0.0
    for item in injected_items:
        total_inj += to_float(item)
    data['Soma Energias Compensadas kWh'] = f"{total_inj:,.3f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    # --- 7. Valores Financeiros Detalhados ---

    # Somatório Valores Operações R$
    tc_val_match = re.search(r"Total Consolidado\s+([\d,]+)", text)
    data['Somatório Valores Operações R$'] = tc_val_match.group(1) if tc_val_match else "0,00"

    # Contribuição Iluminação Pública
    data['Contrib Ilum Pública'] = extract_val(r"Contrib\. Custeio IP-CIP Municipal.*?(\d+,\d+)", text)

    # --- 8. Tributos (Alíquotas) ---
    
    # ICMS, PIS, COFINS da linha "Total Consolidado"
    tc_match = re.search(r"Total Consolidado\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", text)
    
    if tc_match:
        data['Alíquotas'] = {
            "ICMS": tc_match.group(3), 
            "PIS": tc_match.group(5),    
            "COFINS": tc_match.group(6)  
        }
    else:
        data['Alíquotas'] = "Não encontrado"

    # --- 9. Dados Bancários ---
    
    # Linha Digitável (Código de Barras)
    barcode = extract_val(r"(\d{11,}\s\d{11,}\s\d{11,}\s\d{11,})", text)
    data['Linha Digitável'] = barcode

    # --- Saída de Dados ---
    print("-" * 50)
    print("DADOS DA FATURA CPFL")
    print("-" * 50)
    for k, v in data.items():
        if isinstance(v, dict):
            print(f"{k}: {v}")
        else:
            print(f"{k}: {v}")
    print("-" * 50)

if __name__ == "__main__":
    extract_cpfl_data("fatura_cpfl.pdf")