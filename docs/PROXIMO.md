# Próximo

> Este arquivo é **lido por regex**, não por humano. Uma chave por linha, `chave: valor`, sem
> markdown, sem lista, sem negrito. O que vier depois de `#` é comentário e é ignorado.
>
> Quem lê: o hook de abertura do plugin `playbook` (`sessao-abre.ps1`), e o `/oi` quando não há hook.
> Quem escreve: o `/tchau`, ao avançar o ponteiro, e o `/360`, ao desenhar o roadmap.
>
> **Nenhuma chave existe sem consumidor declarado.** Não invente campo aqui sem dizer quem o lê.

chat: C1 # humano + título da sessão
titulo: Os anúncios no ar # humano
perfil: padrao # /360 e /tchau (política)
modelo: sonnet # hook e /oi conferem contra a sessão
esforco: medium # hook e /oi conferem contra a sessão
forma: sessao # vocabulário aceito: sessao
maquina: qualquer # /oi compara com esta máquina e avisa
plan-mode: nao # /oi imprime "abra com Shift+Tab"
persona: produtor de anúncio que tira do papel dois vídeos curtos da Vesk e põe a campanha no ar, com o teto do Igor e o dado da curva já correndo
objetivo: a C1 do docs/ROADMAP.md. Escrever com o Igor o roteiro dos anúncios A e B (15 a 30 s, a marca em segundos diferentes), a lista de passos da campanha na conta da Vesk na Meta, e conferir os vídeos, o segundo da marca, a campanha no ar com o teto e o primeiro export. Quem grava, cria a campanha e publica é o Igor. A C2 (a vitrine) pode andar junto

<!--
`modelo:` e `esforco:` são SEMPRE re-resolvidos pelo /tchau a partir da tabela de perfis do
docs/ROADMAP.md, nunca copiados do ponteiro anterior.

`maquina:` aceita `qualquer` ou o nome da máquina.
-->
