# Bolsas - Campus Serra

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

## Visão Geral

**Total de Bolsas de IC (Campus Serra):** {{ ic_scholarships|length }}

{% if all_data.get('statistics') and all_data['statistics'].get('student_recurrence_serra') %}
{% set recurrence = all_data['statistics']['student_recurrence_serra'] %}

**Total de Estudantes Únicos:** {{ recurrence['total_unique_students'] }}

---

## Recorrência de Participação dos Estudantes

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ recurrence['student_profiles']['only_bolsista'] }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Apenas Bolsista</div>
  </div>
  <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ recurrence['student_profiles']['only_voluntario'] }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Apenas Voluntário</div>
  </div>
  <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ recurrence['student_profiles']['mixed'] }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Ambos (Misto)</div>
  </div>
</div>

<div id="chart-student-recurrence" style="width:100%;height:450px;margin-bottom:10px;"></div>

<p style="font-size: 14px; color: #555; font-style: italic; margin-bottom: 30px; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #9467bd;">
  <strong>Legenda:</strong> Este gráfico mostra quantas vezes cada estudante participou de programas de IC. Por exemplo, se 270 estudantes fizeram apenas 1 IC, isso significa que eles tiveram uma única participação (seja como bolsista ou voluntário). Estudantes que aparecem em "2 ICs" participaram de dois programas diferentes ao longo do tempo, e assim por diante. Isso ajuda a entender a taxa de retenção e continuidade dos estudantes em pesquisa.
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
    hovertemplate: '<b>%{x}</b><br>%{y} estudantes<extra></extra>'
  }];
  
  var layout = {
    title: {
      text: 'Número de Participações em IC por Estudante (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Número de Participações',
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Número de Estudantes',
      gridcolor: '#f0f0f0',
      rangemode: 'tozero'
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white'
  };
  
  Plotly.newPlot('chart-student-recurrence', data, layout);
})();
</script>

### Detalhamento por Modalidade

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Número de Participações</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Como Bolsista</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Como Voluntário</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #d1d1d1;"><strong>Total Geral</strong></th>
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
  <strong>Nota:</strong> A soma das colunas "Como Bolsista" e "Como Voluntário" pode ser maior que o "Total Geral" porque alguns estudantes participaram em ambas as modalidades ({{ recurrence['student_profiles']['mixed'] }} estudantes).
</p>

{% else %}
<p style="color: #d62728; font-weight: bold;">⚠ Estatísticas de recorrência não disponíveis. Execute: <code>python3 scripts/calculate_student_recurrence.py</code></p>
{% endif %}

---

