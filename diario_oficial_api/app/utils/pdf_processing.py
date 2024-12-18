import os
import re
import fitz  # PyMuPDF
from datetime import datetime
from app.services.banco import inserir_dados_no_banco

def extrair_atos(page, page_num, atos_separados_folder, data=None):
    """
    Extrai atos administrativos de uma página e os salva como PDFs.
    """
    dados_atos = []
    text = page.get_text("text")

    regex_ato = (
    r'(ATO Nº\.? (\d+)/(\d{2,4})\s+.*?O PRESIDENTE DA ASSEMBLEIA LEGISLATIVA DO ESTADO DE PERNAMBUCO,'
    r'.*?RESOLVE:.*?Deputado ÁLVARO PORTO\s+Presidente)')

    matches_atos = re.finditer(regex_ato, text, re.DOTALL)
    
    for match in matches_atos:
        ato_text = match.group(0)
        ato_numero = match.group(2)
        ato_ano = match.group(3) 

        # Nome e caminho do arquivo PDF
        pdf_name = f"Ato_{ato_numero}_{ato_ano}.pdf"
        pdf_path_novo = os.path.join(atos_separados_folder, pdf_name)

        # Verificar se o PDF já existe
        if os.path.exists(pdf_path_novo):
            print(f"O PDF do ato {ato_numero}/{ato_ano} já existe. Pulando...")
            continue

        # Salvar ato em um novo PDF
        new_pdf = fitz.open()
        new_page = new_pdf.new_page(width=page.rect.width, height=page.rect.height)
        
        text_instances = page.search_for(ato_text)
        for instance in text_instances:
            clip_rect = instance
            pix = page.get_pixmap(clip=clip_rect, dpi=300)
            new_page.insert_image(clip_rect, pixmap=pix)
        
        new_pdf.save(pdf_path_novo, garbage=4, deflate=False)
        new_pdf.close()
        print(f"PDF salvo: {pdf_path_novo}")
        print(data)
        data_obj = datetime.strptime(data, "%d/%m/%Y")
        
        # Coletar dados do ato
        dados_atos.append({
            "DIA_DIARIO": data_obj,
            "PAGINA": f"Pág. {page_num+1}",
            "ATO_TIPO": "Ato",
            "ATO_NUMERO": ato_numero,
            "ATO_ANO": ato_ano,
            "NOME": f"Ato nº{ato_numero}/{ato_ano}",
            "TEXTO": ato_text
        })

    return dados_atos


def extrair_portarias(page, page_num, portarias_separadas_folder, data=None):
    """
    Extrai portarias de uma página e as salva como PDFs.
    """
    dados_portarias = []
    text = page.get_text("text")

    matches_portarias = re.finditer(r'(PORTARIA Nº\.? (\d+)/(\d+).*?(Superintendente Geral|Primeiro Secretário|Presidente))', text, re.DOTALL)
    
    for match in matches_portarias:
        portaria_text = match.group(0)
        portaria_numero = match.group(2) 
        portaria_ano = match.group(3) 

        # Nome e caminho do arquivo PDF
        pdf_name = f"Portaria_{portaria_numero}_{portaria_ano}.pdf"
        pdf_path_novo = os.path.join(portarias_separadas_folder, pdf_name)

        # Verificar se o PDF já existe
        if os.path.exists(pdf_path_novo):
            print(f"O PDF da portaria {portaria_numero}/{portaria_ano} já existe. Pulando...")
            continue

        # Salvar portaria em um novo PDF
        new_pdf = fitz.open()
        new_page = new_pdf.new_page(width=page.rect.width, height=page.rect.height)
        
        text_instances = page.search_for(portaria_text)
        for instance in text_instances:
            clip_rect = instance
            pix = page.get_pixmap(clip=clip_rect, dpi=300)
            new_page.insert_image(clip_rect, pixmap=pix)
        
        new_pdf.save(pdf_path_novo, garbage=4, deflate=False)
        new_pdf.close()
        print(f"PDF salvo: {pdf_path_novo}")
        
        data_obj = datetime.strptime(data, "%d/%m/%Y")
    
        # Coletar dados da portaria
        dados_portarias.append({
            "DIA_DIARIO": data_obj,
            "PAGINA": f"Pág. {page_num+1}",
            "ATO_TIPO": "Portaria",
            "ATO_NUMERO": portaria_numero,
            "ATO_ANO": portaria_ano,
            "NOME": f"Portaria nº{portaria_numero}/{portaria_ano}",
            "TEXTO": portaria_text
        })

    return dados_portarias


