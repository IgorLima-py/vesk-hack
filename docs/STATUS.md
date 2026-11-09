# Status

> **Este documento ganha de todos os outros.** Se qualquer outro doc do projeto contradisser o
> que está aqui, este vale.

Escrito pelo `/tchau` no fim de cada sessão, lido pelo `/oi` na abertura da seguinte. Quem lê é
sempre alguém **sem nenhum contexto**. Este repositório é público: nada aqui leva segredo, dado
pessoal ou número de cliente.

`[V]` marca o que a sessão que escreveu conferiu por comando ou leitura; `[?]` marca o que veio de
antes ou foi só dito.

## Onde estamos

05/11/2026: o repositório nasceu com a licença PolyForm Noncommercial 1.0.0 [V], o README de esqueleto, as regras
(`CLAUDE.md`), o que o regulamento pede (`docs/hackathon.md`), o que a Meta e o TikTok dão por anúncio
(`docs/fontes.md`) e o roadmap de C1 a C13 (`docs/ROADMAP.md`), escritos na sessão que decidiu o hack. Nenhum código
ainda.

09/11/2026: nenhuma fatia tinha começado, e a fila em sequência já não cabia até 28/11. Por decisão do Igor, a fila
virou ondas (bloco 2 do `docs/ROADMAP.md`), e uma sessão orquestradora (a seção O) abre as fatias em paralelo, cada
uma no seu worktree. O ponteiro está no orquestrador. As regras de quem anda em paralelo estão no `CLAUDE.md`. Ainda
nenhum código. A mudança foi escrita de fora, numa sessão do outro repositório, e não teve `/tchau` daqui.

## Próximo passo imediato

O orquestrador (Opus, esforço high, na Karen) abre a onda 1: a C1 (os anúncios, com o Igor), a C2 (a vitrine e o
rascunho) e a C3 (os exemplos com gabarito e o contrato do motor), cada uma na sua sessão.

## Pendências

- [V] O repositório no GitHub (`IgorLima-py/vesk-hack`) foi criado público em 06/11/2026, e o C0 sobe nele no `/tchau`
  da sessão que o escreveu. A configuração (`.gitignore`, `.gitattributes`, `.claude/settings.json`) e o cabeçalho do
  `docs/DESVIOS.md` foram escritos do zero no evento, sem copiar modelo de antes dele (6.2 do regulamento).
- O motor na nuvem é feito no repositório do motor, de 07 a 10/11. A C6 confere se ele subiu com o `curl` da
  dependência.
- O domínio `hack.vesklab.com` (C2), a conta do Modal e a do Resend são do Igor.
- O arquivo das palavras proibidas (`vesk-hack-videos/proibido.txt`, fora do git) existe só na máquina que escreveu
  este repositório. Em outra, o `test -s` do bloco 3 barra a fatia até o arquivo ser copiado de lá.
- Bateria: o `python -m pytest -q` não acha teste (`no tests ran`, sai 5), porque ainda não há código. A trava do
  playbook barrou o primeiro push do C0, e ele subiu no segundo, com este registro. A C2 põe os testes no push.

## O que foi tentado e não funcionou

- Nada ainda.
