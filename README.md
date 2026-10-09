# TreinoX Web — MVP 0.1.0

## Versão online publicada (demonstração)

- **Site:** https://treinox-web.vercel.app
- **Código da demonstração:** `preview/index.html` (estático, sem credenciais)
- **Exercícios:** 24 GIFs esquemáticos originais gerados via GitHub Actions em `preview/gifs/`.
- **Fluxo:** perfil casa/academia, objetivo, nível, dias, quatro exemplos gratuitos e calendário de quatro semanas.
- **Pagamento:** intencionalmente desativado; nenhum checkout real ocorre na demonstração.
- **QA:** `node preview/test.mjs` e GitHub Actions `TreinoX Preview QA`.

**Atenção:** o projeto React + Cloudflare Worker descrito nas seções abaixo corresponde ao **pacote técnico MVP separado**, ainda não importado integralmente neste repositório. As instruções para Asaas e Cloudflare somente se aplicarão depois que essa base estiver no GitHub. Não use esta prévia para cobrar clientes ou prescrever treinos; GIFs esquemáticos não demonstram com precisão a execução biomecânica.


Sistema web responsivo com **prévia de quatro exercícios gratuita**, questionário de perfil, **24 exercícios animados em GIF original**, programa de **quatro semanas**, registro de progresso e checkout Pix Asaas protegido no servidor.

> **Estado do projeto:** MVP técnico para avaliação. Não realizar vendas reais antes da revisão profissional dos treinos, publicação da política de privacidade adequada, autenticação com recuperação de conta e testes de pagamento em sandbox.

## Requisitos e decisões de arquitetura

- Node.js 22, npm 10.
- React + TypeScript + Vite no frontend, sem segredo no navegador.
- Cloudflare Workers para API e arquivos estáticos; Cloudflare D1 (SQLite gerenciado) para sessões, perfis, pedidos e progresso.
- Pix Asaas: servidor cria cliente/cobrança e entrega QR; apenas webhook **validado** + verificação no Asaas libera o plano.
- GIFs originais em `public/gifs/*.gif`: independência de licença/API externa, sem mensalidade de vídeos no MVP. São **ilustrações esquemáticas** e precisam de revisão técnica antes da comercialização.
- Dados sensíveis: CPF enviado diretamente ao Asaas via backend, **não armazenado** no banco do TreinoX. Preferências de treino armazenadas; nenhum dado médico coletado.
- Sessão: cookie `HttpOnly; SameSite=Lax`, `Secure` no HTTPS; duração de 30 dias. **Limitação atual**: não há recuperação de acesso em outro dispositivo. Implementar autenticação segura antes de vendas reais.

## Estrutura do projeto

```text
treinox-web/
├── .github/workflows/ci.yml       # testes e build em push/PR
├── public/gifs/*.gif              # 24 animações originais
├── shared/
│   ├── catalog.ts                 # biblioteca de exercícios
│   ├── plan.ts                    # motor determinístico de quatro semanas
│   └── validation.ts              # validação de perfil e CPF
├── src/
│   ├── components/ExerciseCard.tsx
│   ├── lib/api.ts                 # chamadas HTTP
│   ├── styles/app.css             # design system responsivo
│   ├── App.tsx                     # fluxo do cliente
│   └── main.tsx
├── worker/
│   ├── index.ts                   # API, autenticação, controle de acesso, Asaas
│   └── schema.sql                 # tabelas e índices D1
├── tests/plan.test.ts             # suíte unitária
├── docs/generate_gifs.py          # gerador das animações autorais
├── wrangler.jsonc                 # configuração Cloudflare
└── .dev.vars.example              # modelo de segredos locais
```

## Teste local (SEM PAGAR)

```bash
npm install
# Linux/macOS:
cp .dev.vars.example .dev.vars
# Windows PowerShell:
# Copy-Item .dev.vars.example .dev.vars
```

Na cópia `.dev.vars`, defina o seguinte para **testar o desbloqueio só em localhost**:

```env
DEV_DEMO_UNLOCK=true
```

Não precisa colocar chaves Asaas para testar o questionário e a demonstração.

```bash
npm run db:migrate:local
npm run dev:full
```

Abra **http://127.0.0.1:8787** no navegador. Responda ao questionário, veja os quatro exercícios gratuitos e clique em **Acessar modo demonstração (sandbox)** para experimentar o programa completo e marcar progresso. O atalho de demonstração é impossível de ativar em domínio público pela regra do backend.

