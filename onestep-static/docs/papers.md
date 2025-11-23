# Research Papers - Campus Serra

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
  #papersTable {
    width: 100% !important;
    table-layout: fixed !important;
  }
  #papersTable td {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
  }
</style>

<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>

{% set data = load_papers_data() %}
{% set researchers = data['researchers'] %}
{% set metadata = data %}

## Overview

{% set ns = namespace(total_pubs=0, all_years=[], total_years=0) %}
{% for r in researchers %}
  {% set pubs = r['statistics']['papers_by_year'].values()|sum %}
  {% set ns.total_pubs = ns.total_pubs + pubs %}
  {% for year in r['statistics']['papers_by_year'].keys() %}
    {% if year not in ns.all_years %}
      {% set _ = ns.all_years.append(year) %}
    {% endif %}
  {% endfor %}
{% endfor %}
{% set year_range = ns.all_years|map('int')|list %}
{% set min_year = year_range|min if year_range else 2000 %}
{% set max_year = year_range|max if year_range else 2025 %}
{% set years_span = max_year - min_year + 1 %}
{% set avg_pubs_per_year = (ns.total_pubs / years_span)|round(1) %}

**Total Researchers:** {{ metadata['total_researchers'] }}  
**Total Citations:** {{ researchers|sum(attribute='statistics.total_citations') }}

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-bottom: 30px;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ researchers|length }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Researchers</div>
  </div>
  <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ researchers|sum(attribute='statistics.total_citations') }}</div>
    <div style="font-size: 14px; margin-top: 5px;">Total Citations</div>
  </div>
</div>

### Research Areas Overview

<div id="research-areas-chart" style="width:100%;height:450px;margin-bottom:30px;"></div>

