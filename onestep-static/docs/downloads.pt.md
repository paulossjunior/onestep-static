# Downloads de Dados

Esta página fornece acesso a todos os arquivos de dados de pesquisa em formato JSON. Estes conjuntos de dados contêm informações abrangentes sobre projetos de pesquisa, bolsas, estudantes, orientadores e redes de colaboração no Campus Serra.

---

## Conjuntos de Dados Disponíveis

### 📊 Projetos de Pesquisa
**Arquivo:** [research_projects.json](data/research_projects.json)  
**Formato:** JSON  
**Descrição:** Base de dados completa de projetos de pesquisa do Campus Serra.

**Contém:**
- Identificação do projeto (ID, título)
- Cronograma (data de início, data de término)
- Coordenador e pesquisadores
- Estudantes envolvidos
- Grupo de pesquisa e área do conhecimento
- Linha de pesquisa e natureza
- Organizações parceiras
- Informações de financiamento
- Contagem de publicações
- Palavras-chave

**Casos de uso:**
- Analisar tendências de pesquisa ao longo do tempo
- Identificar padrões de colaboração
- Acompanhar resultados de projetos
- Estudar distribuição de financiamento

---

### 🎓 Bolsas de IC
**Arquivo:** [scholarships.json](data/scholarships.json)  
**Formato:** JSON  
**Descrição:** Base de dados de bolsas de Iniciação Científica (IC) concedidas a estudantes.

**Contém:**
- Informações do estudante (nome, email, curso)
- Detalhes do orientador
- Programa e modalidade da bolsa (remunerada/voluntária)
- Título do projeto e área de pesquisa
- Período (data de início, data de término, ano)
- Agência de fomento e valor
- Campus de execução
- Status (cancelada, aceita)

**Casos de uso:**
- Acompanhar participação de estudantes em pesquisa
- Analisar fontes e valores de financiamento
- Estudar padrões de distribuição de bolsas
- Identificar relações orientador-estudante

---

### 👥 Estudantes
**Arquivo:** [students.json](data/students.json)  
**Formato:** JSON  
**Descrição:** Dados agregados sobre atividades de pesquisa dos estudantes.

**Contém:**
- Identificação do estudante (nome, email, campus)
- Projetos de pesquisa participados
- Bolsas de IC recebidas
- Orientadores com quem trabalhou
- Colaborações com outros estudantes
- Estatísticas (total de projetos, bolsas, anos ativos)
- Linha do tempo de atividades

**Casos de uso:**
- Analisar engajamento de estudantes em pesquisa
- Acompanhar progressão de carreira de estudantes
- Identificar estudantes altamente engajados
- Estudar redes de colaboração

---

### 👨‍🏫 Orientadores
**Arquivo:** [supervisors.json](data/supervisors.json)  
**Formato:** JSON  
**Descrição:** Dados agregados sobre atividades de pesquisa dos orientadores.

**Contém:**
- Identificação do orientador (nome, email, campus)
- Projetos de pesquisa coordenados
- Bolsas de IC orientadas
- Estudantes orientados
- Colaborações com outros orientadores
- Estatísticas (total de projetos, orientações, anos ativos)
- Áreas de pesquisa e grupos

**Casos de uso:**
- Analisar produtividade de orientadores
- Identificar líderes de pesquisa
- Estudar padrões de orientação
- Acompanhar atividades de grupos de pesquisa

---

### 🔬 Grupos de Pesquisa
**Arquivo:** [research_group.json](data/research_group.json)  
**Formato:** JSON  
**Descrição:** Informações sobre grupos de pesquisa e suas atividades.

**Contém:**
- Identificação e descrição do grupo
- Projetos associados
- Membros e líderes
- Linhas de pesquisa
- Áreas do conhecimento
- Localização do campus

**Casos de uso:**
- Mapear estrutura de grupos de pesquisa
- Analisar produtividade de grupos
- Estudar colaborações interdisciplinares
- Acompanhar áreas de foco de pesquisa

---

### 🤝 Análise de Parcerias
**Arquivo:** [partnership_analysis.json](data/partnership_analysis.json)  
**Formato:** JSON  
**Descrição:** Análise de parcerias externas e colaborações.

**Contém:**
- Organizações parceiras e seus projetos
- Grupos de pesquisa externos
- Estatísticas de colaboração
- Distribuição de parcerias
- Contagem de projetos por parceiro

**Casos de uso:**
- Identificar parceiros externos principais
- Analisar padrões de colaboração
- Estudar conexões indústria-academia
- Acompanhar evolução de parcerias

---

