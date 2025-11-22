# Scholarships - Campus Serra

{% set all_data = load_scholarship_data() %}
{% set scholarships = all_data['scholarships'] %}

{# Filter Serra campus and remove duplicates by ID #}
{% set seen_ids = [] %}
{% set ic_scholarships = [] %}
{% for s in scholarships %}
  {% if s['execution_campus'] == 'Serra' and s['id'] not in seen_ids %}
    {% set _ = seen_ids.append(s['id']) %}
    {% set _ = ic_scholarships.append(s) %}
  {% endif %}
{% endfor %}

## Overview

**Total IC Scholarships (Campus Serra):** {{ ic_scholarships|length }}



{% if all_data.get('statistics') and all_data['statistics'].get('student_recurrence_serra') %}
{% set recurrence = all_data['statistics']['student_recurrence_serra'] %}

**Total Unique Students:** {{ recurrence['total_unique_students'] }}

---

## Student Participation Recurrence

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ recurrence['student_profiles']['only_bolsista'] }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Only Scholarship Holder</div>
  </div>
  <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ recurrence['student_profiles']['only_voluntario'] }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Only Volunteer</div>
  </div>
  <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ recurrence['student_profiles']['mixed'] }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Both (Mixed)</div>
  </div>
</div>

<div id="chart-student-recurrence" style="width:100%;height:450px;margin-bottom:10px;"></div>

<p style="font-size: 14px; color: #555; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #9467bd;">
  <strong>Legend:</strong> This chart shows how many times each student participated in IC programs. For example, if 270 students did only 1 IC, it means they had a single participation (either as a scholarship holder or volunteer). Students appearing in "2 ICs" participated in two different programs over time, and so on. This helps understand the retention rate and continuity of students in research.
</p>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
<script>
(function() {
  var participationDist = {{ recurrence['participation_distribution']|tojson }};
  
  var counts = [];
  var students = [];
  
  // Sort by number of participations
  var sortedKeys = Object.keys(participationDist).map(Number).sort(function(a, b) { return a - b; });
  
  sortedKeys.forEach(function(count) {
    counts.push(count + ' IC' + (count > 1 ? 's' : ''));
    students.push(participationDist[String(count)]);
  });
  
  var data = [{
    x: counts,
    y: students,
    text: students,
    type: 'bar',
    marker: {
      color: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'],
      line: {
        color: '#333',
        width: 1.5
      }
    },
    textposition: 'outside',
    textfont: {size: 14, color: '#333', weight: 'bold'},
    hovertemplate: '<b>%{x}</b><br>%{y} students<extra></extra>'
  }];
  
  var layout = {
    title: {
      text: 'Number of IC Participations per Student (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Number of Participations',
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Number of Students',
      gridcolor: '#f0f0f0',
      rangemode: 'tozero'
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white'
  };
  
  Plotly.newPlot('chart-student-recurrence', data, layout);
})();
</script>

### Breakdown by Modality

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Number of Participations</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">As Scholarship Holder</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">As Volunteer</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #d1d1d1;"><strong>Total</strong></th>
    </tr>
  </thead>
  <tbody>
    {% for count_str, total in recurrence['participation_distribution'].items() %}
    {% set count = count_str|int %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ count }} IC{{ 's' if count > 1 else '' }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if count_str in recurrence['bolsista_distribution'] %}
          {{ recurrence['bolsista_distribution'][count_str] }}
        {% else %}
          -
        {% endif %}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if count_str in recurrence['voluntario_distribution'] %}
          {{ recurrence['voluntario_distribution'][count_str] }}
        {% else %}
          -
        {% endif %}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; background-color: #f0f0f0; font-weight: bold;">
        {{ total }}
      </td>
    </tr>
    {% endfor %}
    <tr style="background-color: #d1d1d1; font-weight: bold;">
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">TOTAL</td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        {% set bolsista_total = recurrence['bolsista_distribution'].values()|sum %}
        {{ bolsista_total }}
      </td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        {% set voluntario_total = recurrence['voluntario_distribution'].values()|sum %}
        {{ voluntario_total }}
      </td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #c0c0c0;">
        {{ recurrence['total_unique_students'] }}
      </td>
    </tr>
  </tbody>
</table>

<p style="font-size: 14px; color: #666; margin-top: 10px;">
  <strong>Note:</strong> The sum of "As Scholarship Holder" and "As Volunteer" columns may be greater than the "Total" because some students participated in both modalities ({{ recurrence['student_profiles']['mixed'] }} students).
</p>

{% else %}
<p style="color: #d62728; font-weight: bold;">⚠ Recurrence statistics not available. Run: <code>python3 scripts/calculate_student_recurrence.py</code></p>
{% endif %}

---

## Scholarship Holders vs Volunteers Over Time