Para desenvolvimento com hot reload, abra `npm run dev` em outro terminal, mantendo o Worker na porta 8787. Se a aplicação não carregar API, use `npm run dev:full`.

## Ativar Pix via Asaas SANDBOX

1. Crie uma conta no ambiente de teste do Asaas e obtenha uma chave **sandbox**.
2. Em `.dev.vars`, configure `ASAAS_API_KEY` e `ASAAS_WEBHOOK_TOKEN` com valores diferentes.
3. Mantenha `ASAAS_ENV` no `wrangler.jsonc` como `sandbox`.
4. Use o checkout para gerar o Pix de teste. Para o webhook chegar ao Asaas será necessário um **endereço HTTPS público de teste** (o Asaas não alcança localhost sem túnel).
5. No painel do Asaas cadastre o webhook apontando para `https://SEU_DOMINIO/api/webhooks/asaas` com o token exato configurado no Worker. Escolha eventos `PAYMENT_RECEIVED` e `PAYMENT_CONFIRMED`.
6. O sistema confirma o ID, valor, referência e situação diretamente na API do Asaas. Ele **não confia** somente na mensagem recebida.

O endpoint de criação de clientes do Asaas exige CPF (11 dígitos) e nome. Nenhuma chave de API deve estar em arquivos enviados ao GitHub.

## Publicar na Cloudflare

Crie um repositório GitHub novo, por exemplo `treinox-web`, e envie apenas o conteúdo deste projeto. **Nunca envie `.dev.vars` ou `.env`**.

```bash
npm install
npx wrangler login
npx wrangler d1 create treinox_db
```

Copie o `database_id` retornado e substitua `00000000-0000-0000-0000-000000000000` em `wrangler.jsonc`.

```bash
npm run db:migrate:remote
npx wrangler secret put ASAAS_API_KEY
npx wrangler secret put ASAAS_WEBHOOK_TOKEN
npm run deploy
```

Primeiro publique **em sandbox**, verifique o webhook por HTTPS e apenas depois altere `ASAAS_ENV` para `production`, troque as chaves pelos segredos de produção e repita os testes (sem habilitar o modo demonstração).

> A hospedagem pode começar no plano gratuito dentro dos limites de uso, mas taxas Asaas e custos de domínio/serviços externos são variáveis. Não há garantia de custo zero com vendas.

## API

| Método | Rota | Finalidade |
|---|---|---|
| GET | `/api/session` | Cria sessão cookie e informa disponibilidade do checkout |
| POST | `/api/profile` | Persiste preferências validadas |
| GET | `/api/plan` | Quatro exercícios gratuitos; semanas completas só para pagos |
| POST | `/api/checkout` | Valida comprador, cria cliente e cobrança Asaas Pix |
| GET | `/api/checkout/status` | Consulta situação registrada de pagamento |
| POST | `/api/webhooks/asaas` | Token de webhook + verificação ativa + idempotência |
| GET/POST | `/api/progress` | Progresso exclusivo para clientes liberados |
| POST | `/api/demo-unlock` | Simula compra apenas sandbox em localhost com flag explícita |
| GET | `/api/health` | Resposta operacional |

## Verificação

```bash
npm run check
npm run build
```

Também teste manualmente: mobile 320 px; desktop; sem internet; pagamentos pendentes; webhook repetido; tentativa de alterar `paid` no frontend; exercício inexistente no progresso; sessão expirada; CPF inválido; comprou e trocou de navegador; tempo de carregamento de GIF em 3G.

## Limitações importantes para resolver antes de comercializar

1. **Revisão por profissional habilitado** dos treinos, GIFs, progressão e critérios de elegibilidade; atualmente são exemplos não-prescritivos.
2. **Identidade e recuperação de conta** (autenticação de e-mail, proteção contra abuso, acesso cross-device e acesso persistente ao programa).
3. **LGPD**: política, retenção/exclusão, base legal, consentimento quando necessário, canal de atendimento.
4. **Observabilidade**: logging sem PII, alertas para falhas do Asaas, métricas básicas, logs de auditoria.
5. **Comercial**: termos, regras de reembolso, validade do produto e emissão fiscal aplicável.
6. **Segurança/abuso**: ativar rate limiting e proteção de bots na Cloudflare, testes e monitoração de webhooks.

### Direitos sobre imagens

Os GIFs deste MVP foram produzidos por código no arquivo `docs/generate_gifs.py`, sem copiar animações de bibliotecas de terceiros. Para usar um catálogo comercial maior, contrate uma licença apropriada ou produza os movimentos com um instrutor.