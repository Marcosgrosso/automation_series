import smtplib
from getpass import getpass
import datetime
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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

# Obter o mês do dia anterior em português
mes_atual = meses[data_atual.month]

# Obter o ano do dia anterior
ano_atual = data_atual.strftime("%Y")

# Criar a string no formato desejado
string_atual = "previsoes_" + dia_atual + "_" + mes_atual + "_" + ano_atual + ".csv"

def encaminhar_email(origem, senha, destino, assunto, mensagem):
    try:
        # Configurações do servidor SMTP
        servidor_smtp = 'smtp.gmail.com'
        porta_smtp = 587

        # Criação da conexão com o servidor SMTP
        conexao = smtplib.SMTP(servidor_smtp, porta_smtp)
        conexao.starttls()

        # Autenticação com as credenciais
        conexao.login(origem, senha)

        # Envio do e-mail
        cabecalho = f"From: {origem}\nTo: {destino}\nSubject: {assunto}\n"
        mensagem_completa = cabecalho + mensagem.as_string()
        conexao.sendmail(origem, destino, mensagem_completa.encode('utf-8'))

        # Encerramento da conexão com o servidor SMTP
        conexao.quit()

        print("E-mail enviado com sucesso!")
    except smtplib.SMTPAuthenticationError:
        print("Erro de autenticação: Nome de usuário ou senha inválidos.")
    except smtplib.SMTPException as e:
        print("Erro ao enviar o e-mail:", e)


# Função para gerar o corpo do e-mail com base no dia da semana
def gerar_corpo_email():
    # Criação do corpo de e-mail
    mensagem = MIMEMultipart()

    # Texto do e-mail
    texto = """
    <p>Olá professor,</p>

    <p>Segue em anexo o arquivo CSV contendo as <b>previsões diárias</b>. O arquivo contém o dia em que a temperatura foi predita, a predição da temperatura média, o limite inferior e limite superior do intervalo com 95% de confiança para a previsão.</p>

    <p>Aqui está o link do nosso site, contendo mais informações sobre o modelo: <a href="https://gabrieltalasso-trabalho-series-streamlit-app-vug9p4.streamlit.app/">Site do trabalho</a></p>

    <p>Aqui está o link do nosso repositório onde está alocado o site: <a href="https://github.com/GabrielTalasso/trabalho-series">Repositório GitHub trabalho-series</a></p>

    <p>Aqui está o link do nosso repositório que realiza a automatização: <a href="https://github.com/Marcosgrosso/automation_series">Repositório GitHub automation_series</a></p>

    <p>Cordialmente,</p>

    Marcos José Grosso Filho - 236226,
    Gabriel Ukstin Talasso - 235078,
    Tiago Henrique Silva Monteiro - 217517
    """
    parte_texto = MIMEText(texto, "html")
    mensagem.attach(parte_texto)

    # Anexo de arquivo CSV
    caminho_arquivo = "data/" + string_atual
    nome_arquivo = string_atual
    with open(caminho_arquivo, "rb") as arquivo:
        parte_anexo = MIMEBase("application", "octet-stream")
        parte_anexo.set_payload(arquivo.read())
    encoders.encode_base64(parte_anexo)
    parte_anexo.add_header(
        "Content-Disposition",
        f"attachment; filename= {nome_arquivo}",
    )
    mensagem.attach(parte_anexo)

    return mensagem

# Função para enviar o e-mail
def enviar_email():
    origem = 'seriestemporaiss@gmail.com'
    senha = 'aloqkbbsftrgjiol'
    destino = ['m236226@dac.unicamp.br', 't217517@dac.unicamp.br', 'g235078@dac.unicamp.br', 'ctrucios@unicamp.br'] #, 't217517@dac.unicamp.br', 'g235078@dac.unicamp.br'
    assunto = f"Previsões do dia {date.today()} - Trabalho de Séries Temporais"
    mensagem = gerar_corpo_email()

    # Encaminhar e-mail
    encaminhar_email(origem, senha, destino, assunto, mensagem)

enviar_email()
