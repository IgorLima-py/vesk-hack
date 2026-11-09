# Próximo

> Este arquivo é **lido por regex**, não por humano. Uma chave por linha, `chave: valor`, sem
> markdown, sem lista, sem negrito. O que vier depois de `#` é comentário e é ignorado.
>
> Quem lê: o hook de abertura do plugin `playbook` (`sessao-abre.ps1`), e o `/oi` quando não há hook.
> Quem escreve: o `/tchau`, ao avançar o ponteiro, e o `/360`, ao desenhar o roadmap.
>
> **Nenhuma chave existe sem consumidor declarado.** Não invente campo aqui sem dizer quem o lê.

chat: O # humano + título da sessão
titulo: O orquestrador das ondas # humano
perfil: dificil # /360 e /tchau (política)
modelo: opus # hook e /oi conferem contra a sessão
esforco: high # hook e /oi conferem contra a sessão
forma: sessao # vocabulário aceito: sessao
maquina: Karen # /oi compara com esta máquina e avisa
plan-mode: nao # /oi imprime "abra com Shift+Tab"
persona: chefe de obra que abre cada frente assim que o terreno deixa, nunca faz o trabalho de uma frente por ela, e diz ao dono numa tabela o que roda e o que espera a mão dele
objetivo: a seção O do docs/ROADMAP.md. Tocar a fila em ondas: abrir cada fatia cuja dependência passa, numa sessão própria com worktree, o perfil da seção e plan mode quando ela pede, e dar ao Igor a tabela do que roda e do que espera a mão dele. Começa pela onda 1 (C1, C2 e C3). Nunca faz o trabalho de uma fatia, nunca aprova plano nem decide pelo Igor, e nunca junta ramo na main

<!--
`modelo:` e `esforco:` são SEMPRE re-resolvidos pelo /tchau a partir da tabela de perfis do
docs/ROADMAP.md, nunca copiados do ponteiro anterior.

`maquina:` aceita `qualquer` ou o nome da máquina.
-->
