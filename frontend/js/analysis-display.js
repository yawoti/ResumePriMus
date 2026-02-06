// Analysis Results Display Logic

let currentAnalysisResults = null;

function displayAnalysisResults(results) {
    /**
     * Display all analysis results in the UI
     *
     * @param {object} results - Complete analysis results
     */

    // Store results globally for download
    currentAnalysisResults = results;

    // Display executive summary scores
    displayExecutiveSummary(results);

    // Display each step
    displayStep1JobAnalysis(results.step1_job_analysis);
    displayStep2GapAnalysis(results.step2_gap_analysis);
    displayStep3ATSScan(results.step3_ats_scan);
    displayStep4OptimizedResume(results.step4_optimized_resume);
}

function displayExecutiveSummary(results) {
    // Display match score
    const matchScore = results.step2_gap_analysis?.match_score || 0;
    document.getElementById('match-score').textContent = matchScore;

    // Display ATS score
    const atsScore = results.step3_ats_scan?.ats_score || 0;
    document.getElementById('ats-score').textContent = atsScore;
}

function displayStep1JobAnalysis(data) {
    const container = document.getElementById('job-analysis-content');
    container.innerHTML = '';

    // Required Skills
    const reqSection = createSection('Required Skills (Must-Have)');
    reqSection.appendChild(createList(data.required_skills));
    container.appendChild(reqSection);

    // Preferred Skills
    const prefSection = createSection('Preferred Skills (Nice-to-Have)');
    prefSection.appendChild(createList(data.preferred_skills));
    container.appendChild(prefSection);

    // Key Responsibilities
    const respSection = createSection('Key Responsibilities');
    respSection.appendChild(createList(data.key_responsibilities));
    container.appendChild(respSection);

    // ATS Keywords
    const keywordsSection = createSection('ATS Keywords');
    keywordsSection.appendChild(createList(data.ats_keywords));
    container.appendChild(keywordsSection);
}

function displayStep2GapAnalysis(data) {
    const container = document.getElementById('gap-analysis-content');
    container.innerHTML = '';

    // Match Score with Bar
    const scoreSection = createSection('Match Score');
    const scoreBar = createScoreBar(data.match_score);
    scoreSection.appendChild(scoreBar);
    container.appendChild(scoreSection);

    // Strengths
    const strengthsSection = createSection('Strengths');
    const strengthsList = createList(data.strengths, 'analysis-list strengths');
    strengthsSection.appendChild(strengthsList);
    container.appendChild(strengthsSection);

    // Gaps
    const gapsSection = createSection('Gaps to Address');
    if (data.gaps && data.gaps.length > 0) {
        const gapsList = document.createElement('ul');
        gapsList.className = 'analysis-list gaps';

        data.gaps.forEach(gap => {
            const li = document.createElement('li');

            const badge = document.createElement('span');
            badge.className = `priority-badge priority-${gap.priority}`;
            badge.textContent = gap.priority.toUpperCase();

            li.appendChild(badge);
            li.appendChild(document.createTextNode(
                `${gap.keyword} - ${gap.suggestion}`
            ));

            gapsList.appendChild(li);
        });

        gapsSection.appendChild(gapsList);
    }
    container.appendChild(gapsSection);

    // Keyword Match Table
    if (data.keyword_matches) {
        const tableSection = createSection('Keyword Match Table');
        const table = createKeywordMatchTable(data.keyword_matches);
        tableSection.appendChild(table);
        container.appendChild(tableSection);
    }
}

function displayStep3ATSScan(data) {
    const container = document.getElementById('ats-scan-content');
    container.innerHTML = '';

    // ATS Score with Bar
    const scoreSection = createSection('ATS Compatibility Score');
    const scoreBar = createScoreBar(data.ats_score);
    scoreSection.appendChild(scoreBar);
    container.appendChild(scoreSection);

    // Issues
    if (data.issues) {
        const issuesSection = createSection('Issues Found');
        const issuesContainer = document.createElement('div');
        issuesContainer.className = 'issues-container';

        if (data.issues.formatting && data.issues.formatting.length > 0) {
            const formatDiv = createIssueCategory('Formatting Issues', data.issues.formatting, 'formatting');
            issuesContainer.appendChild(formatDiv);
        }

        if (data.issues.content && data.issues.content.length > 0) {
            const contentDiv = createIssueCategory('Content Issues', data.issues.content, 'content');
            issuesContainer.appendChild(contentDiv);
        }

        if (data.issues.keywords && data.issues.keywords.length > 0) {
            const keywordsDiv = createIssueCategory('Keyword Issues', data.issues.keywords, 'keywords');
            issuesContainer.appendChild(keywordsDiv);
        }

        issuesSection.appendChild(issuesContainer);
        container.appendChild(issuesSection);
    }

    // Section Readability
    if (data.section_readability) {
        const readabilitySection = createSection('Section-by-Section Readability');
        const readabilityGrid = createReadabilityGrid(data.section_readability);
        readabilitySection.appendChild(readabilityGrid);
        container.appendChild(readabilitySection);
    }

    // Recommendations
    if (data.recommendations && data.recommendations.length > 0) {
        const recSection = createSection('Recommendations');
        const recList = document.createElement('ul');
        recList.className = 'recommendations-list';

        data.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recList.appendChild(li);
        });

        recSection.appendChild(recList);
        container.appendChild(recSection);
    }
}

