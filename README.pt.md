# Padrões de Integração para Agentes

> Um catálogo de padrões de integração para sistemas multi-agentes de IA — o vocabulário que faltava entre os Enterprise Integration Patterns e a era agêntica.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Contribuições Bem-vindas](https://img.shields.io/badge/contribuições-bem--vindas-brightgreen.svg)](CONTRIBUTING.md)

**Ler em:** [English 🇺🇸](README.md)

---

## Por que este catálogo existe

Em 2003, Gregor Hohpe e Bobby Woolf publicaram *Enterprise Integration Patterns* — um vocabulário de 65 padrões nomeados que deu aos arquitetos uma linguagem comum para conectar sistemas distribuídos. Esse livro se tornou a base do middleware empresarial, dos message brokers e dos ESBs por mais de duas décadas.

Em 2025, estamos construindo uma nova classe de sistemas distribuídos: **redes de agentes de IA autônomos** que colaboram para resolver tarefas complexas. Esses agentes se comunicam por protocolos como o [Model Context Protocol (MCP)](https://modelcontextprotocol.io) e o [Agent-to-Agent (A2A)](https://a2a-protocol.org), orquestrados por frameworks como LangGraph, AutoGen, CrewAI e Spring AI.

Mas nos falta um vocabulário compartilhado. Times reinventam os mesmos padrões com nomes diferentes. Revisões arquiteturais debatem os mesmos trade-offs sem termos em comum. Papers existem que taxonomizam o espaço (arXiv:2501.06322, arXiv:2502.14321, arXiv:2508.01186), mas param aquém de padrões prescritivos e nomeados — com estrutura de intenção, problema e solução.

**Este repositório preenche essa lacuna.**

Inspirado por:
- Enterprise Integration Patterns (Hohpe & Woolf, 2003)
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) (HumanLayer, 2025)
- Especificação do protocolo A2A (Google)
- Especificação do MCP da Anthropic (v2025-11-25)
- Surveys acadêmicos sobre sistemas multi-agentes com LLMs (2025–2026)

---

## A Base Protocolada

Antes dos padrões, os dois protocolos que definem a superfície de integração dos sistemas agênticos modernos:

### Model Context Protocol (MCP) — Integração Vertical
> *"A porta USB-C para IA"*

O MCP (Anthropic, 2024) é construído sobre JSON-RPC 2.0, inspirado no Language Server Protocol. Ele padroniza como os agentes se conectam **para baixo** — a ferramentas, fontes de dados e recursos.

```
 Agente (Host)
     │
     ▼  MCP (JSON-RPC 2.0)
 ┌─────────┐   ┌──────────┐   ┌──────────┐
 │Ferrament│   │ Recursos │   │ Prompts  │
 └─────────┘   └──────────┘   └──────────┘
```

**O que o MCP oferece:** invocação de ferramentas, acesso a recursos, templates de prompt, sampling.

### Agent-to-Agent (A2A) — Integração Horizontal
> *"O HTTP para agentes"*

O A2A (Google, abril de 2025) permite que agentes descubram e deleguem tarefas a **outros agentes** sem expor estado interno, memória ou ferramentas. A descoberta acontece via **Agent Cards** — manifestos de capacidades servidos em `/.well-known/agent.json`.

```
 Agente A ──── A2A ────► Agente B
              │                 │
         Agent Cards       Agent Cards
         (capacidades)     (capacidades)
```

**O que o A2A oferece:** descoberta de agentes, delegação de tarefas, negociação de capacidades, interoperabilidade entre frameworks.

### O Eixo Complementar

Ambos os protocolos coexistem sob a Agentic AI Foundation (AAIF) da Linux Foundation desde dezembro de 2025. Eles não são concorrentes:

```
             A2A (horizontal — agente-a-agente)
               ◄──────────────────────────────►
     Agente A                              Agente B
        │                                      │
        ▼  MCP (vertical)               MCP  ▼
   Ferramentas/Dados                Ferramentas/Dados
```

> **Nota de segurança:** A combinação de A2A e MCP introduz riscos compostos — ataques de confusão, downgrade e relay-abuse surgem porque os dois protocolos operam sob premissas de confiança diferentes. Veja [Padrões de Segurança](#-padrões-de-segurança). (arXiv:2505.03864, arXiv:2602.11327)

---

## Como Ler os Padrões

Cada padrão segue esta estrutura:

| Campo | Descrição |
|---|---|
| **Intenção** | Propósito em uma frase |
| **Problema** | Quais forças este padrão resolve |
| **Solução** | A abordagem estrutural |
| **Diagrama** | Representação visual |
| **Consequências** | Trade-offs (forças resolvidas vs. introduzidas) |
| **Usos Conhecidos** | Onde aparece em sistemas em produção |
| **Padrões Relacionados** | O que usar antes, depois ou em vez disso |

---

## Catálogo de Padrões

### 📨 Padrões de Mensageria

Regem como agentes trocam informações.

---

#### 1. Mensagem Direta

**Intenção:** Enviar uma tarefa de um agente para exatamente outro por um canal ponto-a-ponto.

**Problema:** Um agente precisa delegar uma subtarefa específica para outro agente com capacidades conhecidas, sem transmitir para todos.

**Solução:** Estabeleça um canal dedicado entre dois agentes. O remetente envia uma mensagem estruturada (tarefa + contexto) para o endpoint do receptor. O receptor confirma o recebimento e retorna um resultado.

```
┌──────────┐    Requisição de Tarefa    ┌──────────┐
│ Agente A │ ─────────────────────────► │ Agente B │
│          │ ◄───────────────────────── │          │
└──────────┘    Resultado da Tarefa     └──────────┘
```

**Consequências:**
- ✅ Simples, previsível, fácil de rastrear
- ✅ Baixa latência — sem intermediários
- ❌ Acoplamento — o remetente precisa conhecer o endereço do receptor
- ❌ Sem balanceamento de carga ou failover sem infraestrutura adicional

**Usos Conhecidos:** Delegação de tarefas via A2A, arestas nó-a-nó no LangGraph, chamadas de ferramentas em agentes ReAct.

**Padrões Relacionados:** [Registro de Agent Cards](#4-registro-de-agent-cards) (para descoberta), [Delegação Supervisionada](#11-delegação-supervisionada) (para confiabilidade).

---

#### 2. Mensagem Broadcast

**Intenção:** Enviar informação de um agente para todos os agentes interessados simultaneamente, sem saber quem são.

**Problema:** Um agente produz informação (uma observação, uma mudança de estado, um resultado de subtarefa) que múltiplos agentes precisam processar.

**Solução:** Publique a mensagem em um canal ou tópico compartilhado. Os agentes interessados se inscrevem e reagem de forma independente. O publicador não tem conhecimento dos assinantes.

```
              ┌──────────┐
              │ Agente A │ (Publicador)
              └────┬─────┘
                   │ publicar("pedido_criado")
        ┌──────────┼──────────┐
        ▼          ▼          ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ Agente B │ │ Agente C │ │ Agente D │
  └──────────┘ └──────────┘ └──────────┘
```

**Consequências:**
- ✅ Desacoplado — o publicador não conhece os assinantes
- ✅ Facilmente extensível — adicione agentes sem modificar o publicador
- ❌ Sem garantia de entrega sem infraestrutura
- ❌ Risco de tempestades de mensagens se assinantes produzem novas mensagens

**Usos Conhecidos:** Fluxos event-driven no CrewAI, broadcasts de group chat no AutoGen, pipelines de agentes sobre Kafka.

**Padrões Relacionados:** [Scatter-Gather](#9-scatter-gather) (quando você precisa de resultados), [Coreografia](#13-coreografia) (coordenação orientada a eventos).

---

#### 3. Quadro-Negro (Blackboard)

**Intenção:** Compartilhar um espaço de contexto mutável e estruturado que múltiplos agentes leem e escrevem de forma assíncrona.

**Problema:** Múltiplos agentes trabalham em partes do mesmo problema. Nenhum agente tem a visão completa, mas todos precisam ler os resultados intermediários dos outros.

**Solução:** Mantenha um "quadro-negro" compartilhado — um armazenamento de chave-valor ou documento estruturado. Agentes leem o estado relevante, contribuem com seus resultados e observam as mudanças. Um controlador opcional monitora o quadro-negro e aciona agentes quando condições relevantes são atendidas.

```
                ┌──────────────┐
                │  Quadro-Negro│
                │  (contexto   │
                │  compartilh.)│
                └──────┬───────┘
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
 ┌──────────┐    ┌──────────┐    ┌──────────┐
 │ Agente A │    │ Agente B │    │ Agente C │
 │(lê/escreve)  │(lê/escreve)  │(lê/escreve)
 └──────────┘    └──────────┘    └──────────┘
```

**Consequências:**
- ✅ Natural para agentes paralelos e fracamente acoplados
- ✅ Agentes contribuem no seu próprio ritmo
- ❌ Requer resolução de conflitos quando agentes escrevem na mesma chave
- ❌ Difícil raciocinar sobre causalidade sem ordenação de eventos

**Usos Conhecidos:** Memória compartilhada no AutoGen, workflows de pesquisa multi-agente com documento compartilhado.

**Padrões Relacionados:** [Injeção de Contexto](#6-injeção-de-contexto) (para contexto somente-leitura), [Orquestrador](#12-orquestrador) (para controle centralizado).

---

### 🗺️ Padrões de Descoberta

Como agentes encontram uns aos outros sem endereços fixos.

---

#### 4. Registro de Agent Cards

**Intenção:** Permitir que agentes anunciem suas capacidades e sejam descobertos por outros agentes em tempo de execução, sem configuração prévia.

**Problema:** Em um sistema multi-agente dinâmico, você não pode fixar no código qual agente trata qual tarefa. Novos agentes entram no sistema, capacidades mudam, e as decisões de roteamento precisam acontecer em tempo de execução.

**Solução:** Cada agente publica um **Agent Card** — um manifesto de capacidades estruturado — em um endpoint bem conhecido (`/.well-known/agent.json`). Um registro (ou descoberta peer-to-peer) indexa esses cards. Agentes consultam o registro pelas capacidades de que precisam e, em seguida, estabelecem conexões diretas.

```
Agent Card:
{
  "name": "AgenteDeExtracao",
  "description": "Extrai dados estruturados de PDFs",
  "skills": [{ "id": "pdf-extract", "name": "Extração de PDF" }],
  "url": "https://agentes.example.com/extrator",
  "authentication": { "schemes": ["bearer"] }
}

  ┌──────────┐  "quem extrai PDFs?"  ┌──────────────────┐
  │ Agente A │ ─────────────────────►│ Registro         │
  │          │ ◄───────────────────── │  (Agent Cards)   │
  └──────────┘  "Agente B consegue"  └──────────────────┘
       │
       │ conecta diretamente
       ▼
  ┌──────────┐
  │ Agente B │
  └──────────┘
```

**Consequências:**
- ✅ Composição dinâmica — agentes entram/saem sem reconfiguração
- ✅ Roteamento baseado em capacidades
- ❌ Registro vira ponto único de falha
- ❌ Cards desatualizados se os agentes não atualizam suas capacidades

**Usos Conhecidos:** Especificação A2A Agent Cards, AWS Bedrock Agent Aliases, catálogo de agentes Azure AI Foundry.

**Padrões Relacionados:** [Roteador por Conteúdo](#8-roteador-por-conteúdo) (roteamento após descoberta), [Proxy de Agente](#5-proxy-de-agente) (camada de abstração).

---

#### 5. Proxy de Agente

**Intenção:** Prover uma interface estável para um agente (ou grupo de agentes), ocultando detalhes de implementação, diferenças de protocolo ou versionamento.

**Problema:** Os consumidores das capacidades de um agente não deveriam precisar saber se o agente é uma única chamada LLM, um subgrafo de agentes, uma API externa ou qual protocolo ele fala.

**Solução:** Introduza um agente proxy que apresenta uma interface uniforme. O proxy traduz protocolos (ex.: A2A ↔ MCP), roteia para os agentes de backend apropriados e gerencia o versionamento.

```
 ┌──────────────┐          ┌──────────────┐
 │ Agente       │  A2A     │   Proxy de   │   A2A/MCP/REST
 │ Consumidor   │ ────────►│   Agente     │ ─────────────►  Backend(s)
 └──────────────┘          └──────────────┘
```

**Consequências:**
- ✅ Desacopla consumidores da implementação
- ✅ Habilita testes A/B e migração gradual
- ❌ Adiciona um hop de rede e latência
- ❌ O proxy vira gargalo se não for stateless

**Usos Conhecidos:** Nós de agente remoto no LangGraph, padrões de API gateway para endpoints de agentes, servidores proxy MCP.

**Padrões Relacionados:** [Registro de Agent Cards](#4-registro-de-agent-cards), [Disjuntor](#16-disjuntor-circuit-breaker).

---

### ⚡ Padrões de Contexto

Como agentes compartilham, injetam e gerenciam informação contextual — inspirados nos primitivos MCP.

---

#### 6. Injeção de Contexto

**Intenção:** Fornecer ao agente contexto externo relevante (documentos, registros de banco, estado do usuário) antes que ele raciocine, sem que o agente precise buscá-lo.

**Problema:** A qualidade do raciocínio de um agente depende do contexto. Exigir que os agentes busquem ativamente cada peça de contexto que precisam é lento, os acopla a fontes de dados e frequentemente ultrapassa os limites da janela de contexto.

**Solução:** Antes de invocar um agente, um host ou orquestrador recupera o contexto relevante das fontes de dados (via MCP Resources) e o injeta no prompt ou mensagem do agente. O agente raciocina sobre o contexto pré-montado.

```
 ┌────────────────────────────────────────┐
 │              Host                      │
 │  ┌──────────┐     ┌─────────────────┐  │
 │  │  MCP     │────►│ Montador de     │  │
 │  │ Resources│     │ Contexto        │  │
 │  └──────────┘     └────────┬────────┘  │
 └───────────────────────────┼────────────┘
                              │ injeta contexto
                              ▼
                        ┌──────────┐
                        │  Agente  │
                        └──────────┘
```

**Consequências:**
- ✅ Agentes permanecem stateless e focados no raciocínio
- ✅ Contexto é controlado e auditável
- ❌ O host precisa saber qual contexto é relevante (qualidade da recuperação importa)
- ❌ Contextos grandes consomem tokens; a recuperação precisa ser precisa

**Usos Conhecidos:** Pipelines RAG, recuperação contextual da Anthropic, MCP Resources no Claude Desktop.

**Padrões Relacionados:** [Quadro-Negro](#3-quadro-negro-blackboard) (contexto mutável compartilhado), [Provedor de Ferramentas](#7-provedor-de-ferramentas) (uso ativo de ferramentas vs. injeção passiva).

---

#### 7. Provedor de Ferramentas

**Intenção:** Expor capacidades (funções, APIs, consultas de dados) para agentes como ferramentas invocáveis através de uma interface padronizada.

**Problema:** Agentes precisam tomar ações no mundo — consultar bancos de dados, chamar APIs, executar código, buscar na web. Codificar essas capacidades fixamente nos agentes os torna frágeis e não reutilizáveis.

**Solução:** Encapsule capacidades como MCP Tools com schemas estruturados. Agentes descobrem as ferramentas disponíveis via o endpoint `tools/list` do MCP e as invocam via `tools/call`. O provedor de ferramentas gerencia a execução e retorna resultados estruturados.

```
 ┌──────────┐  tools/list    ┌──────────────────────────┐
 │  Agente  │ ─────────────► │   Servidor MCP Tools     │
 │          │ ◄───────────── │                          │
 │          │  [lista]       │  ┌────────────────────┐  │
 │          │                │  │ buscar_web()       │  │
 │          │  tools/call    │  │ consultar_banco()  │  │
 │          │ ─────────────► │  │ executar_codigo()  │  │
 │          │ ◄───────────── │  └────────────────────┘  │
 └──────────┘  [resultado]   └──────────────────────────┘
```

**Consequências:**
- ✅ Agentes desacoplados de implementações específicas de ferramentas
- ✅ Ferramentas podem ser versionadas, substituídas ou mockadas de forma independente
- ❌ Schemas de ferramentas precisam ser bem projetados; schemas ruins confundem LLMs
- ❌ Explosão de ferramentas — ferramentas demais degradam o desempenho do agente

**Usos Conhecidos:** MCP Tool Servers, LangChain Tools, OpenAI Function Calling.

**Padrões Relacionados:** [Injeção de Contexto](#6-injeção-de-contexto), [Escopo Mínimo de Ferramentas](#18-escopo-mínimo-de-ferramentas).

---

### 🔀 Padrões de Roteamento

Como as tarefas são distribuídas entre os agentes.

---

#### 8. Roteador por Conteúdo

**Intenção:** Rotear uma tarefa recebida para o agente apropriado com base no conteúdo, tipo ou atributos da própria tarefa.

**Problema:** Um sistema recebe tarefas diversas que requerem agentes especializados diferentes. Um humano (ou chamador) não deveria precisar saber qual agente trata qual tipo de tarefa.

**Solução:** Um agente roteador examina o conteúdo, os metadados ou a intenção de cada tarefa recebida e a encaminha para o agente especialista apropriado. O roteador pode usar classificação de intenção via LLM, correspondência baseada em regras ou similaridade por embeddings.

```
                     ┌──────────────────────────┐
                     │  Agente Roteador         │
   Tarefa Recebida──►│  (classificador LLM ou   │
                     │   motor de regras)       │
                     └──────────┬───────────────┘
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
       ┌──────────┐      ┌──────────┐      ┌──────────┐
       │ Agente   │      │ Agente   │      │ Agente   │
       │ Código   │      │ Pesquisa │      │ Dados    │
       └──────────┘      └──────────┘      └──────────┘
```

**Consequências:**
- ✅ Ponto de entrada único para chamadores
- ✅ Especialistas podem evoluir de forma independente
- ❌ Roteador é gargalo e ponto único de falha
- ❌ Erros de classificação causam roteamento incorreto

**Usos Conhecidos:** Modo Supervisor do AWS Bedrock, arestas condicionais do LangGraph, roteamento semântico no CrewAI.

**Padrões Relacionados:** [Orquestrador](#12-orquestrador) (quando o roteamento é apenas o primeiro passo), [Registro de Agent Cards](#4-registro-de-agent-cards) (roteamento baseado em capacidades).

---

#### 9. Scatter-Gather

**Intenção:** Enviar a mesma tarefa para múltiplos agentes em paralelo e então agregar as respostas em um único resultado coerente.

**Problema:** Questões complexas se beneficiam de múltiplas perspectivas independentes. Consultas sequenciais são lentas. A melhor resposta pode exigir a síntese de saídas diversas.

**Solução:** Um despachante envia a tarefa para N agentes simultaneamente. Cada agente processa de forma independente. Um agregador aguarda as respostas e as sintetiza — por votação, fusão ou um agente de síntese.

```
                ┌──────────┐
                │Despachante│
                └────┬──────┘
     ┌───────────────┼───────────────┐
     ▼               ▼               ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Agente A │   │ Agente B │   │ Agente C │
└────┬─────┘   └────┬─────┘   └────┬─────┘
     └───────────────┼───────────────┘
                     ▼
               ┌──────────┐
               │ Agregador│
               └──────────┘
```

**Consequências:**
- ✅ Execução paralela reduz latência vs. sequencial
- ✅ Múltiplas perspectivas melhoram qualidade
- ❌ N× custo de tokens
- ❌ A agregação é não-trivial; requer uma etapa de síntese

**Usos Conhecidos:** Debate multi-agente (Google DeepMind), chamadas de ferramentas paralelas, avaliação ensemble de agentes.

**Padrões Relacionados:** [Orquestrador](#12-orquestrador) (coordena o scatter-gather), [Mensagem Broadcast](#2-mensagem-broadcast) (quando você não precisa de resultados).

---

#### 10. Pipeline

**Intenção:** Passar uma tarefa por uma sequência de agentes, onde cada agente transforma ou enriquece o resultado antes de passá-lo para o próximo.

**Problema:** Uma tarefa complexa requer uma série de transformações — cada etapa depende do resultado anterior.

**Solução:** Encadeie agentes como estágios de pipeline. A saída do agente N torna-se a entrada do agente N+1. Cada agente tem uma responsabilidade focada.

```
 Entrada ─► Agente A ─► Agente B ─► Agente C ─► Saída
            (Planejar) (Executar)  (Verificar)
```

**Consequências:**
- ✅ Separação clara de responsabilidades; cada agente é testável de forma isolada
- ✅ Fácil inserir, remover ou substituir estágios
- ❌ Sequencial — latência total = soma de todos os estágios
- ❌ Erros iniciais propagam por todos os estágios subsequentes

**Usos Conhecidos:** Grafos lineares no LangGraph, processo sequencial do CrewAI, workflow de "encadeamento de prompts" da Anthropic.

**Padrões Relacionados:** [Scatter-Gather](#9-scatter-gather) (paralelizar estágios independentes), [Checkpoint e Retomada](#17-checkpoint-e-retomada) (para pipelines longos).

---

### 🎭 Padrões de Coordenação

Como múltiplos agentes decidem quem faz o quê.

---

#### 11. Delegação Supervisionada

**Intenção:** Um agente supervisor decompõe um objetivo em subtarefas, delega cada uma a um agente especialista, monitora a execução e intervém em caso de falha.

**Problema:** Objetivos complexos excedem a capacidade de qualquer agente único. As tarefas precisam ser distribuídas, mas o objetivo geral deve permanecer coerente e as falhas precisam ser tratadas.

**Solução:** O supervisor mantém o plano de alto nível, atribui tarefas a agentes trabalhadores (via Mensagem Direta ou A2A), monitora o progresso e faz retry, reatribui ou escalona em caso de falha. O supervisor nunca executa tarefas de domínio por conta própria — ele apenas coordena.

```
                ┌────────────────┐
                │  Agente        │
                │  Supervisor    │
                └──┬─────────────┘
      ┌────────────┼────────────┐
      ▼            ▼            ▼
 ┌──────────┐  ┌──────────┐  ┌──────────┐
 │Trabalhad.│  │Trabalhad.│  │Trabalhad.│
 │    A     │  │    B     │  │    C     │
 └──────────┘  └──────────┘  └──────────┘
```

**Consequências:**
- ✅ Responsabilidade clara; o supervisor é dono do objetivo
- ✅ Tolerância a falhas — o supervisor pode fazer retry ou reatribuir
- ❌ O supervisor é gargalo
- ❌ A qualidade do supervisor determina a qualidade geral

**Usos Conhecidos:** Multi-Agent Supervisor do AWS Bedrock, GroupChatManager do AutoGen, padrão supervisor do LangGraph.

**Padrões Relacionados:** [Orquestrador](#12-orquestrador) (mais leve, sem loop de monitoramento), [Disjuntor](#16-disjuntor-circuit-breaker) (para falhas de trabalhadores).

---

#### 12. Orquestrador

**Intenção:** Um coordenador central define o fluxo de execução, sequencia chamadas de agentes e gerencia o estado — sem monitorar agentes individuais em tempo de execução.

**Problema:** Um workflow requer a coordenação de múltiplos agentes em uma sequência definida, mas você precisa de um único lugar que defina o plano de execução e mantenha o estado compartilhado.

**Solução:** O orquestrador mantém o grafo do workflow. Ele chama agentes em sequência ou em paralelo de acordo com o plano, passa o estado entre as etapas e trata a lógica de bifurcação. Diferente de um supervisor, ele segue um plano pré-definido em vez de decidir dinamicamente com base em monitoramento.

```
 ┌────────────────────────────────────────────┐
 │           Orquestrador                     │
 │                                            │
 │  passo1 ──► passo2 ──► passo3 ──► fim    │
 │    │            │           │             │
 │    ▼            ▼           ▼             │
 │  Agente A   Agente B    Agente C          │
 └────────────────────────────────────────────┘
```

**Consequências:**
- ✅ Execução previsível; fácil de auditar e testar
- ✅ Gerenciamento de estado centralizado
- ❌ O orquestrador precisa ser atualizado quando o workflow muda
- ❌ Menos adaptável que a coreografia para cenários dinâmicos

**Usos Conhecidos:** StateGraph do LangGraph, planejadores do Semantic Kernel (Azure), padrão "orquestrador-subagentes" da Anthropic.

**Padrões Relacionados:** [Coreografia](#13-coreografia) (alternativa descentralizada), [Delegação Supervisionada](#11-delegação-supervisionada) (quando monitoramento é necessário).

---

#### 13. Coreografia

**Intenção:** Agentes coordenam por meio de eventos sem um controlador central — cada agente sabe o que fazer ao receber um evento específico.

**Problema:** A orquestração centralizada cria gargalos e pontos únicos de falha. Em sistemas de alta escala ou altamente dinâmicos, você precisa que os agentes se coordenem sem depender de um coordenador.

**Solução:** Cada agente assina eventos relevantes para seu papel e publica eventos quando conclui. Nenhum agente conhece o fluxo global — cada um conhece apenas seus gatilhos e saídas. O workflow emerge da interação de agentes localmente racionais.

```
  [tarefa_criada] ──► Agente A ──► [dados_extraídos]
                                          │
                      [dados_extraídos] ──► Agente B ──► [analisado]
                                                              │
                                          [analisado] ──► Agente C ──► [concluído]
```

**Consequências:**
- ✅ Altamente desacoplado — agentes podem ser desenvolvidos e implantados de forma independente
- ✅ Sem ponto único de falha
- ❌ O fluxo global é implícito; difícil entender e depurar
- ❌ Transações distribuídas e compensações são complexas

**Usos Conhecidos:** Pipelines de agentes sobre Kafka, processo event-driven do CrewAI, padrões saga em agentes.

**Padrões Relacionados:** [Orquestrador](#12-orquestrador) (alternativa centralizada), [Agente de Carta Morta](#15-agente-de-carta-morta) (para eventos não tratados).

---

#### 14. Delegação Peer-to-Peer (A2A)

**Intenção:** Um agente delega diretamente uma subtarefa a outro agente por meio de um canal de capacidade negociada, sem envolver um coordenador central.

**Problema:** Um agente descobre durante a execução que uma subtarefa requer capacidades que ele não possui. Ele precisa encontrar e delegar para um par capaz sem envolver um supervisor.

**Solução:** Usando a descoberta por Agent Cards, o agente identifica um par com a capacidade necessária, estabelece um canal A2A, envia a tarefa e aguarda o resultado. O agente delegante retoma quando o resultado é recebido.

```
 ┌──────────┐              ┌──────────────────┐
 │ Agente A │  1. Descobrir│ Registro         │
 │ (precisa │ ────────────►│ (Agent Cards)    │
 │ OCR PDF) │ ◄──────────  └──────────────────┘
 │          │  2. "Agente B tem habilidade pdf-ocr"
 │          │
 │          │  3. Requisição de Tarefa A2A
 │          │ ───────────────────────────────────► Agente B
 │          │ ◄─────────────────────────────────── (OCR PDF)
 │          │  4. Resultado da Tarefa A2A
 └──────────┘
```

**Consequências:**
- ✅ Sem coordenador; escala horizontalmente
- ✅ Agentes permanecem autônomos; podem delegar dinamicamente
- ❌ Overhead de descoberta por delegação
- ❌ Confiança precisa ser estabelecida entre cada par de agentes

**Usos Conhecidos:** Protocolo A2A do Google, fluxos multi-agente do Salesforce Agentforce.

**Padrões Relacionados:** [Registro de Agent Cards](#4-registro-de-agent-cards), [Delegação Supervisionada](#11-delegação-supervisionada) (quando um supervisor deve controlar a delegação).

---

### 🛡️ Padrões de Resiliência

Como sistemas agênticos falham de forma controlada e se recuperam.

---

#### 15. Agente de Carta Morta

**Intenção:** Rotear tarefas que não podem ser processadas (falhas, sem rota ou com timeout) para um agente dedicado ou humano para inspeção e resolução.

**Problema:** Em qualquer sistema distribuído, algumas mensagens não podem ser processadas. Sem uma rede de segurança, tarefas com falha são descartadas silenciosamente.

**Solução:** Qualquer tarefa não processável é encaminhada para um Agente de Carta Morta — tipicamente uma interface de humano-no-loop, um sistema de alertas ou uma fila para revisão manual. O agente de carta morta registra a falha, notifica os operadores e opcionalmente habilita o reprocessamento.

```
 ┌──────────┐  falha      ┌────────────────────┐
 │ Agente A │ ──────────► │ Agente de Carta    │
 └──────────┘             │ Morta              │
                          │                    │
                          │ ┌────────────────┐ │
                          │ │ Revisão humana │ │
                          │ │ / alerta       │ │
                          │ └────────────────┘ │
                          └────────────────────┘
```

**Consequências:**
- ✅ Sem perda silenciosa de dados
- ✅ Rede de segurança com humano-no-loop
- ❌ Requer monitoramento e atenção humana
- ❌ Volume de carta morta é um sinal de saúde do sistema

**Usos Conhecidos:** Padrões HITL no cookbook de agentes da Anthropic, interrupt/resume no LangGraph, ferramenta de input humano do CrewAI.

**Padrões Relacionados:** [Disjuntor](#16-disjuntor-circuit-breaker) (prevenir falhas em cascata), [Checkpoint e Retomada](#17-checkpoint-e-retomada) (retry a partir do último estado conhecido).

---

#### 16. Disjuntor (Circuit Breaker)

**Intenção:** Parar de fazer chamadas para um agente ou ferramenta com falha, dar tempo para recuperação e retomar automaticamente quando ficar saudável.

**Problema:** Quando uma dependência de agente ou ferramenta falha, retries contínuos amplificam a carga, causam falhas em cascata e consomem recursos sem produzir resultados.

**Solução:** Envolva chamadas a agentes/ferramentas externos com um disjuntor. Após N falhas consecutivas, o circuito abre — todas as chamadas subsequentes falham rápido sem tentar a chamada downstream. Após um timeout, uma chamada de sonda testa a recuperação. Com sucesso, o circuito fecha.

```
              ┌──────────────────┐
   chamada──► │  Disjuntor       │
              │                  │
              │  FECHADO: passa  │──► Agente B (saudável)
              │  ABERTO: falha   │──► Erro (rápido)
              │  MEIO: sonda     │──► Agente B (testando)
              └──────────────────┘
```

**Consequências:**
- ✅ Previne falhas em cascata
- ✅ Falha rápida dá aos chamadores chance de tentar alternativas
- ❌ Requer ajuste de limiares e timeouts de recuperação
- ❌ Falsos positivos podem bloquear agentes saudáveis temporariamente

**Usos Conhecidos:** Padrões de resiliência do Spring AI, RetryWithError do LangChain, políticas de retry do Temporal.

**Padrões Relacionados:** [Proxy de Agente](#5-proxy-de-agente) (disjuntor frequentemente implementado no proxy), [Agente de Carta Morta](#15-agente-de-carta-morta) (rotear falhas).

---

#### 17. Checkpoint e Retomada

**Intenção:** Persistir o estado intermediário do agente para que tarefas de longa duração possam ser pausadas e retomadas sem reiniciar do zero.

**Problema:** Workflows longos de agentes levam minutos ou horas. Falhas de rede, limites de janela de contexto, restrições de custo ou requisitos de revisão humana podem interromper a execução. Reiniciar do zero é caro e pode produzir resultados inconsistentes.

**Solução:** Após cada etapa significativa, serializar e persistir o estado do agente (memória, progresso da tarefa, contexto acumulado). Em caso de falha ou interrupção, carregar o último checkpoint e retomar a partir desse ponto.

```
 Passo 1 ──► [Checkpoint] ──► Passo 2 ──► [Checkpoint] ──► Passo 3
                                                   ↑
                                        (retomar aqui em falha)
```

**Consequências:**
- ✅ Sobrevive a falhas; habilita tarefas de longo horizonte
- ✅ Habilita revisão humana em checkpoints
- ❌ Complexidade de armazenamento de checkpoint e versionamento de schema
- ❌ Operações não-idempotentes podem produzir duplicatas ao retomar

**Usos Conhecidos:** Persistência/memória do LangGraph (checkpointers SQLite/Postgres), AWS Step Functions para workflows de agentes, princípio "Seja dono do seu fluxo de controle" do 12-factor-agents.

**Padrões Relacionados:** [Agente Idempotente](#agente-idempotente), [Agente de Carta Morta](#15-agente-de-carta-morta).

---

### 🔐 Padrões de Segurança

Como estabelecer confiança, limitar o raio de explosão e detectar ataques em redes de agentes.

---

#### 18. Escopo Mínimo de Ferramentas

**Intenção:** Conceder a cada agente acesso apenas ao conjunto mínimo de ferramentas e recursos que ele precisa para concluir sua tarefa.

**Problema:** Agentes com acesso a ferramentas poderosas (execução de código, escritas em banco, APIs externas) podem causar danos irreversíveis por injeção de prompt, má configuração ou bugs.

**Solução:** Defina escopos de ferramentas no nível do servidor MCP. Cada agente recebe uma conexão a um servidor MCP configurado apenas com as ferramentas relevantes para seu papel. O escopo é aplicado na camada MCP, não no prompt do agente.

```
 ┌─────────────────────┐        ┌────────────────────────────────────┐
 │  Agente de Pesquisa │──MCP──►│ Servidor MCP (escopo somente-leit.)│
 └─────────────────────┘        │  - buscar_web()                    │
                                │  - ler_documento()                 │
                                └────────────────────────────────────┘

 ┌─────────────────────┐        ┌────────────────────────────────────┐
 │  Agente de Execução │──MCP──►│ Servidor MCP (escopo de escrita)   │
 └─────────────────────┘        │  - escrever_arquivo()              │
                                │  - executar_codigo()               │
                                └────────────────────────────────────┘
```

**Consequências:**
- ✅ Limita o raio de explosão de agentes comprometidos ou confusos
- ✅ Auditável: o acesso a ferramentas é declarado, não emergente
- ❌ Requer design antecipado de escopo de ferramentas por papel de agente
- ❌ Escopos excessivamente restritivos bloqueiam ações legítimas do agente

**Usos Conhecidos:** Modelo de permissão MCP do Claude, IAM AWS para papéis de agentes, orientação da Anthropic sobre footprint mínimo.

**Padrões Relacionados:** [Fronteira de Confiança](#19-fronteira-de-confiança).

---

#### 19. Fronteira de Confiança

**Intenção:** Definir explicitamente quais agentes confiam em quais outros agentes, e em que nível, prevenindo delegação de tarefas ou acesso a dados não autorizados.

**Problema:** Em um sistema multi-agente usando A2A, um atacante (ou agente comprometido) pode tentar se passar por um agente confiável ou injetar tarefas maliciosas por canais agente-a-agente.

**Solução:** Defina camadas de confiança explicitamente. Agentes verificam a identidade dos chamadores via autenticação de Agent Card (OAuth/bearer tokens) antes de aceitar tarefas. Agentes internos que se chamam estão em uma zona de confiança mais alta do que agentes voltados para o exterior.

```
 ┌──────────────────────────────────────────────────────────┐
 │  ZONA NÃO CONFIÁVEL                                      │
 │  Requisições externas ──────────────────────────────     │
 │                      ▼                                  │
 │  ┌─────────────────────────────────────────────────────┐ │
 │  │  ZONA DE GATEWAY (A2A autenticado)                  │ │
 │  │  Agente Gateway ────────────────────────────        │ │
 │  │               ▼                                    │ │
 │  │  ┌─────────────────────────────────────────────┐   │ │
 │  │  │  ZONA CONFIÁVEL (agentes internos)          │   │ │
 │  │  │  Agente A ◄──── Agente B                   │   │ │
 │  │  └─────────────────────────────────────────────┘   │ │
 │  └─────────────────────────────────────────────────────┘ │
 └──────────────────────────────────────────────────────────┘
```

**Consequências:**
- ✅ Defesa em profundidade — perímetro + níveis de confiança internos
- ✅ Limita movimento lateral em caso de comprometimento
- ❌ Decisões de confiança precisam ser atualizadas conforme o sistema evolui
- ❌ Zonas de confiança interna excessivamente estritas atrasam a colaboração legítima

**Usos Conhecidos:** Autenticação A2A via Agent Cards, padrões de segurança de mesh empresarial para agentes.

**Padrões Relacionados:** [Escopo Mínimo de Ferramentas](#18-escopo-mínimo-de-ferramentas), [Proxy de Agente](#5-proxy-de-agente) (papel de gateway).

---

#### 20. Firewall de Prompt

**Intenção:** Inspecionar e sanitizar o conteúdo que flui para o contexto do agente para prevenir ataques de injeção de prompt de fontes de dados externas.

**Problema:** Quando agentes processam conteúdo externo (páginas web, documentos de usuário, respostas de API), adversários podem incorporar instruções nesse conteúdo para sequestrar o comportamento do agente — um ataque de injeção de prompt.

**Solução:** Insira uma camada de firewall entre fontes de dados externas e o contexto do agente. O firewall usa um LLM separado e restrito (ou filtro baseado em regras) para identificar e neutralizar instruções incorporadas antes que o conteúdo alcance o agente principal.

```
 Dados Externos ──► [Firewall de Prompt] ──► Contexto do Agente
   (não confiável)    (sanitizar/sinalizar)   (entrada confiável)
```

**Consequências:**
- ✅ Reduz risco de injeção de prompt de conteúdo externo
- ✅ Pode ser ajustado de forma independente da lógica do agente
- ❌ O firewall em si pode ser contornado; não é uma solução completa
- ❌ Filtragem excessivamente agressiva pode remover conteúdo legítimo

**Usos Conhecidos:** Guardrails da Invariant Labs, NeMo Guardrails, LlamaGuard para pipelines de agentes.

**Padrões Relacionados:** [Escopo Mínimo de Ferramentas](#18-escopo-mínimo-de-ferramentas), [Fronteira de Confiança](#19-fronteira-de-confiança).

---

## Mapa de Padrões

```
                    PADRÕES DE INTEGRAÇÃO PARA AGENTES
                    ════════════════════════════════════

  MENSAGERIA             DESCOBERTA           CONTEXTO
  ──────────             ──────────           ────────
  1. Mensagem Direta     4. Registro de       6. Injeção de Contexto
  2. Broadcast              Agent Cards       7. Provedor de Ferramentas
  3. Quadro-Negro        5. Proxy de Agente

  ROTEAMENTO             COORDENAÇÃO          RESILIÊNCIA
  ──────────             ───────────          ───────────
  8.  Roteador           11. Delegação        15. Agente de Carta Morta
      por Conteúdo           Supervisionada   16. Disjuntor
  9.  Scatter-Gather     12. Orquestrador     17. Checkpoint e Retomada
  10. Pipeline           13. Coreografia
                         14. Delegação P2P    SEGURANÇA
                                              ─────────
                                              18. Escopo Mínimo de
                                                  Ferramentas
                                              19. Fronteira de Confiança
                                              20. Firewall de Prompt
```

---

## Relação com Enterprise Integration Patterns

| Padrão EIP | Análogo em Agentes | Observações |
|---|---|---|
| Message Channel | Mensagem Direta (canal A2A) | 1:1 |
| Publish-Subscribe | Mensagem Broadcast | 1:N |
| Shared Database | Quadro-Negro | Agentes em vez de aplicações |
| Message Router | Roteador por Conteúdo | Classificação via LLM |
| Scatter-Gather | Scatter-Gather | Mapeamento direto |
| Pipes and Filters | Pipeline | Agentes como filtros |
| Process Manager | Orquestrador | Máquina de estado explícita |
| Event-Driven Consumer | Coreografia | Agentes reagem a eventos |
| Dead Letter Channel | Agente de Carta Morta | HITL como o "canal" |
| Message Endpoint | Agent Card | Manifesto de capacidades |
| Circuit Breaker | Disjuntor | Mapeamento direto |

**O que é novo (sem análogo EIP):**
- Injeção de Contexto — gerenciamento de contexto de prompt é único aos LLMs
- Provedor de Ferramentas — o protocolo de ferramentas do MCP não tem análogo EIP
- Delegação Supervisionada — hierarquias recursivas de agentes
- Firewall de Prompt — ataques de injeção são específicos de agentes
- Fronteira de Confiança — o modelo de confiança dividido A2A/MCP é novo
- Checkpoint e Retomada — gerenciamento de janela de contexto

---

## A Lacuna na Literatura

Este catálogo aborda uma lacuna confirmada pela literatura acadêmica de surveys (junho de 2026):

> *"Nenhum trabalho único ainda fornece um catálogo abrangente de padrões de integração para agentes baseados em LLM no nível de especificidade e prescritibilidade do livro Enterprise Integration Patterns."*
>
> — Síntese de pesquisa sobre arXiv:2501.06322, arXiv:2502.14321, arXiv:2508.01186, arXiv:2604.02369

Os trabalhos mais próximos:
- **arXiv:2501.06322** — taxonomia 5 dimensões (atores, tipos, estruturas, estratégias, protocolos) — descritiva, não prescritiva
- **arXiv:2502.14321** — survey de paradigmas de comunicação (passagem de mensagens, ato de fala, quadro-negro)
- **arXiv:2508.01186** — classificação de workflow 2 eixos (IEEE ICAIBD 2025)
- **arXiv:2604.02369** — análise de lacunas de protocolos em 18 protocolos de agentes
- **12-Factor Agents** (HumanLayer) — princípios operacionais, não padrões de integração

---

## Recursos Relacionados

### Protocolos
- [A2A Protocol](https://a2a-protocol.org) — Especificação Agent-to-Agent
- [Model Context Protocol](https://modelcontextprotocol.io) — Spec MCP da Anthropic (v2025-11-25)
- [Agentic AI Foundation (AAIF)](https://linuxfoundation.org) — Linux Foundation, ambos os protocolos

### Frameworks
- [LangGraph](https://github.com/langchain-ai/langgraph) — Orquestração stateful de agentes
- [AutoGen](https://github.com/microsoft/autogen) — Framework multi-agente da Microsoft
- [CrewAI](https://github.com/crewAIInc/crewAI) — Coordenação de agentes baseada em papéis
- [Spring AI](https://spring.io/projects/spring-ai) — Framework de agentes Java empresarial
- [Google ADK](https://google.github.io/adk-docs/) — Agent Development Kit

### Papers Acadêmicos
- [arXiv:2502.14321](https://arxiv.org/abs/2502.14321) — Survey centrado em comunicação de sistemas multi-agentes baseados em LLM
- [arXiv:2501.06322](https://arxiv.org/abs/2501.06322) — Survey de mecanismos de colaboração multi-agente
- [arXiv:2508.01186](https://arxiv.org/abs/2508.01186) — Survey sobre workflow de agentes (IEEE ICAIBD 2025)
- [arXiv:2505.03864](https://arxiv.org/abs/2505.03864) — De Glue-Code a Protocolos (segurança A2A+MCP)
- [arXiv:2604.02369](https://arxiv.org/pdf/2604.02369) — Análise de lacunas de protocolos em 18 protocolos de agentes

### Arte Anterior
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com) — Hohpe & Woolf (2003)
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) — HumanLayer (2025)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (2024)
- [Choosing the Right Multi-Agent Architecture](https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture) — LangChain

---

## Contribuindo

Este é um catálogo vivo. Os padrões evoluem conforme o campo avança.

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes sobre:
- Propor novos padrões
- Questionar padrões existentes
- Adicionar usos conhecidos e exemplos de implementação
- Traduzir para outros idiomas

---

## Licença

[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

Você é livre para compartilhar e adaptar este material para qualquer finalidade, desde que dê o crédito apropriado.

---

*Mantido pela comunidade. Não afiliado à Anthropic, Google ou HumanLayer.*