<script>
(function() {
  var researchers = {{ researchers|tojson }};
  
  // Aggregate data by research interest
  var interestData = {};
  
  researchers.forEach(function(r) {
    var interests = r.researcher.interests || [];
    var papers = r.statistics.papers_by_year;
    var totalPapers = Object.values(papers).reduce(function(a, b) { return a + b; }, 0);
    var citations = r.statistics.total_citations;
    
    interests.forEach(function(interest) {
      if (!interestData[interest]) {
        interestData[interest] = {
          papers: 0,
          citations: 0,
          researchers: []
        };
      }
      interestData[interest].papers += totalPapers;
      interestData[interest].citations += citations;
      interestData[interest].researchers.push(r.researcher.name);
    });
  });
  
  // Sort by citations and get top 10
  var sortedInterests = Object.keys(interestData).sort(function(a, b) {
    return interestData[b].citations - interestData[a].citations;
  }).slice(0, 10);
  
  var interests = sortedInterests;
  var citations = interests.map(function(i) { return interestData[i].citations; });
  
  var trace2 = {
    x: interests,
    y: citations,
    name: 'Citations',
    type: 'scatter',
    mode: 'lines+markers+text',
    text: citations,
    textposition: 'top center',
    line: {width: 3, color: '#f5576c'},
    marker: {size: 10, color: '#f5576c'},
    yaxis: 'y',
    hovertemplate: '<b>%{x}</b><br>Citations: %{y}<extra></extra>'
  };
  
  var data = [trace2];
  
  var layout = {
    title: {
      text: 'Top 10 Research Areas - Citations',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      tickangle: -45,
      automargin: true
    },
    yaxis: {
      title: 'Citations',
      titlefont: {color: '#f5576c'},
      tickfont: {color: '#f5576c'},
      side: 'left',
      rangemode: 'tozero'
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    legend: {
      x: 0.02,
      y: 0.98,
      bgcolor: 'rgba(255,255,255,0.9)',
      bordercolor: '#ccc',
      borderwidth: 1
    },
    margin: {t: 60, b: 120, l: 60, r: 80},
    height: 450
  };
  
  Plotly.newPlot('research-areas-chart', data, layout);
})();
</script>

### Publications and Citations by Year

<div id="pubs-citations-by-year-chart" style="width:100%;height:450px;margin-bottom:30px;"></div>

<script>
(function() {
  var researchers = {{ researchers|tojson }};
  
  // Aggregate publications by year
  var yearPubs = {};
  researchers.forEach(function(r) {
    var papersByYear = r.statistics.papers_by_year;
    Object.keys(papersByYear).forEach(function(year) {
      if (!yearPubs[year]) {
        yearPubs[year] = 0;
      }
      yearPubs[year] += papersByYear[year];
    });
  });
  
  // Aggregate citations by year
  var yearCitations = {};
  researchers.forEach(function(r) {
    var citationsByYear = r.statistics.citations_by_year;
    citationsByYear.forEach(function(item) {
      var year = item.year;
      if (!yearCitations[year]) {
        yearCitations[year] = 0;
      }
      var citeCount = item.citations || item.cites || 0;
      yearCitations[year] += citeCount;
    });
  });
  
  // Get all years and sort
  var allYears = new Set([...Object.keys(yearPubs), ...Object.keys(yearCitations)]);
  var years = Array.from(allYears).map(Number).sort();
  
  var citations = years.map(function(y) { return yearCitations[y] || 0; });
  
  var trace2 = {
    x: years,
    y: citations,
    name: 'Citations',
    type: 'scatter',
    mode: 'lines+markers+text',
    text: citations,
    textposition: 'top center',
    line: {width: 3, color: '#f5576c'},
    marker: {size: 8, color: '#f5576c'},
    yaxis: 'y',
    hovertemplate: '<b>Year %{x}</b><br>Citations: %{y}<extra></extra>'
  };
  
  var data = [trace2];
  
  var layout = {
    title: {
      text: 'Citations by Year (All Researchers)',
      font: {size: 18, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Year',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Citations',
      titlefont: {color: '#f5576c'},
      tickfont: {color: '#f5576c'},
      side: 'left',
      rangemode: 'tozero'
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    legend: {
      x: 0.02,
      y: 0.98,
      bgcolor: 'rgba(255,255,255,0.9)',
      bordercolor: '#ccc',
      borderwidth: 1
    },
    margin: {t: 60, b: 50, l: 60, r: 80},
    height: 450
  };
  
  Plotly.newPlot('pubs-citations-by-year-chart', data, layout);
})();
</script>

---

## Researchers Summary

<div style="margin-bottom: 20px;">
  <input type="text" id="searchInput" placeholder="Search researcher or paper..." 
         style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 4px;">
</div>

<table id="researchersTable" style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 13px; table-layout: fixed;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; cursor: pointer; width: 25%;" onclick="sortTable(0)">
        Name ▼
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; cursor: pointer; width: 10%;" onclick="sortTable(1)">
        Citations
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; cursor: pointer; width: 10%;" onclick="sortTable(2)">
        h-index
      </th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; width: 35%;">
        Research Interests
      </th>
    </tr>
  </thead>
  <tbody>
    {% for item in researchers|sort(attribute='researcher.name') %}
    <tr class="researcher-row">
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        <strong>{{ item['researcher']['name'] }}</strong>
        {% if item['researcher']['email'] %}
        <br><small style="color: #666;">{{ item['researcher']['email'] }}</small>
        {% endif %}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        <span style="font-weight: bold; color: #f5576c;">{{ item['statistics']['total_citations'] }}</span>
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">
        <span style="font-weight: bold; color: #28a745;">{{ item['statistics']['h_index']['all_time'] }}</span>
      </td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        <div style="display: flex; flex-wrap: wrap; gap: 3px; line-height: 1.8;">
          {% for interest in item['researcher']['interests'] %}
            <span style="background: #e3f2fd; color: #1565c0; padding: 2px 6px; border-radius: 3px; font-size: 11px; white-space: nowrap;">{{ interest }}</span>
          {% endfor %}
        </div>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>

<script>
// Search functionality
document.getElementById('searchInput').addEventListener('keyup', function() {
  var input = this.value.toLowerCase();
  var rows = document.querySelectorAll('.researcher-row');
  
  rows.forEach(function(row) {
    var text = row.textContent.toLowerCase();
    row.style.display = text.includes(input) ? '' : 'none';
  });
});

// Sort table functionality
function sortTable(columnIndex) {
  var table = document.getElementById('researchersTable');
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

## Top 10 Most Cited Papers (All Researchers)

{% set all_papers = [] %}
{% for item in researchers %}
  {% for paper in item['all_papers'] %}
    {% set _ = all_papers.append({'paper': paper, 'researcher': item['researcher']['name']}) %}
  {% endfor %}
{% endfor %}

{% set sorted_papers = all_papers|sort(attribute='paper.citations', reverse=True) %}
{% set top_papers = sorted_papers[:10] %}

<table style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 13px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Title</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; width: 150px;">Researcher</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Year</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 100px;">Citations</th>
    </tr>
  </thead>
  <tbody>
    {% for item in top_papers %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ loop.index }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        <strong>{{ item['paper']['title'] }}</strong>
        <br><small style="color: #666;">{{ item['paper']['authors'] }}</small>
        <br><small style="color: #999;">{{ item['paper']['publication'] }}</small>
      </td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        <small>{{ item['researcher'] }}</small>
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ item['paper']['year'] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold; color: #f5576c;">
        {{ item['paper']['citations'] }}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>

---

{% for item in researchers|sort(attribute='researcher.name') %}

## {{ item['researcher']['name'] }}

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
  <p style="margin: 5px 0;"><strong>Campus:</strong> {{ item['researcher']['campus'] }}</p>
  <p style="margin: 5px 0;"><strong>Affiliation:</strong> {{ item['researcher']['affiliation'] }}</p>
  {% if item['researcher']['email'] %}
  <p style="margin: 5px 0;"><strong>Email:</strong> {{ item['researcher']['email'] }}</p>
  {% endif %}
  <p style="margin: 5px 0;"><strong>Google Scholar:</strong> <a href="{{ item['researcher']['scholar_url'] }}" target="_blank">View Profile</a></p>
  <p style="margin: 10px 0 5px 0;"><strong>Research Interests:</strong></p>
  <div style="display: flex; flex-wrap: wrap; gap: 8px; margin: 5px 0 10px 0;">
    {% for interest in item['researcher']['interests'] %}
      <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 500;">{{ interest }}</span>
    {% endfor %}
  </div>
  <p style="margin: 5px 0;">
    <strong>h-index:</strong> 
    <span style="color: #28a745; font-weight: bold;">{{ item['statistics']['h_index']['all_time'] }}</span> (all time) | 
    <span style="color: #4facfe; font-weight: bold;">{{ item['statistics']['h_index']['since_2020'] }}</span> (since 2020)
  </p>
  <p style="margin: 5px 0;">
    <strong>i10-index:</strong> 
    <span style="color: #667eea; font-weight: bold;">{{ item['statistics']['i10_index']['all_time'] }}</span> (all time) | 
    <span style="color: #f5576c; font-weight: bold;">{{ item['statistics']['i10_index']['since_2020'] }}</span> (since 2020)
  </p>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; margin-bottom: 20px;">
  <div style="background: #f5576c; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ item['statistics']['total_citations'] }}</div>
    <div style="font-size: 12px;">Total Citations</div>
  </div>
  <div style="background: #4facfe; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ item['statistics']['h_index']['all_time'] }}</div>
    <div style="font-size: 12px;">h-index (all time)</div>
  </div>
  <div style="background: #00f2fe; color: white; padding: 15px; border-radius: 6px; text-align: center;">
    <div style="font-size: 24px; font-weight: bold;">{{ "%.1f"|format(item['statistics']['average_citations_per_paper']) }}</div>
    <div style="font-size: 12px;">Avg Citations/Paper</div>
  </div>
</div>


### Citation Timeline

<div id="citations-chart-{{ loop.index }}" style="width:100%;height:350px;margin-bottom:20px;"></div>

<script>
(function() {
  var citationsByYear = {{ item['statistics']['citations_by_year']|tojson }};
  
  var years = citationsByYear.map(function(item) { return item.year; });
  var citations = citationsByYear.map(function(item) { return item.citations || item.cites || 0; });
  
  var data = [{
    x: years,
    y: citations,
    type: 'scatter',
    mode: 'lines+markers+text',
    text: citations,
    textposition: 'top center',
    line: {width: 3, color: '#f5576c'},
    marker: {size: 8, color: '#f5576c'},
    fill: 'tozeroy',
    fillcolor: 'rgba(245, 87, 108, 0.2)',
    hovertemplate: '<b>Year %{x}</b><br>%{y} citations<extra></extra>'
  }];
  
  var layout = {
    title: {
      text: 'Citations by Year',
      font: {size: 16, family: 'Arial, sans-serif', color: '#222'}
    },
    xaxis: {
      title: 'Year',
      dtick: 1,
      gridcolor: '#e5e5e5'
    },
    yaxis: {
      title: 'Number of Citations',
      gridcolor: '#f0f0f0',
      rangemode: 'tozero'
    },
    plot_bgcolor: '#fafafa',
    paper_bgcolor: 'white',
    margin: {t: 50, b: 50, l: 50, r: 20},
    height: 350
  };
  
  Plotly.newPlot('citations-chart-{{ loop.index }}', data, layout);
})();
</script>

### Top 5 Most Cited Papers

<table style="width:100%; border-collapse: collapse; margin: 15px 0; font-size: 13px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 40px;">#</th>
      <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6;">Title & Details</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Year</th>
      <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 100px;">Citations</th>
    </tr>
  </thead>
  <tbody>
    {% for paper in item['top_5_papers'] %}
    <tr>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold;">{{ loop.index }}</td>
      <td style="padding: 8px; border: 1px solid #dee2e6;">
        <strong>{{ paper['title'] }}</strong>
        <br><small style="color: #666;">{{ paper['authors'] }}</small>
        <br><small style="color: #999;">{{ paper['publication'] }}</small>
        {% if paper['link'] %}
        <br><a href="{{ paper['link'] }}" target="_blank" style="font-size: 11px;">View on Google Scholar →</a>
        {% endif %}
      </td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ paper['year'] }}</td>
      <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold; color: #f5576c;">
        {{ paper['citations'] }}
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>

### All Publications ({{ item['all_papers']|length }})

<details style="margin-bottom: 20px;">
  <summary style="cursor: pointer; padding: 10px; background: #e9ecef; border-radius: 4px; font-weight: bold;">
    📋 View Complete Publications List
  </summary>
  <div style="margin-top: 10px;">
    <table style="width:100%; border-collapse: collapse; font-size: 13px;">
      <thead>
        <tr style="background-color: #f8f9fa;">
          <th style="padding: 8px; text-align: left; border: 1px solid #dee2e6;">Title & Details</th>
          <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Year</th>
          <th style="padding: 8px; text-align: center; border: 1px solid #dee2e6; width: 100px;">Citations</th>
        </tr>
      </thead>
      <tbody>
        {% for paper in item['all_papers']|sort(attribute='citations', reverse=True) %}
        <tr>
          <td style="padding: 8px; border: 1px solid #dee2e6;">
            <strong>{{ paper['title'] }}</strong>
            <br><small style="color: #666;">{{ paper['authors'] }}</small>
            <br><small style="color: #999;">{{ paper['publication'] }}</small>
            {% if paper['link'] %}
            <br><a href="{{ paper['link'] }}" target="_blank" style="font-size: 11px;">View on Google Scholar →</a>
            {% endif %}
          </td>
          <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6;">{{ paper['year'] }}</td>
          <td style="padding: 8px; text-align: center; border: 1px solid #dee2e6; font-weight: bold; color: #f5576c;">
            {{ paper['citations'] }}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</details>

---

{% endfor %}
