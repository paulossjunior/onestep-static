# Pesquisadores - Campus Serra

{% set data = load_supervisors_data() %}
{% set all_supervisors = data['supervisors'] %}
{% set metadata = data['metadata'] %}

{# Filter only Serra campus supervisors #}
{% set supervisors = [] %}
{% for sup in all_supervisors %}
  {% if sup['campus'] == 'Serra' %}
    {% set _ = supervisors.append(sup) %}
  {% endif %}
{% endfor %}

## Visão Geral

**Total de Pesquisadores (Campus Serra):** {{ supervisors|length }}

{# Calculate statistics for Serra campus only #}
{% set serra_with_projects = supervisors|selectattr('research_projects')|list|length %}
{% set serra_with_supervisions = supervisors|selectattr('ic_supervisions')|list|length %}
{% set serra_with_both = 0 %}
{% for sup in supervisors %}
  {% if sup['research_projects'] and sup['ic_supervisions'] %}
    {% set serra_with_both = serra_with_both + 1 %}
  {% endif %}
{% endfor %}

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ serra_with_projects }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Com Projetos de Pesquisa</div>
  </div>
  <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ serra_with_supervisions }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Com Orientações de IC</div>
  </div>
  <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ serra_with_both }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Com Ambos</div>
  </div>
</div>

---

## Lista de Pesquisadores

{# Sort supervisors by total activity (projects + supervisions) #}
{% set sorted_supervisors = supervisors|sort(attribute='statistics.total_projects', reverse=True) %}

<div style="margin-bottom: 20px;">
  <input type="text" id="searchInput" placeholder="Buscar pesquisador..." 
         style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 4px;">
</div>

<table id="supervisorsTable" style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(0)">
        Nome ▼
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(1)">
        Campus
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(2)">
        Projetos
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(3)">
        Orientações IC
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(4)">
        Anos Ativos
      </th>
    </tr>
  </thead>
  <tbody>
    {% for supervisor in sorted_supervisors %}
    <tr class="supervisor-row">
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        <strong>{{ supervisor['name'] }}</strong>
        {% if supervisor['email'] %}
        <br><small style="color: #666;">{{ supervisor['email'] }}</small>
        {% endif %}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {{ supervisor['campus'] if supervisor['campus'] else '-' }}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        <span style="font-weight: bold; color: #667eea;">{{ supervisor['statistics']['total_projects'] }}</span>
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        <span style="font-weight: bold; color: #f5576c;">{{ supervisor['statistics']['total_supervisions'] }}</span>
        {% if supervisor['statistics']['total_supervisions'] > 0 %}
        <br><small style="color: #666;">
          {{ supervisor['statistics']['total_scholarship_holders'] }} bolsistas, 
          {{ supervisor['statistics']['total_volunteers'] }} voluntários
        </small>
        {% endif %}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if supervisor['statistics']['year_range'] %}
          {{ supervisor['statistics']['year_range']['min'] }} - {{ supervisor['statistics']['year_range']['max'] }}
        {% else %}
          -
        {% endif %}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<script>
// Search functionality
document.getElementById('searchInput').addEventListener('keyup', function() {
  var input = this.value.toLowerCase();
  var rows = document.querySelectorAll('.supervisor-row');
  
  rows.forEach(function(row) {
    var text = row.textContent.toLowerCase();
    row.style.display = text.includes(input) ? '' : 'none';
  });
});

// Sort table functionality
function sortTable(columnIndex) {
  var table = document.getElementById('supervisorsTable');
  var tbody = table.querySelector('tbody');
  var rows = Array.from(tbody.querySelectorAll('tr'));
  
  rows.sort(function(a, b) {
    var aValue = a.cells[columnIndex].textContent.trim();
    var bValue = b.cells[columnIndex].textContent.trim();
    
    // Try to parse as number
    var aNum = parseFloat(aValue);
    var bNum = parseFloat(bValue);
    
    if (!isNaN(aNum) && !isNaN(bNum)) {
      return bNum - aNum; // Descending for numbers
    }
    
    return aValue.localeCompare(bValue); // Ascending for text
  });
  
  rows.forEach(function(row) {
    tbody.appendChild(row);
  });
}
</script>

