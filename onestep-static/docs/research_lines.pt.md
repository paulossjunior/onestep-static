# Linhas de Pesquisa - Campus Serra

<style>
  .md-content {
    max-width: 100% !important;
  }
  .md-content__inner {
    max-width: 100% !important;
    margin: 0 auto !important;
    padding: 0 20px !important;
  }
</style>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>

{% set data = load_research_lines_data() %}
{% set metadata = data['metadata'] %}
{% set research_lines = data['research_lines'] %}

## Visão Geral

A pesquisa no Campus Serra está organizada em **{{ metadata['total_research_lines'] }} linhas de pesquisa temáticas**, cobrindo diversas áreas do conhecimento e promovendo colaboração interdisciplinar.

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 30px 0;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">
    <div style="font-size: 40px; font-weight: bold;">{{ metadata['total_research_lines'] }}</div>
    <div style="font-size: 15px; margin-top: 8px;">Linhas de Pesquisa</div>
  </div>
  <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">
    <div style="font-size: 40px; font-weight: bold;">{{ metadata['total_projects'] }}</div>
    <div style="font-size: 15px; margin-top: 8px;">Total de Projetos</div>
  </div>
  <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">
    <div style="font-size: 40px; font-weight: bold;">{{ metadata['total_supervisors'] }}</div>
    <div style="font-size: 15px; margin-top: 8px;">Pesquisadores</div>
  </div>
  <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">
    <div style="font-size: 40px; font-weight: bold;">{{ metadata['total_students'] }}</div>
    <div style="font-size: 15px; margin-top: 8px;">Estudantes</div>
  </div>
  <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">
    <div style="font-size: 40px; font-weight: bold;">{{ metadata['total_ic_scholarships'] }}</div>
    <div style="font-size: 15px; margin-top: 8px;">Bolsas IC</div>
  </div>
</div>

### Top 20 Linhas de Pesquisa por Número de Projetos

<div id="top-lines-chart" style="width:100%;height:600px;margin:30px 0;"></div>

<script>
(function() {
  var lines = {{ research_lines|tojson }};
  
  // Get top 20
  var top20 = lines.slice(0, 20);
  
  var names = top20.map(function(l) { return l.name; }).reverse();
  var projects = top20.map(function(l) { return l.statistics.total_projects; }).reverse();
  var supervisors = top20.map(function(l) { return l.statistics.total_supervisors; }).reverse();
  var students = top20.map(function(l) { return l.statistics.total_students; }).reverse();
  
  var trace1 = {
    x: projects,
    y: names,
    name: 'Projetos',
    type: 'bar',
    orientation: 'h',
    marker: {color: '#667eea'}
  };
  
  var trace2 = {
    x: supervisors,
    y: names,
    name: 'Pesquisadores',
    type: 'bar',
    orientation: 'h',
    marker: {color: '#4facfe'}
  };
  
  var trace3 = {
    x: students,
    y: names,
    name: 'Estudantes',
    type: 'bar',
    orientation: 'h',
    marker: {color: '#43e97b'}
  };
  
  var data = [trace1, trace2, trace3];
  
  var layout = {
    title: {
      text: 'Top 20 Linhas de Pesquisa - Projetos, Pesquisadores & Estudantes',
      font: {size: 18, family: 'Arial, sans-serif'}
    },
    barmode: 'group',
    xaxis: {title: 'Quantidade', gridcolor: '#f0f0f0'},
    yaxis: {automargin: true, tickfont: {size: 11}},
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    margin: {t: 60, b: 50, l: 250, r: 50},
    height: 600,
    legend: {x: 0.7, y: 1.1, orientation: 'h'}
  };
  
  Plotly.newPlot('top-lines-chart', data, layout);
})();
</script>

---

## Lista de Linhas de Pesquisa

<div style="margin-bottom: 20px;">
  <input type="text" id="searchInput" placeholder="Buscar linha de pesquisa..." 
         style="width: 100%; padding: 12px; font-size: 16px; border: 2px solid #ddd; border-radius: 6px;">
</div>

<table id="linesTable" style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 12px; text-align: left; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(0)">
        Linha de Pesquisa ▼
      </th>
      <th style="padding: 12px; text-align: center; border: 1px solid #dee2e6; cursor: pointer; width: 100px;" onclick="sortTable(1)">
        Projetos
      </th>
      <th style="padding: 12px; text-align: center; border: 1px solid #dee2e6; cursor: pointer; width: 120px;" onclick="sortTable(2)">
        Pesquisadores
      </th>
      <th style="padding: 12px; text-align: center; border: 1px solid #dee2e6; cursor: pointer; width: 100px;" onclick="sortTable(3)">
        Estudantes
      </th>
      <th style="padding: 12px; text-align: center; border: 1px solid #dee2e6; cursor: pointer; width: 100px;" onclick="sortTable(4)">
        Bolsas IC
      </th>
    </tr>
  </thead>
  <tbody>
    {% for line in research_lines %}
    <tr class="line-row">
      <td style="padding: 10px; border: 1px solid #dee2e6;">
        <strong>{{ line['name'] }}</strong>
        {% if line['knowledge_areas'] %}
        <br><small style="color: #666;">Áreas: {{ line['knowledge_areas']|join(', ') }}</small>
        {% endif %}
      </td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        <span style="font-weight: bold; color: #667eea;">{{ line['statistics']['total_projects'] }}</span>
      </td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        <span style="font-weight: bold; color: #4facfe;">{{ line['statistics']['total_supervisors'] }}</span>
      </td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        <span style="font-weight: bold; color: #43e97b;">{{ line['statistics']['total_students'] }}</span>
      </td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        <span style="font-weight: bold; color: #fa709a;">{{ line['statistics']['total_ic_scholarships'] }}</span>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<script>
