# Estudantes - Campus Serra

<style>
  .md-content {
    max-width: 100% !important;
  }
  .md-content__inner {
    max-width: 100% !important;
    margin: 0 auto !important;
    padding: 0 20px !important;
  }
  article {
    max-width: 100% !important;
  }
  .md-typeset table:not([class]) {
    display: table !important;
    width: 100% !important;
    table-layout: fixed !important;
  }
  #studentsTable {
    width: 100% !important;
    table-layout: fixed !important;
  }
  #studentsTable td {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
    hyphens: auto !important;
  }
  #studentsTable th {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
  }
  body {
    overflow-x: hidden !important;
  }
  .md-container {
    overflow-x: hidden !important;
  }
</style>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>

{% set data = load_students_data() %}
{% set all_students = data['students'] %}
{% set metadata = data['metadata'] %}

{# Filter only Serra campus students #}
{% set students = [] %}
{% for student in all_students %}
  {% if student['campus'] == 'Serra' %}
    {% set _ = students.append(student) %}
  {% endif %}
{% endfor %}

## Visão Geral

**Total de Estudantes (Campus Serra):** {{ students|length }}

{# Calculate statistics for Serra campus only #}
{% set serra_with_projects = students|selectattr('research_projects')|list|length %}
{% set serra_with_scholarships = students|selectattr('ic_scholarships')|list|length %}

{% set ns = namespace(serra_with_both=0, serra_with_collabs=0, total_scholarship_holders=0, total_volunteers=0) %}

{% for student in students %}
  {% if student['research_projects'] and student['ic_scholarships'] %}
    {% set ns.serra_with_both = ns.serra_with_both + 1 %}
  {% endif %}
  {% if student.get('collaborations') %}
    {% set ns.serra_with_collabs = ns.serra_with_collabs + 1 %}
  {% endif %}
  {% set ns.total_scholarship_holders = ns.total_scholarship_holders + student['statistics']['total_as_scholarship_holder'] %}
  {% set ns.total_volunteers = ns.total_volunteers + student['statistics']['total_as_volunteer'] %}
{% endfor %}

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-bottom: 30px;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ serra_with_projects }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Com Projetos de Pesquisa</div>
  </div>
  <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ serra_with_scholarships }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Com Bolsas de IC</div>
  </div>
  <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ ns.serra_with_both }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Com Ambos</div>
  </div>
  <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ ns.serra_with_collabs }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Com Colaborações</div>
  </div>
</div>

### Estatísticas de Bolsas

<div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 20px; border-radius: 8px; margin-bottom: 30px;">
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">{{ ns.total_scholarship_holders }}</div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Total de Bolsistas</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Bolsas remuneradas</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">{{ ns.total_volunteers }}</div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Total de Voluntários</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Participação não remunerada</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">
        {{ ns.total_scholarship_holders + ns.total_volunteers }}
      </div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Total de Participações</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Todas as atividades de IC</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">
        {{ "%.1f"|format((ns.total_scholarship_holders / (ns.total_scholarship_holders + ns.total_volunteers) * 100)) if (ns.total_scholarship_holders + ns.total_volunteers) > 0 else 0 }}%
      </div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Taxa de Bolsas</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Remuneradas vs total</div>
    </div>
  </div>
</div>

---

## Entendendo as Colaborações entre Estudantes

