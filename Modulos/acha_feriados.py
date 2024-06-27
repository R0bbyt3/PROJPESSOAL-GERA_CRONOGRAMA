import datetime

# Dicionário de feriados incluindo possíveis emendas
feriados = {
    'Confraternização Universal': '01/01',
    'Carnaval': '12/02',  # A emenda seria no dia 11/02
    'Quarta-feira de Cinzas (meio expediente)': '13/02',
    'Sexta-feira Santa': '29/03',
    'Tiradentes': '21/04',
    'Dia de São Jorge': '23/04',
    'Dia do Trabalho': '01/05',
    'Corpus Christi': '30/05',  # A emenda seria no dia 31/05
    'Independência do Brasil': '07/09',
    'Nossa Senhora Aparecida': '12/10',
    'Finados': '02/11',
    'Proclamação da República': '15/11',  # A emenda seria no dia 16/11
    'Dia da Consciência Negra': '20/11',
    'Natal': '25/12'
}

def acha_feriados(ano, data_inicio, data_fim):
    # Convertendo as strings de data para objetos datetime
    data_inicio = datetime.datetime.strptime(f"{data_inicio}/{ano}", "%d/%m/%Y")
    data_fim = datetime.datetime.strptime(f"{data_fim}/{ano}", "%d/%m/%Y")
    
    # Lista para contar a frequência de feriados em cada dia da semana
    frequencia = [0, 0, 0, 0, 0, 0, 0]  # Segunda a Domingo

    # Iterar sobre cada feriado e verificar se está no intervalo
    for nome, data in feriados.items():
        data_feriado = datetime.datetime.strptime(f"{data}/{ano}", "%d/%m/%Y")
        if data_inicio <= data_feriado <= data_fim:
            # Ajustando o índice porque o Python conta segunda-feira como 0
            dia_semana = data_feriado.weekday()  # Segunda é 0, Domingo é 6
            frequencia[dia_semana] += 1

    return frequencia

# Exemplo de como usar a função
print(acha_feriados(2024, '27/09', '10/12'))
