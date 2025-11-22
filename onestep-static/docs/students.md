# Students - Campus Serra

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

## Overview

**Total Students (Campus Serra):** {{ students|length }}

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
    <div style="font-size: 14px; margin-top: 5px;">With Research Projects</div>
  </div>
  <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ serra_with_scholarships }}</div>
    <div style="font-size: 14px; margin-top: 5px;">With IC Scholarships</div>
  </div>
  <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ ns.serra_with_both }}</div>
    <div style="font-size: 14px; margin-top: 5px;">With Both</div>
  </div>
  <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <div style="font-size: 32px; font-weight: bold;">{{ ns.serra_with_collabs }}</div>
    <div style="font-size: 14px; margin-top: 5px;">With Collaborations</div>
  </div>
</div>

### Scholarship Statistics

<div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 20px; border-radius: 8px; margin-bottom: 30px;">
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">{{ ns.total_scholarship_holders }}</div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Total Scholarship Holders</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Paid scholarships</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">{{ ns.total_volunteers }}</div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Total Volunteers</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Unpaid participation</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">
        {{ ns.total_scholarship_holders + ns.total_volunteers }}
      </div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Total Participations</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">All IC activities</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 36px; font-weight: bold; color: #333;">
        {{ "%.1f"|format((ns.total_scholarship_holders / (ns.total_scholarship_holders + ns.total_volunteers) * 100)) if (ns.total_scholarship_holders + ns.total_volunteers) > 0 else 0 }}%
      </div>
      <div style="font-size: 14px; color: #555; margin-top: 5px;">Scholarship Rate</div>
      <div style="font-size: 11px; color: #777; margin-top: 3px;">Paid vs total</div>
    </div>
  </div>
</div>

---

## Understanding Student Collaborations

<div style="background-color: #e3f2fd; padding: 20px; border-radius: 8px; margin-bottom: 30px; border-left: 4px solid #2196f3;">
  <h4 style="margin-top: 0; color: #1565c0;">💡 What are Student Collaborations?</h4>
  
  <p style="margin: 10px 0;">
    <strong>Student collaborations</strong> occur when two or more students work together on the same research project. 
    This metric helps identify:
  </p>
  
  <ul style="margin: 10px 0 10px 20px;">
    <li><strong>Teamwork experience:</strong> Students who have worked with peers on research projects</li>
    <li><strong>Networking:</strong> Students who have built connections with other researchers</li>
    <li><strong>Collaborative projects:</strong> Research projects that involve multiple students</li>
  </ul>
  
  <p style="margin: 10px 0;">
    <strong>Example:</strong> If a research project lists 3 students (Alice, Bob, and Charlie), then:
  </p>
  <ul style="margin: 10px 0 10px 20px;">
    <li>Alice has 2 collaborators (Bob and Charlie) on 1 shared project</li>
    <li>Bob has 2 collaborators (Alice and Charlie) on 1 shared project</li>
    <li>Charlie has 2 collaborators (Alice and Bob) on 1 shared project</li>
  </ul>
  
  <p style="margin: 10px 0;">
    <strong>Why it matters:</strong> Students with more collaborations typically have:
  </p>
  <ul style="margin: 10px 0 10px 20px;">
    <li>✓ Stronger teamwork skills</li>
    <li>✓ Broader research network</li>
    <li>✓ Experience in collaborative research environments</li>
    <li>✓ Exposure to different perspectives and approaches</li>
  </ul>
</div>

---

## Students List

{# Sort students alphabetically by name #}
{% set sorted_students = students|sort(attribute='name') %}

<div style="margin-bottom: 20px;">
  <input type="text" id="searchInput" placeholder="Search student..." 
         style="width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 4px;">
</div>

<table id="studentsTable" style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 12px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; width: 15%;">
        Name
      </th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; width: 35%;">
        Research Projects
      </th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6; width: 35%;">
        IC Scholarships
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 8%;">
        Collaborators
      </th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 7%;">
        Years
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
          <span style="color: #999; font-size: 11px;">No projects</span>
        {% endif %}
      </td>
      <td style="padding: 8px; border: 1px solid #dee2e6; vertical-align: top;">
        {% if student['ic_scholarships'] %}
          <div style="font-size: 11px;">
            {% for scholarship in student['ic_scholarships'] %}
              <div style="margin-bottom: 8px; {% if not loop.last %}border-bottom: 1px solid #eee; padding-bottom: 8px;{% endif %}">
                <strong style="color: #333;">{{ scholarship.get('project_title') or scholarship.get('research_project_title', 'Untitled') }}</strong>
                {% if scholarship.get('advisor') %}
                <br><span style="color: #2e7d32;">👤 {{ scholarship['advisor'] }}</span>
                {% endif %}
                <br><span style="color: #666;">
                  📅 {{ scholarship['year'] }} | 
                  {% if scholarship['modality'] == 'Bolsista' %}
                    💰 Scholarship
                  {% else %}
                    🤝 Volunteer
                  {% endif %}
                </span>
              </div>
            {% endfor %}
          </div>
        {% else %}
          <span style="color: #999; font-size: 11px;">No scholarships</span>
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

## Top 10 Students

### By Research Projects

<table style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 13px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Student</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Total</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Projects & Coordinators</th>
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

### By IC Scholarships

<table style="width:100%; border-collapse: collapse; margin: 20px 0; font-size: 13px;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Student</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 80px;">Total</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Scholarships & Advisors</th>
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
              <strong>{{ scholarship.get('project_title') or scholarship.get('research_project_title', 'Untitled') }}</strong>
              {% if scholarship.get('advisor') %}
              <br><span style="color: #2e7d32;">👤 {{ scholarship['advisor'] }}</span>
              {% endif %}
              <span style="color: #666;"> | {{ scholarship['year'] }} | 
              {% if scholarship['modality'] == 'Bolsista' %}💰 Paid{% else %}🤝 Volunteer{% endif %}</span>
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

### By Collaborations

<table style="width:100%; border-collapse: collapse; margin: 20px 0;">
  <thead>
    <tr style="background-color: #e9ecef;">
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6; width: 50px;">#</th>
      <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Name</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Collaborators</th>
      <th style="padding: 10px; text-align: center; border: 1px solid #dee2e6;">Shared Projects</th>
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
