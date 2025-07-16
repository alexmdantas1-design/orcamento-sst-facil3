
# Requisitos: pip install streamlit fpdf pandas openpyxl

import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd

# Carregar planilhas
precos_df = pd.read_excel("Planilha de preços.xlsx", sheet_name="Preco por servico")
cidades_df = pd.read_excel("Planilha de preços.xlsx", sheet_name="Cidade")

# Função para determinar faixa por número de trabalhadores
def obter_faixa(trabalhadores):
    if trabalhadores <= 5:
        return "ATÉ 5"
    elif trabalhadores <= 19:
        return "DE 6 A 19"
    elif trabalhadores <= 34:
        return "DE 20 A 34"
    elif trabalhadores <= 49:
        return "DE 35 A 49"
    elif trabalhadores <= 74:
        return "DE 50 A 74"
    elif trabalhadores <= 99:
        return "DE 75 A 99"
    else:
        return "ACIMA DE 100"

# Função para buscar valor por serviço, faixa, tipo e porte
def pegar_preco(servico, faixa, tipo, porte):
    linha = precos_df[(precos_df["servico"] == servico) &
                      (precos_df["faixa"] == faixa) &
                      (precos_df["tipo"] == tipo) &
                      (precos_df["porte"] == porte)]
    return float(linha["valor"].values[0]) if not linha.empty else 0.0

# Valor da cidade (alinhamento)
def pegar_valor_cidade(cidade):
    linha = cidades_df[cidades_df["cidade"].str.lower() == cidade.lower()]
    return float(linha["valor"].values[0]) if not linha.empty else 0.0

# Função para gerar PDF
def gerar_pdf(dados, servicos, valores, cidade_valor, desconto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "SST FÁCIL - PROPOSTA DE ORÇAMENTO", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Data de emissão: {datetime.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, "Prezado(a),

É com a solidez de mais de uma década de atuação e a expertise consolidada desde 2012 que a SST FÁCIL Saúde e Segurança do Trabalho apresenta esta proposta. Com raízes no Seridó Potiguar e uma trajetória que se estende por diversos estados como Rio Grande do Norte, Paraíba, Pernambuco e Minas Gerais, nos firmamos como referência em engenharia, com um destaque notório na área de Segurança do Trabalho.

Nossa equipe é composta por especialistas altamente qualificados, que unem o conhecimento técnico a uma vasta experiência prática em diferentes setores e portes de empresas. Isso nos permite não apenas identificar e gerenciar os riscos de forma eficaz, mas também oferecer soluções personalizadas que garantem a conformidade legal, promovem um ambiente de trabalho mais seguro e otimizam a produtividade da sua operação.

Este orçamento é um convite para você investir na excelência e na tranquilidade de ter um parceiro com comprovada capacidade para elevar os padrões de segurança e saúde em sua organização.")

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "
Dados do Cliente:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Razão Social: {dados['razao']}", ln=True)
    pdf.cell(0, 8, f"CNPJ: {dados['cnpj']}", ln=True)
    pdf.cell(0, 8, f"Cidade: {dados['cidade']}", ln=True)
    pdf.cell(0, 8, f"Nº de trabalhadores: {dados['funcionarios']}", ln=True)
    pdf.cell(0, 8, f"Tipo: {dados['tipo']}", ln=True)
    pdf.cell(0, 8, f"Porte: {dados['porte']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Serviços Contratados:", ln=True)
    pdf.set_font("Arial", "", 11)
    total = 0
    for nome, valor in valores.items():
        pdf.multi_cell(0, 8, f"- {nome}
  Valor: R$ {valor:.2f}".replace(".", ","))
        pdf.ln(1)
        if "ESOCIAL" in nome:
            total += valor
        else:
            total += valor * (1 - desconto)

    total += cidade_valor
    pdf.multi_cell(0, 8, f"- Valor do Alinhamento (cidade): R$ {cidade_valor:.2f}".replace(".", ","))

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"TOTAL FINAL: R$ {total:.2f}".replace(".", ","), ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 8, "Agradecemos pela confiança. Este orçamento é válido por 15 dias a partir da data de emissão.", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, "Este é o momento ideal para sua empresa avançar na gestão de segurança e saúde no trabalho. Nossa agenda de projetos é cuidadosamente planejada para garantir a dedicação e a qualidade que cada cliente merece, permitindo que poucas novas parcerias sejam iniciadas a cada ciclo.

Aproveite a oportunidade de contar com uma equipe experiente e preparada para transformar a realidade da sua empresa. Garanta agora mesmo a sua prioridade e inicie sua jornada rumo a um ambiente de trabalho mais seguro e produtivo. Estamos à disposição para qualquer esclarecimento e para darmos o próximo passo em direção a essa parceria de sucesso. Contato: 84 99669-2013")

    nome_arquivo = f"orcamento_{dados['cnpj'].replace('/', '').replace('.', '').replace('-', '')}.pdf"
    pdf.output(nome_arquivo)
    return nome_arquivo
