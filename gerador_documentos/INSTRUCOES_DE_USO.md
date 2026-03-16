# Gerador de Documentos — Ricardo Passos Advocacia

## Guia de Instalação e Uso (passo a passo para iniciantes)

Este programa gera automaticamente três documentos jurídicos a partir dos dados de cada cliente:
- **Procuração**
- **Declaração de Hipossuficiência**
- **Contrato de Prestação de Serviços**

---

## PARTE 1 — COMO INSTALAR

### Opção A: Usar o programa já pronto (.exe) — RECOMENDADO para usuários comuns

Se alguém da equipe de TI já gerou o arquivo `GeradorDocumentos.exe`:

1. **Copie o arquivo** `GeradorDocumentos.exe` para uma pasta no seu computador
   - Exemplo: crie uma pasta `C:\Programas\GeradorDocumentos\` e coloque o arquivo lá

2. **Dê dois cliques** no arquivo `GeradorDocumentos.exe` para abrir o programa

3. **Pronto!** O programa vai abrir na tela

> **Aviso do Windows:** Na primeira vez, o Windows pode mostrar uma tela azul dizendo "O Windows protegeu o computador". Isso é normal para programas feitos internamente. Para continuar:
> 1. Clique em **"Mais informações"** (texto pequeno abaixo da mensagem)
> 2. Clique no botão **"Executar assim mesmo"**
> 3. O programa vai abrir normalmente

> **Dica:** Para facilitar o acesso no dia a dia, clique com o botão direito no `GeradorDocumentos.exe` e escolha **"Criar atalho"**. Depois arraste o atalho para a Área de Trabalho.

---

### Opção B: Gerar o .exe a partir do código (para equipe de TI)

Quem for responsável por gerar o executável precisa fazer o seguinte **uma única vez**:

1. **Instale o Python 3.11 ou superior:** https://www.python.org/downloads/
   - Durante a instalação, **marque a caixa "Add Python to PATH"** (muito importante!)

2. **Abra o Prompt de Comando:**
   - Tecle `Windows + R` no teclado
   - Digite `cmd` e aperte Enter

3. **Navegue até a pasta do projeto:**
   ```
   cd C:\caminho\para\gerador_documentos
   ```

4. **Instale as dependências:**
   ```
   pip install -r requirements.txt
   ```

5. **Gere o executável:**
   ```
   pyinstaller build.spec
   ```

6. O arquivo `GeradorDocumentos.exe` será criado dentro da pasta `dist\`

7. **Distribua** esse `.exe` para os demais membros da equipe

---

## PARTE 2 — COMO USAR O PROGRAMA

### Passo 1: Selecionar os templates (modelos de documentos)

Toda vez que abrir o programa, você precisa indicar onde estão os modelos dos documentos:

1. **Abra o programa** (dois cliques no `GeradorDocumentos.exe`)

2. Na parte de cima da tela, você verá a seção **"Templates"** com a mensagem "Nenhum template selecionado"

3. Clique no botão **"Selecionar arquivos"**

4. Uma janela do Windows vai abrir para você escolher arquivos. Navegue até a pasta onde estão os 3 modelos:
   - `Procuracao_TEMPLATE.docx`
   - `Declaracao_Hipossuficiencia_TEMPLATE.docx`
   - `Contrato_Prestacao_Servicos_TEMPLATE.docx`

5. **Selecione os 3 arquivos de uma vez** (segure a tecla `Ctrl` e clique em cada um) e clique **"Abrir"**

6. O programa vai mostrar **"✔ 3/3 templates carregados"** — isso significa que está tudo certo!

> **Importante:** Os nomes dos arquivos de template devem ser exatamente como mostrado acima. Se os nomes forem diferentes, o programa não vai reconhecê-los.

---

### Passo 2: Informar os dados dos clientes

Existem **duas formas** de informar os dados. Escolha a que preferir:

---

#### Forma 1: A partir de uma planilha Excel (para vários clientes de uma vez)

1. Preencha a planilha modelo `Cadastro_Clientes_RicardoPassos.xlsx` com os dados dos clientes (uma linha por cliente)

2. No programa, certifique-se de que a aba **"Excel / Forms"** está selecionada (é a aba padrão que já aparece aberta)

3. Clique em **"Selecionar arquivo"** e escolha a planilha preenchida

4. O programa vai mostrar uma tabela com todos os clientes encontrados:
   - Cada linha tem um checkbox (quadradinho) para selecionar ou desmarcar o cliente
   - Por padrão, todos vêm **selecionados**
   - Para desmarcar algum, clique no checkbox da linha
   - Use **"Selecionar todos"** ou **"Desmarcar todos"** para agilizar

5. Se algum cliente tiver dados incompletos ou CPF inválido, a linha aparecerá com um aviso amarelo (⚠). Você pode gerar mesmo assim — o aviso é apenas informativo

---

#### Forma 2: Digitando os dados manualmente (um cliente por vez)

1. Clique na aba **"Dados Manuais"** na parte de cima

2. Preencha o formulário com os dados do cliente. Os campos com **asterisco (*)** são obrigatórios:
   - **Dados Pessoais:** Nome Completo*, Nacionalidade*, Estado Civil*, Profissão, RG*, CPF*
   - **Endereço:** Logradouro e Número*, Complemento, Bairro*, Cidade*, UF*, CEP*
   - **Contato:** E-mail, Telefone(s)
   - **Dados do Caso:** Parte Contrária / Réu*

3. O campo **UF** é uma lista — clique nele e selecione o estado

4. Se o CPF digitado for inválido, aparecerá um aviso amarelo abaixo do campo (não impede a geração)

---

### Passo 3: Escolher quais documentos gerar

Na parte inferior da tela, você verá três opções com checkbox:
- ☑ Procuração
- ☑ Declaração de Hipossuficiência
- ☑ Contrato

Por padrão, os três vêm marcados. Desmarque os que não quiser gerar.

> **Nota:** Se algum template não foi carregado no Passo 1, o checkbox correspondente ficará desabilitado (cinza).

---

### Passo 4: Gerar os documentos

1. Clique no botão **"Gerar Documentos"**

2. Uma barra de progresso aparecerá durante a geração

3. Ao terminar, o programa mostra a lista de documentos gerados com:
   - **✔** para documentos gerados com sucesso
   - **✕** para documentos que falharam (com a descrição do erro)

4. Clique no botão **"Abrir pasta"** para ir direto à pasta onde os documentos foram salvos

5. Para gerar para outro cliente (aba manual), clique em **"Limpar"** e preencha novamente

---

## PARTE 3 — ONDE FICAM OS DOCUMENTOS GERADOS

- Os documentos são salvos automaticamente na pasta **`saida`** (criada ao lado do `GeradorDocumentos.exe`), dentro de uma subpasta com a data e hora da geração (ex: `saida\2026-03-16_14-30-00\`)
- Os nomes dos arquivos seguem o padrão:
  - `Nome_do_Cliente_Procuracao.docx`
  - `Nome_do_Cliente_Declaracao_Hipossuficiencia.docx`
  - `Nome_do_Cliente_Contrato.docx`
- Se dois clientes tiverem o mesmo nome, o segundo arquivo recebe `_v2` no final
- Após gerar, clique em **"Abrir pasta"** para acessar diretamente os documentos

---

## PERGUNTAS FREQUENTES

**O programa precisa de internet para funcionar?**
Não. Tudo funciona no seu computador, sem necessidade de internet.

**Posso usar o programa em qualquer computador do escritório?**
Sim, basta copiar o `GeradorDocumentos.exe` para o computador desejado. Cada computador precisará ter acesso à pasta onde estão os templates.

**Preciso selecionar os templates toda vez que abrir o programa?**
Sim. Toda vez que abrir o programa, você precisa clicar em "Selecionar arquivos" e escolher os 3 modelos de template. É rápido: basta selecionar os 3 arquivos de uma vez.

**E se um documento falhar durante a geração em lote?**
O programa continua gerando os demais documentos normalmente. No final, ele mostra um relatório indicando quais tiveram sucesso (✔) e quais falharam (✕).

**Preciso instalar o Python no meu computador?**
Não, se você está usando o arquivo `.exe`. O Python só é necessário para quem vai gerar o executável (normalmente a equipe de TI).

**Como mudo o tipo de ação nos documentos?**
O tipo de ação está escrito diretamente no modelo (template). Peça ao responsável pelos modelos que edite o arquivo `.docx` correspondente.

**A data nos documentos é gerada automaticamente?**
Sim! A data é preenchida automaticamente com o dia em que os documentos são gerados, no formato por extenso (ex: "16 de março de 2026").

**O que são "placeholders" que aparecem nos templates?**
São marcações no formato `{{NOME_DO_CAMPO}}` dentro dos arquivos Word. O programa substitui essas marcações pelos dados reais do cliente. Você não precisa se preocupar com isso — basta usar os templates fornecidos.
