import pandas as pd
import datetime
import numpy as np

from predict_model import predict

# Mapear os nomes dos meses em português
meses = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}

# Obter a data atual
data_atual = datetime.date.today()

# Converter o dia em uma string com dois dígitos
dia_atual = data_atual.strftime("%d")

# Obter o mês atual
mes_atual = meses[data_atual.month]

# Obter o ano atual
ano_atual = data_atual.strftime("%Y")

# Criar a string no formato desejado
string_atual = "previsoes_" + dia_atual + "_" + mes_atual + "_" + ano_atual + ".csv"

# Calcular a data do dia anterior
data_anterior = data_atual - datetime.timedelta(days=1)

# Converter o dia em uma string com dois dígitos
dia_anterior = data_anterior.strftime("%d")

# Obter o mês do dia anterior em português
mes_anterior = meses[data_anterior.month]

# Obter o ano do dia anterior
ano_anterior = data_anterior.strftime("%Y")

# Criar a string no formato desejado
string_anterior = "previsoes_" + dia_anterior + "_" + mes_anterior + "_" + ano_anterior + ".csv"




# Dados
dados = pd.read_csv(string_anterior, index_col = False)
# Criar DataFrame
df = pd.DataFrame(dados)

# Converter a coluna "dia" para o tipo datetime
df['Dia'] = pd.to_datetime(df['Dia'])

# Criar uma nova linha
input = predict()
nova_linha = {'Dia': input[0],'Previsão': input[1],'Intervalo Inferior': input[2],'Intervalo Superior': input[3]}
nova_linha = pd.DataFrame.from_dict([nova_linha])

# Adicionar a nova linha ao DataFrame
df = pd.concat([df, nova_linha], ignore_index=False)

# Salvar o DataFrame como arquivo CSV
df.to_csv(string_atual, index=False)
