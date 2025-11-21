# Researchers - Campus Serra

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

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

## Overview

**Total Researchers (Campus Serra):** {{ supervisors|length }}

{# Calculate statistics for Serra campus only #}
{% set serra_with_projects = supervisors|selectattr('research_projects')|list|length %}
{% set serra_with_supervisions = supervisors|selectattr('ic_supervisions')|list|length %}
{% set serra_with_both = 0 %}
{% set serra_with_collabs = 0 %}
{% set total_serra_collabs = 0 %}
{% set total_serra_collab_instances = 0 %}

{% for sup in supervisors %}
  {% if sup['research_projects'] and sup['ic_supervisions'] %}
    {% set serra_with_both = serra_with_both + 1 %}
  {% endif %}
  {% if sup.get('collaborations') %}
    {% set serra_with_collabs = serra_with_collabs + 1 %}
    {% set total_serra_collabs = total_serra_collabs + sup['collaborations']|length %}
    {% for collab_name, collab_data in sup['collaborations'].items() %}
      {% set total_serra_collab_instances = total_serra_collab_instances + collab_data['count'] %}
    {% endfor %}
  {% endif %}
{% endfor %}

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-bottom: 30px;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ serra_with_projects }}</div>
    <div style="font-size: 14px; margin-top: 5px;">With Research Projects</div>
  </div>
  <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ serra_with_supervisions }}</div>
    <div style="font-size: 14px; margin-top: 5px;">With IC Supervisions</div>
  </div>
  <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ serra_with_both }}</div>
    <div style="font-size: 14px; margin-top: 5px;">With Both</div>
  </div>
  <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ serra_with_collabs }}</div>
    <div style="font-size: 14px; margin-top: 5px;">With Collaborations</div>
  </div>
</div>

### Collaboration Network Statistics

<div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 20px; border-radius: 8px; margin-bottom: 30px;">
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">{{ total_serra_collabs }}</div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Unique Collaborations</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Total unique researcher pairs</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">{{ total_serra_collab_instances }}</div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Collaboration Instances</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Total shared projects</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">
        {{ "%.1f"|format(total_serra_collab_instances / serra_with_collabs) if serra_with_collabs > 0 else 0 }}
      </div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Avg. Collaborations</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Per active researcher</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">
        {{ "%.1f"|format(total_serra_collabs / serra_with_collabs) if serra_with_collabs > 0 else 0 }}
      </div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Network Density</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Avg. unique partners</div>
    </div>
  </div>
</div>

### Top Collaborators Network

<div id="top-collaborators-chart" style="width:100%;height:500px;margin-bottom:30px;"></div>