### 🌐 Estatísticas de Rede
**Arquivo:** [network_stats.json](data/network_stats.json)  
**Formato:** JSON  
**Descrição:** Métricas e estatísticas de análise de rede.

**Contém:**
- Métricas de rede de colaboração
- Medidas de centralidade
- Resultados de detecção de comunidades
- Densidade e conectividade da rede
- Nós e hubs principais

**Casos de uso:**
- Analisar redes de colaboração
- Identificar hubs de pesquisa
- Estudar fluxo de conhecimento
- Detectar comunidades de pesquisa

---

## Formato dos Dados

Todos os arquivos estão em formato **JSON (JavaScript Object Notation)**, que é:
- ✅ Legível por humanos e analisável por máquinas
- ✅ Compatível com a maioria das linguagens de programação
- ✅ Fácil de importar em ferramentas de análise de dados
- ✅ Estruturado e hierárquico

### Exemplo de Estrutura

```json
{
  "metadata": {
    "generated_at": "2025-11-22T10:30:00",
    "total_records": 100,
    "source": "Campus Serra"
  },
  "data": [
    {
      "id": "123",
      "name": "Exemplo",
      "details": {...}
    }
  ]
}
```

---

## Como Usar

### Exemplo em Python
```python
import json

# Carregar dados
with open('research_projects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Acessar projetos
projects = data['projects']
for project in projects:
    print(project['title'])
```

### Exemplo em JavaScript
```javascript
// Carregar dados
fetch('research_projects.json')
  .then(response => response.json())
  .then(data => {
    // Acessar projetos
    const projects = data.projects;
    projects.forEach(project => {
      console.log(project.title);
    });
  });
```

### Exemplo em R
```r
library(jsonlite)

# Carregar dados
data <- fromJSON('research_projects.json')

# Acessar projetos
projects <- data$projects
head(projects)
```

---

## Atualizações dos Dados

{% set current_date = get_current_date() %}

**Última Atualização:** {{ current_date['date_str'] }}

Os conjuntos de dados são atualizados automaticamente quando:
- Novos projetos de pesquisa são registrados
- Bolsas são concedidas ou modificadas
- Informações de estudantes ou orientadores mudam
- Análise de rede é recalculada

---

## Licença e Uso

**Termos de Uso:**
- ✅ Livre para uso acadêmico e de pesquisa
- ✅ Atribuição necessária ao publicar resultados
- ✅ Sem uso comercial sem permissão
- ✅ Dados fornecidos "como estão" sem garantias

**Citação:**
```
Dados de Pesquisa do Campus Serra (2025). 
Instituto Federal do Espírito Santo - Campus Serra.
Disponível em: [URL]
```

---

## Suporte

Para dúvidas, problemas ou solicitações de dados:
- 📧 Contato: [research@serra.ifes.edu.br](mailto:research@serra.ifes.edu.br)
- 🐛 Reportar problemas: [GitHub Issues](https://github.com/your-repo/issues)
- 📖 Documentação: [Documentação Completa](index.md)

---

## Baixar Todos

**Links Rápidos de Download:**

| Arquivo | Tamanho | Registros | Download |
|---------|---------|-----------|----------|
| research_projects.json | ~500 KB | ~300 projetos | [⬇️ Download](data/research_projects.json) |
| scholarships.json | ~800 KB | ~1000 bolsas | [⬇️ Download](data/scholarships.json) |
| students.json | ~600 KB | ~500 estudantes | [⬇️ Download](data/students.json) |
| supervisors.json | ~400 KB | ~150 orientadores | [⬇️ Download](data/supervisors.json) |
| research_group.json | ~100 KB | ~30 grupos | [⬇️ Download](data/research_group.json) |
| partnership_analysis.json | ~200 KB | Dados de análise | [⬇️ Download](data/partnership_analysis.json) |
| network_stats.json | ~150 KB | Métricas de rede | [⬇️ Download](data/network_stats.json) |

---

<div style="background-color: #e7f5ff; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #1971c2;">
  <h3 style="margin-top: 0;">💡 Dicas para Análise de Dados</h3>
  <ul>
    <li><strong>Comece com metadados:</strong> Verifique a seção de metadados em cada arquivo para contexto</li>
    <li><strong>Valide dados:</strong> Sempre valide tipos de dados e trate valores ausentes</li>
    <li><strong>Junte conjuntos de dados:</strong> Use IDs para juntar conjuntos relacionados (ex: ID do estudante, ID do projeto)</li>
    <li><strong>Séries temporais:</strong> Use campos de data para análise temporal</li>
    <li><strong>Análise de rede:</strong> Combine estudantes, orientadores e projetos para gráficos de rede</li>
  </ul>
</div>
