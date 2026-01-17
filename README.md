# Glassdoor Job Scraper

## Introducao
Este projeto atualmente automatiza o login no Glassdoor usando Selenium e uma conta Google, preparando o ambiente para futuras etapas de raspagem.
As funcionalidades de coleta de vagas, exportacao e envio por e-mail estao previstas para uma proxima fase.

## Requisitos
- Python 3.10+
- Google Chrome ou Chromium
- ChromeDriver compativel com a versao do navegador
- Conta Google (para login no Glassdoor)
- Acesso a um servidor SMTP para envio do e-mail

## Dependencias
Instale as bibliotecas principais (ajuste conforme o `requirements.txt` se existir):
- selenium
- pandas
- openpyxl (para salvar em .xlsx)

Exemplo:
```bash
python -m pip install selenium pandas openpyxl
```

## Variaveis de ambiente
Defina as variaveis abaixo antes de executar o login automatizado:
- `BROWSER_LOCATION`: caminho para o executavel do Chrome/Chromium
- `CHROMEDRIVER_PATH`: caminho para o ChromeDriver
- `GOOGLE_EMAIL`: e-mail da conta Google
- `GOOGLE_PASSWORD`: senha da conta Google

## Como executar
```bash
python main.py
```

## Jenkins
Existe um `Jenkinsfile` na raiz do projeto. Para usar:
1. Crie um job do tipo Pipeline no Jenkins.
2. Aponte o repo do projeto.
3. Garanta que as variaveis de ambiente estejam configuradas no Jenkins (Credentials ou env vars).
4. Agende a execucao com cron, se quiser rodar periodicamente.

## Observacoes
- O Glassdoor pode alterar o layout, o que pode quebrar seletores do Selenium.
- Respeite os Termos de Uso do Glassdoor ao fazer raspagem.
- Recomendado executar em ambiente isolado (virtualenv) e com VPN se necessario.

## Em producao (planejado)
- Raspagem de vagas para Suporte Tecnico, NOC, Desenvolvedor Java Jr e Analista de Redes.
- Armazenamento em planilha com pandas.
- Envio automatico das vagas por e-mail.

## Estrutura
```
.
├─ Jenkinsfile
└─ main.py
```
