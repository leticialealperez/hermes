---

## 📁 Estrutura da pasta `hermes/`

```
hermes/
├── assets/
│   └── icon.ico                # (opcional) Ícone do app
├── main.py                     # Código principal com GUI + Selenium
├── requirements.txt            # Dependências do projeto
└── README.md                   # Instruções de uso
```

---

## 📄 `main.py`

Esse é o script completo com interface gráfica, envio via Selenium, logs e barra de progresso.

---

## 📄 `requirements.txt`

```txt
selenium
pandas
pyperclip
```

> Use:

```bash
pip install -r requirements.txt
```

---

## 📄 `README.md`

````markdown
# Hermes (com Interface Gráfica)

Este aplicativo permite o envio automatizado de mensagens no WhatsApp Web com suporte a:

✅ Texto  
✅ Imagens com ou sem legenda  
✅ Vídeos com ou sem legenda  
✅ Leitura de contatos de um arquivo CSV  
✅ Interface gráfica com barra de progresso e logs

---

## 📦 Pré-requisitos

- Google Chrome instalado
- ChromeDriver compatível com a versão do seu navegador
- Python 3.10+ e pip

```bash
pip install -r requirements.txt
```
````

---

## 🛠️ Como gerar o .EXE

1. Instale o PyInstaller:

```bash
pip install pyinstaller
```

2. Gere o executável:

```bash
pyinstaller --noconfirm --onefile --windowed whatsapp_sender.py
```

(Opcional com ícone:)

```bash
pyinstaller --noconfirm --onefile --windowed --icon=assets/icon.ico whatsapp_sender.py
```

3. O `.exe` será gerado na pasta `dist/`

---

## 📑 Formato do CSV

Seu arquivo `.csv` precisa conter **uma coluna chamada `telefone`**, no seguinte formato:

```
telefone
5511987654321
5584999999999
```

---

## 🧩 Dica

Mantenha o ChromeDriver na mesma pasta do `.exe` ou adicione ao PATH do Windows.
