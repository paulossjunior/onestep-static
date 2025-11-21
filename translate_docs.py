#!/usr/bin/env python3
"""Script to translate key terms in Portuguese documentation files."""

import re

# Translation dictionary for research_projects
translations_projects = {
    # Chart titles and labels
    "title: 'Year'": "title: 'Ano'",
    "title: 'Count'": "title: 'Contagem'",
    "title: 'Number of Projects per Student'": "title: 'Número de Projetos por Estudante'",
    "title: 'Number of Students'": "title: 'Número de Estudantes'",
    "title: 'Expected Completion Year'": "title: 'Ano de Conclusão Esperado'",
    
    # Legend and labels
    "name: 'All Students'": "name: 'Todos os Estudantes'",
    "name: 'With Funding'": "name: 'Com Financiamento'",
    "name: 'Without Funding'": "name: 'Sem Financiamento'",
    "name: 'Completed'": "name: 'Concluídos'",
    "name: 'Ongoing'": "name: 'Em Andamento'",
    "name: 'With Research Group'": "name: 'Com Grupo de Pesquisa'",
    "name: 'Without Research Group'": "name: 'Sem Grupo de Pesquisa'",
    "name: 'Projects'": "name: 'Projetos'",
    "name: 'Researchers'": "name: 'Pesquisadores'",
    "name: 'Students'": "name: 'Estudantes'",
    
    # Section titles
    "### Project Status Over Time": "### Status dos Projetos ao Longo do Tempo",
    "### Ongoing Projects - Expected Completion by Year": "### Projetos em Andamento - Conclusão Esperada por Ano",
    "### Researcher Collaboration Network": "### Rede de Colaboração de Pesquisadores",
    "### Projects by Research Group Association": "### Projetos por Associação a Grupos de Pesquisa",
    "### Student Involvement Over Time": "### Envolvimento de Estudantes ao Longo do Tempo",
    "### Student Participation Distribution": "### Distribuição de Participação de Estudantes",
    
    # Descriptions
    "This chart shows the distribution of projects by their completion status.": "Este gráfico mostra a distribuição de projetos por status de conclusão.",
    "The **Completed** line represents projects that have finished": "A linha **Concluídos** representa projetos que foram finalizados",
    "while the **Ongoing** line shows projects that are still in progress.": "enquanto a linha **Em Andamento** mostra projetos que ainda estão em progresso.",
    "This helps track the balance between concluded research and active investigations.": "Isso ajuda a rastrear o equilíbrio entre pesquisas concluídas e investigações ativas.",
    
    "This chart shows how many ongoing projects are expected to be completed each year": "Este gráfico mostra quantos projetos em andamento devem ser concluídos a cada ano",
    "helping to visualize the project pipeline and upcoming milestones.": "ajudando a visualizar o pipeline de projetos e marcos futuros.",
    
    "**Total ongoing projects:**": "**Total de projetos em andamento:**",
    
    "This chart shows the distribution of projects associated with research groups versus independent projects over time": "Este gráfico mostra a distribuição de projetos associados a grupos de pesquisa versus projetos independentes ao longo do tempo",
    "helping to understand the role of research groups in project organization.": "ajudando a entender o papel dos grupos de pesquisa na organização de projetos.",
    
    "This chart illustrates student participation in research projects throughout the years.": "Este gráfico ilustra a participação de estudantes em projetos de pesquisa ao longo dos anos.",
    "The **All Students** line shows the total number of students engaged annually": "A linha **Todos os Estudantes** mostra o número total de estudantes engajados anualmente",
    "while the **With Funding** and **Without Funding** lines distinguish between students working on funded versus unfunded projects.": "enquanto as linhas **Com Financiamento** e **Sem Financiamento** distinguem entre estudantes trabalhando em projetos financiados versus não financiados.",
    "This helps identify trends in student research opportunities and the impact of funding on student involvement.": "Isso ajuda a identificar tendências em oportunidades de pesquisa para estudantes e o impacto do financiamento no envolvimento estudantil.",
    
    "This bar chart reveals how many students participated in multiple research projects.": "Este gráfico de barras revela quantos estudantes participaram de múltiplos projetos de pesquisa.",
    "Each bar represents a participation level": "Cada barra representa um nível de participação",
    "for example, if the bar at position": "por exemplo, se a barra na posição",
    "This distribution helps understand student engagement patterns and identifies students with sustained research involvement across multiple projects.": "Esta distribuição ajuda a entender padrões de engajamento estudantil e identifica estudantes com envolvimento sustentado em pesquisa através de múltiplos projetos.",
    
    # Table headers
    "**ID:**": "**ID:**",
    "**Period:**": "**Período:**",
    "**Coordinator:**": "**Coordenador:**",
    "**Research Group:**": "**Grupo de Pesquisa:**",
    "**Knowledge Area:**": "**Área de Conhecimento:**",
    "**Research Line:**": "**Linha de Pesquisa:**",
    "**Nature:**": "**Natureza:**",
    "**Researchers:**": "**Pesquisadores:**",
    "**Students:**": "**Estudantes:**",
    "**Keywords:**": "**Palavras-chave:**",
    "**Partner:**": "**Parceiro:**",
    "**Publications:**": "**Publicações:**",
    "**Funding:**": "**Financiamento:**",
    
    # Misc
    "**Total projects:**": "**Total de projetos:**",
    "Highly Engaged Students (5+ Projects)": "Estudantes Altamente Engajados (5+ Projetos)",
    "The following students have demonstrated exceptional commitment by participating in 5 or more research projects:": "Os seguintes estudantes demonstraram compromisso excepcional ao participar de 5 ou mais projetos de pesquisa:",
    "Student Name": "Nome do Estudante",
    "Number of Projects": "Número de Projetos",
    "**Total:**": "**Total:**",
    "student(s) with sustained research involvement": "estudante(s) com envolvimento sustentado em pesquisa",
}