function displayStep4OptimizedResume(data) {
    const container = document.getElementById('optimized-resume-content');
    container.innerHTML = '';

    // Resume Preview
    const preview = document.createElement('div');
    preview.className = 'resume-preview';
    preview.textContent = data.formatted_text || 'No optimized resume generated';

    container.appendChild(preview);
}

// Helper Functions

function createSection(title) {
    const section = document.createElement('div');
    section.className = 'analysis-section';

    const heading = document.createElement('h4');
    heading.textContent = title;
    section.appendChild(heading);

    return section;
}

function createList(items, className = 'analysis-list') {
    const ul = document.createElement('ul');
    ul.className = className;

    if (!items || items.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'None found';
        li.style.borderLeft = '4px solid #9ca3af';
        li.style.color = '#6b7280';
        ul.appendChild(li);
        return ul;
    }

    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        ul.appendChild(li);
    });

    return ul;
}

function createScoreBar(score) {
    const container = document.createElement('div');
    container.className = 'score-indicator';

    const bar = document.createElement('div');
    bar.className = 'score-bar';

    const fill = document.createElement('div');
    fill.className = 'score-fill';

    // Determine color based on score
    if (score >= 75) {
        fill.classList.add('high');
    } else if (score >= 50) {
        fill.classList.add('medium');
    } else {
        fill.classList.add('low');
    }

    fill.style.width = `${score}%`;
    fill.textContent = `${score}%`;

    bar.appendChild(fill);
    container.appendChild(bar);

    return container;
}

function createKeywordMatchTable(keywordMatches) {
    const table = document.createElement('table');
    table.className = 'keyword-table';

    // Header
    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Keyword</th>
            <th>Present in Resume</th>
        </tr>
    `;
    table.appendChild(thead);

    // Body
    const tbody = document.createElement('tbody');

    Object.entries(keywordMatches).forEach(([keyword, isPresent]) => {
        const tr = document.createElement('tr');

        const tdKeyword = document.createElement('td');
        tdKeyword.textContent = keyword;

        const tdStatus = document.createElement('td');
        const statusSpan = document.createElement('span');
        statusSpan.className = `keyword-match ${isPresent ? 'present' : 'missing'}`;
        statusSpan.textContent = isPresent ? 'Yes' : 'No';
        tdStatus.appendChild(statusSpan);

        tr.appendChild(tdKeyword);
        tr.appendChild(tdStatus);
        tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    return table;
}

function createIssueCategory(title, issues, type) {
    const div = document.createElement('div');
    div.className = 'issue-category';

    const heading = document.createElement('h5');
    heading.textContent = title;
    div.appendChild(heading);

    const ul = document.createElement('ul');
    ul.className = `issue-list ${type}`;

    issues.forEach(issue => {
        const li = document.createElement('li');
        li.textContent = issue;
        ul.appendChild(li);
    });

    div.appendChild(ul);
    return div;
}

function createReadabilityGrid(sectionReadability) {
    const grid = document.createElement('div');
    grid.className = 'readability-grid';

    Object.entries(sectionReadability).forEach(([section, status]) => {
        const item = document.createElement('div');
        item.className = `readability-item ${status}`;

        const sectionName = document.createElement('div');
        sectionName.className = 'section-name';
        sectionName.textContent = section;

        const statusDiv = document.createElement('div');
        statusDiv.className = 'status';
        statusDiv.textContent = status.replace(/_/g, ' ').toUpperCase();

        item.appendChild(sectionName);
        item.appendChild(statusDiv);
        grid.appendChild(item);
    });

    return grid;
}
