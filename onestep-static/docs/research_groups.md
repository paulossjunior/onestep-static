# Research Groups

{% set df = pd_read_json("../data/research_group.json") %}
{% set df = df[df['campus'] == 'Serra'] %}
{% set df = df.sort_values('name') %}

{# Load projects to check which groups have projects #}
{% set projects_check_df = pd_read_json("../data/research_projects.json") %}
{% set projects_check_df = projects_check_df[projects_check_df['campus'] == 'Serra'] %}

{% for index, row in df.iterrows() %}
    {# Create anchor link for group name only if group has projects #}
    {% set group_name_str = row['name']|string %}
    {% set group_anchor = group_name_str|replace(' ', '-')|replace(',', '')|replace(':', '')|replace('.', '')|lower %}
    {% set group_has_projects = projects_check_df[projects_check_df['research_group'] == group_name_str] %}
    {% if group_has_projects|length > 0 %}
        {% set _ = df.at.__setitem__((index, "name"), "[" + group_name_str + "](#" + group_anchor + ")") %}
    {% else %}
        {% set _ = df.at.__setitem__((index, "name"), group_name_str) %}
    {% endif %}
    {% set _ = df.at.__setitem__((index, "repository"), "[Link](" + row.repository + ")") %}
    {% set leader_links = [] %}
    {% for leader in row.leaders %}
        {% set _ = leader_links.append("[" + leader.name + "](mailto:" + leader.email + ")") %}
    {% endfor %}
    {% set _ = df.at.__setitem__((index, "leaders"), "<br>".join(leader_links)) %}
{% endfor %}

{% set df = df.rename(columns={
    'short_name': 'Short Name',
    'name': 'Name',
    'campus': 'Campus',
    'knowledge_area': 'Knowledge Area',
    'repository': 'Repository',
    'leaders': 'Leaders'
}) %}

{{ df | convert_to_md_table }}

---

{% set groups_df = pd_read_json("../data/research_group.json") %}
{% set groups_df = groups_df[groups_df['campus'] == 'Serra'] %}
{% set groups_df = groups_df.sort_values('name') %}

{% set projects_df = pd_read_json("../data/research_projects.json") %}
{% set projects_df = projects_df[projects_df['campus'] == 'Serra'] %}

{% for group_index, group in groups_df.iterrows() %}
{% set group_name = group['name'] %}
{% set group_projects = projects_df[projects_df['research_group'] == group_name].copy() %}

{% if group_projects|length > 0 %}

{# Remove duplicates based on project ID #}
{% set group_projects = group_projects.drop_duplicates(subset=['id'], keep='first') %}

{# Create anchor ID for the group #}
{% set group_anchor = group_name|replace(' ', '-')|replace(',', '')|replace(':', '')|replace('.', '')|lower %}

## <span id="{{ group_anchor }}">{{ group_name }}</span>

**Total projects:** {{ group_projects|length }}

{# Prepare table data FIRST #}
{% set group_projects = group_projects.sort_values('title') %}
{% set group_projects = group_projects.reset_index(drop=True) %}

{% for proj_index, project in group_projects.iterrows() %}
{% set coordinator_link = "[" + project.coordinator + "](mailto:" + project.coordinator_email + ")" if project.coordinator_email else project.coordinator %}
{% set _ = group_projects.at.__setitem__((proj_index, "coordinator"), coordinator_link) %}
{% set period = (project.start_date|string) + " to " + (project.end_date|string) %}
{% set _ = group_projects.at.__setitem__((proj_index, "period"), period) %}
{% set researchers_str = project.researchers|join(', ') if project.researchers and project.researchers|length > 0 else '' %}
{% set _ = group_projects.at.__setitem__((proj_index, "researchers"), researchers_str) %}
{% set students_str = project.students|join(', ') if project.students and project.students|length > 0 else '' %}
{% set _ = group_projects.at.__setitem__((proj_index, "students"), students_str) %}
{% set keywords_str = project.keywords|join(', ') if project.keywords and project.keywords|length > 0 else '' %}
{% set _ = group_projects.at.__setitem__((proj_index, "keywords"), keywords_str) %}
{% set pub_fund = "Pub: " + (project.publications_count|string) + " / Fund: " + (project.funding_count|string) %}
{% set _ = group_projects.at.__setitem__((proj_index, "pub_fund"), pub_fund) %}
{% endfor %}

{% set group_projects = group_projects.rename(columns={
    'title': 'Title',
    'period': 'Period',
    'coordinator': 'Coordinator',
    'researchers': 'Researchers',
    'students': 'Students',
    'research_line': 'Research Line',
    'nature': 'Nature',
    'keywords': 'Keywords',
    'partner': 'Partner',
    'pub_fund': 'Pub/Fund'
}) %}

{% set group_projects = group_projects[['Title', 'Period', 'Coordinator', 'Researchers', 'Students', 'Research Line', 'Nature', 'Keywords', 'Partner', 'Pub/Fund']] %}

{{ group_projects | convert_to_md_table }}

---

### Visualizations

{# Extract years and categorize projects #}
{% set original_projects = projects_df[projects_df['research_group'] == group_name].copy() %}
{% set original_projects = original_projects.drop_duplicates(subset=['id'], keep='first') %}

{% set year_all = {} %}
{% set year_funded = {} %}
{% set year_partner = {} %}

{% for proj_index, project in original_projects.iterrows() %}
{% set start_date = project.start_date %}
{% if start_date %}
{% set parts = start_date.split('-') %}
{% if parts|length == 3 %}
{% set year = parts[2] %}
{% if year|length == 2 %}
{% set year_int = year|int %}
{% set full_year = (2000 + year_int) if year_int < 50 else (1900 + year_int) %}
{% else %}
{% set full_year = year|int %}
{% endif %}

{# Count all projects #}
{% if full_year in year_all %}
{% set _ = year_all.__setitem__(full_year, year_all[full_year] + 1) %}
{% else %}
{% set _ = year_all.__setitem__(full_year, 1) %}
{% endif %}

{# Count projects with funding #}
{% if project.funding_count and project.funding_count|int > 0 %}
{% if full_year in year_funded %}
{% set _ = year_funded.__setitem__(full_year, year_funded[full_year] + 1) %}
{% else %}
{% set _ = year_funded.__setitem__(full_year, 1) %}
{% endif %}
{% endif %}

{# Count projects with partners #}
{% if project.partner and project.partner.strip() %}
{% if full_year in year_partner %}
{% set _ = year_partner.__setitem__(full_year, year_partner[full_year] + 1) %}
{% else %}
{% set _ = year_partner.__setitem__(full_year, 1) %}
{% endif %}
{% endif %}

{% endif %}
{% endif %}
{% endfor %}

{# Create timeline chart with three lines #}
{% if year_all|length > 0 %}
{% set sorted_years = year_all.keys()|list|sort %}
{% set counts_all = [] %}
{% set counts_funded = [] %}
{% set counts_partner = [] %}

{% for year in sorted_years %}
{% set _ = counts_all.append(year_all[year]) %}
{% set _ = counts_funded.append(year_funded[year] if year in year_funded else 0) %}
{% set _ = counts_partner.append(year_partner[year] if year in year_partner else 0) %}
{% endfor %}

<div id="chart-timeline-{{ group_index }}" style="width:100%;height:450px;margin-bottom:30px;"></div>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
<script>
(function() {
  var data = [
    {
      x: {{ sorted_years|tojson }},
      y: {{ counts_all|tojson }},
      text: {{ counts_all|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'All Projects',
      line: {color: '#1f77b4', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#1f77b4'}
    },
    {
      x: {{ sorted_years|tojson }},
      y: {{ counts_funded|tojson }},
      text: {{ counts_funded|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'With Funding',
      line: {color: '#2ca02c', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#2ca02c'}
    },
    {
      x: {{ sorted_years|tojson }},
      y: {{ counts_partner|tojson }},
      text: {{ counts_partner|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'With Partners',
      line: {color: '#ff7f0e', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#ff7f0e'}
    }
  ];
  
  var layout = {
    title: 'Projects Over Time by Category',
    xaxis: {
      title: 'Year',
      dtick: 1,
      tickmode: 'linear'
    },
    yaxis: {
    },
    hovermode: 'x unified',
    legend: {
      x: 0.02,
      y: 0.98,
      bgcolor: 'rgba(255,255,255,0.8)',
      bordercolor: '#ccc',
      borderwidth: 1
    }
  };
  
  Plotly.newPlot('chart-timeline-{{ group_index }}', data, layout);
})();
</script>

{% endif %}

{# Count students over time and create student-project mapping #}
{% set year_students = {} %}
{% set year_students_funded = {} %}
{% set year_students_unfunded = {} %}
{% set student_projects = {} %}

{% for proj_index, project in original_projects.iterrows() %}
{% set start_date = project.start_date %}
{% if start_date %}
{% set parts = start_date.split('-') %}
{% if parts|length == 3 %}
{% set year = parts[2] %}
{% if year|length == 2 %}
{% set year_int = year|int %}
{% set full_year = (2000 + year_int) if year_int < 50 else (1900 + year_int) %}
{% else %}
{% set full_year = year|int %}
{% endif %}

{# Count students per year #}
{% if project.students and project.students|length > 0 %}
{% set student_count = project.students|length %}
{% set has_funding = project.funding_count and project.funding_count|int > 0 %}

{# Total students #}
{% if full_year in year_students %}
{% set _ = year_students.__setitem__(full_year, year_students[full_year] + student_count) %}
{% else %}
{% set _ = year_students.__setitem__(full_year, student_count) %}
{% endif %}

{# Students in funded projects #}
{% if has_funding %}
{% if full_year in year_students_funded %}
{% set _ = year_students_funded.__setitem__(full_year, year_students_funded[full_year] + student_count) %}
{% else %}
{% set _ = year_students_funded.__setitem__(full_year, student_count) %}
{% endif %}
{% else %}
{# Students in unfunded projects #}
{% if full_year in year_students_unfunded %}
{% set _ = year_students_unfunded.__setitem__(full_year, year_students_unfunded[full_year] + student_count) %}
{% else %}
{% set _ = year_students_unfunded.__setitem__(full_year, student_count) %}
{% endif %}
{% endif %}

{# Map students to projects #}
{% for student in project.students %}
{% set student_name = student.strip() %}
{% if student_name %}
{% if student_name not in student_projects %}
{% set _ = student_projects.__setitem__(student_name, []) %}
{% endif %}
{% set _ = student_projects[student_name].append(project.title) %}
{% endif %}
{% endfor %}
{% endif %}

{% endif %}
{% endif %}
{% endfor %}

{# Create students timeline chart #}
{% if year_students|length > 0 %}
{% set sorted_years_students = year_students.keys()|list|sort %}
{% set counts_students = [] %}
{% set counts_students_funded = [] %}
{% set counts_students_unfunded = [] %}

{% for year in sorted_years_students %}
{% set _ = counts_students.append(year_students[year]) %}
{% set _ = counts_students_funded.append(year_students_funded[year] if year in year_students_funded else 0) %}
{% set _ = counts_students_unfunded.append(year_students_unfunded[year] if year in year_students_unfunded else 0) %}
{% endfor %}

<div id="chart-students-{{ group_index }}" style="width:100%;height:450px;margin-bottom:30px;"></div>

<script>
(function() {
  var data = [
    {
      x: {{ sorted_years_students|tojson }},
      y: {{ counts_students|tojson }},
      text: {{ counts_students|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'All Students',
      line: {color: '#d62728', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#d62728'}
    },
    {
      x: {{ sorted_years_students|tojson }},
      y: {{ counts_students_funded|tojson }},
      text: {{ counts_students_funded|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'With Funding',
      line: {color: '#2ca02c', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#2ca02c'}
    },
    {
      x: {{ sorted_years_students|tojson }},
      y: {{ counts_students_unfunded|tojson }},
      text: {{ counts_students_unfunded|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Without Funding',
      line: {color: '#ff7f0e', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#ff7f0e'}
    }
  ];
  
  var layout = {
    title: 'Number of Students Over Time',
    xaxis: {
      title: 'Year',
      dtick: 1,
      tickmode: 'linear'
    },
    yaxis: {
    },
    hovermode: 'x unified',
    legend: {
      x: 0.02,
      y: 0.98,
      bgcolor: 'rgba(255,255,255,0.8)',
      bordercolor: '#ccc',
      borderwidth: 1
    }
  };
  
  Plotly.newPlot('chart-students-{{ group_index }}', data, layout);
})();
</script>

{% endif %}

{# Create students table #}
{% if student_projects|length > 0 %}

### Students and Their Projects

**Total unique students:** {{ student_projects|length }}

{# Create list with student name and project count for sorting #}
{% set students_with_count = [] %}
{% for student_name, projects_list in student_projects.items() %}
{% set _ = students_with_count.append((student_name, projects_list, projects_list|length)) %}
{% endfor %}

{# Sort by count (third element) in descending order #}
{% set students_sorted = students_with_count|sort(attribute='2', reverse=True) %}

<table>
<thead>
<tr>
<th>Student</th>
<th>Projects</th>
<th>Total</th>
</tr>
</thead>
<tbody>
{% for student_name, projects_list, count in students_sorted %}
<tr>
<td>{{ student_name }}</td>
<td>
<ul style="margin: 0; padding-left: 20px;">
{% for project in projects_list %}
<li>{{ project }}</li>
{% endfor %}
</ul>
</td>
<td style="text-align: center;">{{ count }}</td>
</tr>
{% endfor %}
</tbody>
</table>

{% endif %}

{# Count researcher participation (coordinators + researchers) #}
{% set researcher_projects = {} %}

{% for proj_index, project in original_projects.iterrows() %}
{# Add coordinator #}
{% if project.coordinator and project.coordinator.strip() %}
{% set coordinator_name = project.coordinator.strip() %}
{% if coordinator_name not in researcher_projects %}
{% set _ = researcher_projects.__setitem__(coordinator_name, []) %}
{% endif %}
{% set _ = researcher_projects[coordinator_name].append(project.title) %}
{% endif %}

{# Add researchers #}
{% if project.researchers and project.researchers|length > 0 %}
{% for researcher in project.researchers %}
{% set researcher_name = researcher.strip() %}
{% if researcher_name %}
{% if researcher_name not in researcher_projects %}
{% set _ = researcher_projects.__setitem__(researcher_name, []) %}
{% endif %}
{% set _ = researcher_projects[researcher_name].append(project.title) %}
{% endif %}
{% endfor %}
{% endif %}
{% endfor %}

{# Count how many projects each researcher participated in #}
{% set researcher_participation_distribution = {} %}
{% for researcher_name, projects_list in researcher_projects.items() %}
{% set count = projects_list|length %}
{% if count in researcher_participation_distribution %}
{% set _ = researcher_participation_distribution.__setitem__(count, researcher_participation_distribution[count] + 1) %}
{% else %}
{% set _ = researcher_participation_distribution.__setitem__(count, 1) %}
{% endif %}
{% endfor %}

{# Create bar chart for researcher participation distribution #}
{% if researcher_participation_distribution|length > 0 %}
{% set sorted_researcher_participation = researcher_participation_distribution.keys()|list|sort %}
{% set researcher_counts = [] %}

{% for num_projects in sorted_researcher_participation %}
{% set _ = researcher_counts.append(researcher_participation_distribution[num_projects]) %}
{% endfor %}

### Researcher Participation Distribution

This bar chart shows how many researchers (coordinators and researchers) participated in multiple projects within this research group. Each bar represents a participation level: for example, if the bar at position "1" shows 5 researchers, it means 5 researchers participated in exactly one project. This distribution helps understand researcher engagement patterns and identifies researchers with sustained involvement across multiple projects.

<div id="chart-researcher-participation-{{ group_index }}" style="width:100%;height:450px;margin-bottom:30px;"></div>

<script>
(function() {
  var data = [{
    x: {{ sorted_researcher_participation|tojson }},
    y: {{ researcher_counts|tojson }},
    text: {{ researcher_counts|tojson }},
    type: 'bar',
    marker: {
      color: '#2ca02c',
      line: {
        color: '#1e7d1e',
        width: 1.5
      }
    },
    textposition: 'outside',
    textfont: {size: 12, color: '#2ca02c'},
    hovertemplate: '<b>%{x} project(s)</b><br>%{y} researchers<extra></extra>'
  }];
  
  var layout = {
    title: 'Researcher Participation Distribution (Total: {{ researcher_projects|length }} unique researchers)',
    xaxis: {
      title: 'Number of Projects per Researcher',
      dtick: 1,
      tickmode: 'linear'
    },
    yaxis: {
      title: 'Number of Researchers'
    },
    hovermode: 'closest'
  };
  
  Plotly.newPlot('chart-researcher-participation-{{ group_index }}', data, layout);
})();
</script>

{# List highly engaged researchers (3 or more projects) #}
{% set highly_engaged_researchers = [] %}
{% for researcher_name, projects_list in researcher_projects.items() %}
{% set count = projects_list|length %}
{% if count >= 3 %}
{% set _ = highly_engaged_researchers.append((researcher_name, count)) %}
{% endif %}
{% endfor %}

{% if highly_engaged_researchers|length > 0 %}
{% set highly_engaged_researchers = highly_engaged_researchers|sort(attribute='1', reverse=True) %}

<div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
  <h4 style="margin-top: 0;">Highly Engaged Researchers (3+ Projects)</h4>
  <p>The following researchers have demonstrated exceptional commitment by participating in 3 or more research projects within this group:</p>
  <table style="width:100%; border-collapse: collapse;">
    <thead>
      <tr style="background-color: #e9ecef;">
        <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Researcher Name</th>
        <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Number of Projects</th>
      </tr>
    </thead>
    <tbody>
      {% for researcher_name, count in highly_engaged_researchers %}
      <tr>
        <td style="padding: 8px; border: 1px solid #dee2e6;">{{ researcher_name }}</td>
        <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;"><strong>{{ count }}</strong></td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  <p style="margin-bottom: 0; margin-top: 15px; font-size: 0.9em; color: #6c757d;">
    <strong>Total:</strong> {{ highly_engaged_researchers|length }} researcher(s) with sustained research involvement
  </p>
</div>

{% endif %}

{% endif %}

{# Load network statistics from pre-generated file #}
{% set network_stats_all = pd_read_json("../data/network_stats.json") %}
{% set stats_dict = network_stats_all.to_dict() if not network_stats_all.empty else {} %}
{% set stats = stats_dict.get(group_name, {}) if stats_dict else {} %}

{# Create collaboration network graph using pre-calculated data #}
{% if stats and stats.get('graph') %}
### Collaboration Network

**This network graph visualizes the collaboration relationships between all people involved in the research group's projects.**

<div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
  <h4 style="margin-top: 0;">How to Read This Graph:</h4>
  <ul style="margin-bottom: 0;">
    <li><strong>Nodes (circles)</strong> represent people: coordinators, researchers, and students</li>
    <li><strong>Node size</strong> indicates how many connections a person has (larger = more collaborative)</li>
    <li><strong>Edges (lines)</strong> connect people who worked together on projects</li>
    <li><strong>Edge thickness</strong> shows collaboration strength (thicker = more projects together)</li>
    <li><strong>Colors</strong>: Red = Coordinators, Turquoise = Researchers, Light Green = Students</li>
    <li><strong>Interactive</strong>: Hover over nodes/edges for details, drag to rearrange, scroll to zoom</li>
  </ul>
</div>

<div id="network-{{ group_index }}" style="width:100%;height:800px;border:1px solid #ddd;border-radius:8px;background-color:white;"></div>

<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<script>
(function() {
  // Load pre-calculated network data
  var graphData = {{ stats.graph|tojson }};
  
  // Create network
  var container = document.getElementById('network-{{ group_index }}');
  var data = {
    nodes: new vis.DataSet(graphData.nodes),
    edges: new vis.DataSet(graphData.edges)
  };
  
  var options = {
    nodes: {
      shape: 'dot',
      font: {
        size: 12,
        face: 'Arial'
      }
    },
    edges: {
      smooth: {
        type: 'continuous'
      },
      color: {
        inherit: false,
        color: '#848484',
        highlight: '#FF0000'
      }
    },
    groups: {
      coordinator: {
        color: {
          background: '#FF6B6B',
          border: '#C92A2A',
          highlight: {
            background: '#FF8787',
            border: '#C92A2A'
          }
        }
      },
      researcher: {
        color: {
          background: '#4ECDC4',
          border: '#0B7285',
          highlight: {
            background: '#66D9E8',
            border: '#0B7285'
          }
        }
      },
      student: {
        color: {
          background: '#95E1D3',
          border: '#087F5B',
          highlight: {
            background: '#B2F2E8',
            border: '#087F5B'
          }
        }
      }
    },
    physics: {
      stabilization: {
        iterations: 300
      },
      barnesHut: {
        gravitationalConstant: -15000,
        springConstant: 0.02,
        springLength: 150,
        avoidOverlap: 0.5
      }
    },
    interaction: {
      hover: true,
      tooltipDelay: 100
    }
  };
  
  var network = new vis.Network(container, data, options);
  
  // Add legend
  var legend = document.createElement('div');
  legend.style.cssText = 'position:absolute;top:10px;right:10px;background:rgba(255,255,255,0.95);padding:15px;border:2px solid #ddd;border-radius:8px;font-size:13px;box-shadow:0 2px 8px rgba(0,0,0,0.1);';
  legend.innerHTML = '<strong style="font-size:14px;">Legend</strong><br><br>' +
    '<div style="margin:5px 0;"><span style="color:#FF6B6B;font-size:20px;">●</span> <strong>Coordinators</strong></div>' +
    '<div style="margin:5px 0;"><span style="color:#4ECDC4;font-size:20px;">●</span> <strong>Researchers</strong></div>' +
    '<div style="margin:5px 0;"><span style="color:#95E1D3;font-size:20px;">●</span> <strong>Students</strong></div>' +
    '<hr style="margin:10px 0;">' +
    '<small><strong>Node size:</strong> # connections<br><strong>Edge width:</strong> # collaborations</small>';
  container.style.position = 'relative';
  container.appendChild(legend);
})();
</script>
{% endif %}

{% if stats and stats.get('total_people') %}
<div style="background-color: #e7f5ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
  <h4 style="margin-top: 0; color: #1971c2;">Network Statistics</h4>
  <table style="width:100%; border-collapse: collapse;">
    <tr>
      <td style="padding:5px;"><strong>Total People:</strong></td>
      <td>{{ stats.get('total_people', 0) }}</td>
      <td style="padding:5px;"><strong>Total Connections:</strong></td>
      <td>{{ stats.get('total_connections', 0) }}</td>
    </tr>
    <tr>
      <td style="padding:5px;"><strong>Coordinators:</strong></td>
      <td>{{ stats.get('coordinators', 0) }}</td>
      <td style="padding:5px;"><strong>Researchers:</strong></td>
      <td>{{ stats.get('researchers', 0) }}</td>
    </tr>
    <tr>
      <td style="padding:5px;"><strong>Students:</strong></td>
      <td>{{ stats.get('students', 0) }}</td>
      <td style="padding:5px;"><strong>Avg. Connections/Person:</strong></td>
      <td>{{ stats.get('avg_connections_per_person', 0) }}</td>
    </tr>
    {% if stats.get('most_connected_person') %}
    <tr>
      <td colspan="4" style="padding:5px;">
        <strong>Most Connected Person:</strong> {{ stats.most_connected_person.get('name', '') }} 
        ({{ stats.most_connected_person.get('connections', 0) }} connections)
      </td>
    </tr>
    {% endif %}
    {% if stats.get('strongest_collaboration') %}
    <tr>
      <td colspan="4" style="padding:5px;">
        <strong>Strongest Collaboration:</strong> {{ stats.strongest_collaboration.get('people', [])|join(' ↔ ') }} 
        ({{ stats.strongest_collaboration.get('projects_together', 0) }} projects together)
      </td>
    </tr>
    {% endif %}
  </table>
</div>
{% endif %}

{% endif %}
{% endfor %}