# Translation dictionary for research_groups
translations_groups = {
    # Title
    "# Research Groups": "# Grupos de Pesquisa",
    
    # Table headers
    "'Short Name'": "'Nome Curto'",
    "'Name'": "'Nome'",
    "'Campus'": "'Campus'",
    "'Knowledge Area'": "'Área de Conhecimento'",
    "'Repository'": "'Repositório'",
    "'Leaders'": "'Líderes'",
    
    # Project table headers
    "'Title'": "'Título'",
    "'Period'": "'Período'",
    "'Coordinator'": "'Coordenador'",
    "'Researchers'": "'Pesquisadores'",
    "'Students'": "'Estudantes'",
    "'Research Line'": "'Linha de Pesquisa'",
    "'Nature'": "'Natureza'",
    "'Keywords'": "'Palavras-chave'",
    "'Partner'": "'Parceiro'",
    "'Pub/Fund'": "'Pub/Fin'",
    
    # Section titles
    "### Visualizations": "### Visualizações",
    "### Students and Their Projects": "### Estudantes e Seus Projetos",
    "### Collaboration Network": "### Rede de Colaboração",
    
    # Text content
    "**Total projects:**": "**Total de projetos:**",
    "**Total unique students:**": "**Total de estudantes únicos:**",
    
    # Chart titles
    "title: 'Projects Over Time by Category'": "title: 'Projetos ao Longo do Tempo por Categoria'",
    "title: 'Number of Students Over Time'": "title: 'Número de Estudantes ao Longo do Tempo'",
    "title: 'Year'": "title: 'Ano'",
    
    # Legend items
    "name: 'All Projects'": "name: 'Todos os Projetos'",
    "name: 'With Funding'": "name: 'Com Financiamento'",
    "name: 'With Partners'": "name: 'Com Parceiros'",
    "name: 'All Students'": "name: 'Todos os Estudantes'",
    "name: 'Without Funding'": "name: 'Sem Financiamento'",
    
    # Network descriptions
    "**This network graph visualizes the collaboration relationships between all people involved in the research group's projects.**": "**Este grafo de rede visualiza as relações de colaboração entre todas as pessoas envolvidas nos projetos do grupo de pesquisa.**",
    
    "How to Read This Graph:": "Como Ler Este Gráfico:",
    "<strong>Nodes (circles)</strong> represent people: coordinators, researchers, and students": "<strong>Nós (círculos)</strong> representam pessoas: coordenadores, pesquisadores e estudantes",
    "<strong>Node size</strong> indicates how many connections a person has (larger = more collaborative)": "<strong>Tamanho do nó</strong> indica quantas conexões uma pessoa tem (maior = mais colaborativo)",
    "<strong>Edges (lines)</strong> connect people who worked together on projects": "<strong>Arestas (linhas)</strong> conectam pessoas que trabalharam juntas em projetos",
    "<strong>Edge thickness</strong> shows collaboration strength (thicker = more projects together)": "<strong>Espessura da aresta</strong> mostra força da colaboração (mais espessa = mais projetos juntos)",
    "<strong>Colors</strong>: Red = Coordinators, Turquoise = Researchers, Light Green = Students": "<strong>Cores</strong>: Vermelho = Coordenadores, Turquesa = Pesquisadores, Verde Claro = Estudantes",
    "<strong>Interactive</strong>: Hover over nodes/edges for details, drag to rearrange, scroll to zoom": "<strong>Interativo</strong>: Passe o mouse sobre nós/arestas para detalhes, arraste para reorganizar, role para zoom",
    
    # Legend labels
    "<strong>Legend</strong>": "<strong>Legenda</strong>",
    "<strong>Coordinators</strong>": "<strong>Coordenadores</strong>",
    "<strong>Researchers</strong>": "<strong>Pesquisadores</strong>",
    "<strong>Students</strong>": "<strong>Estudantes</strong>",
    "<strong>Node size:</strong> # connections": "<strong>Tamanho do nó:</strong> # conexões",
    "<strong>Edge width:</strong> # collaborations": "<strong>Espessura da aresta:</strong> # colaborações",
    
    # Network statistics
    "Network Statistics": "Estatísticas da Rede",
    "<strong>Total People:</strong>": "<strong>Total de Pessoas:</strong>",
    "<strong>Total Connections:</strong>": "<strong>Total de Conexões:</strong>",
    "<strong>Coordinators:</strong>": "<strong>Coordenadores:</strong>",
    "<strong>Researchers:</strong>": "<strong>Pesquisadores:</strong>",
    "<strong>Students:</strong>": "<strong>Estudantes:</strong>",
    "<strong>Avg. Connections/Person:</strong>": "<strong>Média de Conexões/Pessoa:</strong>",
    "<strong>Most Connected Person:</strong>": "<strong>Pessoa Mais Conectada:</strong>",
    "connections": "conexões",
    "<strong>Strongest Collaboration:</strong>": "<strong>Colaboração Mais Forte:</strong>",
    "projects together": "projetos juntos",
    
    # Table headers in students section
    "<th>Student</th>": "<th>Estudante</th>",
    "<th>Projects</th>": "<th>Projetos</th>",
    "<th>Total</th>": "<th>Total</th>",
}

def translate_file(filepath, translations):
    """Translate a file using the translation dictionary."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply translations
    for english, portuguese in translations.items():
        content = content.replace(english, portuguese)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Translated: {filepath}")

if __name__ == "__main__":
    translate_file("onestep-static/docs/research_projects.pt.md", translations_projects)
    translate_file("onestep-static/docs/research_groups.pt.md", translations_groups)
    print("Translation complete!")
