# Gerador de Documentos — Ricardo Passos Advocacia

## Guia Completo de Instalação e Uso

Este programa gera automaticamente três documentos jurídicos (Procuração, Declaração de Hipossuficiência e Contrato) a partir dos dados de cada cliente.

---

## PARTE 1 — INSTALAÇÃO

### Opção A: Usar o programa já pronto (.exe) — RECOMENDADO

Se alguém da equipe de TI já gerou o arquivo `GeradorDocumentos.exe`, basta:

1. Copie o arquivo `GeradorDocumentos.exe` para uma pasta no seu computador (ex: `C:\Programas\GeradorDocumentos\`)
2. Dê dois cliques no arquivo `GeradorDocumentos.exe` para abrir
3. Pronto! O programa vai abrir na tela

> **Nota:** Na primeira vez, o Windows pode exibir um aviso de "programa desconhecido". Clique em **"Mais informações"** e depois em **"Executar assim mesmo"**. Isso é normal para programas feitos internamente.

---

### Opção B: Gerar o .exe a partir do código (para TI)

Quem for responsável por gerar o executável precisa fazer o seguinte **uma única vez**:

1. Instale o Python 3.11 ou superior no computador: https://www.python.org/downloads/
   - Durante a instalação, **marque a opção "Add Python to PATH"**

2. Abra o Prompt de Comando (tecle `Windows + R`, digite `cmd` e aperte Enter)

3. Navegue até a pasta do projeto:
   ```
   cd C:\caminho\para\gerador_documentos
   ```

4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

5. Gere o executável:
   ```
   pyinstaller build.spec
   ```

6. O arquivo `GeradorDocumentos.exe` será criado dentro da pasta `dist\`

7. Copie esse `.exe` para a pasta desejada e distribua para a equipe

---

## PARTE 2 — CONFIGURAÇÃO INICIAL (só na primeira vez)

Ao abrir o programa pela primeira vez, ele precisa saber duas coisas:
- **Onde estão os modelos (templates)** dos documentos
- **Onde salvar os documentos gerados**

### Passo a passo:

1. **Abra o programa** (dois cliques no `GeradorDocumentos.exe`)

2. Você verá um aviso amarelo dizendo que as pastas não estão configuradas. Isso é normal na primeira vez.

3. **Clique no ícone de engrenagem** ⚙ no canto superior direito da tela. A janela de Preferências vai abrir.

4. **Configure a pasta de templates:**
   - Clique em **"Procurar..."** ao lado de "Pasta de templates padrão"
   - Navegue até a pasta onde estão os 3 arquivos de modelo:
     - `Procuracao_TEMPLATE.docx`
     - `Declaracao_Hipossuficiencia_TEMPLATE.docx`
     - `Contrato_Prestacao_Servicos_TEMPLATE.docx`
   - Selecione essa pasta e clique **OK**
   - (Opcional) Clique em **"Testar"** para confirmar que os arquivos foram encontrados

5. **Configure a pasta de saída:**
   - Clique em **"Procurar..."** ao lado de "Pasta de saída"
   - Escolha a pasta onde os documentos prontos serão salvos (ex: uma pasta na rede do escritório)
   - Selecione essa pasta e clique **OK**
   - (Opcional) Clique em **"Testar"** para confirmar que a pasta está acessível

6. Clique em **"Salvar"**

7. O programa vai recarregar e você verá a mensagem **"✔ Usando modelos padrão"** na tela principal. Tudo certo!

> **Importante:** Essa configuração é salva automaticamente. Na próxima vez que abrir o programa, ele já vai lembrar das pastas configuradas.

---

## PARTE 3 — COMO GERAR DOCUMENTOS

Existem duas formas de informar os dados do cliente:

---

### Forma 1: A partir de uma planilha Excel (para vários clientes de uma vez)

1. Preencha a planilha modelo `Cadastro_Clientes_RicardoPassos.xlsx` com os dados dos clientes (uma linha por cliente)

2. No programa, certifique-se de que a aba **"Excel / Forms"** está selecionada (é a aba padrão)

3. Clique em **"Selecionar arquivo"** e escolha a planilha preenchida

4. O programa vai exibir uma tabela com todos os clientes encontrados. Cada linha tem um checkbox para selecionar/desmarcar:
   - Por padrão, todos os clientes vêm **selecionados**
   - Para desmarcar algum, clique no checkbox da linha
   - Use **"Selecionar todos"** ou **"Desmarcar todos"** para agilizar

5. Se algum cliente tiver dados incompletos ou CPF inválido, a linha aparecerá com um aviso amarelo (⚠). Você pode gerar mesmo assim — o aviso é apenas informativo.

6. Na parte inferior da tela, escolha quais documentos gerar (os três vêm marcados por padrão):
   - ☑ Procuração
   - ☑ Declaração de Hipossuficiência
   - ☑ Contrato

7. Clique em **"Gerar Documentos"**

8. Uma barra de progresso aparecerá. Ao terminar, o programa mostra a lista de arquivos gerados e um botão **"Abrir pasta"** para ir direto à pasta de saída.

---

### Forma 2: Digitando os dados manualmente (para um cliente por vez)

1. Clique na aba **"Dados Manuais"**

2. Preencha o formulário com os dados do cliente. Os campos com **asterisco (*)** são obrigatórios:
   - **Dados Pessoais:** Nome Completo*, Nacionalidade*, Estado Civil*, Profissão, RG*, CPF*
   - **Endereço:** Logradouro e Número*, Complemento, Bairro*, Cidade*, UF*, CEP*
   - **Contato:** E-mail, Telefone(s)
   - **Dados do Caso:** Parte Contrária / Réu*

3. O campo **UF** é uma lista suspensa — clique nele e selecione o estado

4. Se o CPF digitado for inválido, aparecerá um aviso amarelo abaixo do campo (não impede a geração)

5. Na parte inferior, escolha quais documentos gerar

6. Clique em **"Gerar Documentos"**

7. Para gerar documentos para outro cliente, clique em **"Limpar"** para limpar o formulário e comece novamente

---

## PARTE 4 — ONDE FICAM OS DOCUMENTOS GERADOS

- Os arquivos são salvos na **pasta de saída** que você configurou em Preferências
- Os nomes dos arquivos seguem o padrão:
  - `Nome_do_Cliente_Procuracao.docx`
  - `Nome_do_Cliente_Declaracao_Hipossuficiencia.docx`
  - `Nome_do_Cliente_Contrato.docx`
- Se dois clientes tiverem o mesmo nome, o segundo arquivo recebe `_v2` no final
- Após gerar, clique em **"Abrir pasta"** para acessar diretamente os arquivos

---

## PARTE 5 — USANDO UM MODELO DIFERENTE (PONTUALMENTE)

Se em alguma situação especial você precisar usar um modelo de documento diferente do padrão (por exemplo, um modelo de Procuração adaptado para um caso específico):

1. Na tela principal, clique em **"Usar modelo diferente nesta sessão ▾"**
2. Uma área com três seletores de arquivo aparecerá
3. Clique em **"Selecionar..."** ao lado do documento que deseja substituir
4. Escolha o arquivo `.docx` alternativo
5. O indicador de status vai mudar para mostrar qual documento está usando modelo personalizado
6. Gere os documentos normalmente

> **Importante:** Essa substituição vale apenas enquanto o programa estiver aberto. Quando você fechar e abrir novamente, ele voltará a usar os modelos padrão da pasta configurada. Os modelos originais **nunca** são alterados.

---

## PERGUNTAS FREQUENTES

**O programa precisa de internet para funcionar?**
Não. Tudo funciona localmente, sem necessidade de internet.

**Posso usar o programa em qualquer computador do escritório?**
Sim, basta que o computador tenha acesso à pasta de templates e à pasta de saída (geralmente na rede interna).

**O que acontece se eu fechar o programa sem salvar?**
As Preferências (pastas configuradas) são salvas automaticamente quando você clica em "Salvar" na janela de Preferências. Os documentos gerados já ficam salvos na pasta de saída assim que a geração terminar.

**E se um documento falhar durante a geração em lote?**
O programa continua gerando os demais documentos normalmente. No final, ele mostra um relatório indicando quais tiveram sucesso (✔) e quais falharam (✕).

**Preciso instalar o Python no meu computador?**
Não, se você está usando o arquivo `.exe`. O Python só é necessário para quem vai gerar o executável (normalmente a equipe de TI).

**Como mudo o tipo de ação nos documentos (ex: de "reclamação trabalhista" para "ação judicial")?**
O tipo de ação está escrito diretamente no modelo (template). Peça ao responsável pelos modelos que edite o arquivo `.docx` correspondente na pasta de templates.

**A data nos documentos é gerada automaticamente?**
Sim! A data é preenchida automaticamente com o dia em que os documentos são gerados, no formato por extenso (ex: "15 de março de 2026").