<script>
(function() {
  var supervisors = {{ supervisors|tojson }};
  
  // Calculate top collaborators across all Serra researchers
  var collabCounts = {};
  supervisors.forEach(function(sup) {
    if (sup.collaborations) {
      Object.keys(sup.collaborations).forEach(function(collabName) {
        if (!collabCounts[collabName]) {
          collabCounts[collabName] = 0;
        }
        collabCounts[collabName] += sup.collaborations[collabName].count;
      });
    }
  });
  
  // Sort and get top 20
  var topCollabs = Object.keys(collabCounts)
    .map(function(name) {
      return {name: name, count: collabCounts[name]};
    })
    .sort(function(a, b) { return b.count - a.count; })
    .slice(0, 20);
  
  var names = topCollabs.map(function(c) { return c.name; });
  var counts = topCollabs.map(function(c) { return c.count; });
  
  var data = [{
    x: counts,
    y: names,
    type: 'bar',
    orientation: 'h',
    marker: {
      color: counts,
      colorscale: [
        [0, '#e3f2fd'],
        [0.3, '#64b5f6'],
        [0.6, '#2196f3'],
        [1, '#0d47a1']
      ],
      line: {color: '#1565c0', width: 1}
    },
    text: counts.map(function(c) { return c + ' project' + (c > 1 ? 's' : ''); }),
    textposition: 'outside',
    hovertemplate: '<b>%{y}</b><br>%{x} total collaborations<extra></extra>'
  }];
  
  var layout = {
    title: {
      text: 'Top 20 Most Active Collaborators (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Total Collaboration Instances',
      gridcolor: '#f0f0f0'
    },
    yaxis: {
      automargin: true,
      tickfont: {size: 11}
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    margin: {t: 60, b: 50, l: 220, r: 80},
    height: 500
  };
  
  Plotly.newPlot('top-collaborators-chart', data, layout);
})();
</script>

---

## Researchers List

{# Sort supervisors by total activity (projects + supervisions) #}
{% set sorted_supervisors = supervisors|sort(attribute='statistics.total_projects', reverse=True) %}

<div style="margin-bottom: 20px;">
  <input type="text" id="searchInput" placeholder="Search researcher..." 
         style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 4px;">
</div>

<table id="supervisorsTable" style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(0)">
        Name ▼
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(1)">
        Campus
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(2)">
        Projects
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(3)">
        IC Supervisions
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; cursor: pointer;" onclick="sortTable(4)">
        Active Years
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
          {{ supervisor['statistics']['total_scholarship_holders'] }} scholarship holders, 
          {{ supervisor['statistics']['total_volunteers'] }} volunteers
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

## Top 10 Researchers

### By Research Projects

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Name</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Campus</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Total Projects</th>
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

### By IC Supervisions

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Name</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Campus</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Total Supervisions</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Scholarship Holders</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Volunteers</th>
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

## Individual Researcher Profiles

{% for supervisor in supervisors|sort(attribute='name') %}

### {{ supervisor['name'] }}

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
  <p style="margin: 5px 0;"><strong>Campus:</strong> {{ supervisor['campus'] if supervisor['campus'] else 'Not specified' }}</p>
  {% if supervisor['email'] %}
  <p style="margin: 5px 0;"><strong>Email:</strong> {{ supervisor['email'] }}</p>
  {% endif %}
  <p style="margin: 5px 0;">
    <strong>Activity:</strong> 
    {% if supervisor['statistics']['year_range'] %}
      {% set current_year = 2025 %}
      {% if supervisor['statistics']['year_range']['max'] >= current_year - 1 %}
        <span style="color: #28a745; font-weight: bold;">✓ ACTIVE</span>
      {% else %}
        <span style="color: #6c757d;">○ Inactive since {{ supervisor['statistics']['year_range']['max'] }}</span>
      {% endif %}
      ({{ supervisor['statistics']['year_range']['min'] }} - {{ supervisor['statistics']['year_range']['max'] }})
    {% else %}
      <span style="color: #6c757d;">No activity data</span>
    {% endif %}
  </p>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px;">
  <div style="background: #667eea; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ supervisor['statistics']['total_projects'] }}</div>
    <div style="font-size: 12px;">Projects</div>
  </div>
  <div style="background: #f5576c; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ supervisor['statistics']['total_supervisions'] }}</div>
    <div style="font-size: 12px;">Supervisions</div>
  </div>
  <div style="background: #4facfe; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ supervisor['statistics']['total_scholarship_holders'] }}</div>
    <div style="font-size: 12px;">Scholarship Holders</div>
  </div>
  <div style="background: #00f2fe; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ supervisor['statistics']['total_volunteers'] }}</div>
    <div style="font-size: 12px;">Volunteers</div>
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
      name: 'Projects with Funding',
      line: {width: 2.5, color: '#28a745'},
      marker: {size: 7},
      textposition: 'top center',
      textfont: {size: 9, color: '#28a745'},
      hovertemplate: '<b>Projects with Funding</b><br>Year: %{x}<br>%{y} projects<extra></extra>'
    },
    {
      x: years,
      y: projectsWithoutFunding,
      text: projectsWithoutFunding,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Projects without Funding',
      line: {width: 2.5, color: '#6c757d', dash: 'dash'},
      marker: {size: 7},
      textposition: 'top center',
      textfont: {size: 9, color: '#6c757d'},
      hovertemplate: '<b>Projects without Funding</b><br>Year: %{x}<br>%{y} projects<extra></extra>'
    },
    {
      x: years,
      y: bolsistas,
      text: bolsistas,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Scholarship Holders',
      line: {width: 2.5, color: '#007bff'},
      marker: {size: 7},
      textposition: 'bottom center',
      textfont: {size: 9, color: '#007bff'},
      hovertemplate: '<b>Scholarship Holders</b><br>Year: %{x}<br>%{y} supervisions<extra></extra>'
    },
    {
      x: years,
      y: voluntarios,
      text: voluntarios,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Volunteers',
      line: {width: 2.5, color: '#ffc107'},
      marker: {size: 7},
      textposition: 'bottom center',
      textfont: {size: 9, color: '#ffc107'},
      hovertemplate: '<b>Volunteers</b><br>Year: %{x}<br>%{y} supervisions<extra></extra>'
    }
  ];
  
  var layout = {
    title: {
      text: 'Evolution of Projects and Supervisions',
      font: {size: 16, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Year',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Count',
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

{# Build collaboration network from the collaborations field #}
{% set collaborators = supervisor.get('collaborations', {}) %}

{% if collaborators %}
#### Collaboration Network ({{ collaborators|length }} collaborators)

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
  <h4 style="margin: 0 0 15px 0; color: white;">🤝 Collaboration Overview</h4>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
    <div style="text-align: center;">
      <div style="font-size: 32px; font-weight: bold;">{{ collaborators|length }}</div>
      <div style="font-size: 13px; opacity: 0.9;">Total Collaborators</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 32px; font-weight: bold;">
        {% set total_collabs = 0 %}
        {% for name, data in collaborators.items() %}
          {% set total_collabs = total_collabs + data['count'] %}
        {% endfor %}
        {{ total_collabs }}
      </div>
      <div style="font-size: 13px; opacity: 0.9;">Shared Projects</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 32px; font-weight: bold;">
        {{ "%.1f"|format(total_collabs / collaborators|length) if collaborators|length > 0 else 0 }}
      </div>
      <div style="font-size: 13px; opacity: 0.9;">Avg. Projects/Collaborator</div>
    </div>
  </div>
</div>

{# Top Collaborators Bar Chart #}
<div id="collab-chart-{{ loop.index }}" style="width:100%;height:400px;margin-bottom:20px;"></div>

<script>
(function() {
  var collaborators = {{ collaborators|tojson }};
  
  // Sort collaborators by count and get top 15
  var collabArray = Object.keys(collaborators).map(function(name) {
    return {
      name: name,
      count: collaborators[name].count,
      projects: collaborators[name].projects
    };
  }).sort(function(a, b) {
    return b.count - a.count;
  }).slice(0, 15);
  
  var names = collabArray.map(function(c) { return c.name; });
  var counts = collabArray.map(function(c) { return c.count; });
  
  // Count roles
  var roleStats = {coordinator: 0, researcher: 0, coResearcher: 0};
  collabArray.forEach(function(c) {
    c.projects.forEach(function(p) {
      if (p.role === 'coordinator') roleStats.coordinator++;
      else if (p.role === 'researcher') roleStats.researcher++;
      else if (p.role === 'co-researcher') roleStats.coResearcher++;
    });
  });
  
  var data = [{
    x: counts,
    y: names,
    type: 'bar',
    orientation: 'h',
    marker: {
      color: counts,
      colorscale: [
        [0, '#e3f2fd'],
        [0.5, '#4facfe'],
        [1, '#667eea']
      ],
      line: {color: '#0088cc', width: 1}
    },
    text: counts.map(function(c) { return c + ' project' + (c > 1 ? 's' : ''); }),
    textposition: 'outside',
    hovertemplate: '<b>%{y}</b><br>%{x} shared project(s)<extra></extra>'
  }];
  
  var layout = {
    title: {
      text: 'Top 15 Collaborators by Shared Projects',
      font: {size: 16, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Number of Shared Projects',
      gridcolor: '#f0f0f0'
    },
    yaxis: {
      automargin: true,
      tickfont: {size: 11}
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    margin: {t: 50, b: 50, l: 200, r: 50},
    height: 400
  };
  
  Plotly.newPlot('collab-chart-{{ loop.index }}', data, layout);
})();
</script>

{# Collaboration Timeline Graph #}
<div id="collab-timeline-{{ loop.index }}" style="width:100%;height:400px;margin-bottom:20px;"></div>

<script>
(function() {
  var collaborators = {{ collaborators|tojson }};
  var researchProjects = {{ supervisor['research_projects']|tojson }};
  
  // Extract years from projects and count collaborations per year
  var yearCollabs = {};
  var yearRoles = {};
  
  Object.keys(collaborators).forEach(function(collabName) {
    var collab = collaborators[collabName];
    
    collab.projects.forEach(function(proj) {
      // Find the project in research_projects to get the year
      var matchingProject = researchProjects.find(function(rp) {
        return rp.id === proj.id || rp.title === proj.title;
      });
      
      if (matchingProject && matchingProject.start_date && matchingProject.start_date.length >= 8) {
        var year = parseInt('20' + matchingProject.start_date.slice(-2));
        
        if (!yearCollabs[year]) {
          yearCollabs[year] = 0;
          yearRoles[year] = {coordinator: 0, researcher: 0, coResearcher: 0};
        }
        
        yearCollabs[year]++;
        
        if (proj.role === 'coordinator') yearRoles[year].coordinator++;
        else if (proj.role === 'researcher') yearRoles[year].researcher++;
        else if (proj.role === 'co-researcher') yearRoles[year].coResearcher++;
      }
    });
  });
  
  var years = Object.keys(yearCollabs).map(Number).sort();
  var collabCounts = years.map(function(y) { return yearCollabs[y]; });
  var coordinatorCounts = years.map(function(y) { return yearRoles[y].coordinator; });
  var researcherCounts = years.map(function(y) { return yearRoles[y].researcher; });
  var coResearcherCounts = years.map(function(y) { return yearRoles[y].coResearcher; });
  
  var data = [
    {
      x: years,
      y: coordinatorCounts,
      name: 'As Coordinator',
      type: 'scatter',
      mode: 'lines+markers',
      stackgroup: 'one',
      line: {width: 2, color: '#28a745'},
      marker: {size: 6},
      hovertemplate: '<b>As Coordinator</b><br>Year: %{x}<br>%{y} collaborations<extra></extra>'
    },
    {
      x: years,
      y: researcherCounts,
      name: 'As Researcher',
      type: 'scatter',
      mode: 'lines+markers',
      stackgroup: 'one',
      line: {width: 2, color: '#007bff'},
      marker: {size: 6},
      hovertemplate: '<b>As Researcher</b><br>Year: %{x}<br>%{y} collaborations<extra></extra>'
    },
    {
      x: years,
      y: coResearcherCounts,
      name: 'As Co-Researcher',
      type: 'scatter',
      mode: 'lines+markers',
      stackgroup: 'one',
      line: {width: 2, color: '#ffc107'},
      marker: {size: 6},
      hovertemplate: '<b>As Co-Researcher</b><br>Year: %{x}<br>%{y} collaborations<extra></extra>'
    }
  ];
  
  var layout = {
    title: {
      text: 'Collaboration Timeline by Role',
      font: {size: 16, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Year',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Number of Collaborations',
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
  
  Plotly.newPlot('collab-timeline-{{ loop.index }}', data, layout);
})();
</script>

{# Interactive Network Visualization #}
<div id="network-{{ loop.index }}" style="width:100%;height:500px;border:1px solid #ddd;border-radius:8px;margin-bottom:20px;background:#fff;"></div>

<script>
(function() {
  // Wait for vis library to be loaded
  if (typeof vis === 'undefined') {
    console.error('vis-network library not loaded');
    return;
  }
  
  var collaborators = {{ collaborators|tojson }};
  
  if (!collaborators || Object.keys(collaborators).length === 0) {
    document.getElementById('network-{{ loop.index }}').innerHTML = 
      '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#999;">No collaboration data available</div>';
    return;
  }
  
  // Create nodes
  var nodes = [
    {
      id: 0,
      label: '{{ supervisor["name"][:20] }}',
      color: {background: '#667eea', border: '#4a5fc1'},
      font: {color: 'white', size: 14, bold: true},
      size: 35,
      title: '<b>{{ supervisor["name"] }}</b><br>Principal Researcher<br>' + 
             Object.keys(collaborators).length + ' collaborators'
    }
  ];
  
  var edges = [];
  var nodeId = 1;
  
  // Add collaborator nodes and edges
  Object.keys(collaborators).forEach(function(name) {
    var collab = collaborators[name];
    var size = 15 + Math.min(collab.count * 2, 30);
    
    // Count role types
    var roles = {coordinator: 0, researcher: 0, coResearcher: 0};
    collab.projects.forEach(function(p) {
      if (p.role === 'coordinator') roles.coordinator++;
      else if (p.role === 'researcher') roles.researcher++;
      else if (p.role === 'co-researcher') roles.coResearcher++;
    });
    
    var roleText = '';
    if (roles.coordinator > 0) roleText += roles.coordinator + ' as coordinator<br>';
    if (roles.researcher > 0) roleText += roles.researcher + ' as researcher<br>';
    if (roles.coResearcher > 0) roleText += roles.coResearcher + ' as co-researcher';
    
    // Color based on primary role
    var color = '#4facfe';
    if (roles.coordinator > roles.researcher && roles.coordinator > roles.coResearcher) {
      color = '#28a745'; // Green for coordinator
    } else if (roles.researcher > roles.coResearcher) {
      color = '#007bff'; // Blue for researcher
    } else {
      color = '#ffc107'; // Yellow for co-researcher
    }
    
    nodes.push({
      id: nodeId,
      label: name.substring(0, 18) + (name.length > 18 ? '...' : ''),
      color: {background: color, border: '#333'},
      size: size,
      title: '<b>' + name + '</b><br>' + collab.count + ' shared project(s)<br>' + roleText
    });
    
    edges.push({
      from: 0,
      to: nodeId,
      value: collab.count,
      title: collab.count + ' shared project(s)',
      color: {color: '#999', opacity: 0.5},
      width: Math.min(collab.count / 2, 5)
    });
    
    nodeId++;
  });
  
  var container = document.getElementById('network-{{ loop.index }}');
  
  if (!container) {
    console.error('Container network-{{ loop.index }} not found');
    return;
  }
  
  try {
    var data = {
      nodes: new vis.DataSet(nodes), 
      edges: new vis.DataSet(edges)
    };
    
    var options = {
      physics: {
        enabled: true,
        stabilization: {iterations: 150},
        barnesHut: {
          gravitationalConstant: -10000,
          springConstant: 0.04,
          springLength: 180,
          avoidOverlap: 0.5
        }
      },
      interaction: {
        hover: true,
        tooltipDelay: 100,
        navigationButtons: true,
        keyboard: true
      },
      nodes: {
        shape: 'dot',
        font: {size: 11, face: 'Arial'}
      },
      edges: {
        smooth: {type: 'continuous'}
      }
    };
    
    var network = new vis.Network(container, data, options);
    
    // Handle stabilization
    network.on('stabilizationIterationsDone', function() {
      network.setOptions({physics: false});
    });
    
  } catch (error) {
    console.error('Error creating network visualization:', error);
    container.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#dc3545;">Error loading network visualization</div>';
  }
})();
</script>

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 6px; margin-bottom: 20px;">
  <p style="margin: 5px 0; font-size: 14px;">
    <strong>📊 Collaboration Role Distribution:</strong>
  </p>
  <div style="display: flex; gap: 15px; margin: 10px 0; flex-wrap: wrap;">
    <div style="display: flex; align-items: center; gap: 5px;">
      <div style="width: 16px; height: 16px; background: #28a745; border-radius: 50%;"></div>
      <span style="font-size: 13px;">As Coordinator</span>
    </div>
    <div style="display: flex; align-items: center; gap: 5px;">
      <div style="width: 16px; height: 16px; background: #007bff; border-radius: 50%;"></div>
      <span style="font-size: 13px;">As Researcher</span>
    </div>
    <div style="display: flex; align-items: center; gap: 5px;">
      <div style="width: 16px; height: 16px; background: #ffc107; border-radius: 50%;"></div>
      <span style="font-size: 13px;">As Co-Researcher</span>
    </div>
  </div>
  
  {% set top_collab = collaborators.items()|sort(attribute='1.count', reverse=True)|first %}
  <ul style="margin: 10px 0; font-size: 13px; color: #555;">
    <li><strong>Most frequent collaborator:</strong> 
      {{ top_collab[0] }} ({{ top_collab[1]['count'] }} project{{ 's' if top_collab[1]['count'] > 1 else '' }})
    </li>
    <li><strong>Collaboration intensity:</strong>
      {% if (total_collabs / collaborators|length) >= 5 %}
        <span style="color: #28a745; font-weight: bold;">● High</span> - Strong recurring partnerships
      {% elif (total_collabs / collaborators|length) >= 2 %}
        <span style="color: #ffc107; font-weight: bold;">● Medium</span> - Regular collaborations
      {% else %}
        <span style="color: #6c757d;">● Low</span> - Diverse network
      {% endif %}
    </li>
  </ul>
  
  <p style="margin: 5px 0; font-size: 12px; color: #666; font-style: italic;">
    💡 <strong>How to interpret:</strong> The central node (purple) represents the researcher. 
    Node colors indicate the primary collaboration role. Node size reflects the number of shared projects. 
    You can drag nodes, zoom, and hover for details.
  </p>
</div>

{# Detailed Collaborators Table #}
<details style="margin-bottom: 20px;">
  <summary style="cursor: pointer; padding: 10px; background: #e9ecef; border-radius: 4px; font-weight: bold;">
    📋 View Detailed Collaborators List ({{ collaborators|length }} total)
  </summary>
  <div style="margin-top: 10px;">
    <table style="width:100%; border-collapse: collapse; font-size: 13px;">
      <thead>
        <tr style="background-color: #e9ecef;">
          <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6;">Collaborator</th>
          <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 100px;">Projects</th>
          <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 150px;">Roles</th>
        </tr>
      </thead>
      <tbody>
        {% for name, data in collaborators.items()|sort(attribute='1.count', reverse=True) %}
        <tr>
          <td style="padding: 8px; border: 1px solid #dee2e6;">{{ name }}</td>
          <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">
            {{ data['count'] }}
          </td>
          <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
            {% set roles = {'coordinator': 0, 'researcher': 0, 'co-researcher': 0} %}
            {% for project in data['projects'] %}
              {% if project['role'] in roles %}
                {% set _ = roles.__setitem__(project['role'], roles[project['role']] + 1) %}
              {% endif %}
            {% endfor %}
            <small>
              {% if roles['coordinator'] > 0 %}
                <span style="color: #28a745;">●{{ roles['coordinator'] }} coord</span>
              {% endif %}
              {% if roles['researcher'] > 0 %}
                <span style="color: #007bff;">●{{ roles['researcher'] }} res</span>
              {% endif %}
              {% if roles['co-researcher'] > 0 %}
                <span style="color: #ffc107;">●{{ roles['co-researcher'] }} co-res</span>
              {% endif %}
            </small>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</details>
{% endif %}

{% if supervisor['research_projects'] %}
#### Research Projects ({{ supervisor['research_projects']|length }})

<table style="width:100%; border-collapse: collapse; margin: 15px 0; font-size: 14px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6;">Title</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 100px;">Period</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Status</th>
    </tr>
  </thead>
  <tbody>
    {% for project in supervisor['research_projects'] %}
    <tr>
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        <strong>{{ project['title'] }}</strong>
        {% if project['code'] %}
        <br><small style="color: #666;">Code: {{ project['code'] }}</small>
        {% endif %}
        {% if project['knowledge_area'] %}
        <br><small style="color: #666;">Area: {{ project['knowledge_area'] }}</small>
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
          <span style="color: #28a745; font-weight: bold;">● Active</span>
        {% elif project['status'] and (project['status'] == 'CONCLUIDO' or project['status'] == 'Concluído') %}
          <span style="color: #6c757d;">○ Completed</span>
        {% elif project['end_date'] and project['end_date']|length >= 8 %}
          {% set end_year_int = ('20' + project['end_date'][-2:])|int %}
          {% if end_year_int >= 2024 %}
            <span style="color: #28a745; font-weight: bold;">● Active</span>
          {% else %}
            <span style="color: #6c757d;">○ Completed</span>
          {% endif %}
        {% else %}
          <span style="color: #999;">- Undefined</span>
        {% endif %}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endif %}

{% if supervisor['ic_supervisions'] %}
#### Scientific Initiation Supervisions ({{ supervisor['ic_supervisions']|length }})

<table style="width:100%; border-collapse: collapse; margin: 15px 0; font-size: 14px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6;">Student</th>
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6;">Project</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Year</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 100px;">Modality</th>
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
        <small>{{ supervision['project_title'] if supervision['project_title'] else supervision['research_project_title'] if supervision['research_project_title'] else 'Not specified' }}</small>
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {{ supervision['year'] }}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if supervision['modality'] == 'Bolsista' %}
          <span style="color: #007bff; font-weight: bold;">💰 Scholarship</span>
        {% else %}
          <span style="color: #6c757d;">🤝 Volunteer</span>
        {% endif %}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% set current_year = 2025 %}
        {% if supervision['year'] >= current_year - 1 %}
          <span style="color: #28a745; font-weight: bold;">● Active</span>
        {% else %}
          <span style="color: #6c757d;">○ Completed</span>
        {% endif %}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endif %}

{% if not supervisor['research_projects'] and not supervisor['ic_supervisions'] %}
<p style="color: #6c757d; font-style: italic;">No projects or supervisions registered.</p>
{% endif %}

---

{% endfor %}
