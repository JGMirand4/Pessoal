import os
import re
import fitz  # PyMuPDF
from datetime import datetime
from app.services.banco import inserir_dados_no_banco

def extract_and_save_acts_with_integration(pdf_path, output_folder, conexao):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    dados_para_inserir = []
    atos_separados_folder = os.path.join(output_folder, "atos_separados")
    os.makedirs(atos_separados_folder, exist_ok=True)

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        matches = re.finditer(r'(ATO Nº (\d+)/(\d+).*?Presidente)', text, re.DOTALL)
        
        for match in matches:
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
            
            # Salvar o PDF
            new_pdf.save(pdf_path_novo, garbage=4, deflate=False)
            new_pdf.close()
            print(f"PDF salvo: {pdf_path_novo}")

            # Coletar dados para inserção no banco
            dados_para_inserir.append({
                "DIA_DIARIO": datetime.now(),
                "PAGINA": f"Página {page_num+1}",
                "ATO_TIPO": "Ato Administrativo",
                "ATO_NUMERO": ato_numero,
                "ATO_ANO": ato_ano,
                "NOME": f"Ato nº{ato_numero}/{ato_ano}",
                "TEXTO": ato_text
            })
    
    # Inserir dados no banco
    if dados_para_inserir:
        inserir_dados_no_banco(conexao, dados_para_inserir)