def extrair_oficios(page, page_num, oficios_separados_folder, data=None):
    """
    Extrai ofícios de uma página e os salva como PDFs, incluindo duas linhas após 'Atenciosamente'.
    """
    dados_oficios = []
    text = page.get_text("text")

    matches_oficios = re.finditer(
        r'(OFÍCIO Nº (\d+)/(\d+)|Ofício nº (\d+)/(\d+)|Ofício GAB nº (\d+)/(\d+)|OFÍCIO (\d+)/(\d+)/GAB.*?Deputado Estadual)', 
        text, 
        re.DOTALL
    )

    for match in matches_oficios:
        oficio_text = match.group(0)
        numero = match.group(2) or match.group(4) or match.group(6) or match.group(7) or match.group(8)
        ano = match.group(3) or match.group(5) or match.group(7) or match.group(8) or match.group(9)

        pdf_name = f"Oficio_{numero}_{ano}.pdf" if numero and ano else "Oficio_indeterminado.pdf"
        pdf_path_novo = os.path.join(oficios_separados_folder, pdf_name)

        # Verificar se o PDF já existe
        if os.path.exists(pdf_path_novo):
            print(f"O PDF do ofício {numero}/{ano} já existe. Pulando...")
            continue

        # Salvar ofício em um novo PDF
        new_pdf = fitz.open()
        new_page = new_pdf.new_page(width=page.rect.width, height=page.rect.height)

        text_instances = page.search_for(oficio_text)
        for instance in text_instances:
            clip_rect = instance
            pix = page.get_pixmap(clip=clip_rect, dpi=300)
            new_page.insert_image(clip_rect, pixmap=pix)
        
        new_pdf.save(pdf_path_novo, garbage=4, deflate=False)
        new_pdf.close()
        print(f"PDF salvo: {pdf_path_novo}")
        print(type(data))

        data_obj = datetime.strptime(data, "%d/%m/%Y")

        # Coletar dados do ofício
        dados_oficios.append({
            "DIA_DIARIO": data_obj,
            "PAGINA": f"Pág. {page_num+1}",
            "ATO_TIPO": "Ofício",
            "ATO_NUMERO": numero if numero else "Indeterminado",
            "ATO_ANO": ano if ano else "Indeterminado",
            "NOME": f"Ofício nº{numero}/{ano}" if numero and ano else "Ofício Indeterminado",
            "TEXTO": oficio_text
        })

    return dados_oficios

def extract_and_save_acts_with_integration(pdf_path, output_folder, conexao, data=None):
    """
    Processa um PDF e extrai atos, portarias e ofícios, incluindo o tipo de diário no campo 'PAGINA'.
    """
    if not os.path.isfile(pdf_path):
        print(f"Erro: {pdf_path} não é um arquivo válido.")
        return

    # Identificar tipo de diário a partir do nome do arquivo ou caminho
    diario_nome = os.path.basename(pdf_path)
    if "LegislativoExtra" in diario_nome:
        tipo_diario = "LegislativoExtra"
    elif "Legislativo" in diario_nome:
        tipo_diario = "Legislativo"
    elif "ExecutivoExtra" in diario_nome:
        tipo_diario = "ExecutivoExtra"
    elif "Executivo" in diario_nome:
        tipo_diario = "Executivo"
    else:
        tipo_diario = "Desconhecido"


    os.makedirs(output_folder, exist_ok=True)
    atos_separados_folder = os.path.join(output_folder, "atos_separados")
    portarias_separadas_folder = os.path.join(output_folder, "portarias_separadas")
    oficios_separados_folder = os.path.join(output_folder, "oficios_separados")
    os.makedirs(atos_separados_folder, exist_ok=True)
    os.makedirs(portarias_separadas_folder, exist_ok=True)
    os.makedirs(oficios_separados_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    dados_para_inserir = []

    print(data)
    for page_num in range(len(doc)):
        if tipo_diario != "Executivo":
            page = doc[page_num]
        
            # Extrair atos
            atos = extrair_atos(page, page_num, atos_separados_folder, data)
            for ato in atos:
                ato["PAGINA"] += f"/{tipo_diario}"  
            dados_para_inserir.extend(atos)

            # Extrair portarias
            portarias = extrair_portarias(page, page_num, portarias_separadas_folder, data)
            for portaria in portarias:
                portaria["PAGINA"] += f"/{tipo_diario}"  
            dados_para_inserir.extend(portarias)

            # Extrair ofícios
            oficios = extrair_oficios(page, page_num, oficios_separados_folder, data)
            for oficio in oficios:
                oficio["PAGINA"] += f"/{tipo_diario}" 
            dados_para_inserir.extend(oficios)
    
    # Inserir no banco de dados
    if dados_para_inserir:
        inserir_dados_no_banco(conexao, dados_para_inserir)