// Search functionality
document.getElementById('searchInput').addEventListener('keyup', function() {
  var input = this.value.toLowerCase();
  var rows = document.querySelectorAll('.line-row');
  
  rows.forEach(function(row) {
    var text = row.textContent.toLowerCase();
    row.style.display = text.includes(input) ? '' : 'none';
  });
});

// Sort table functionality
function sortTable(columnIndex) {
  var table = document.getElementById('linesTable');
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

{% for line in research_lines %}

## {{ line['name'] }}

<div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
    <div style="text-align: center;">
      <div style="font-size: 32px; font-weight: bold; color: #667eea;">{{ line['statistics']['total_projects'] }}</div>
      <div style="font-size: 13px; color: #666;">Projetos</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 32px; font-weight: bold; color: #4facfe;">{{ line['statistics']['total_supervisors'] }}</div>
      <div style="font-size: 13px; color: #666;">Pesquisadores</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 32px; font-weight: bold; color: #43e97b;">{{ line['statistics']['total_students'] }}</div>
      <div style="font-size: 13px; color: #666;">Estudantes</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 32px; font-weight: bold; color: #fa709a;">{{ line['statistics']['total_ic_scholarships'] }}</div>
      <div style="font-size: 13px; color: #666;">Bolsas IC</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 32px; font-weight: bold; color: #28a745;">{{ line['statistics']['projects_with_funding'] }}</div>
      <div style="font-size: 13px; color: #666;">Com Fomento</div>
    </div>
  </div>
  
  {% if line['statistics']['year_range'] %}
  <div style="margin-top: 15px; text-align: center; color: #666;">
    <strong>Período Ativo:</strong> {{ line['statistics']['year_range']['min'] }} - {{ line['statistics']['year_range']['max'] }}
  </div>
  {% endif %}
  
  {% if line['knowledge_areas'] %}
  <div style="margin-top: 15px;">
    <strong>Áreas do Conhecimento:</strong>
    <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px;">
      {% for area in line['knowledge_areas'] %}
      <span style="background: #e3f2fd; color: #1565c0; padding: 4px 10px; border-radius: 4px; font-size: 12px;">{{ area }}</span>
      {% endfor %}
    </div>
  </div>
  {% endif %}
</div>

### Pesquisadores ({{ line['statistics']['total_supervisors'] }})

<div style="display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0;">
  {% for supervisor in line['supervisors'] %}
  <span style="background: #667eea; color: white; padding: 6px 12px; border-radius: 5px; font-size: 13px;">{{ supervisor }}</span>
  {% endfor %}
</div>

### Estudantes ({{ line['statistics']['total_students'] }})

<div style="display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0;">
  {% for student in line['students'] %}
  <span style="background: #43e97b; color: white; padding: 6px 12px; border-radius: 5px; font-size: 13px;">{{ student }}</span>
  {% endfor %}
</div>

### Projetos ({{ line['statistics']['total_projects'] }})

<details style="margin: 20px 0;">
  <summary style="cursor: pointer; padding: 12px; background: #e9ecef; border-radius: 6px; font-weight: bold;">
    📋 Ver Todos os Projetos
  </summary>
  <div style="margin-top: 15px;">
    <table style="width:100%; border-collapse: collapse; font-size: 13px;">
      <thead>
        <tr style="background-color: #f8f9fa;">
          <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Título</th>
          <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 150px;">Coordenador</th>
          <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 100px;">Período</th>
        </tr>
      </thead>
      <tbody>
        {% for project in line['projects'] %}
        <tr>
          <td style="padding: 8px; border: 1px solid #dee2e6;">
            {{ project['title'] }}
            {% if project['research_group'] %}
            <br><small style="color: #666;">Grupo: {{ project['research_group'] }}</small>
            {% endif %}
          </td>
          <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
            <small>{{ project['coordinator'] }}</small>
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
            <small>{{ start_year }}-{{ end_year }}</small>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</details>

{% if line['ic_scholarships'] %}
### Bolsas IC ({{ line['statistics']['total_ic_scholarships'] }})

<details style="margin: 20px 0;">
  <summary style="cursor: pointer; padding: 12px; background: #e9ecef; border-radius: 6px; font-weight: bold;">
    🎓 Ver Todas as Bolsas IC
  </summary>
  <div style="margin-top: 15px;">
    <table style="width:100%; border-collapse: collapse; font-size: 13px;">
      <thead>
        <tr style="background-color: #f8f9fa;">
          <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Estudante</th>
          <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Orientador</th>
          <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Ano</th>
          <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 100px;">Modalidade</th>
        </tr>
      </thead>
      <tbody>
        {% for scholarship in line['ic_scholarships'] %}
        <tr>
          <td style="padding: 8px; border: 1px solid #dee2e6;">{{ scholarship['student'] }}</td>
          <td style="padding: 8px; border: 1px solid #dee2e6;">{{ scholarship['advisor'] }}</td>
          <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ scholarship['year'] }}</td>
          <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
            {% if scholarship['modality'] == 'Bolsista' %}
              <span style="color: #007bff;">💰 Bolsista</span>
            {% else %}
              <span style="color: #6c757d;">🤝 Voluntário</span>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</details>
{% endif %}

---

{% endfor %}