## Bolsistas vs Voluntários ao Longo do Tempo

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
  <strong>Legenda:</strong> Este gráfico mostra a evolução do número de participantes em bolsas de Iniciação Científica no Campus Serra ao longo dos anos, separados por modalidade. A linha preta (TOTAL) representa o número total de bolsas por ano, enquanto as linhas azul e laranja mostram respectivamente bolsistas remunerados e voluntários. Observe o crescimento significativo nos últimos anos.
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
      hovertemplate: '<b>TOTAL</b><br>Ano: %{x}<br>%{y} bolsas<extra></extra>'
    },
    {
      x: years,
      y: bolsistas,
      text: bolsistas,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Bolsista',
      line: {width: 3, color: '#1f77b4'},
      marker: {size: 9},
      textposition: 'top center',
      textfont: {size: 11, color: '#1f77b4'},
      hovertemplate: '<b>Bolsista</b><br>Ano: %{x}<br>%{y} bolsas<extra></extra>'
    },
    {
      x: years,
      y: voluntarios,
      text: voluntarios,
      type: 'scatter',
      mode: 'lines+markers+text',
      name: 'Voluntário',
      line: {width: 3, color: '#ff7f0e'},
      marker: {size: 9},
      textposition: 'top center',
      textfont: {size: 11, color: '#ff7f0e'},
      hovertemplate: '<b>Voluntário</b><br>Ano: %{x}<br>%{y} bolsas<extra></extra>'
    }
  ];
  
  var layout = {
    title: {
      text: 'Evolução de Bolsistas e Voluntários (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Ano',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Número de Participantes',
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

### Resumo por Modalidade

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Ano</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Bolsista</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Voluntário</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; background-color: #d1d1d1;"><strong>TOTAL</strong></th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">% Bolsista</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">% Voluntário</th>
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

## Bolsas ao Longo do Tempo por Programa

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
  <strong>Legenda:</strong> Este gráfico apresenta a distribuição de bolsas de IC por programa ao longo do tempo. Cada linha colorida representa um programa específico (PIBIC, PIBIT, PIBITI, etc.), permitindo visualizar quais programas tiveram maior participação em cada ano. A linha preta (TOTAL) mostra o número total de bolsas independente do programa.
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
    hovertemplate: '<b>TOTAL</b><br>Ano: %{x}<br>Bolsas: %{y}<extra></extra>'
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
      hovertemplate: '<b>' + program + '</b><br>Ano: %{x}<br>Bolsas: %{y}<extra></extra>'
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
      name: 'Sem Programa',
      line: {width: 2.5, color: '#999999', dash: 'dash'},
      marker: {size: 8},
      textposition: 'top center',
      textfont: {size: 10, color: '#999999'},
      hovertemplate: '<b>Sem Programa</b><br>Ano: %{x}<br>Bolsas: %{y}<extra></extra>'
    });
  }
  
  var layout = {
    title: {
      text: 'Bolsas de IC ao Longo do Tempo por Programa (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Ano',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Número de Bolsas',
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

### Resumo por Ano e Programa

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Ano</th>
      {% for program in all_programs %}
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">{{ program }}</th>
      {% endfor %}
      {% if year_blank.values()|sum > 0 %}
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Sem Programa</th>
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

## Bolsas por Agência de Fomento ao Longo do Tempo

{# Count scholarships by year and funding agency #}
{% set year_agency_data = {} %}
{% set year_agency_totals = {} %}
{% set all_agencies = [] %}

{% for s in ic_scholarships %}
  {% set year = s['year'] %}
  {% set agency = s['funding_agency'] if s['funding_agency'] and s['funding_agency'].strip() else 'Sem Agência' %}
  
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
  <strong>Legenda:</strong> Este gráfico mostra a origem do financiamento das bolsas ao longo dos anos. As principais agências de fomento são: <strong>Ifes</strong> (recursos institucionais), <strong>Fapes</strong> (Fundação de Amparo à Pesquisa do Espírito Santo), <strong>CNPq</strong> (Conselho Nacional de Desenvolvimento Científico e Tecnológico), e <strong>Voluntário</strong> (sem remuneração). A linha tracejada cinza representa bolsas sem agência especificada.
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
    hovertemplate: '<b>TOTAL</b><br>Ano: %{x}<br>Bolsas: %{y}<extra></extra>'
  });
  
  // Define colors for each agency
  var agencyColors = {
    'Ifes': '#1f77b4',
    'Fapes': '#ff7f0e',
    'CNPq': '#2ca02c',
    'Voluntário': '#d62728',
    'Sem Agência': '#999999'
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
    var lineStyle = agency === 'Sem Agência' ? 'dash' : 'solid';
    
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
      hovertemplate: '<b>' + agency + '</b><br>Ano: %{x}<br>Bolsas: %{y}<extra></extra>'
    });
  });
  
  var layout = {
    title: {
      text: 'Bolsas por Agência de Fomento ao Longo do Tempo (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Ano',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Número de Bolsas',
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

### Resumo por Ano e Agência de Fomento

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Ano</th>
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

## Distribuição de Bolsas por Valor

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
  <strong>Legenda:</strong> Este gráfico apresenta a evolução dos valores mensais das bolsas ao longo do tempo. Cada linha colorida representa um valor específico de bolsa (R$ 100, R$ 300, R$ 400, etc.). Note que os valores foram ajustados ao longo dos anos, com aumento gradual nos valores das bolsas, especialmente a partir de 2023. Os valores são agrupados em faixas de R$ 100 para facilitar a visualização.
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
        hovertemplate: '<b>R$ ' + value.toFixed(2) + '</b><br>Ano: %{x}<br>%{y} bolsas<extra></extra>'
      });
    }
  });
  
  var layout = {
    title: {
      text: 'Distribuição de Bolsas por Valor ao Longo do Tempo (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Ano',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Número de Bolsas',
      gridcolor: '#f0f0f0',
      rangemode: 'tozero'
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    hovermode: 'x unified',
    legend: {
      title: {text: 'Valor da Bolsa'},
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

### Resumo de Valores por Ano

<table style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 12px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">Ano</th>
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
  <strong>Legenda:</strong> Este gráfico de barras mostra o investimento financeiro total em bolsas de IC por ano no Campus Serra. Os valores representam a soma de todas as bolsas remuneradas concedidas em cada ano. O crescimento do investimento reflete tanto o aumento no número de bolsas quanto a valorização dos valores pagos aos bolsistas ao longo do tempo.
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
    hovertemplate: '<b>Ano %{x}</b><br>Investimento: R$ %{y:,.2f}<extra></extra>'
  }];
  
  var layout = {
    title: {
      text: 'Investimento em Bolsas por Ano (Campus Serra)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Ano',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Valor Total (R$)',
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

### Resumo Financeiro por Ano

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Ano</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Número de Bolsas</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Investimento Total</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Valor Médio por Bolsa</th>
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

{% for year in sorted_years %}

## {{ year }}

**Total:** {{ by_year[year]|length }} bolsas

{# Sort scholarships by student name #}
{% set sorted_scholarships = by_year[year]|sort(attribute='student') %}

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Estudante</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Orientador</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Programa</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Projeto</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Período</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Valor</th>
    </tr>
  </thead>
  <tbody>
    {% for s in sorted_scholarships %}
    <tr>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ s['student'] }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ s['advisor'] }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ s['program'] }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">{{ s['project_title'] if s['project_title'] else 'N/A' }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ s['start_date'] }} até {{ s['end_date'] }}</td>
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