{# Count by year and modality #}
{% set year_modality_data = {} %}
{% set year_bolsista = {} %}
{% set year_voluntario = {} %}

{% for s in ic_scholarships %}
  {% set year = s['year'] %}
  {% set modality = s['modality'] %}
  
  {% if year not in year_modality_data %}
    {% set _ = year_modality_data.__setitem__(year, {}) %}
    {% set _ = year_bolsista.__setitem__(year, 0) %}
    {% set _ = year_voluntario.__setitem__(year, 0) %}
  {% endif %}
  
  {% if modality == 'Bolsista' %}
    {% set _ = year_bolsista.__setitem__(year, year_bolsista[year] + 1) %}
  {% elif modality == 'Voluntário' %}
    {% set _ = year_voluntario.__setitem__(year, year_voluntario[year] + 1) %}
  {% endif %}
{% endfor %}

{% set modality_years = year_bolsista.keys()|list|sort %}

<div id="chart-modality-timeline" style="width:100%;height:450px;margin-bottom:10px;"></div>

<p style="font-size: 14px; color: #555; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #1f77b4;">
  <strong>Legend:</strong> This chart shows the evolution of the number of participants in Scientific Initiation scholarships at Campus Serra over the years, separated by modality. The black line (TOTAL) represents the total number of scholarships per year, while the blue and orange lines show paid scholarship holders and volunteers respectively. Note the significant growth in recent years.
</p>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>

{# Prepare arrays for chart #}
{% set bolsista_counts = [] %}
{% set voluntario_counts = [] %}
{% set total_counts = [] %}

{% for year in modality_years %}
  {% set _ = bolsista_counts.append(year_bolsista[year]) %}
  {% set _ = voluntario_counts.append(year_voluntario[year]) %}
  {% set _ = total_counts.append(year_bolsista[year] + year_voluntario[year]) %}
{% endfor %}

<script>
(function() {
  var years = {{ modality_years|tojson }};
  var bolsistas = {{ bolsista_counts|tojson }};
  var voluntarios = {{ voluntario_counts|tojson }};
  var totals = {{ total_counts|tojson }};
  
  var data = [
    {
      x: years,
      y: totals,
      text: totals,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'TOTAL',
      line: {width: 4, color: '#000000'},
      marker: {size: 10},
      textposition: 'top center',
      textfont: {size: 12, color: '#000000', weight: 'bold'},
      hovertemplate: '<b>TOTAL</b><br>Year: %{x}<br>%{y} scholarships<extra></extra>'
    },
    {
      x: years,
      y: bolsistas,
      text: bolsistas,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Scholarship Holder',
      line: {width: 3, color: '#1f77b4'},
      marker: {size: 9},
      textposition: 'top center',
      textfont: {size: 11, color: '#1f77b4'},
      hovertemplate: '<b>Scholarship Holder</b><br>Year: %{x}<br>%{y} scholarships<extra></extra>'
    },
    {
      x: years,
      y: voluntarios,
      text: voluntarios,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Volunteer',
      line: {width: 3, color: '#ff7f0e'},
      marker: {size: 9},
      textposition: 'top center',
      textfont: {size: 11, color: '#ff7f0e'},
      hovertemplate: '<b>Volunteer</b><br>Year: %{x}<br>%{y} scholarships<extra></extra>'
    }
  ];
  
  var layout = {
    title: {
      text: 'Evolution of Scholarship Holders and Volunteers (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Year',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Number of Participants',
      gridcolor: '#f0f0f0'
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
    }
  };
  
  Plotly.newPlot('chart-modality-timeline', data, layout);
})();
</script>

### Summary by Modality

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Year</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Scholarship Holder</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Volunteer</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #d1d1d1;"><strong>TOTAL</strong></th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">% Scholarship</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">% Volunteer</th>
    </tr>
  </thead>
  <tbody>
    {% for year in modality_years %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ year }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ year_bolsista[year] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ year_voluntario[year] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; background-color: #f0f0f0; font-weight: bold;">
        {{ year_bolsista[year] + year_voluntario[year] }}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% set total = year_bolsista[year] + year_voluntario[year] %}
        {% if total > 0 %}
          {{ "%.1f"|format(year_bolsista[year] / total * 100) }}%
        {% else %}
          -
        {% endif %}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% set total = year_bolsista[year] + year_voluntario[year] %}
        {% if total > 0 %}
          {{ "%.1f"|format(year_voluntario[year] / total * 100) }}%
        {% else %}
          -
        {% endif %}
      </td>
    </tr>
    {% endfor %}
    <tr style="background-color: #d1d1d1; font-weight: bold;">
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">TOTAL</td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">{{ year_bolsista.values()|sum }}</td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">{{ year_voluntario.values()|sum }}</td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #c0c0c0;">
        {{ year_bolsista.values()|sum + year_voluntario.values()|sum }}
      </td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        {% set grand_total = year_bolsista.values()|sum + year_voluntario.values()|sum %}
        {{ "%.1f"|format(year_bolsista.values()|sum / grand_total * 100) }}%
      </td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        {% set grand_total = year_bolsista.values()|sum + year_voluntario.values()|sum %}
        {{ "%.1f"|format(year_voluntario.values()|sum / grand_total * 100) }}%
      </td>
    </tr>
  </tbody>
</table>

---

## Scholarships Over Time by Program

