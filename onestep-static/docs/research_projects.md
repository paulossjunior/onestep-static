# Research Projects

{% set df = pd_read_json("../data/research_projects.json") %}
{% set df = df[df['campus'] == 'Serra'] %}

{# Extract year from start_date and add as a column #}
{% set years = [] %}
{% for index, row in df.iterrows() %}
    {% set start_date = row.start_date %}
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
            {% set _ = years.append(full_year) %}
        {% else %}
            {% set _ = years.append(0) %}
        {% endif %}
    {% else %}
        {% set _ = years.append(0) %}
    {% endif %}
{% endfor %}
{% set _ = df.__setitem__('year', years) %}

{# Sort by year descending, then by title #}
{% set df = df.sort_values(['year', 'title'], ascending=[False, True]) %}

{# Get unique years for sections #}
{% set unique_years = df['year'].unique()|list %}
{% set unique_years = unique_years|sort(reverse=True) %}

{# Display statistics #}
**Total Projects:** {{ df|length }}  
**Years:** {{ unique_years|length }} ({{ unique_years[-1] if unique_years else 'N/A' }} - {{ unique_years[0] if unique_years else 'N/A' }})

---

## Visualizations

This section presents visual analytics of research projects over time, providing insights into project trends, student involvement, and participation patterns.

### Projects Over Time

The following chart shows the evolution of research projects across mutually exclusive categories. The **All Projects** line (bold) represents the total. Projects are categorized as: **Funding + Partners** (both), **Only Funding** (no partners), **Only Partners** (no funding), or **Neither** (independent projects). The sum of the four categories equals the total.

{# Count projects by year and category (mutually exclusive) #}
{% set year_all = {} %}
{% set year_both = {} %}
{% set year_only_funding = {} %}
{% set year_only_partner = {} %}
{% set year_neither = {} %}
{% set year_students = {} %}
{% set year_students_funded = {} %}
{% set year_students_unfunded = {} %}

{% for index, row in df.iterrows() %}
{% set start_date = row.start_date %}
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

{# Check if has funding or partner #}
{% set has_funding = row.funding_count and row.funding_count|int > 0 %}
{% set has_partner = row.partner and row.partner.strip() %}

{# Categorize into mutually exclusive groups #}
{% if has_funding and has_partner %}
{# Both funding and partner #}
{% if full_year in year_both %}
{% set _ = year_both.__setitem__(full_year, year_both[full_year] + 1) %}
{% else %}
{% set _ = year_both.__setitem__(full_year, 1) %}
{% endif %}
{% elif has_funding %}
{# Only funding #}
{% if full_year in year_only_funding %}
{% set _ = year_only_funding.__setitem__(full_year, year_only_funding[full_year] + 1) %}
{% else %}
{% set _ = year_only_funding.__setitem__(full_year, 1) %}
{% endif %}
{% elif has_partner %}
{# Only partner #}
{% if full_year in year_only_partner %}
{% set _ = year_only_partner.__setitem__(full_year, year_only_partner[full_year] + 1) %}
{% else %}
{% set _ = year_only_partner.__setitem__(full_year, 1) %}
{% endif %}
{% else %}
{# Neither funding nor partner #}
{% if full_year in year_neither %}
{% set _ = year_neither.__setitem__(full_year, year_neither[full_year] + 1) %}
{% else %}
{% set _ = year_neither.__setitem__(full_year, 1) %}
{% endif %}
{% endif %}

{# Count students per year #}
{% if row.students and row.students|length > 0 %}
{% set student_count = row.students|length %}
{% set has_funding = row.funding_count and row.funding_count|int > 0 %}

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
{% endif %}

{% endif %}
{% endif %}
{% endfor %}

{# Create timeline chart with five lines (mutually exclusive categories) #}
{% if year_all|length > 0 %}
{% set sorted_years = year_all.keys()|list|sort %}
{% set counts_all = [] %}
{% set counts_both = [] %}
{% set counts_only_funding = [] %}
{% set counts_only_partner = [] %}
{% set counts_neither = [] %}

{% for year in sorted_years %}
{% set _ = counts_all.append(year_all[year]) %}
{% set _ = counts_both.append(year_both[year] if year in year_both else 0) %}
{% set _ = counts_only_funding.append(year_only_funding[year] if year in year_only_funding else 0) %}
{% set _ = counts_only_partner.append(year_only_partner[year] if year in year_only_partner else 0) %}
{% set _ = counts_neither.append(year_neither[year] if year in year_neither else 0) %}
{% endfor %}

<div id="chart-timeline-all" style="width:100%;height:450px;margin-bottom:30px;"></div>

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
      line: {color: '#1f77b4', width: 3},
      marker: {size: 10},
      textposition: 'top center',
      textfont: {size: 11, color: '#1f77b4', weight: 'bold'}
    },
    {
      x: {{ sorted_years|tojson }},
      y: {{ counts_both|tojson }},
      text: {{ counts_both|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Funding + Partners',
      line: {color: '#17becf', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#17becf'}
    },
    {
      x: {{ sorted_years|tojson }},
      y: {{ counts_only_funding|tojson }},
      text: {{ counts_only_funding|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Only Funding',
      line: {color: '#2ca02c', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#2ca02c'}
    },
    {
      x: {{ sorted_years|tojson }},
      y: {{ counts_only_partner|tojson }},
      text: {{ counts_only_partner|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Only Partners',
      line: {color: '#ff7f0e', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#ff7f0e'}
    },
    {
      x: {{ sorted_years|tojson }},
      y: {{ counts_neither|tojson }},
      text: {{ counts_neither|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Neither',
      line: {color: '#d62728', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#d62728'}
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
  
  Plotly.newPlot('chart-timeline-all', data, layout);
})();
</script>

{% endif %}

### Project Status Over Time

This chart shows the distribution of projects by their completion status. The **Completed** line represents projects that have finished, while the **Ongoing** line shows projects that are still in progress. This helps track the balance between concluded research and active investigations.

{# Count completed and ongoing projects by year #}
{% set year_completed = {} %}
{% set year_ongoing = {} %}
{% set current_year = 2025 %}

{% for index, row in df.iterrows() %}
{% set start_date = row.start_date %}
{% set end_date = row.end_date %}
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

{# Determine if project is completed or ongoing #}
{% set is_completed = false %}
{% if end_date %}
{% set end_parts = end_date.split('-') %}
{% if end_parts|length == 3 %}
{% set end_year = end_parts[2] %}
{% if end_year|length == 2 %}
{% set end_year_int = end_year|int %}
{% set end_full_year = (2000 + end_year_int) if end_year_int < 50 else (1900 + end_year_int) %}
{% else %}
{% set end_full_year = end_year|int %}
{% endif %}
{% if end_full_year < current_year %}
{% set is_completed = true %}
{% endif %}
{% endif %}
{% endif %}

{# Count by status #}
{% if is_completed %}
{% if full_year in year_completed %}
{% set _ = year_completed.__setitem__(full_year, year_completed[full_year] + 1) %}
{% else %}
{% set _ = year_completed.__setitem__(full_year, 1) %}
{% endif %}
{% else %}
{% if full_year in year_ongoing %}
{% set _ = year_ongoing.__setitem__(full_year, year_ongoing[full_year] + 1) %}
{% else %}
{% set _ = year_ongoing.__setitem__(full_year, 1) %}
{% endif %}
{% endif %}

{% endif %}
{% endif %}
{% endfor %}

{# Create status chart #}
{% if year_completed|length > 0 or year_ongoing|length > 0 %}
{% set all_years = [] %}
{% for year in year_completed.keys() %}
{% if year not in all_years %}
{% set _ = all_years.append(year) %}
{% endif %}
{% endfor %}
{% for year in year_ongoing.keys() %}
{% if year not in all_years %}
{% set _ = all_years.append(year) %}
{% endif %}
{% endfor %}
{% set sorted_years_status = all_years|sort %}
{% set counts_completed = [] %}
{% set counts_ongoing = [] %}

{% for year in sorted_years_status %}
{% set _ = counts_completed.append(year_completed[year] if year in year_completed else 0) %}
{% set _ = counts_ongoing.append(year_ongoing[year] if year in year_ongoing else 0) %}
{% endfor %}

<div id="chart-status-all" style="width:100%;height:450px;margin-bottom:30px;"></div>

<script>
(function() {
  var data = [
    {
      x: {{ sorted_years_status|tojson }},
      y: {{ counts_completed|tojson }},
      text: {{ counts_completed|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Completed',
      line: {color: '#9467bd', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#9467bd'}
    },
    {
      x: {{ sorted_years_status|tojson }},
      y: {{ counts_ongoing|tojson }},
      text: {{ counts_ongoing|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Ongoing',
      line: {color: '#17becf', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#17becf'}
    }
  ];
  
  var layout = {
    title: 'Project Status Over Time',
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
  
  Plotly.newPlot('chart-status-all', data, layout);
})();
</script>

{% endif %}

### Ongoing Projects - Expected Completion by Year

This chart shows how many ongoing projects are expected to be completed each year, helping to visualize the project pipeline and upcoming milestones.

{# Collect ongoing projects and remove duplicates #}
{% set ongoing_projects_list = [] %}
{% set seen_project_ids = [] %}
{% set current_year_check = 2025 %}

{% for idx, row in df.iterrows() %}
{% set end_date = row.end_date %}
{% set is_ongoing = true %}

{% if end_date %}
{% set end_parts = end_date.split('-') %}
{% if end_parts|length == 3 %}
{% set end_year = end_parts[2] %}
{% if end_year|length == 2 %}
{% set end_year_int = end_year|int %}
{% set end_full_year = (2000 + end_year_int) if end_year_int < 50 else (1900 + end_year_int) %}
{% else %}
{% set end_full_year = end_year|int %}
{% endif %}
{% if end_full_year < current_year_check %}
{% set is_ongoing = false %}
{% endif %}
{% endif %}
{% endif %}

{# Add only if ongoing and not duplicate #}
{% if is_ongoing and row.id not in seen_project_ids %}
{% set _ = ongoing_projects_list.append(row) %}
{% set _ = seen_project_ids.append(row.id) %}
{% endif %}
{% endfor %}

{# Sort by end date #}
{% set ongoing_projects_list = ongoing_projects_list|sort(attribute='end_date') %}

{# Create completion chart #}
{% if ongoing_projects_list|length > 0 %}

**Total ongoing projects:** {{ ongoing_projects_list|length }}

{% set chart_height = ongoing_projects_list|length * 25 + 150 %}
{% if chart_height > 700 %}
{% set chart_height = 700 %}
{% endif %}

{# Count projects by completion year #}
{% set completion_by_year = {} %}

{% for project in ongoing_projects_list %}
{% set end_date = project.end_date %}
{% if end_date %}
{% set end_parts = end_date.split('-') %}
{% if end_parts|length == 3 %}
{% set end_year = end_parts[2] %}
{% if end_year|length == 2 %}
{% set end_year_int = end_year|int %}
{% set end_full_year = (2000 + end_year_int) if end_year_int < 50 else (1900 + end_year_int) %}
{% else %}
{% set end_full_year = end_year|int %}
{% endif %}

{% if end_full_year in completion_by_year %}
{% set _ = completion_by_year.__setitem__(end_full_year, completion_by_year[end_full_year] + 1) %}
{% else %}
{% set _ = completion_by_year.__setitem__(end_full_year, 1) %}
{% endif %}
{% endif %}
{% endif %}
{% endfor %}

{# Count unique researchers/coordinators and students by completion year #}
{% set researchers_by_year = {} %}
{% set students_by_year = {} %}

{% for project in ongoing_projects_list %}
{% set end_date = project.end_date %}
{% if end_date %}
{% set end_parts = end_date.split('-') %}
{% if end_parts|length == 3 %}
{% set end_year = end_parts[2] %}
{% if end_year|length == 2 %}
{% set end_year_int = end_year|int %}
{% set end_full_year = (2000 + end_year_int) if end_year_int < 50 else (1900 + end_year_int) %}
{% else %}
{% set end_full_year = end_year|int %}
{% endif %}

{# Initialize sets for this year if not exists #}
{% if end_full_year not in researchers_by_year %}
{% set _ = researchers_by_year.__setitem__(end_full_year, []) %}
{% endif %}
{% if end_full_year not in students_by_year %}
{% set _ = students_by_year.__setitem__(end_full_year, []) %}
{% endif %}

{# Add coordinator to researchers list #}
{% if project.coordinator and project.coordinator.strip() %}
{% set coordinator_name = project.coordinator.strip() %}
{% if coordinator_name not in researchers_by_year[end_full_year] %}
{% set _ = researchers_by_year[end_full_year].append(coordinator_name) %}
{% endif %}
{% endif %}

{# Add researchers to list #}
{% if project.researchers and project.researchers|length > 0 %}
{% for researcher in project.researchers %}
{% set researcher_name = researcher.strip() %}
{% if researcher_name and researcher_name not in researchers_by_year[end_full_year] %}
{% set _ = researchers_by_year[end_full_year].append(researcher_name) %}
{% endif %}
{% endfor %}
{% endif %}

{# Add students to list #}
{% if project.students and project.students|length > 0 %}
{% for student in project.students %}
{% set student_name = student.strip() %}
{% if student_name and student_name not in students_by_year[end_full_year] %}
{% set _ = students_by_year[end_full_year].append(student_name) %}
{% endif %}
{% endfor %}
{% endif %}

{% endif %}
{% endif %}
{% endfor %}

{% set sorted_years_completion = completion_by_year.keys()|list|sort %}
{% set counts_completion = [] %}
{% set counts_researchers = [] %}
{% set counts_students = [] %}

{% for year in sorted_years_completion %}
{% set _ = counts_completion.append(completion_by_year[year]) %}
{% set _ = counts_researchers.append(researchers_by_year[year]|length if year in researchers_by_year else 0) %}
{% set _ = counts_students.append(students_by_year[year]|length if year in students_by_year else 0) %}
{% endfor %}

<div id="chart-completion-ongoing" style="width:100%;height:500px;margin-bottom:30px;"></div>

<script>
(function() {
  var data = [
    {
      x: {{ sorted_years_completion|tojson }},
      y: {{ counts_completion|tojson }},
      text: {{ counts_completion|tojson }},
      name: 'Projects',
      type: 'bar',
      marker: {
        color: '#1f77b4',
        line: {
          color: '#0d47a1',
          width: 2
        }
      },
      textposition: 'outside',
      textfont: {
        size: 12,
        color: '#1f77b4'
      },
      hovertemplate: '<b>Projects</b><br>Year %{x}<br>%{y} projects<extra></extra>'
    },
    {
      x: {{ sorted_years_completion|tojson }},
      y: {{ counts_researchers|tojson }},
      text: {{ counts_researchers|tojson }},
      name: 'Researchers',
      type: 'bar',
      marker: {
        color: '#2ca02c',
        line: {
          color: '#1e7d1e',
          width: 2
        }
      },
      textposition: 'outside',
      textfont: {
        size: 12,
        color: '#2ca02c'
      },
      hovertemplate: '<b>Researchers</b><br>Year %{x}<br>%{y} researchers<extra></extra>'
    },
    {
      x: {{ sorted_years_completion|tojson }},
      y: {{ counts_students|tojson }},
      text: {{ counts_students|tojson }},
      name: 'Students',
      type: 'bar',
      marker: {
        color: '#d62728',
        line: {
          color: '#a51d1d',
          width: 2
        }
      },
      textposition: 'outside',
      textfont: {
        size: 12,
        color: '#d62728'
      },
      hovertemplate: '<b>Students</b><br>Year %{x}<br>%{y} students<extra></extra>'
    }
  ];
  
  var layout = {
    title: {
      text: 'Ongoing Projects: Completion Timeline with People Involved',
      font: {
        size: 18,
        family: 'Arial, sans-serif',
        color: '#222'
      }
    },
    xaxis: {
      title: {
        text: 'Expected Completion Year',
        font: {
          size: 14,
          family: 'Arial, sans-serif',
          color: '#333'
        }
      },
      dtick: 1,
      tickfont: {
        size: 13,
        family: 'Arial, sans-serif',
        color: '#444'
      },
      gridcolor: '#e5e5e5',
      showgrid: true
    },
    yaxis: {
      title: {
        text: 'Count',
        font: {
          size: 14,
          family: 'Arial, sans-serif',
          color: '#333'
        }
      },
      tickfont: {
        size: 13,
        family: 'Arial, sans-serif',
        color: '#444'
      },
      gridcolor: '#f0f0f0',
      showgrid: true
    },
    barmode: 'group',
    margin: {
      l: 80,
      r: 50,
      t: 90,
      b: 80
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    hovermode: 'closest',
    legend: {
      x: 0.02,
      y: 0.98,
      bgcolor: 'rgba(255,255,255,0.9)',
      bordercolor: '#ccc',
      borderwidth: 1,
      font: {
        size: 12,
        family: 'Arial, sans-serif'
      }
    }
  };
  
  Plotly.newPlot('chart-completion-ongoing', data, layout);
})();
</script>

<details style="margin: 20px 0;">
<summary style="cursor: pointer; font-weight: bold; padding: 10px; background-color: #e9ecef; border-radius: 5px;">
  📋 View Detailed List of Ongoing Projects ({{ ongoing_projects_list|length }})
</summary>
<div style="margin-top: 15px;">
<table style="width:100%; border-collapse: collapse;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Project Title</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Coordinator</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Period</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Research Group</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Funding</th>
    </tr>
  </thead>
  <tbody>
    {% for project in ongoing_projects_list %}
    <tr>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ project.title }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ project.coordinator }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ project.start_date }} to {{ project.end_date }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ project.research_group if project.research_group else "N/A" }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if project.funding_count and project.funding_count|int > 0 %}
        <span style="color: #2ca02c; font-weight: bold;">✓ Yes</span>
        {% else %}
        <span style="color: #6c757d;">✗ No</span>
        {% endif %}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
</div>
</details>

### Researcher Collaboration Network

This network graph visualizes collaboration relationships between researchers (coordinators and researchers) in ongoing projects. Node size indicates the number of collaborations, and edge thickness shows how many projects researchers have worked together on.

<div id="network-researchers-ongoing" style="width:100%;height:700px;border:1px solid #ddd;border-radius:8px;background-color:white;margin:20px 0;"></div>

<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<script>
(function() {
  var nodes = [];
  var edges = [];
  var nodeMap = {};
  var edgeMap = {};
  var nodeId = 0;
  
  // Process all ongoing projects to build network
  {% for project in ongoing_projects_list %}
  var coordinator = {{ project.coordinator|tojson }};
  var researchers = {{ project.researchers|tojson }};
  var projectTitle = {{ project.title|tojson }};
  
  // Combine coordinator and researchers
  var allResearchers = [];
  if (coordinator) {
    allResearchers.push(coordinator);
  }
  if (researchers && Array.isArray(researchers)) {
    allResearchers = allResearchers.concat(researchers);
  }
  
  // Add all researchers as nodes
  allResearchers.forEach(function(researcher) {
    if (researcher && researcher.trim()) {
      var researcherName = researcher.trim();
      if (!nodeMap[researcherName]) {
        nodeMap[researcherName] = nodeId++;
        nodes.push({
          id: nodeMap[researcherName],
          label: researcherName,
          title: 'Researcher: ' + researcherName,
          value: 1,
          group: researcher === coordinator ? 'coordinator' : 'researcher'
        });
      }
    }
  });
  
  // Create edges between all pairs of researchers in this project
  for (var i = 0; i < allResearchers.length; i++) {
    for (var j = i + 1; j < allResearchers.length; j++) {
      var r1 = allResearchers[i];
      var r2 = allResearchers[j];
      
      if (r1 && r2 && r1.trim() && r2.trim()) {
        var r1Trimmed = r1.trim();
        var r2Trimmed = r2.trim();
        
        // Skip self-relationships (same person)
        if (r1Trimmed === r2Trimmed) {
          continue;
        }
        
        var id1 = nodeMap[r1Trimmed];
        var id2 = nodeMap[r2Trimmed];
        
        // Create edge key (sorted to avoid duplicates)
        var edgeKey = id1 < id2 ? id1 + '-' + id2 : id2 + '-' + id1;
        
        if (!edgeMap[edgeKey]) {
          edgeMap[edgeKey] = {
            from: Math.min(id1, id2),
            to: Math.max(id1, id2),
            value: 0,
            projects: []
          };
        }
        edgeMap[edgeKey].value++;
        edgeMap[edgeKey].projects.push(projectTitle);
      }
    }
  }
  {% endfor %}
  
  // Convert edge map to array
  for (var key in edgeMap) {
    var edge = edgeMap[key];
    edges.push({
      from: edge.from,
      to: edge.to,
      value: edge.value,
      title: 'Collaborations: ' + edge.value + ' project(s)',
      width: Math.min(edge.value * 2, 10)
    });
  }
  
  // Update node sizes based on connections
  nodes.forEach(function(node) {
    var connections = edges.filter(function(e) {
      return e.from === node.id || e.to === node.id;
    }).length;
    node.value = connections + 1;
    node.title = node.title + ' (' + connections + ' collaboration(s))';
  });
  
  // Create network
  var container = document.getElementById('network-researchers-ongoing');
  var data = {
    nodes: new vis.DataSet(nodes),
    edges: new vis.DataSet(edges)
  };
  
  var options = {
    nodes: {
      shape: 'dot',
      font: {
        size: 14,
        face: 'Arial',
        color: '#333'
      },
      borderWidth: 2,
      shadow: true
    },
    edges: {
      smooth: {
        type: 'continuous'
      },
      color: {
        inherit: false,
        color: '#848484',
        highlight: '#FF0000'
      },
      shadow: true
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
      }
    },
    physics: {
      stabilization: {
        iterations: 400
      },
      barnesHut: {
        gravitationalConstant: -20000,
        springConstant: 0.02,
        springLength: 150,
        avoidOverlap: 0.5
      }
    },
    interaction: {
      hover: true,
      tooltipDelay: 100,
      navigationButtons: true,
      keyboard: true
    }
  };
  
  var network = new vis.Network(container, data, options);
  
  // Add legend
  var legend = document.createElement('div');
  legend.style.cssText = 'position:absolute;top:10px;right:10px;background:rgba(255,255,255,0.95);padding:15px;border:2px solid #ddd;border-radius:8px;font-size:13px;box-shadow:0 2px 8px rgba(0,0,0,0.1);z-index:1000;';
  legend.innerHTML = '<strong style="font-size:14px;">Legend</strong><br><br>' +
    '<div style="margin:5px 0;"><span style="color:#FF6B6B;font-size:20px;">●</span> <strong>Coordinators</strong></div>' +
    '<div style="margin:5px 0;"><span style="color:#4ECDC4;font-size:20px;">●</span> <strong>Researchers</strong></div>' +
    '<hr style="margin:10px 0;">' +
    '<small><strong>Node size:</strong> # collaborations<br><strong>Edge width:</strong> # projects together</small>' +
    '<hr style="margin:10px 0;">' +
    '<small><strong>Total researchers:</strong> ' + nodes.length + '<br>' +
    '<strong>Total collaborations:</strong> ' + edges.length + '</small>';
  container.style.position = 'relative';
  container.appendChild(legend);
  
  // Deep Network Analysis
  var analysis = document.createElement('div');
  analysis.style.cssText = 'background-color:#e7f5ff;padding:20px;border-radius:8px;margin-top:20px;';
  
  // 1. Basic Metrics
  var totalNodes = nodes.length;
  var totalEdges = edges.length;
  var coordinatorCount = nodes.filter(function(n) { return n.group === 'coordinator'; }).length;
  var researcherCount = nodes.filter(function(n) { return n.group === 'researcher'; }).length;
  
  // 2. Degree Distribution
  var degrees = nodes.map(function(n) { return n.value - 1; });
  var maxDegree = Math.max.apply(null, degrees);
  var minDegree = Math.min.apply(null, degrees);
  var avgDegree = degrees.reduce(function(a, b) { return a + b; }, 0) / degrees.length;
  
  // 3. Find most connected researchers (top 5)
  var sortedByDegree = nodes.slice().sort(function(a, b) { return b.value - a.value; });
  var top5 = sortedByDegree.slice(0, 5);
  
  // 4. Find strongest collaborations (top 5)
  var sortedEdges = edges.slice().sort(function(a, b) { return b.value - a.value; });
  var top5Edges = sortedEdges.slice(0, 5);
  
  // 5. Network Density (actual edges / possible edges)
  var possibleEdges = (totalNodes * (totalNodes - 1)) / 2;
  var density = (totalEdges / possibleEdges * 100).toFixed(2);
  
  // 6. Isolated nodes (no connections)
  var isolatedNodes = nodes.filter(function(n) { return n.value === 1; }).length;
  
  // 7. Average collaboration strength
  var totalCollaborations = edges.reduce(function(sum, e) { return sum + e.value; }, 0);
  var avgCollabStrength = (totalCollaborations / totalEdges).toFixed(2);
  
  // 8. Find collaboration clusters (simple heuristic: nodes with 3+ connections)
  var hubs = nodes.filter(function(n) { return n.value > 4; });
  
  // Build HTML
  var html = '<h4 style="margin-top:0;color:#1971c2;">🔬 Deep Network Analysis</h4>';
  
  // Basic Statistics
  html += '<div style="background-color:white;padding:15px;border-radius:5px;margin:10px 0;">';
  html += '<h5 style="margin-top:0;color:#1864ab;">📊 Basic Network Metrics</h5>';
  html += '<table style="width:100%;border-collapse:collapse;">';
  html += '<tr><td style="padding:5px;"><strong>Total Researchers:</strong></td><td>' + totalNodes + '</td>';
  html += '<td style="padding:5px;"><strong>Coordinators:</strong></td><td>' + coordinatorCount + '</td></tr>';
  html += '<tr><td style="padding:5px;"><strong>Researchers:</strong></td><td>' + researcherCount + '</td>';
  html += '<td style="padding:5px;"><strong>Collaboration Pairs:</strong></td><td>' + totalEdges + '</td></tr>';
  html += '<tr><td style="padding:5px;"><strong>Network Density:</strong></td><td>' + density + '%</td>';
  html += '<td style="padding:5px;"><strong>Isolated Researchers:</strong></td><td>' + isolatedNodes + '</td></tr>';
  html += '</table></div>';
  
  // Degree Statistics
  html += '<div style="background-color:white;padding:15px;border-radius:5px;margin:10px 0;">';
  html += '<h5 style="margin-top:0;color:#1864ab;">📈 Collaboration Degree Analysis</h5>';
  html += '<p style="margin:5px 0;"><strong>Average Collaborations per Researcher:</strong> ' + avgDegree.toFixed(2) + '</p>';
  html += '<p style="margin:5px 0;"><strong>Max Collaborations:</strong> ' + maxDegree + ' | <strong>Min:</strong> ' + minDegree + '</p>';
  html += '<p style="margin:5px 0;"><strong>Average Projects per Collaboration:</strong> ' + avgCollabStrength + '</p>';
  html += '<p style="margin:5px 0;"><strong>Research Hubs (4+ collaborations):</strong> ' + hubs.length + ' researchers</p>';
  html += '</div>';
  
  // Top 5 Most Connected
  html += '<div style="background-color:white;padding:15px;border-radius:5px;margin:10px 0;">';
  html += '<h5 style="margin-top:0;color:#1864ab;">⭐ Top 5 Most Connected Researchers</h5>';
  html += '<ol style="margin:5px 0;padding-left:20px;">';
  top5.forEach(function(node) {
    var role = node.group === 'coordinator' ? '👨‍🏫' : '👨‍🔬';
    html += '<li><strong>' + node.label + '</strong> ' + role + ' - ' + (node.value - 1) + ' collaborations</li>';
  });
  html += '</ol></div>';
  
  // Top 5 Strongest Collaborations
  html += '<div style="background-color:white;padding:15px;border-radius:5px;margin:10px 0;">';
  html += '<h5 style="margin-top:0;color:#1864ab;">🤝 Top 5 Strongest Collaborations</h5>';
  html += '<ol style="margin:5px 0;padding-left:20px;">';
  top5Edges.forEach(function(edge) {
    var person1 = nodes.find(function(n) { return n.id === edge.from; });
    var person2 = nodes.find(function(n) { return n.id === edge.to; });
    html += '<li><strong>' + person1.label + '</strong> ↔ <strong>' + person2.label + 
            '</strong> - ' + edge.value + ' project(s) together</li>';
  });
  html += '</ol></div>';
  
  // Network Insights
  html += '<div style="background-color:#fff3cd;padding:15px;border-radius:5px;margin:10px 0;border-left:4px solid #ffc107;">';
  html += '<h5 style="margin-top:0;color:#856404;">💡 Network Insights</h5>';
  
  if (density < 10) {
    html += '<p style="margin:5px 0;">• <strong>Sparse Network:</strong> Low density (' + density + '%) suggests specialized, focused collaborations rather than broad interconnection.</p>';
  } else if (density < 30) {
    html += '<p style="margin:5px 0;">• <strong>Moderate Network:</strong> Density of ' + density + '% indicates a healthy balance of specialized and cross-functional collaborations.</p>';
  } else {
    html += '<p style="margin:5px 0;">• <strong>Dense Network:</strong> High density (' + density + '%) shows strong interconnection and frequent cross-collaboration.</p>';
  }
  
  if (hubs.length > 0) {
    html += '<p style="margin:5px 0;">• <strong>Hub Structure:</strong> ' + hubs.length + ' researchers act as collaboration hubs, connecting multiple research efforts.</p>';
  }
  
  if (isolatedNodes > 0) {
    html += '<p style="margin:5px 0;">• <strong>Isolated Researchers:</strong> ' + isolatedNodes + ' researcher(s) work independently without collaborations in ongoing projects.</p>';
  }
  
  var avgStrength = parseFloat(avgCollabStrength);
  if (avgStrength > 2) {
    html += '<p style="margin:5px 0;">• <strong>Strong Partnerships:</strong> Average of ' + avgCollabStrength + ' projects per collaboration indicates sustained, long-term partnerships.</p>';
  } else {
    html += '<p style="margin:5px 0;">• <strong>Diverse Collaborations:</strong> Average of ' + avgCollabStrength + ' projects per collaboration suggests researchers work with varied partners.</p>';
  }
  
  html += '</div>';
  
  analysis.innerHTML = html;
  container.parentNode.insertBefore(analysis, container.nextSibling);
})();
</script>
{% endif %}

### Projects by Research Group Association

This chart shows the distribution of projects associated with research groups versus independent projects over time, helping to understand the role of research groups in project organization.

{# Count projects by research group association #}
{% set year_with_group = {} %}
{% set year_without_group = {} %}

{% for index, row in df.iterrows() %}
{% set start_date = row.start_date %}
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

{# Check if project has research group #}
{% if row.research_group and row.research_group.strip() %}
{% if full_year in year_with_group %}
{% set _ = year_with_group.__setitem__(full_year, year_with_group[full_year] + 1) %}
{% else %}
{% set _ = year_with_group.__setitem__(full_year, 1) %}
{% endif %}
{% else %}
{% if full_year in year_without_group %}
{% set _ = year_without_group.__setitem__(full_year, year_without_group[full_year] + 1) %}
{% else %}
{% set _ = year_without_group.__setitem__(full_year, 1) %}
{% endif %}
{% endif %}

{% endif %}
{% endif %}
{% endfor %}

{# Create research group association chart #}
{% if year_with_group|length > 0 or year_without_group|length > 0 %}
{% set all_years_group = [] %}
{% for year in year_with_group.keys() %}
{% if year not in all_years_group %}
{% set _ = all_years_group.append(year) %}
{% endif %}
{% endfor %}
{% for year in year_without_group.keys() %}
{% if year not in all_years_group %}
{% set _ = all_years_group.append(year) %}
{% endif %}
{% endfor %}
{% set sorted_years_group = all_years_group|sort %}
{% set counts_with_group = [] %}
{% set counts_without_group = [] %}

{% for year in sorted_years_group %}
{% set _ = counts_with_group.append(year_with_group[year] if year in year_with_group else 0) %}
{% set _ = counts_without_group.append(year_without_group[year] if year in year_without_group else 0) %}
{% endfor %}

<div id="chart-group-association" style="width:100%;height:450px;margin-bottom:30px;"></div>

<script>
(function() {
  var data = [
    {
      x: {{ sorted_years_group|tojson }},
      y: {{ counts_with_group|tojson }},
      text: {{ counts_with_group|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'With Research Group',
      line: {color: '#2ca02c', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#2ca02c'}
    },
    {
      x: {{ sorted_years_group|tojson }},
      y: {{ counts_without_group|tojson }},
      text: {{ counts_without_group|tojson }},
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Without Research Group',
      line: {color: '#d62728', width: 2},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#d62728'}
    }
  ];
  
  var layout = {
    title: 'Projects by Research Group Association Over Time',
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
  
  Plotly.newPlot('chart-group-association', data, layout);
})();
</script>

{% endif %}

### Student Involvement Over Time

This chart illustrates student participation in research projects throughout the years. The **All Students** line shows the total number of students engaged annually, while the **With Funding** and **Without Funding** lines distinguish between students working on funded versus unfunded projects. This helps identify trends in student research opportunities and the impact of funding on student involvement.

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

<div id="chart-students-all" style="width:100%;height:450px;margin-bottom:30px;"></div>

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
  
  Plotly.newPlot('chart-students-all', data, layout);
})();
</script>

{% endif %}

{# Count how many projects each student participated in #}
{% set student_project_count = {} %}

{% for index, row in df.iterrows() %}
{% if row.students and row.students|length > 0 %}
{% for student in row.students %}
{% set student_name = student.strip() %}
{% if student_name %}
{% if student_name in student_project_count %}
{% set _ = student_project_count.__setitem__(student_name, student_project_count[student_name] + 1) %}
{% else %}
{% set _ = student_project_count.__setitem__(student_name, 1) %}
{% endif %}
{% endif %}
{% endfor %}
{% endif %}
{% endfor %}

{# Count how many students participated in X projects #}
{% set participation_distribution = {} %}
{% for student_name, count in student_project_count.items() %}
{% if count in participation_distribution %}
{% set _ = participation_distribution.__setitem__(count, participation_distribution[count] + 1) %}
{% else %}
{% set _ = participation_distribution.__setitem__(count, 1) %}
{% endif %}
{% endfor %}

{# Create bar chart for student participation distribution #}
{% if participation_distribution|length > 0 %}
{% set sorted_participation = participation_distribution.keys()|list|sort %}
{% set student_counts = [] %}

{% for num_projects in sorted_participation %}
{% set _ = student_counts.append(participation_distribution[num_projects]) %}
{% endfor %}

### Student Participation Distribution

This bar chart reveals how many students participated in multiple research projects. Each bar represents a participation level: for example, if the bar at position "1" shows 150 students, it means 150 students participated in exactly one project. Similarly, a bar at position "2" with 100 students indicates 100 students participated in two projects. This distribution helps understand student engagement patterns and identifies students with sustained research involvement across multiple projects.

<div id="chart-student-participation" style="width:100%;height:450px;margin-bottom:30px;"></div>

<script>
(function() {
  var data = [{
    x: {{ sorted_participation|tojson }},
    y: {{ student_counts|tojson }},
    text: {{ student_counts|tojson }},
    type: 'bar',
    marker: {
      color: '#1f77b4',
      line: {
        color: '#0d47a1',
        width: 1.5
      }
    },
    textposition: 'outside',
    textfont: {size: 12, color: '#1f77b4'},
    hovertemplate: '<b>%{x} project(s)</b><br>%{y} students<extra></extra>'
  }];
  
  var layout = {
    title: 'Student Participation Distribution (Total: {{ student_project_count|length }} unique students)',
    xaxis: {
      title: 'Number of Projects per Student',
      dtick: 1,
      tickmode: 'linear'
    },
    yaxis: {
      title: 'Number of Students'
    },
    hovermode: 'closest'
  };
  
  Plotly.newPlot('chart-student-participation', data, layout);
})();
</script>

{# List students with 5 or more projects #}
{% set highly_engaged_students = [] %}
{% for student_name, count in student_project_count.items() %}
{% if count >= 5 %}
{% set _ = highly_engaged_students.append((student_name, count)) %}
{% endif %}
{% endfor %}

{% if highly_engaged_students|length > 0 %}
{% set highly_engaged_students = highly_engaged_students|sort(attribute='1', reverse=True) %}

<div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
  <h4 style="margin-top: 0;">Highly Engaged Students (5+ Projects)</h4>
  <p>The following students have demonstrated exceptional commitment by participating in 5 or more research projects:</p>
  <table style="width:100%; border-collapse: collapse;">
    <thead>
      <tr style="background-color: #e9ecef;">
        <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Student Name</th>
        <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Number of Projects</th>
      </tr>
    </thead>
    <tbody>
      {% for student_name, count in highly_engaged_students %}
      <tr>
        <td style="padding: 8px; border: 1px solid #dee2e6;">{{ student_name }}</td>
        <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;"><strong>{{ count }}</strong></td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  <p style="margin-bottom: 0; margin-top: 15px; font-size: 0.9em; color: #6c757d;">
    <strong>Total:</strong> {{ highly_engaged_students|length }} student(s) with sustained research involvement
  </p>
</div>

{% endif %}

{% endif %}

---

{% for year in unique_years %}
{% if year > 0 %}

## {{ year }}

{% set year_df = df[df['year'] == year] %}
**Total projects:** {{ year_df|length }}

{% for index, row in year_df.iterrows() %}

### {{ loop.index }}. {{ row.title }}

- **ID:** {{ row.id }}
- **Period:** {{ row.start_date }} to {{ row.end_date }}
- **Coordinator:** {{ row.coordinator }}{% if row.coordinator_email %} ([{{ row.coordinator_email }}](mailto:{{ row.coordinator_email }})){% endif %}

{% if row.research_group %}- **Research Group:** {{ row.research_group }}
{% endif %}{% if row.knowledge_area %}- **Knowledge Area:** {{ row.knowledge_area }}
{% endif %}{% if row.research_line %}- **Research Line:** {{ row.research_line }}
{% endif %}{% if row.nature %}- **Nature:** {{ row.nature }}
{% endif %}{% if row.researchers and row.researchers|length > 0 %}- **Researchers:** {{ row.researchers|join(', ') }}
{% endif %}{% if row.students and row.students|length > 0 %}- **Students:** {{ row.students|join(', ') }}
{% endif %}{% if row.keywords and row.keywords|length > 0 %}- **Keywords:** {{ row.keywords|join(', ') }}
{% endif %}{% if row.partner %}- **Partner:** {{ row.partner }}
{% endif %}{% if row.publications_count != '0' or row.funding_count != '0' %}- **Publications:** {{ row.publications_count }} | **Funding:** {{ row.funding_count }}
{% endif %}
{% endfor %}

{% endif %}
{% endfor %}