---

## Top 10 Pesquisadores

### Por Projetos de Pesquisa

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Nome</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Campus</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Total de Projetos</th>
    </tr>
  </thead>
  <tbody>
    {% for supervisor in supervisors|sort(attribute='statistics.total_projects', reverse=True) %}
    {% if supervisor['statistics']['total_projects'] > 0 and loop.index <= 10 %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ loop.index }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ supervisor['name'] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ supervisor['campus'] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold; color: #667eea;">
        {{ supervisor['statistics']['total_projects'] }}
      </td>
    </tr>
    {% endif %}
    {% endfor %}
  </tbody>
</table>

### Por Orientações de IC

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Nome</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Campus</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Total de Orientações</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Bolsistas</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Voluntários</th>
    </tr>
  </thead>
  <tbody>
    {% for supervisor in supervisors|sort(attribute='statistics.total_supervisions', reverse=True) %}
    {% if supervisor['statistics']['total_supervisions'] > 0 and loop.index <= 10 %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ loop.index }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ supervisor['name'] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ supervisor['campus'] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold; color: #f5576c;">
        {{ supervisor['statistics']['total_supervisions'] }}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {{ supervisor['statistics']['total_scholarship_holders'] }}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {{ supervisor['statistics']['total_volunteers'] }}
      </td>
    </tr>
    {% endif %}
    {% endfor %}
  </tbody>
</table>


---

## Perfis Individuais dos Pesquisadores

{% for supervisor in supervisors|sort(attribute='name') %}

### {{ supervisor['name'] }}

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
  <p style="margin: 5px 0;"><strong>Campus:</strong> {{ supervisor['campus'] if supervisor['campus'] else 'Não especificado' }}</p>
  {% if supervisor['email'] %}
  <p style="margin: 5px 0;"><strong>Email:</strong> {{ supervisor['email'] }}</p>
  {% endif %}
  <p style="margin: 5px 0;">
    <strong>Atividade:</strong> 
    {% if supervisor['statistics']['year_range'] %}
      {% set current_year = 2025 %}
      {% if supervisor['statistics']['year_range']['max'] >= current_year - 1 %}
        <span style="color: #28a745; font-weight: bold;">✓ ATIVO</span>
      {% else %}
        <span style="color: #6c757d;">○ Inativo desde {{ supervisor['statistics']['year_range']['max'] }}</span>
      {% endif %}
      ({{ supervisor['statistics']['year_range']['min'] }} - {{ supervisor['statistics']['year_range']['max'] }})
    {% else %}
      <span style="color: #6c757d;">Sem dados de atividade</span>
    {% endif %}
  </p>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px;">
  <div style="background: #667eea; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ supervisor['statistics']['total_projects'] }}</div>
    <div style="font-size: 12px;">Projetos</div>
  </div>
  <div style="background: #f5576c; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ supervisor['statistics']['total_supervisions'] }}</div>
    <div style="font-size: 12px;">Orientações</div>
  </div>
  <div style="background: #4facfe; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ supervisor['statistics']['total_scholarship_holders'] }}</div>
    <div style="font-size: 12px;">Bolsistas</div>
  </div>
  <div style="background: #00f2fe; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ supervisor['statistics']['total_volunteers'] }}</div>
    <div style="font-size: 12px;">Voluntários</div>
  </div>
</div>