{# Count scholarships by year and program #}
{% set year_program_data = {} %}
{% set year_totals = {} %}
{% set year_blank = {} %}
{% set all_programs = [] %}

{% for s in ic_scholarships %}
  {% set year = s['year'] %}
  {% set program = s['program'] %}
  
  {# Initialize year if not exists #}
  {% if year not in year_program_data %}
    {% set _ = year_program_data.__setitem__(year, {}) %}
    {% set _ = year_totals.__setitem__(year, 0) %}
    {% set _ = year_blank.__setitem__(year, 0) %}
  {% endif %}
  
  {# Count totals #}
  {% set _ = year_totals.__setitem__(year, year_totals[year] + 1) %}
  
  {# Count by program or blank #}
  {% if program and program.strip() %}
    {# Track all programs #}
    {% if program not in all_programs %}
      {% set _ = all_programs.append(program) %}
    {% endif %}
    
    {% if program not in year_program_data[year] %}
      {% set _ = year_program_data[year].__setitem__(program, 0) %}
    {% endif %}
    {% set _ = year_program_data[year].__setitem__(program, year_program_data[year][program] + 1) %}
  {% else %}
    {# Count blank programs #}
    {% set _ = year_blank.__setitem__(year, year_blank[year] + 1) %}
  {% endif %}
{% endfor %}

{# Prepare data for chart #}
{% set chart_years = year_program_data.keys()|list|sort %}

<div id="chart-scholarships-by-program" style="width:100%;height:500px;margin-bottom:10px;"></div>

<p style="font-size: 14px; color: #555; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #2ca02c;">
  <strong>Legend:</strong> This chart presents the distribution of IC scholarships by program over time. Each colored line represents a specific program (PIBIC, PIBIT, PIBITI, etc.), allowing you to visualize which programs had greater participation in each year. The black line (TOTAL) shows the total number of scholarships regardless of program.
</p>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
<script>
(function() {
  var years = {{ chart_years|tojson }};
  var programs = {{ all_programs|tojson }};
  var yearTotals = {{ year_totals|tojson }};
  var yearBlank = {{ year_blank|tojson }};
  var yearProgramData = {{ year_program_data|tojson }};
  
  var data = [];
  
  // Add total line (bold)
  var totalCounts = [];
  years.forEach(function(year) {
    totalCounts.push(yearTotals[year] || 0);
  });
  
  data.push({
    x: years,
    y: totalCounts,
    text: totalCounts,
    type: 'scatter',
    mode: 'lines+markers+text',
    name: 'TOTAL',
    line: {width: 4, color: '#000000'},
    marker: {size: 10},
    textposition: 'top center',
    textfont: {size: 12, color: '#000000', weight: 'bold'},
    hovertemplate: '<b>TOTAL</b><br>Year: %{x}<br>Scholarships: %{y}<extra></extra>'
  });
  
  // Add program lines
  var colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22'];
  
  programs.forEach(function(program, idx) {
    var counts = [];
    years.forEach(function(year) {
      var count = yearProgramData[year] && yearProgramData[year][program] ? yearProgramData[year][program] : 0;
      counts.push(count);
    });
    
    data.push({
      x: years,
      y: counts,
      text: counts,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: program,
      line: {width: 2.5, color: colors[idx % colors.length]},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10},
      hovertemplate: '<b>' + program + '</b><br>Year: %{x}<br>Scholarships: %{y}<extra></extra>'
    });
  });
  
  // Add blank/empty program line
  var blankCounts = [];
  years.forEach(function(year) {
    blankCounts.push(yearBlank[year] || 0);
  });
  
  if (blankCounts.some(function(c) { return c > 0; })) {
    data.push({
      x: years,
      y: blankCounts,
      text: blankCounts,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'No Program',
      line: {width: 2.5, color: '#999999', dash: 'dash'},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#999999'},
      hovertemplate: '<b>No Program</b><br>Year: %{x}<br>Scholarships: %{y}<extra></extra>'
    });
  }
  
  var layout = {
    title: {
      text: 'IC Scholarships Over Time by Program (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Year',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Number of Scholarships',
      gridcolor: '#f0f0f0'
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
    }
  };
  
  Plotly.newPlot('chart-scholarships-by-program', data, layout);
})();
</script>

### Summary by Year and Program

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Year</th>
      {% for program in all_programs %}
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">{{ program }}</th>
      {% endfor %}
      {% if year_blank.values()|sum > 0 %}
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">No Program</th>
      {% endif %}
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #d1d1d1;"><strong>TOTAL</strong></th>
    </tr>
  </thead>
  <tbody>
    {% for year in chart_years %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ year }}</td>
      {% for program in all_programs %}
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if year in year_program_data and program in year_program_data[year] %}
          {{ year_program_data[year][program] }}
        {% else %}
          -
        {% endif %}
      </td>
      {% endfor %}
      {% if year_blank.values()|sum > 0 %}
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if year in year_blank and year_blank[year] > 0 %}
          {{ year_blank[year] }}
        {% else %}
          -
        {% endif %}
      </td>
      {% endif %}
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; background-color: #f0f0f0; font-weight: bold;">
        {{ year_totals[year] }}
      </td>
    </tr>
    {% endfor %}
    <tr style="background-color: #d1d1d1; font-weight: bold;">
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">TOTAL</td>
      {% for program in all_programs %}
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        {% set program_total = 0 %}
        {% for year in chart_years %}
          {% if year in year_program_data and program in year_program_data[year] %}
            {% set program_total = program_total + year_program_data[year][program] %}
          {% endif %}
        {% endfor %}
        {{ program_total }}
      </td>
      {% endfor %}
      {% if year_blank.values()|sum > 0 %}
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        {{ year_blank.values()|sum }}
      </td>
      {% endif %}
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #c0c0c0;">
        {{ year_totals.values()|sum }}
      </td>
    </tr>
  </tbody>
</table>

---

## Scholarships by Funding Agency Over Time

{# Count scholarships by year and funding agency #}
{% set year_agency_data = {} %}
{% set year_agency_totals = {} %}
{% set all_agencies = [] %}

{% for s in ic_scholarships %}
  {% set year = s['year'] %}
  {% set agency = s['funding_agency'] if s['funding_agency'] and s['funding_agency'].strip() else 'No Agency' %}
  
  {# Initialize year if not exists #}
  {% if year not in year_agency_data %}
    {% set _ = year_agency_data.__setitem__(year, {}) %}
    {% set _ = year_agency_totals.__setitem__(year, 0) %}
  {% endif %}
  
  {# Count totals #}
  {% set _ = year_agency_totals.__setitem__(year, year_agency_totals[year] + 1) %}
  
  {# Track all agencies #}
  {% if agency not in all_agencies %}
    {% set _ = all_agencies.append(agency) %}
  {% endif %}
  
  {% if agency not in year_agency_data[year] %}
    {% set _ = year_agency_data[year].__setitem__(agency, 0) %}
  {% endif %}
  {% set _ = year_agency_data[year].__setitem__(agency, year_agency_data[year][agency] + 1) %}
{% endfor %}

{# Prepare data for chart #}
{% set agency_years = year_agency_data.keys()|list|sort %}

<div id="chart-scholarships-by-agency" style="width:100%;height:500px;margin-bottom:10px;"></div>

<p style="font-size: 14px; color: #555; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #ff7f0e;">
  <strong>Legend:</strong> This chart shows the source of scholarship funding over the years. The main funding agencies are: <strong>Ifes</strong> (institutional resources), <strong>Fapes</strong> (Espírito Santo Research Support Foundation), <strong>CNPq</strong> (National Council for Scientific and Technological Development), and <strong>Voluntário</strong> (unpaid volunteers). The dashed gray line represents scholarships without a specified agency.
</p>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
<script>
(function() {
  var years = {{ agency_years|tojson }};
  var agencies = {{ all_agencies|tojson }};
  var yearTotals = {{ year_agency_totals|tojson }};
  var yearAgencyData = {{ year_agency_data|tojson }};
  
  var data = [];
  
  // Add total line (bold)
  var totalCounts = [];
  years.forEach(function(year) {
    totalCounts.push(yearTotals[String(year)] || 0);
  });
  
  data.push({
    x: years,
    y: totalCounts,
    text: totalCounts,
    type: 'scatter',
    mode: 'lines+markers+text',
    name: 'TOTAL',
    line: {width: 4, color: '#000000'},
    marker: {size: 10},
    textposition: 'top center',
    textfont: {size: 12, color: '#000000', weight: 'bold'},
    hovertemplate: '<b>TOTAL</b><br>Year: %{x}<br>Scholarships: %{y}<extra></extra>'
  });
  
  // Define colors for each agency
  var agencyColors = {
    'Ifes': '#1f77b4',
    'Fapes': '#ff7f0e',
    'CNPq': '#2ca02c',
    'Voluntário': '#d62728',
    'No Agency': '#999999'
  };
  
  // Add agency lines
  agencies.forEach(function(agency) {
    var counts = [];
    years.forEach(function(year) {
      var yearStr = String(year);
      var count = yearAgencyData[yearStr] && yearAgencyData[yearStr][agency] ? yearAgencyData[yearStr][agency] : 0;
      counts.push(count);
    });
    
    var color = agencyColors[agency] || '#9467bd';
    var lineStyle = agency === 'No Agency' ? 'dash' : 'solid';
    
    data.push({
      x: years,
      y: counts,
      text: counts,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: agency,
      line: {width: 2.5, color: color, dash: lineStyle},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10},
      hovertemplate: '<b>' + agency + '</b><br>Year: %{x}<br>Scholarships: %{y}<extra></extra>'
    });
  });
  
  var layout = {
    title: {
      text: 'Scholarships by Funding Agency Over Time (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Year',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Number of Scholarships',
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
    }
  };
  
  Plotly.newPlot('chart-scholarships-by-agency', data, layout);
})();
</script>

### Summary by Year and Funding Agency

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Year</th>
      {% for agency in all_agencies %}
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">{{ agency }}</th>
      {% endfor %}
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #d1d1d1;"><strong>TOTAL</strong></th>
    </tr>
  </thead>
  <tbody>
    {% for year in agency_years %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ year }}</td>
      {% for agency in all_agencies %}
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if year in year_agency_data and agency in year_agency_data[year] %}
          {{ year_agency_data[year][agency] }}
        {% else %}
          -
        {% endif %}
      </td>
      {% endfor %}
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; background-color: #f0f0f0; font-weight: bold;">
        {{ year_agency_totals[year] }}
      </td>
    </tr>
    {% endfor %}
    <tr style="background-color: #d1d1d1; font-weight: bold;">
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">TOTAL</td>
      {% for agency in all_agencies %}
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        {% set agency_total = 0 %}
        {% for year in agency_years %}
          {% if year in year_agency_data and agency in year_agency_data[year] %}
            {% set agency_total = agency_total + year_agency_data[year][agency] %}
          {% endif %}
        {% endfor %}
        {{ agency_total }}
      </td>
      {% endfor %}
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #c0c0c0;">
        {{ year_agency_totals.values()|sum }}
      </td>
    </tr>
  </tbody>
</table>

---

{# Group by year #}
{% set by_year = {} %}
{% for s in ic_scholarships %}
  {% set year = s['year'] %}
  {% if year not in by_year %}
    {% set _ = by_year.__setitem__(year, []) %}
  {% endif %}
  {% set _ = by_year[year].append(s) %}
{% endfor %}

{# Sort years in descending order #}
{% set sorted_years = by_year.keys()|list|sort(reverse=True) %}

## Scholarship Distribution by Value

{# Group scholarships by year and value #}
{% set year_value_distribution = {} %}
{% set all_values = [] %}

{% for s in ic_scholarships %}
  {% set year = s['year'] %}
  {% set value = s['value'] if s['value'] else 0 %}
  
  {# Round value to nearest 100 for grouping #}
  {% set value_rounded = (value / 100)|round(0, 'floor') * 100 %}
  
  {% if year not in year_value_distribution %}
    {% set _ = year_value_distribution.__setitem__(year, {}) %}
  {% endif %}
  
  {% if value_rounded not in year_value_distribution[year] %}
    {% set _ = year_value_distribution[year].__setitem__(value_rounded, 0) %}
  {% endif %}
  
  {% set _ = year_value_distribution[year].__setitem__(value_rounded, year_value_distribution[year][value_rounded] + 1) %}
  
  {# Track all unique values #}
  {% if value_rounded not in all_values and value_rounded > 0 %}
    {% set _ = all_values.append(value_rounded) %}
  {% endif %}
{% endfor %}

{% set sorted_values = all_values|sort %}
{% set value_years = year_value_distribution.keys()|list|sort %}

<div id="chart-value-distribution" style="width:100%;height:500px;margin-bottom:10px;"></div>

<p style="font-size: 14px; color: #555; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #d62728;">
  <strong>Legend:</strong> This chart shows the evolution of monthly scholarship values over time. Each colored line represents a specific scholarship amount (R$ 100, R$ 300, R$ 400, etc.). Note that values have been adjusted over the years, with a gradual increase in scholarship amounts, especially from 2023 onwards. Values are grouped in R$ 100 ranges for easier visualization.
</p>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
<script>
(function() {
  var years = {{ value_years|tojson }};
  var values = {{ sorted_values|tojson }};
  var yearValueData = {{ year_value_distribution|tojson }};
  
  var data = [];
  var colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'];
  
  // Create a line trace for each value amount
  values.forEach(function(value, idx) {
    var counts = [];
    years.forEach(function(year) {
      // The keys in yearValueData are strings with .0 format (e.g., "100.0", "400.0")
      var yearStr = String(year);
      var valueStr = value.toFixed(1); // Convert to "100.0" format
      var count = yearValueData[yearStr] && yearValueData[yearStr][valueStr] ? yearValueData[yearStr][valueStr] : 0;
      counts.push(count);
    });
    
    // Only add if there's at least one non-zero value
    if (counts.some(function(c) { return c > 0; })) {
      data.push({
        x: years,
        y: counts,
        text: counts,
        name: 'R$ ' + value.toFixed(2),
        type: 'scatter',
        mode: 'lines+markers+text',
        line: {width: 2.5, color: colors[idx % colors.length]},
        marker: {size: 8},
        textposition: 'top center',
        textfont: {size: 10},
        hovertemplate: '<b>R$ ' + value.toFixed(2) + '</b><br>Year: %{x}<br>%{y} scholarships<extra></extra>'
      });
    }
  });
  
  var layout = {
    title: {
      text: 'Scholarship Distribution by Value Over Time (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Year',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Number of Scholarships',
      gridcolor: '#f0f0f0',
      rangemode: 'tozero'
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    hovermode: 'x unified',
    legend: {
      title: {text: 'Scholarship Value'},
      x: 0.02,
      y: 0.98,
      bgcolor: 'rgba(255,255,255,0.9)',
      bordercolor: '#ccc',
      borderwidth: 1
    }
  };
  
  Plotly.newPlot('chart-value-distribution', data, layout);
})();
</script>

### Value Summary by Year

<table style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 12px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">Year</th>
      {% for value in sorted_values %}
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">R$ {{ "%.2f"|format(value) }}</th>
      {% endfor %}
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; background-color: #d1d1d1;"><strong>TOTAL</strong></th>
    </tr>
  </thead>
  <tbody>
    {% for year in value_years %}
    <tr>
      <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ year }}</td>
      {% for value in sorted_values %}
      <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6;">
        {% if year in year_value_distribution and value in year_value_distribution[year] %}
          {{ year_value_distribution[year][value] }}
        {% else %}
          -
        {% endif %}
      </td>
      {% endfor %}
      <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6; background-color: #f0f0f0; font-weight: bold;">
        {% set year_total = 0 %}
        {% for value in sorted_values %}
          {% if year in year_value_distribution and value in year_value_distribution[year] %}
            {% set year_total = year_total + year_value_distribution[year][value] %}
          {% endif %}
        {% endfor %}
        {{ year_total }}
      </td>
    </tr>
    {% endfor %}
    <tr style="background-color: #d1d1d1; font-weight: bold;">
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">TOTAL</td>
      {% for value in sorted_values %}
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% set value_total = 0 %}
        {% for year in value_years %}
          {% if year in year_value_distribution and value in year_value_distribution[year] %}
            {% set value_total = value_total + year_value_distribution[year][value] %}
          {% endif %}
        {% endfor %}
        {{ value_total }}
      </td>
      {% endfor %}
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; background-color: #c0c0c0;">
        {% set grand_total = 0 %}
        {% for year in value_years %}
          {% for value in sorted_values %}
            {% if year in year_value_distribution and value in year_value_distribution[year] %}
              {% set grand_total = grand_total + year_value_distribution[year][value] %}
            {% endif %}
          {% endfor %}
        {% endfor %}
        {{ grand_total }}
      </td>
    </tr>
  </tbody>
</table>

---

## Investimento Financeiro ao Longo do Tempo

{# Calculate financial values by year #}
{% set year_values = {} %}

{% for s in ic_scholarships %}
  {% set year = s['year'] %}
  {% set value = s['value'] if s['value'] else 0 %}
  
  {% if year not in year_values %}
    {% set _ = year_values.__setitem__(year, 0) %}
  {% endif %}
  
  {% set _ = year_values.__setitem__(year, year_values[year] + value) %}
{% endfor %}

{% set financial_years = year_values.keys()|list|sort %}
{% set financial_values = [] %}
{% for year in financial_years %}
  {% set _ = financial_values.append(year_values[year]) %}
{% endfor %}

<div id="chart-financial-values" style="width:100%;height:450px;margin-bottom:10px;"></div>

<p style="font-size: 14px; color: #555; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #2ca02c;">
  <strong>Legend:</strong> This bar chart shows the total financial investment in IC scholarships per year at Campus Serra. The values represent the sum of all paid scholarships granted each year. The growth in investment reflects both the increase in the number of scholarships and the appreciation of the amounts paid to scholarship holders over time.
</p>

<script>
(function() {
  var years = {{ financial_years|tojson }};
  var values = {{ financial_values|tojson }};
  
  // Format values for display
  var valuesFormatted = values.map(function(v) {
    return 'R$ ' + v.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
  });
  
  var data = [{
    x: years,
    y: values,
    text: valuesFormatted,
    type: 'bar',
    marker: {
      color: '#2ca02c',
      line: {
        color: '#1e7d1e',
        width: 2
      }
    },
    textposition: 'outside',
    textfont: {size: 10, color: '#2ca02c'},
    hovertemplate: '<b>Year %{x}</b><br>Investment: R$ %{y:,.2f}<extra></extra>'
  }];
  
  var layout = {
    title: {
      text: 'Scholarship Investment by Year (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Year',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Total Value (R$)',
      gridcolor: '#f0f0f0',
      tickformat: ',.2f'
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    hovermode: 'x unified'
  };
  
  Plotly.newPlot('chart-financial-values', data, layout);
})();
</script>

### Financial Summary by Year

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Year</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Number of Scholarships</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Total Investment</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Average Value per Scholarship</th>
    </tr>
  </thead>
  <tbody>
    {% for year in financial_years %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ year }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ year_totals[year] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">R$ {{ "%.2f"|format(year_values[year]) }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if year_totals[year] > 0 %}
          R$ {{ "%.2f"|format(year_values[year] / year_totals[year]) }}
        {% else %}
          -
        {% endif %}
      </td>
    </tr>
    {% endfor %}
    <tr style="background-color: #d1d1d1; font-weight: bold;">
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">TOTAL</td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">{{ year_totals.values()|sum }}</td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">R$ {{ "%.2f"|format(year_values.values()|sum) }}</td>
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        R$ {{ "%.2f"|format(year_values.values()|sum / year_totals.values()|sum) }}
      </td>
    </tr>
  </tbody>
</table>

---

## Financial Investment by Funding Agency Over Time

{# Calculate financial values by year and agency #}
{% set year_agency_values = {} %}

{% for s in ic_scholarships %}
  {% set year = s['year'] %}
  {% set agency = s['funding_agency'] if s['funding_agency'] and s['funding_agency'].strip() else 'No Agency' %}
  {% set value = s['value'] if s['value'] else 0 %}
  
  {% if year not in year_agency_values %}
    {% set _ = year_agency_values.__setitem__(year, {}) %}
  {% endif %}
  
  {% if agency not in year_agency_values[year] %}
    {% set _ = year_agency_values[year].__setitem__(agency, 0) %}
  {% endif %}
  
  {% set _ = year_agency_values[year].__setitem__(agency, year_agency_values[year][agency] + value) %}
{% endfor %}

{% set financial_agency_years = year_agency_values.keys()|list|sort %}

<div id="chart-financial-by-agency" style="width:100%;height:500px;margin-bottom:10px;"></div>

<p style="font-size: 14px; color: #555; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #ff7f0e;">
  <strong>Legend:</strong> This stacked area chart shows the financial investment in IC scholarships broken down by funding agency over time. Each colored area represents a different funding source (Ifes, Fapes, CNPq, Voluntário). The total height of the stacked areas represents the total investment per year. This visualization helps understand which agencies have contributed most to research funding and how their participation has evolved over time.
</p>

<script>
(function() {
  var years = {{ financial_agency_years|tojson }};
  var agencies = {{ all_agencies|tojson }};
  var yearAgencyValues = {{ year_agency_values|tojson }};
  
  var data = [];
  
  // Define colors for each agency
  var agencyColors = {
    'Ifes': '#1f77b4',
    'Fapes': '#ff7f0e',
    'CNPq': '#2ca02c',
    'Voluntário': '#d62728',
    'No Agency': '#999999'
  };
  
  // Add stacked area for each agency
  agencies.forEach(function(agency) {
    var values = [];
    years.forEach(function(year) {
      var yearStr = String(year);
      var value = yearAgencyValues[yearStr] && yearAgencyValues[yearStr][agency] ? yearAgencyValues[yearStr][agency] : 0;
      values.push(value);
    });
    
    var color = agencyColors[agency] || '#9467bd';
    
    // Format values for text display
    var textValues = values.map(function(v) {
      if (v > 0) {
        return 'R$ ' + (v / 1000).toFixed(1) + 'k';
      }
      return '';
    });
    
    data.push({
      x: years,
      y: values,
      text: textValues,
      name: agency,
      type: 'scatter',
      mode: 'lines+text',
      stackgroup: 'one',
      fillcolor: color,
      line: {width: 0.5, color: color},
      textposition: 'inside',
      textfont: {size: 9, color: 'white'},
      hovertemplate: '<b>' + agency + '</b><br>Year: %{x}<br>Investment: R$ %{y:,.2f}<extra></extra>'
    });
  });
  
  var layout = {
    title: {
      text: 'Financial Investment by Funding Agency Over Time (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Year',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Total Investment (R$)',
      gridcolor: '#f0f0f0',
      tickformat: ',.2f',
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
    }
  };
  
  Plotly.newPlot('chart-financial-by-agency', data, layout);
})();
</script>

### Financial Investment Summary by Year and Agency

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Year</th>
      {% for agency in all_agencies %}
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">{{ agency }}</th>
      {% endfor %}
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #d1d1d1;"><strong>TOTAL</strong></th>
    </tr>
  </thead>
  <tbody>
    {% for year in financial_agency_years %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ year }}</td>
      {% for agency in all_agencies %}
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if year in year_agency_values and agency in year_agency_values[year] %}
          R$ {{ "%.2f"|format(year_agency_values[year][agency]) }}
        {% else %}
          -
        {% endif %}
      </td>
      {% endfor %}
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; background-color: #f0f0f0; font-weight: bold;">
        {% set year_total = 0 %}
        {% for agency in all_agencies %}
          {% if year in year_agency_values and agency in year_agency_values[year] %}
            {% set year_total = year_total + year_agency_values[year][agency] %}
          {% endif %}
        {% endfor %}
        R$ {{ "%.2f"|format(year_total) }}
      </td>
    </tr>
    {% endfor %}
    <tr style="background-color: #d1d1d1; font-weight: bold;">
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">TOTAL</td>
      {% for agency in all_agencies %}
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">
        {% set agency_total = 0 %}
        {% for year in financial_agency_years %}
          {% if year in year_agency_values and agency in year_agency_values[year] %}
            {% set agency_total = agency_total + year_agency_values[year][agency] %}
          {% endif %}
        {% endfor %}
        R$ {{ "%.2f"|format(agency_total) }}
      </td>
      {% endfor %}
      <td style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #c0c0c0;">
        {% set grand_total = 0 %}
        {% for year in financial_agency_years %}
          {% for agency in all_agencies %}
            {% if year in year_agency_values and agency in year_agency_values[year] %}
              {% set grand_total = grand_total + year_agency_values[year][agency] %}
            {% endif %}
          {% endfor %}
        {% endfor %}
        R$ {{ "%.2f"|format(grand_total) }}
      </td>
    </tr>
  </tbody>
</table>

---

## Ongoing Scholarships

{# Filter ongoing scholarships - end_date is in the future AND not cancelled #}
{% set current_date = get_current_date() %}
{% set current_year = current_date['year'] %}
{% set current_month = current_date['month'] %}
{% set ongoing_scholarships = [] %}
{% set cancelled_scholarships = [] %}

{% for s in ic_scholarships %}
  {% if s['end_date'] %}
    {# Extract date parts from end_date (format: DD-MM-YY or DD/MM/YYYY) #}
    {% set end_date_parts = s['end_date'].split('-') if '-' in s['end_date'] else s['end_date'].split('/') %}
    {% if end_date_parts|length >= 3 %}
      {% set end_day = end_date_parts[0]|int %}
      {% set end_month = end_date_parts[1]|int %}
      {% set end_year = end_date_parts[2]|int %}
      {# Handle 2-digit years #}
      {% if end_year < 100 %}
        {% set end_year = 2000 + end_year if end_year < 50 else 1900 + end_year %}
      {% endif %}
      {# Check if scholarship is still ongoing (year > current OR (year == current AND month >= current)) #}
      {% set is_ongoing = (end_year > current_year) or (end_year == current_year and end_month >= current_month) %}
      {% if is_ongoing %}
        {# Check if cancelled #}
        {% set is_cancelled = s.get('cancelled', 'FALSE')|upper == 'TRUE' %}
        {% if is_cancelled %}
          {% set _ = cancelled_scholarships.append(s) %}
        {% else %}
          {% set _ = ongoing_scholarships.append(s) %}
        {% endif %}
      {% endif %}
    {% endif %}
  {% endif %}
{% endfor %}

{% if ongoing_scholarships|length > 0 %}

**Total Ongoing Scholarships:** {{ ongoing_scholarships|length }}

{# Sort by student name #}
{% set sorted_ongoing = ongoing_scholarships|sort(attribute='student') %}

<style>
  #ongoingTable {
    width: 100% !important;
    table-layout: fixed !important;
  }
  #ongoingTable td {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
  }
</style>

<table id="ongoingTable" style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 11px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 15%;">Student</th>
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 13%;">Supervisor</th>
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 12%;">Research Line</th>
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 8%;">Program</th>
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 22%;">Project</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 10%;">Period</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 10%;">Modality</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 10%;">Value</th>
    </tr>
  </thead>
  <tbody>
    {% for s in sorted_ongoing %}
    <tr>
      <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">{{ s['student'] }}</td>
      <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">{{ s['advisor'] }}</td>
      <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">
        {% if s.get('knowledge_area') %}
          {{ s['knowledge_area'] }}
        {% else %}
          -
        {% endif %}
      </td>
      <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">{{ s['program'] if s['program'] else '-' }}</td>
      <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">{{ s['project_title'] if s['project_title'] else 'N/A' }}</td>
      <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6; font-size: 10px; vertical-align: top;">{{ s['start_date'] }}<br>to<br>{{ s['end_date'] }}</td>
      <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6; vertical-align: top;">
        {% if s['modality'] == 'Bolsista' %}
          <span style="color: #1f77b4; font-weight: bold;">💰 Paid</span>
        {% else %}
          <span style="color: #ff7f0e; font-weight: bold;">🤝 Volunteer</span>
        {% endif %}
      </td>
      <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6; vertical-align: top;">
        {% if s['value'] %}
          R$ {{ "%.2f"|format(s['value']) }}
        {% else %}
          -
        {% endif %}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>

{% else %}

<p style="color: #666; font-style: italic;">No ongoing scholarships found as of {{ current_date['date_str'] }}.</p>

{% endif %}

{# Show cancelled scholarships if any #}
{% if cancelled_scholarships|length > 0 %}

### Cancelled Scholarships

<div style="background-color: #f8d7da; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #dc3545;">
  <strong>🚫 Cancelled:</strong> {{ cancelled_scholarships|length }} scholarship(s) that would be active as of {{ current_date['date_str'] }} were cancelled and are not included in the active list above.
</div>

{# Sort by student name #}
{% set sorted_cancelled = cancelled_scholarships|sort(attribute='student') %}

<details style="margin-bottom: 20px;">
  <summary style="cursor: pointer; color: #dc3545; font-weight: bold; padding: 10px; background: #f8d7da; border-radius: 4px;">
    Click to view cancelled scholarships ({{ cancelled_scholarships|length }})
  </summary>
  
  <table style="width:100%; border-collapse: collapse; margin: 10px 0; font-size: 11px;">
    <thead>
      <tr style="background-color: #f8d7da;">
        <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 15%;">Student</th>
        <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 13%;">Supervisor</th>
        <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 12%;">Research Line</th>
        <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 8%;">Program</th>
        <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 22%;">Project</th>
        <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 10%;">Period</th>
        <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 10%;">Modality</th>
        <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 10%;">Value</th>
      </tr>
    </thead>
    <tbody>
      {% for s in sorted_cancelled %}
      <tr style="background-color: #fff5f5;">
        <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">{{ s['student'] }}</td>
        <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">{{ s['advisor'] }}</td>
        <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">
          {% if s.get('knowledge_area') %}
            {{ s['knowledge_area'] }}
          {% else %}
            -
          {% endif %}
        </td>
        <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">{{ s['program'] if s['program'] else '-' }}</td>
        <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">{{ s['project_title'] if s['project_title'] else 'N/A' }}</td>
        <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6; font-size: 10px; vertical-align: top;">{{ s['start_date'] }}<br>to<br>{{ s['end_date'] }}</td>
        <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6; vertical-align: top;">
          {% if s['modality'] == 'Bolsista' %}
            <span style="color: #1f77b4; font-weight: bold;">💰 Paid</span>
          {% else %}
            <span style="color: #ff7f0e; font-weight: bold;">🤝 Volunteer</span>
          {% endif %}
        </td>
        <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6; vertical-align: top;">
          {% if s['value'] %}
            R$ {{ "%.2f"|format(s['value']) }}
          {% else %}
            -
          {% endif %}
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</details>

{% endif %}

---

## Students with Multiple Active Scholarships

{# Count scholarships per student for ongoing scholarships #}
{% set student_scholarship_count = {} %}

{% for s in ongoing_scholarships %}
  {% set student_name = s['student'] %}
  {% if student_name not in student_scholarship_count %}
    {% set _ = student_scholarship_count.__setitem__(student_name, []) %}
  {% endif %}
  {% set _ = student_scholarship_count[student_name].append(s) %}
{% endfor %}

{# Filter students with more than one scholarship #}
{% set multiple_scholarships = [] %}
{% for student_name, scholarships in student_scholarship_count.items() %}
  {% if scholarships|length > 1 %}
    {% set _ = multiple_scholarships.append({'name': student_name, 'scholarships': scholarships, 'count': scholarships|length}) %}
  {% endif %}
{% endfor %}

{% if multiple_scholarships|length > 0 %}

{# Sort by number of scholarships (descending) #}
{% set sorted_multiple = multiple_scholarships|sort(attribute='count', reverse=True) %}

**Total Students with Multiple Scholarships:** {{ sorted_multiple|length }}

<div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #ffc107;">
  <strong>⚠️ Important:</strong> Students listed below have multiple active scholarships simultaneously. This may require verification to ensure compliance with institutional policies regarding scholarship accumulation.
</div>

<style>
  #multipleTable {
    width: 100% !important;
    table-layout: fixed !important;
  }
  #multipleTable td {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
  }
</style>

<table id="multipleTable" style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 11px;">
  <thead>
    <tr style="background-color: #fff3cd;">
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 5%;">#</th>
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 20%;">Student</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 8%;">Total</th>
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6; width: 67%;">Active Scholarships Details</th>
    </tr>
  </thead>
  <tbody>
    {% for item in sorted_multiple %}
    <tr>
      <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6; font-weight: bold; vertical-align: top;">{{ loop.index }}</td>
      <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;"><strong>{{ item['name'] }}</strong></td>
      <td style="padding: 6px; text-align: center; border: 1px solid #dee2e6; font-weight: bold; color: #d62728; font-size: 14px; vertical-align: top;">{{ item['count'] }}</td>
      <td style="padding: 6px; border: 1px solid #dee2e6; vertical-align: top;">
        <div style="font-size: 10px;">
          {% for s in item['scholarships'] %}
          <div style="margin-bottom: 8px; padding: 8px; background: #f8f9fa; border-radius: 4px; {% if not loop.last %}margin-bottom: 10px;{% endif %}">
            <strong style="color: #333;">{{ loop.index }}. {{ s['project_title'] if s['project_title'] else 'N/A' }}</strong>
            <br><span style="color: #2e7d32;">👤 Supervisor: {{ s['advisor'] }}</span>
            {% if s.get('knowledge_area') %}
            <br><span style="color: #1565c0;">🔬 {{ s['knowledge_area'] }}</span>
            {% endif %}
            <br><span style="color: #666;">📅 {{ s['start_date'] }} to {{ s['end_date'] }} | 📋 {{ s['program'] if s['program'] else '-' }}</span>
            <br><span style="{% if s['modality'] == 'Bolsista' %}color: #1f77b4;{% else %}color: #ff7f0e;{% endif %} font-weight: bold;">
              {% if s['modality'] == 'Bolsista' %}💰 Paid{% else %}🤝 Volunteer{% endif %}
              {% if s['value'] %} - R$ {{ "%.2f"|format(s['value']) }}{% endif %}
            </span>
          </div>
          {% endfor %}
        </div>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>

{% else %}

<p style="color: #28a745; font-weight: bold;">✓ No students found with multiple active scholarships.</p>

{% endif %}

---

{% for year in sorted_years %}

## {{ year }}

**Total:** {{ by_year[year]|length }} scholarships

{# Sort scholarships by student name #}
{% set sorted_scholarships = by_year[year]|sort(attribute='student') %}

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Student</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Advisor</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Program</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Project</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Period</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Value</th>
    </tr>
  </thead>
  <tbody>
    {% for s in sorted_scholarships %}
    <tr>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ s['student'] }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ s['advisor'] }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ s['program'] }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ s['project_title'] if s['project_title'] else 'N/A' }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ s['start_date'] }} to {{ s['end_date'] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        {% if s['value'] %}
          R$ {{ "%.2f"|format(s['value']) }}
        {% else %}
          -
        {% endif %}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>

{% endfor %}
