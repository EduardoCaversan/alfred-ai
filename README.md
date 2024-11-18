# Alfred - Seu Assistente Pessoal Inteligente
Bem-vindo ao **Alfred** – o seu assistente virtual, inspirado no mestre de sabedoria e estratégia de Gotham, o fiel mordomo do Batman. Assim como Alfred, o assistente está sempre pronto para ajudar, executar tarefas e até contar uma piada, tudo com uma voz amigável e moderna!
Alfred é um assistente pessoal baseado em inteligência artificial que pode executar comandos de voz para controlar seu computador, acessar informações na web, responder perguntas e até fazer piadas para melhorar seu dia.

## Funcionalidades
Alfred não é apenas um assistente de voz qualquer, ele tem diversas funcionalidades que tornam o dia a dia mais fácil:
- **Controle de aplicativos**: Abra qualquer aplicativo instalado no seu sistema com um simples comando de voz.
- **Pesquisa no Google**: Pergunte qualquer coisa ao Alfred, e ele fará uma pesquisa para você no Google ou no YouTube.
- **Pesquisa no YouTube**: Encontre vídeos sobre qualquer tema diretamente no YouTube.
- **Navegação no Azure**: Abra seu portal do Azure ou board de desenvolvimento com comandos personalizados.
- **Respostas inteligentes**: Pergunte qualquer coisa, e Alfred vai usar IA para tentar responder sua dúvida.
- **Piadas para relaxar**: Precisa de um sorriso? Alfred tem piadas para alegrar seu dia!
- **Frases motivacionais**: Alfred compartilha frases que podem inspirar e motivar você a conquistar seus objetivos!

## Tecnologias Utilizadas
- **Python**: O coração do Alfred.
- **Transformers (Hugging Face)**: Para integrar inteligência artificial e responder perguntas.
- **SpeechRecognition**: Para transformar sua fala em texto.
- **pyttsx3**: Para fazer o Alfred "falar" com você.
- **Webbrowser**: Para abrir páginas web e resultados de pesquisa no Google ou YouTube.

## Como Usar
Alfred é simples de usar: basta chamá-lo com um "Alfred", e ele estará pronto para ajudar!
Caso queira sair do programa: Fale sair, ou feche o console!

### Pré-requisitos
Você precisará do Python instalado em sua máquina. Além disso, deve garantir que as dependências necessárias sejam instaladas.

### Instalando as Dependências
Para instalar as dependências do projeto, basta rodar o seguinte comando:
- pip install pyttsx3 speechrecognition transformers webbrowser

### Passo a passo para build
- git clone https://github.com/EduardoCaversan/alfred-ai.git
- cd alfred-ai

### Crie e ative um ambiente virtual (Não é obrigatório, mas recomendo)
- python -m venv venv
- venv\Scripts\activate

### Para rodar o Alfred
- python alfred.py

### Como gerar o executável para windows
- pip install pyinstaller
- pyinstaller --onefile --console --icon=batman.ico alfred.py
Isso gerará o executável na pasta dist/.

### Comandos de Voz Suportados
Aqui estão alguns comandos que você pode usar para interagir com o Alfred:
"Abrir o Google {pesquisa}" caso você não forneça uma pesquisa, ele apenas abrirá a home do Google.
"Abrir o YouTube {pesquisa}" caso você não forneça uma pesquisa, ele apenas abrirá a home do YouTube.
"Qual a hora atual?" na verdade qualquer comando com "hora" ele irá te fornecer a hora atual! 
"Conte uma piada!" piadas do chatgpt kkk.
"Me dê uma frase motivacional" ou "Preciso de motivação" as palavras chave são "frase" e "motivação", ele irá citar frases icônicas do Alfred.
"Pesquisar {pergunta}" ou "Procurar {pergunta}" ele irá buscar na web e trazer os 5 primeiros resultados, incluindo título e link!

### Contribuindo
Se você quiser contribuir com melhorias, corrija bugs ou adicione novos recursos, fique à vontade para fazer um fork e enviar um pull request! Aqui estão alguns passos básicos para começar:
- Faça o fork deste repositório.
- Crie uma branch para sua feature ou correção.
- Dê commit de suas mudanças.
- Envie um pull request para o repositório principal.

### Licença
Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.