{# Calculate detailed statistics by year #}
{% set years_data = {} %}

{# Process research projects #}
{% for project in supervisor['research_projects'] %}
  {% if project['start_date'] and project['start_date']|length >= 8 %}
    {% set year = ('20' + project['start_date'][-2:])|int %}
    {% if year not in years_data %}
      {% set _ = years_data.__setitem__(year, {
        'projects_with_funding': 0,
        'projects_without_funding': 0,
        'bolsistas': 0,
        'voluntarios': 0
      }) %}
    {% endif %}
    
    {# Check if project has external funding #}
    {% if project['partner_organization'] or project['external_research_group'] %}
      {% set _ = years_data[year].__setitem__('projects_with_funding', years_data[year]['projects_with_funding'] + 1) %}
    {% else %}
      {% set _ = years_data[year].__setitem__('projects_without_funding', years_data[year]['projects_without_funding'] + 1) %}
    {% endif %}
  {% endif %}
{% endfor %}

{# Process IC supervisions #}
{% for supervision in supervisor['ic_supervisions'] %}
  {% set year = supervision['year'] %}
  {% if year %}
    {% if year not in years_data %}
      {% set _ = years_data.__setitem__(year, {
        'projects_with_funding': 0,
        'projects_without_funding': 0,
        'bolsistas': 0,
        'voluntarios': 0
      }) %}
    {% endif %}
    
    {% if supervision['modality'] == 'Bolsista' %}
      {% set _ = years_data[year].__setitem__('bolsistas', years_data[year]['bolsistas'] + 1) %}
    {% elif supervision['modality'] == 'Voluntário' %}
      {% set _ = years_data[year].__setitem__('voluntarios', years_data[year]['voluntarios'] + 1) %}
    {% endif %}
  {% endif %}
{% endfor %}

{% if years_data %}
{% set sorted_years = years_data.keys()|list|sort %}
<div id="chart-{{ loop.index }}" style="width:100%;height:350px;margin-bottom:20px;"></div>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
<script>
(function() {
  var years = {{ sorted_years|tojson }};
  var yearsData = {{ years_data|tojson }};
  
  var projectsWithFunding = [];
  var projectsWithoutFunding = [];
  var bolsistas = [];
  var voluntarios = [];
  
  years.forEach(function(year) {
    var yearStr = String(year);
    projectsWithFunding.push(yearsData[yearStr].projects_with_funding || 0);
    projectsWithoutFunding.push(yearsData[yearStr].projects_without_funding || 0);
    bolsistas.push(yearsData[yearStr].bolsistas || 0);
    voluntarios.push(yearsData[yearStr].voluntarios || 0);
  });
  
  var data = [
    {
      x: years,
      y: projectsWithFunding,
      text: projectsWithFunding,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Projetos com Fomento',
      line: {width: 2.5, color: '#28a745'},
      marker: {size: 7},
      textposition: 'top center',
      textfont: {size: 9, color: '#28a745'},
      hovertemplate: '<b>Projetos com Fomento</b><br>Ano: %{x}<br>%{y} projetos<extra></extra>'
    },
    {
      x: years,
      y: projectsWithoutFunding,
      text: projectsWithoutFunding,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Projetos sem Fomento',
      line: {width: 2.5, color: '#6c757d', dash: 'dash'},
      marker: {size: 7},
      textposition: 'top center',
      textfont: {size: 9, color: '#6c757d'},
      hovertemplate: '<b>Projetos sem Fomento</b><br>Ano: %{x}<br>%{y} projetos<extra></extra>'
    },
    {
      x: years,
      y: bolsistas,
      text: bolsistas,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Bolsistas',
      line: {width: 2.5, color: '#007bff'},
      marker: {size: 7},
      textposition: 'bottom center',
      textfont: {size: 9, color: '#007bff'},
      hovertemplate: '<b>Bolsistas</b><br>Ano: %{x}<br>%{y} orientações<extra></extra>'
    },
    {
      x: years,
      y: voluntarios,
      text: voluntarios,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Voluntários',
      line: {width: 2.5, color: '#ffc107'},
      marker: {size: 7},
      textposition: 'bottom center',
      textfont: {size: 9, color: '#ffc107'},
      hovertemplate: '<b>Voluntários</b><br>Ano: %{x}<br>%{y} orientações<extra></extra>'
    }
  ];
  
  var layout = {
    title: {
      text: 'Evolução de Projetos e Orientações',
      font: {size: 16, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Ano',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Quantidade',
      gridcolor: '#f0f0f0',
      rangemode: 'tozero'
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    hovermode: 'x unified',
    legend: {
      x: 0.02,
      y: 0.98,
      bgcolor: 'rgba(255,255,255,0.9)',
      bordercolor: '#ccc',
      borderwidth: 1
    },
    margin: {t: 50, b: 50, l: 50, r: 20}
  };
  
  Plotly.newPlot('chart-{{ loop.index }}', data, layout);
})();
</script>
{% endif %}

{# Build collaboration network #}
{% set collaborators = {} %}
{% for project in supervisor['research_projects'] %}
  {% if project['participants'] %}
    {% for participant in project['participants'] %}
      {% set participant_name = participant.strip() %}
      {% if participant_name and participant_name != supervisor['name'] %}
        {% if participant_name not in collaborators %}
          {% set _ = collaborators.__setitem__(participant_name, {'count': 0, 'projects': []}) %}
        {% endif %}
        {% set _ = collaborators[participant_name].__setitem__('count', collaborators[participant_name]['count'] + 1) %}
        {% set _ = collaborators[participant_name]['projects'].append(project['title'][:50]) %}
      {% endif %}
    {% endfor %}
  {% endif %}
{% endfor %}

{% if collaborators %}
#### Rede de Colaboração ({{ collaborators|length }} colaboradores)

<div id="network-{{ loop.index }}" style="width:100%;height:400px;border:1px solid #ddd;margin-bottom:20px;"></div>

<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<script>
(function() {
  var collaborators = {{ collaborators|tojson }};
  
  // Create nodes
  var nodes = [
    {
      id: 0,
      label: '{{ supervisor["name"][:20] }}',
      color: {background: '#667eea', border: '#4a5fc1'},
      font: {color: 'white', size: 14, bold: true},
      size: 30,
      title: '{{ supervisor["name"] }}<br>Coordenador Principal'
    }
  ];
  
  var edges = [];
  var nodeId = 1;
  
  // Add collaborator nodes and edges
  Object.keys(collaborators).forEach(function(name) {
    var collab = collaborators[name];
    var size = 15 + (collab.count * 3);
    
    nodes.push({
      id: nodeId,
      label: name.substring(0, 15) + (name.length > 15 ? '...' : ''),
      color: {background: '#4facfe', border: '#0088cc'},
      size: size,
      title: name + '<br>' + collab.count + ' projeto(s) em comum'
    });
    
    edges.push({
      from: 0,
      to: nodeId,
      value: collab.count,
      title: collab.count + ' projeto(s)',
      color: {color: '#999', opacity: 0.6}
    });
    
    nodeId++;
  });
  
  var container = document.getElementById('network-{{ loop.index }}');
  var data = {nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges)};
  
  var options = {
    physics: {
      enabled: true,
      stabilization: {iterations: 100},
      barnesHut: {
        gravitationalConstant: -8000,
        springConstant: 0.04,
        springLength: 150
      }
    },
    interaction: {
      hover: true,
      tooltipDelay: 100
    },
    nodes: {
      shape: 'dot',
      font: {size: 12}
    },
    edges: {
      smooth: {type: 'continuous'},
      width: 2
    }
  };
  
  var network = new vis.Network(container, data, options);
})();
</script>

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
  <p style="margin: 5px 0; font-size: 14px;">
    <strong>📊 Estatísticas da Rede:</strong>
  </p>
  <ul style="margin: 10px 0; font-size: 13px; color: #555;">
    <li><strong>Total de colaboradores:</strong> {{ collaborators|length }}</li>
    <li><strong>Colaborador mais frequente:</strong> 
      {% set top_collab = collaborators.items()|sort(attribute='1.count', reverse=True)|first %}
      {{ top_collab[0] }} ({{ top_collab[1]['count'] }} projeto{{ 's' if top_collab[1]['count'] > 1 else '' }})
    </li>
    <li><strong>Total de colaborações:</strong> 
      {% set total_collabs = 0 %}
      {% for name, data in collaborators.items() %}
        {% set total_collabs = total_collabs + data['count'] %}
      {% endfor %}
      {{ total_collabs }} conexões
    </li>
    <li><strong>Média de projetos por colaborador:</strong> 
      {{ "%.1f"|format(total_collabs / collaborators|length) }}
    </li>
  </ul>
  <p style="margin: 5px 0; font-size: 12px; color: #666; font-style: italic;">
    💡 <strong>Como interpretar:</strong> O nó central (roxo) representa o pesquisador. 
    Os nós azuis são colaboradores, com tamanho proporcional ao número de projetos compartilhados. 
    Passe o mouse sobre os nós para ver detalhes. Você pode arrastar os nós para reorganizar a visualização.
  </p>
</div>
{% endif %}

{% if supervisor['research_projects'] %}
#### Projetos de Pesquisa ({{ supervisor['research_projects']|length }})

<table style="width:100%; border-collapse: collapse; margin: 15px 0; font-size: 14px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6;">Título</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 100px;">Período</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Status</th>
    </tr>
  </thead>
  <tbody>
    {% for project in supervisor['research_projects'] %}
    <tr>
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        <strong>{{ project['title'] }}</strong>
        {% if project['code'] %}
        <br><small style="color: #666;">Código: {{ project['code'] }}</small>
        {% endif %}
        {% if project['knowledge_area'] %}
        <br><small style="color: #666;">Área: {{ project['knowledge_area'] }}</small>
        {% endif %}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if project['start_date'] and project['start_date']|length >= 8 %}
          {% set start_year = '20' + project['start_date'][-2:] %}
        {% else %}
          {% set start_year = '?' %}
        {% endif %}
        {% if project['end_date'] and project['end_date']|length >= 8 %}
          {% set end_year = '20' + project['end_date'][-2:] %}
        {% else %}
          {% set end_year = '?' %}
        {% endif %}
        <small>{{ start_year }} - {{ end_year }}</small>
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if project['status'] and (project['status'] == 'EM_ANDAMENTO' or project['status'] == 'Em andamento') %}
          <span style="color: #28a745; font-weight: bold;">● Ativo</span>
        {% elif project['status'] and (project['status'] == 'CONCLUIDO' or project['status'] == 'Concluído') %}
          <span style="color: #6c757d;">○ Concluído</span>
        {% elif project['end_date'] and project['end_date']|length >= 8 %}
          {% set end_year_int = ('20' + project['end_date'][-2:])|int %}
          {% if end_year_int >= 2024 %}
            <span style="color: #28a745; font-weight: bold;">● Ativo</span>
          {% else %}
            <span style="color: #6c757d;">○ Concluído</span>
          {% endif %}
        {% else %}
          <span style="color: #999;">- Indefinido</span>
        {% endif %}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endif %}

{% if supervisor['ic_supervisions'] %}
#### Orientações de Iniciação Científica ({{ supervisor['ic_supervisions']|length }})

<table style="width:100%; border-collapse: collapse; margin: 15px 0; font-size: 14px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6;">Estudante</th>
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6;">Projeto</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Ano</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 100px;">Modalidade</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Status</th>
    </tr>
  </thead>
  <tbody>
    {% for supervision in supervisor['ic_supervisions'] %}
    <tr>
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        <strong>{{ supervision['student'] }}</strong>
        {% if supervision['course'] %}
        <br><small style="color: #666;">{{ supervision['course'] }}</small>
        {% endif %}
      </td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        <small>{{ supervision['project_title'] if supervision['project_title'] else supervision['research_project_title'] if supervision['research_project_title'] else 'Não especificado' }}</small>
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {{ supervision['year'] }}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if supervision['modality'] == 'Bolsista' %}
          <span style="color: #007bff; font-weight: bold;">💰 Bolsista</span>
        {% else %}
          <span style="color: #6c757d;">🤝 Voluntário</span>
        {% endif %}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% set current_year = 2025 %}
        {% if supervision['year'] >= current_year - 1 %}
          <span style="color: #28a745; font-weight: bold;">● Ativo</span>
        {% else %}
          <span style="color: #6c757d;">○ Concluído</span>
        {% endif %}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endif %}

{% if not supervisor['research_projects'] and not supervisor['ic_supervisions'] %}
<p style="color: #6c757d; font-style: italic;">Nenhum projeto ou orientação registrado.</p>
{% endif %}

---

{% endfor %}
