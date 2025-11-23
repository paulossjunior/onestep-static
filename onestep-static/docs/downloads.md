# Data Downloads

This page provides access to all research data files in JSON format. These datasets contain comprehensive information about research projects, scholarships, students, supervisors, and collaboration networks at Campus Serra.

---

## Available Datasets

### 📊 Research Projects
**File:** [research_projects.json](data/research_projects.json)  
**Format:** JSON  
**Description:** Complete database of research projects at Campus Serra.

**Contains:**
- Project identification (ID, title)
- Timeline (start date, end date)
- Coordinator and researchers
- Students involved
- Research group and knowledge area
- Research line and nature
- Partner organizations
- Funding information
- Publications count
- Keywords

**Use cases:**
- Analyze research trends over time
- Identify collaboration patterns
- Track project outcomes
- Study funding distribution

---

### 📚 Research Papers
**File:** [papers.json](data/papers.json)  
**Format:** JSON  
**Description:** Academic publications and citation data from Google Scholar.

**Contains:**
- Researcher profiles (name, affiliation, email)
- Google Scholar profile links
- Publication statistics (total papers, citations, h-index, i10-index)
- Research interests
- Individual publications with:
  - Title, authors, publication venue
  - Citation counts
  - Publication year
  - Links to papers
- Top 10 most cited papers per researcher

**Data Source:** Google Scholar (via SearchAPI.io)

**Use cases:**
- Analyze research impact and citations
- Track publication trends over time
- Identify highly cited papers
- Study research interests and collaborations
- Assess researcher productivity

---

### 🎓 IC Scholarships
**File:** [scholarships.json](data/scholarships.json)  
**Format:** JSON  
**Description:** Database of Scientific Initiation (IC) scholarships awarded to students.

**Contains:**
- Student information (name, email, course)
- Advisor details
- Scholarship program and modality (paid/volunteer)
- Project title and research area
- Period (start date, end date, year)
- Funding agency and value
- Execution campus
- Status (cancelled, accepted)

**Use cases:**
- Track student research participation
- Analyze funding sources and amounts
- Study scholarship distribution patterns
- Identify advisor-student relationships

---

### 👥 Students
**File:** [students.json](data/students.json)  
**Format:** JSON  
**Description:** Aggregated data about students' research activities.

**Contains:**
- Student identification (name, email, campus)
- Research projects participated
- IC scholarships received
- Advisors worked with
- Collaborations with other students
- Statistics (total projects, scholarships, years active)
- Timeline of activities

**Use cases:**
- Analyze student engagement in research
- Track student career progression
- Identify highly engaged students
- Study collaboration networks

---

### 👨‍🏫 Supervisors
**File:** [supervisors.json](data/supervisors.json)  
**Format:** JSON  
**Description:** Aggregated data about supervisors' research activities.

**Contains:**
- Supervisor identification (name, email, campus)
- Research projects coordinated
- IC scholarships supervised
- Students mentored
- Collaborations with other supervisors
- Statistics (total projects, supervisions, years active)
- Research areas and groups

**Use cases:**
- Analyze supervisor productivity
- Identify research leaders
- Study mentorship patterns
- Track research group activities

---

### 🔬 Research Groups
**File:** [research_group.json](data/research_group.json)  
**Format:** JSON  
**Description:** Information about research groups and their activities.

**Contains:**
- Group identification and description
- Associated projects
- Members and leaders
- Research lines
- Knowledge areas
- Campus location

**Use cases:**
- Map research group structure
- Analyze group productivity
- Study interdisciplinary collaborations
- Track research focus areas

---

### 🤝 Partnership Analysis
**File:** [partnership_analysis.json](data/partnership_analysis.json)  
**Format:** JSON  
**Description:** Analysis of external partnerships and collaborations.

**Contains:**
- Partner organizations and their projects
- External research groups
- Collaboration statistics
- Partnership distribution
- Project counts per partner

**Use cases:**
- Identify key external partners
- Analyze collaboration patterns
- Study industry-academia connections
- Track partnership evolution

---

