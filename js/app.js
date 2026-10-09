// Exam Generator App Controller
// Handles form input, API calls, and exam paper rendering

document.addEventListener('DOMContentLoaded', () => {
  const btnGenerate = document.getElementById('btnGenerate');
  const btnDownloadPDF = document.getElementById('btnDownloadPDF');
  const btnRegenerate = document.getElementById('btnRegenerate');
  const classLevelSelect = document.getElementById('classLevel');
  const topicGroup = document.getElementById('topicGroup');
  const topicSelect = document.getElementById('topicSelect');
  const paperWrapper = document.getElementById('paperWrapper');
  const examPaper = document.getElementById('examPaper');

  let currentExamIndex = 0;

  const TOPICS = {
    form1: [
      { id: 'F1T1', title: 'Topic 1: The Concept of Bible and Bible Knowledge' },
      { id: 'F1T2', title: 'Topic 2: God\'s Creation' },
      { id: 'F1T3', title: 'Topic 3: The Fall of Man' },
      { id: 'F1T4', title: 'Topic 4: The Formation of Patriarchs' },
    ],
    form2: [
      { id: 'F2T1', title: 'Topic 1: God\'s Love and Compassion (Includes All Form 1 Topics)' },
      { id: 'F2T2', title: 'Topics 1-2: God\'s Love & Sinai Covenant' },
      { id: 'F2T3', title: 'Topics 1-3: + Statistics & Census' },
      { id: 'F2T4', title: 'Topics 1-4: + Leadership' },
      { id: 'F2T5', title: 'Topics 1-5: All Form 2 Topics' },
    ],
    form5: [
      { id: 'F5T1', title: 'Topic 1: Introduction to Divinity' },
      { id: 'F5T2', title: 'Topics 1-2: + Governance' },
      { id: 'F5T3', title: 'Topics 1-3: + Courage and Decision-Making' },
      { id: 'F5T4', title: 'Topics 1-4: + Teachings of Isaiah' },
      { id: 'F5T5', title: 'Topics 1-5: + Social Justice (Amos)' },
      { id: 'F5T6', title: 'Topics 1-6: + Compassion (Hosea)' },
      { id: 'F5T7', title: 'Topics 1-7: All Form 5 Topics' },
    ],
    form6: [
      { id: 'F6T1', title: 'Topic 1: Overview of NT Books (Includes All Form 5 Topics)' },
      { id: 'F6T2', title: 'Topics 1-2: + Gospel of Matthew' },
      { id: 'F6T3', title: 'Topics 1-3: + Gospel of John' },
      { id: 'F6T4', title: 'Topics 1-4: + Letter to the Romans' },
      { id: 'F6T5', title: 'Topics 1-5: All Form 6 Topics' },
    ],
  };

  classLevelSelect.addEventListener('change', (e) => {
    const level = e.target.value;
    if (level && TOPICS[level]) {
      topicSelect.innerHTML = TOPICS[level].map(t => `<option value="${t.id}">${t.title}</option>`).join('');
      topicGroup.style.display = 'flex';
    } else {
      topicGroup.style.display = 'none';
    }
    updateGenerateButton();
  });

  topicSelect.addEventListener('change', updateGenerateButton);

  function updateGenerateButton() {
    btnGenerate.disabled = !classLevelSelect.value || !topicSelect.value;
  }

  async function runExamGeneration() {
    const schoolName = document.getElementById('schoolName').value;
    const examType = document.getElementById('examType').value;
    const examDate = document.getElementById('examDate').value;
    const level = classLevelSelect.value;
    const selectedTopic = topicSelect.value;

    btnGenerate.disabled = true;
    btnGenerate.textContent = 'Generating...';

    try {
      const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const endpoint = isLocal ? '/.netlify/functions/generate-exam' : '/.netlify/functions/generate-exam';

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          schoolName, examType, examDate, level, selectedTopic, examIndex: currentExamIndex
        })
      });

      if (!response.ok) throw new Error('Failed to generate exam');
      const exam = await response.json();

      renderExamPaper(exam);
      paperWrapper.style.display = 'block';
      btnDownloadPDF.disabled = false;
      btnRegenerate.disabled = false;
      paperWrapper.scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
      alert('Error: ' + err.message + '\n\nMake sure the Netlify function is deployed.');
    } finally {
      btnGenerate.disabled = false;
      btnGenerate.textContent = 'Generate Exam Paper';
    }
  }

  btnGenerate.addEventListener('click', () => {
    currentExamIndex = 0;
    runExamGeneration();
  });

  btnRegenerate.addEventListener('click', () => {
    currentExamIndex++;
    runExamGeneration();
  });

  btnDownloadPDF.addEventListener('click', () => {
    window.print();
  });

  // ===== Exam Paper Rendering =====

  function renderExamPaper(exam) {
    examPaper.innerHTML = '';

    if (exam.type === 'bible-knowledge') {
      renderBKPaper(exam);
    } else {
      renderDVPaper(exam);
    }
  }

  function renderBKPaper(exam) {
    // Cover Page
    const cover = createDiv('necta-page');
    cover.innerHTML = `
      <div class="candidate-header">Candidate Assessment Number: __________________________</div>
      <div style="height: 20px;"></div>
      <div class="cover-row">
        <div></div>
        <div style="text-align:center;">
          <div class="cover-title">THE UNITED REPUBLIC OF TANZANIA</div>
          <div class="cover-title underlined">${escapeHtml(exam.schoolName)}</div>
          <div class="cover-title">${exam.formText} <span class="underlined">${escapeHtml(exam.examType)}</span></div>
        </div>
        <div></div>
      </div>
      <div class="code-time-row">
        <span><b>CODE: ${exam.subjectCode}</b></span>
        <span><b>${exam.subjectName}</b></span>
        <span><b>Duration: ${exam.duration}</b></span>
      </div>
      <div style="text-align:right; font-weight:bold; margin-bottom:12px;">
        Date: ${exam.examDate ? formatDate(exam.examDate) : '____________________________'}
      </div>
      <div class="instructions">
        <h5>Instructions</h5>
        <ol>
          <li>This paper consists of <b>sections A, B and C</b> with a total of <b>ten (10)</b> questions.</li>
          <li>Answer <b>all</b> questions in the spaces provided.</li>
          <li>Section A carries <b>fifteen (15)</b> marks, section B carries <b>seventy (70)</b> marks and section C carries <b>fifteen (15)</b> marks.</li>
          <li>All writing must be in <b>black</b> or <b>blue</b> ink.</li>
          <li>Communication devices, Bibles and any unauthorised materials are <b>not</b> allowed in the assessment room.</li>
          <li>Write your <b>Assessment Number</b> at the top right hand corner of every page.</li>
        </ol>
      </div>
      ${renderAssessorTable(10)}
    `;
    examPaper.appendChild(cover);

    // Section A
    const pageA = createDiv('necta-page');
    pageA.innerHTML = `
      <div class="subject-header">${exam.subjectCode} ${exam.subjectName}</div>
      <div class="candidate-header">Candidate Assessment Number: __________________________</div>
      <div class="section-header">SECTION A (15 Marks)</div>
      <div class="section-sub">Answer <b>all</b> questions in this section.</div>
      <div class="question-text"><b>1.</b> ${exam.q1.stem}</div>
      ${exam.q1.items.map((item, i) => `
        <div class="mcq-container">
          <div class="mcq-row">
            <div class="mcq-q-text">${item.label} ${escapeHtml(item.leadStatement)}</div>
            <div class="mcq-ans-box"></div>
          </div>
          <div class="mcq-options-grid">
            ${item.options.map((opt, j) => `<div>${String.fromCharCode(65+j)} &nbsp; ${escapeHtml(opt)}</div>`).join('')}
          </div>
        </div>
      `).join('')}
      <div class="question-text"><b>2.</b> ${escapeHtml(exam.q2.stem)}</div>
      <table class="matching-lists">
        <tr><th>List A</th><th>List B</th></tr>
        ${exam.q2.listA.map((a, i) => `<tr><td>${escapeHtml(a)}</td><td>${i < exam.q2.listB.length ? exam.q2.listB[i].letter + ' &nbsp; ' + escapeHtml(exam.q2.listB[i].name) : ''}</td></tr>`).join('')}
      </table>
    `;
    examPaper.appendChild(pageA);

    // Section B
    const pageB = createDiv('necta-page');
    let bHtml = `
      <div class="subject-header">${exam.subjectCode} ${exam.subjectName}</div>
      <div class="candidate-header">Candidate Assessment Number: __________________________</div>
      <div class="section-header">SECTION B (70 Marks)</div>
      <div class="section-sub">Answer <b>all</b> questions in this section.</div>
    `;
    exam.sectionB.forEach(q => {
      bHtml += `<div class="question-text"><b>${q.no}.</b> ${escapeHtml(q.stem)}</div>`;
      q.subparts.forEach(sp => {
        bHtml += `<div class="subpart">(${sp.label}) ${escapeHtml(sp.text)}</div>`;
        const lineCount = sp.lines || 3;
        for (let i = 0; i < lineCount; i++) {
          bHtml += `<div class="dotted-line"></div>`;
        }
      });
    });
    pageB.innerHTML = bHtml;
    examPaper.appendChild(pageB);

    // Section C
    const pageC = createDiv('necta-page');
    pageC.innerHTML = `
      <div class="subject-header">${exam.subjectCode} ${exam.subjectName}</div>
      <div class="candidate-header">Candidate Assessment Number: __________________________</div>
      <div class="section-header">SECTION C (15 Marks)</div>
      <div class="section-sub">Answer question <b>ten (10)</b>.</div>
      <div class="question-text"><b>10.</b> ${escapeHtml(exam.q10.statement)} ${escapeHtml(exam.q10.task)}</div>
      ${Array.from({length: 18}, () => '<div class="dotted-line"></div>').join('')}
    `;
    examPaper.appendChild(pageC);
  }

  function renderDVPaper(exam) {
    // Cover Page
    const cover = createDiv('necta-page');
    cover.innerHTML = `
      <div class="candidate-header">Examination Number: __________________________</div>
      <div style="height: 20px;"></div>
      <div class="cover-row">
        <div></div>
        <div style="text-align:center;">
          <div class="cover-title">THE UNITED REPUBLIC OF TANZANIA</div>
          <div class="cover-title underlined">${escapeHtml(exam.schoolName)}</div>
          <div class="cover-title">${exam.formText} <span class="underlined">${escapeHtml(exam.examType)}</span></div>
        </div>
        <div></div>
      </div>
      <div class="code-time-row">
        <span><b>CODE: ${exam.subjectCode}</b></span>
        <span><b>${exam.subjectName}</b></span>
        <span><b>TIME: ${exam.duration}</b></span>
      </div>
      <div style="text-align:right; font-weight:bold; margin-bottom:12px;">
        Date: ${exam.examDate ? formatDate(exam.examDate) : '____________________________'}
      </div>
      <div class="instructions">
        <h5>Instructions</h5>
        <ol>
          <li>This paper consists of section A and section B with total of nine (9) questions.</li>
          <li>Answer all questions in section A and any two questions in section B.</li>
          <li>Cellular phones and any other sort of unauthorized materials are not allowed in the examination room.</li>
          <li>Write your examination number on every page of your answer booklet.</li>
        </ol>
      </div>
      ${renderAssessorTable(9)}
    `;
    examPaper.appendChild(cover);

    // Section A
    const pageA = createDiv('necta-page');
    let aHtml = `
      <div class="subject-header">${exam.subjectCode} ${exam.subjectName}</div>
      <div class="candidate-header">Examination Number: __________________________</div>
      <div class="section-header">SECTION A (60 Marks)</div>
      <div class="section-sub">Answer <b>all</b> questions in this section.</div>
    `;
    exam.sectionA.forEach(q => {
      aHtml += `<div class="question-text"><b>${q.no}.</b> ${escapeHtml(q.stem)}</div>`;
      q.subparts.forEach(sp => {
        aHtml += `<div class="subpart">(${sp.label}) ${escapeHtml(sp.text)}</div>`;
      });
    });
    pageA.innerHTML = aHtml;
    examPaper.appendChild(pageA);

    // Section B
    const pageB = createDiv('necta-page');
    let bHtml = `
      <div class="subject-header">${exam.subjectCode} ${exam.subjectName}</div>
      <div class="candidate-header">Examination Number: __________________________</div>
      <div class="section-header">SECTION B (40 Marks)</div>
      <div class="section-sub">Answer <b>any two (2)</b> questions from this section.</div>
    `;
    exam.sectionB.forEach(q => {
      bHtml += `<div class="question-text"><b>${q.no}.</b> ${escapeHtml(q.stem)}</div>`;
    });
    pageB.innerHTML = bHtml;
    examPaper.appendChild(pageB);
  }

  function renderAssessorTable(numQuestions) {
    let rows = `<tr><th>QUESTION<br/>NUMBER</th><th>QUESTION<br/>ATTEMPTED<br/>(PUT A TICK ✓)</th><th>SCORE</th><th>EXAMINER'S<br/>INITIALS</th></tr>`;
    for (let n = 1; n <= numQuestions; n++) {
      rows += `<tr><td>${n}</td><td></td><td></td><td></td></tr>`;
    }
    rows += `<tr><td><b>TOTAL MARKS</b></td><td></td><td></td><td></td></tr>`;
    rows += `<tr><td><b>CHECKER'S INITIALS</b></td><td></td><td></td><td></td></tr>`;
    return `<table class="assessor-table">${rows}</table>`;
  }

  function createDiv(className) {
    const div = document.createElement('div');
    div.className = className;
    return div;
  }

  function escapeHtml(text) {
    if (!text) return '';
    return String(text).replace(/[&<>'"]/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    }[c]));
  }

  function formatDate(dateStr) {
    if (!dateStr) return '____________________________';
    const [year, month] = dateStr.split('-');
    const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    return `${months[parseInt(month)-1]} ${year}`;
  }
});