<div style="background-color: #e3f2fd; padding: 20px; border-radius: 8px; margin-bottom: 30px; border-left: 4px solid #2196f3;">
  <h4 style="margin-top: 0; color: #1565c0;">💡 O que são Colaborações entre Estudantes?</h4>
  
  <p style="margin: 10px 0;">
    <strong>Colaborações entre estudantes</strong> ocorrem quando dois ou mais estudantes trabalham juntos no mesmo projeto de pesquisa. 
    Esta métrica ajuda a identificar:
  </p>
  
  <ul style="margin: 10px 0 10px 20px;">
    <li><strong>Experiência em trabalho em equipe:</strong> Estudantes que trabalharam com colegas em projetos de pesquisa</li>
    <li><strong>Networking:</strong> Estudantes que construíram conexões com outros pesquisadores</li>
    <li><strong>Projetos colaborativos:</strong> Projetos de pesquisa que envolvem múltiplos estudantes</li>
  </ul>
  
  <p style="margin: 10px 0;">
    <strong>Exemplo:</strong> Se um projeto de pesquisa lista 3 estudantes (Alice, Bob e Charlie), então:
  </p>
  <ul style="margin: 10px 0 10px 20px;">
    <li>Alice tem 2 colaboradores (Bob e Charlie) em 1 projeto compartilhado</li>
    <li>Bob tem 2 colaboradores (Alice e Charlie) em 1 projeto compartilhado</li>
    <li>Charlie tem 2 colaboradores (Alice e Bob) em 1 projeto compartilhado</li>
  </ul>
  
  <p style="margin: 10px 0;">
    <strong>Por que isso importa:</strong> Estudantes com mais colaborações tipicamente têm:
  </p>
  <ul style="margin: 10px 0 10px 20px;">
    <li>✓ Habilidades de trabalho em equipe mais fortes</li>
    <li>✓ Rede de pesquisa mais ampla</li>
    <li>✓ Experiência em ambientes de pesquisa colaborativa</li>
    <li>✓ Exposição a diferentes perspectivas e abordagens</li>
  </ul>
</div>

---

## Lista de Estudantes

{# Sort students alphabetically by name #}
{% set sorted_students = students|sort(attribute='name') %}

<div style="margin-bottom: 20px;">
  <input type="text" id="searchInput" placeholder="Buscar estudante..." 
         style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 4px;">
</div>

<table id="studentsTable" style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 12px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; width: 15%;">
        Nome
      </th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; width: 35%;">
        Projetos de Pesquisa
      </th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; width: 35%;">
        Bolsas de IC
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 8%;">
        Colaboradores
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 7%;">
        Anos
      </th>
    </tr>
  </thead>
  <tbody>
    {% for student in sorted_students %}
    <tr class="student-row">
      <td style="padding: 8px; border: 1px solid #dee2e6; vertical-align: top;">
        <strong>{{ student['name'] }}</strong>
        {% if student['email'] %}
        <br><small style="color: #666; font-size: 10px;">{{ student['email'] }}</small>
        {% endif %}
      </td>
      <td style="padding: 8px; border: 1px solid #dee2e6; vertical-align: top;">
        {% if student['research_projects'] %}
          <div style="font-size: 11px;">
            {% for project in student['research_projects'] %}
              <div style="margin-bottom: 8px; {% if not loop.last %}border-bottom: 1px solid #eee; padding-bottom: 8px;{% endif %}">
                <strong style="color: #333;">{{ project['title'] }}</strong>
                {% if project.get('research_line') %}
                <br><span style="color: #1565c0;">🔬 {{ project['research_line'] }}</span>
                {% endif %}
                {% if project.get('coordinator') %}
                <br><span style="color: #2e7d32;">👤 {{ project['coordinator'] }}</span>
                {% endif %}
                {% if project.get('start_date') %}
                <br><span style="color: #666;">📅 {{ project['start_date'][:10] }}{% if project.get('end_date') %} - {{ project['end_date'][:10] }}{% endif %}</span>
                {% endif %}
              </div>
            {% endfor %}
          </div>
        {% else %}
          <span style="color: #999; font-size: 11px;">Sem projetos</span>
        {% endif %}
      </td>
      <td style="padding: 8px; border: 1px solid #dee2e6; vertical-align: top;">
        {% if student['ic_scholarships'] %}
          <div style="font-size: 11px;">
            {% for scholarship in student['ic_scholarships'] %}
              <div style="margin-bottom: 8px; {% if not loop.last %}border-bottom: 1px solid #eee; padding-bottom: 8px;{% endif %}">
                <strong style="color: #333;">{{ scholarship.get('project_title') or scholarship.get('research_project_title', 'Sem título') }}</strong>
                {% if scholarship.get('advisor') %}
                <br><span style="color: #2e7d32;">👤 {{ scholarship['advisor'] }}</span>
                {% endif %}
                <br><span style="color: #666;">
                  📅 {{ scholarship['year'] }} | 
                  {% if scholarship['modality'] == 'Bolsista' %}
                    💰 Bolsista
                  {% else %}
                    🤝 Voluntário
                  {% endif %}
                </span>
              </div>
            {% endfor %}
          </div>
        {% else %}
          <span style="color: #999; font-size: 11px;">Sem bolsas</span>
        {% endif %}
      </td>
      <td style="padding: 8px; border: 1px solid #dee2e6; text-align: center; vertical-align: top;">
        <span style="font-weight: bold; color: #ff9800; font-size: 16px;">{{ student['statistics']['total_collaborators'] }}</span>
      </td>
      <td style="padding: 8px; border: 1px solid #dee2e6; text-align: center; vertical-align: top; font-size: 11px;">
        {% if student['statistics']['year_range'] %}
          {{ student['statistics']['year_range']['min'] }}<br>-<br>{{ student['statistics']['year_range']['max'] }}
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
  var rows = document.querySelectorAll('.student-row');
  
  rows.forEach(function(row) {
    var text = row.textContent.toLowerCase();
    row.style.display = text.includes(input) ? '' : 'none';
  });
});