### 🌐 Network Statistics
**File:** [network_stats.json](data/network_stats.json)  
**Format:** JSON  
**Description:** Network analysis metrics and statistics.

**Contains:**
- Collaboration network metrics
- Centrality measures
- Community detection results
- Network density and connectivity
- Key nodes and hubs

**Use cases:**
- Analyze collaboration networks
- Identify research hubs
- Study knowledge flow
- Detect research communities

---

## Data Format

All files are in **JSON (JavaScript Object Notation)** format, which is:
- ✅ Human-readable and machine-parsable
- ✅ Compatible with most programming languages
- ✅ Easy to import into data analysis tools
- ✅ Structured and hierarchical

### Example Structure

```json
{
  "metadata": {
    "generated_at": "2025-11-22T10:30:00",
    "total_records": 100,
    "source": "Campus Serra"
  },
  "data": [
    {
      "id": "123",
      "name": "Example",
      "details": {...}
    }
  ]
}
```

---

## How to Use

### Python Example
```python
import json

# Load data
with open('research_projects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Access projects
projects = data['projects']
for project in projects:
    print(project['title'])
```

### JavaScript Example
```javascript
// Load data
fetch('research_projects.json')
  .then(response => response.json())
  .then(data => {
    // Access projects
    const projects = data.projects;
    projects.forEach(project => {
      console.log(project.title);
    });
  });
```

### R Example
```r
library(jsonlite)

# Load data
data <- fromJSON('research_projects.json')

# Access projects
projects <- data$projects
head(projects)
```

---

## Data Updates

{% set current_date = get_current_date() %}

**Last Update:** {{ current_date['date_str'] }}

The datasets are automatically updated when:
- New research projects are registered
- Scholarships are awarded or modified
- Student or supervisor information changes
- Network analysis is recalculated

---

## License and Usage

**Terms of Use:**
- ✅ Free to use for academic and research purposes
- ✅ Attribution required when publishing results
- ✅ No commercial use without permission
- ✅ Data provided "as is" without warranties

**Citation:**
```
Campus Serra Research Data (2025). 
Instituto Federal do Espírito Santo - Campus Serra.
Available at: [URL]
```

---

## Support

For questions, issues, or data requests:
- 📧 Contact: [research@serra.ifes.edu.br](mailto:research@serra.ifes.edu.br)
- 🐛 Report issues: [GitHub Issues](https://github.com/your-repo/issues)
- 📖 Documentation: [Full Documentation](index.md)

---

## Download All

**Quick Download Links:**

| File | Size | Records | Download |
|------|------|---------|----------|
| research_projects.json | ~500 KB | ~300 projects | [⬇️ Download](data/research_projects.json) |
| papers.json | ~800 KB | ~50 researchers | [⬇️ Download](data/papers.json) |
| scholarships.json | ~800 KB | ~1000 scholarships | [⬇️ Download](data/scholarships.json) |
| students.json | ~600 KB | ~500 students | [⬇️ Download](data/students.json) |
| supervisors.json | ~400 KB | ~150 supervisors | [⬇️ Download](data/supervisors.json) |
| research_group.json | ~100 KB | ~30 groups | [⬇️ Download](data/research_group.json) |
| partnership_analysis.json | ~200 KB | Analysis data | [⬇️ Download](data/partnership_analysis.json) |
| network_stats.json | ~150 KB | Network metrics | [⬇️ Download](data/network_stats.json) |

---

<div style="background-color: #e7f5ff; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #1971c2;">
  <h3 style="margin-top: 0;">💡 Tips for Data Analysis</h3>
  <ul>
    <li><strong>Start with metadata:</strong> Check the metadata section in each file for context</li>
    <li><strong>Validate data:</strong> Always validate data types and handle missing values</li>
    <li><strong>Join datasets:</strong> Use IDs to join related datasets (e.g., student ID, project ID)</li>
    <li><strong>Time series:</strong> Use date fields for temporal analysis</li>
    <li><strong>Network analysis:</strong> Combine students, supervisors, and projects for network graphs</li>
  </ul>
</div>
