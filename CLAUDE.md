# vesk-hack

O add-on do Hack Brasil, na trilha Logística & automação: o **piloto automático do criativo**. Ele puxa o vídeo do
anúncio e a curva de retenção da plataforma, manda o vídeo ao motor (um serviço privado, chamado por API) que lê cada
segundo, cruza o que estava na tela com quem saiu, e entrega o laudo, a variante de uma mudança só e o plano do teste.
Repositório público, licença PolyForm Noncommercial 1.0.0. Prazo: 30/11/2026 às 23h59.

- Estado e handoff: `docs/STATUS.md`
- Fila e ponteiro: `docs/ROADMAP.md`, `docs/PROXIMO.md`
- O que o regulamento pede: `docs/hackathon.md`; o que a Meta e o TikTok dão por anúncio: `docs/fontes.md`
- O contrato do motor: `contrato/` (nasce na C3)
- Tarefas avulsas: no Linear, time `VES`, projeto «Hack Brasil — vesk-hack», com uma tarefa espelho por fatia. O
  `/tchau` atualiza o espelho: a fatia que fechou vai para Done, a que abriu vai para In Progress.

bateria: python -m pytest -q

## Regras

- **Tudo aqui é público, para sempre**, inclusive o histórico do git, o `docs/STATUS.md` e todo handoff do `/tchau`.
  Nada de segredo, dado pessoal, nome de prospect ou número de cliente.
- **O motor é uma caixa preta com contrato.** Este repositório só conhece a API (`contrato/`), com a URL e o token
  pelo ambiente. Nunca nomeia, importa ou descreve o projeto privado de onde o motor vem.
- **Segredo só no ambiente.** A URL e o token do motor, a chave do Resend e o token da Meta moram nos segredos do
  Worker e do Modal e no ambiente da máquina. `.dev.vars*` e `.env*` ficam no `.gitignore`. O Claude nunca lê arquivo
  de segredo e nunca digita credencial.
- **O vídeo e o relatório que a pessoa manda** são processados no Modal e apagados depois do laudo, e a variante que
  ela pediu some no prazo do laudo, com as duas coisas escritas na tela. O e-mail que ela digita vive aqui só enquanto
  o pedido roda; o Resend guarda o envio por 30 dias (https://resend.com/pricing), e a tela também diz isso.
- **O Resend envia só o laudo que a pessoa pediu:** o da página, para o e-mail que ela digitou; e o do piloto
  automático (C9), dos anúncios da própria conta da Vesk, para o Igor, que ligou o gatilho. Nunca prospecção, cold
  email ou lista.
- **Dinheiro e publicação são do Igor.** O anúncio e o teste A/B da Vesk gastam só dentro do teto dele, e quem aperta
  publicar é ele. Código deste repositório cria anúncio só pausado.
- **Mensagem em nome do Igor só com o sim dele na hora:** convite a usuário, post, e-mail fora do laudo pedido. A
  prospecção ativa da Vesk é só para empresa dos EUA; no Brasil, só quem chega por conta própria (a C11 decide se
  convidar conhecido conta como prospecção).
- **Nenhum dado de terceiros coletado fora de API oficial** entra aqui. Entram só os anúncios da Vesk, os vídeos
  sintéticos e o que a própria pessoa manda.
- **Linguagem:** em português, «reprodução» e «permanência»; em inglês, «Remain» e «playback». A palavra proibida e o
  que nunca pode vazar para cá estão em `vesk-hack-videos/proibido.txt`, fora do git (bloco 3 do `docs/ROADMAP.md`),
  e nenhuma saída os usa.
- **Todo navegador que abre anúncio abre mudo** (`--mute-audio`).
- **Vídeo, áudio, export e autorização ficam fora do git**, em `C:/Users/Usuario/Desktop/Side-Projects/vesk-hack-videos/`.
- **Commit à vontade; push só no `/tchau`.** O assunto do commit começa pelo código da fatia (`C4: ...`).
- **Fatias em paralelo (desde 09/11), abertas pelo orquestrador** (seção O do `docs/ROADMAP.md`), cada uma no seu
  worktree:
  - ela não mexe no `docs/PROXIMO.md`, porque o ponteiro é do orquestrador;
  - no `/tchau`, a base do diff da segunda opinião é `git merge-base HEAD origin/main` (depois do `git fetch`), porque
    a linha `chat:` do ponteiro não marca o começo dela;
  - ela marca o próprio ✅ na fila e junta na `main` com `git fetch`, `git rebase origin/main` e
    `git push origin HEAD:main`, nunca com força. Num conflito no `docs/STATUS.md`, ficam as duas entradas.