// Sort table functionality
function sortTable(columnIndex) {
  var table = document.getElementById('studentsTable');
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

## Top 10 Estudantes

### Por Projetos de Pesquisa

<table style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 13px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Estudante</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Total</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Projetos e Coordenadores</th>
    </tr>
  </thead>
  <tbody>
    {% for student in students|sort(attribute='statistics.total_projects', reverse=True) %}
    {% if student['statistics']['total_projects'] > 0 and loop.index <= 10 %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ loop.index }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>{{ student['name'] }}</strong></td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold; color: #667eea;">
        {{ student['statistics']['total_projects'] }}
      </td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        {% if student['research_projects'] %}
          <ul style="margin: 0; padding-left: 15px; font-size: 12px;">
            {% for project in student['research_projects'] %}
            <li style="margin: 3px 0;">
              <strong>{{ project['title'] }}</strong>
              {% if project.get('research_line') %}
              <br><span style="color: #1565c0;">🔬 {{ project['research_line'] }}</span>
              {% endif %}
              {% if project.get('coordinator') %}
              <br><span style="color: #2e7d32;">👤 {{ project['coordinator'] }}</span>
              {% endif %}
            </li>
            {% endfor %}
          </ul>
        {% endif %}
      </td>
    </tr>
    {% endif %}
    {% endfor %}
  </tbody>
</table>

### Por Bolsas de IC

<table style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 13px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Estudante</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Total</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Bolsas e Orientadores</th>
    </tr>
  </thead>
  <tbody>
    {% for student in students|sort(attribute='statistics.total_scholarships', reverse=True) %}
    {% if student['statistics']['total_scholarships'] > 0 and loop.index <= 10 %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ loop.index }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>{{ student['name'] }}</strong></td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold; color: #f5576c;">
        {{ student['statistics']['total_scholarships'] }}
      </td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        {% if student['ic_scholarships'] %}
          <ul style="margin: 0; padding-left: 15px; font-size: 12px;">
            {% for scholarship in student['ic_scholarships'] %}
            <li style="margin: 3px 0;">
              <strong>{{ scholarship.get('project_title') or scholarship.get('research_project_title', 'Sem título') }}</strong>
              {% if scholarship.get('advisor') %}
              <br><span style="color: #2e7d32;">👤 {{ scholarship['advisor'] }}</span>
              {% endif %}
              <span style="color: #666;"> | {{ scholarship['year'] }} | 
              {% if scholarship['modality'] == 'Bolsista' %}💰 Bolsista{% else %}🤝 Voluntário{% endif %}</span>
            </li>
            {% endfor %}
          </ul>
        {% endif %}
      </td>
    </tr>
    {% endif %}
    {% endfor %}
  </tbody>
</table>

### Por Colaborações

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Nome</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Colaboradores</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Projetos Compartilhados</th>
    </tr>
  </thead>
  <tbody>
    {% for student in students|sort(attribute='statistics.total_collaborators', reverse=True) %}
    {% if student['statistics']['total_collaborators'] > 0 and loop.index <= 10 %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ loop.index }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ student['name'] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold; color: #ff9800;">
        {{ student['statistics']['total_collaborators'] }}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {{ student['statistics']['total_collaborations'] }}
      </td>
    </tr>
    {% endif %}
    {% endfor %}
  </tbody>
</table>
