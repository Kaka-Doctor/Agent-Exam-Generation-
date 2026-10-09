# Agent Exam Generation

Automated exam paper generator for Tanzanian secondary school Bible Knowledge (Form 1-2) and Divinity (Form 5-6) examinations following NECTA format.

## Features

- **Bible Knowledge Exams (Ordinary Level)**
  - Subject code: 014 BIBLE KNOWLEDGE
  - Duration: 2:30 Hours
  - Section A: 10 MCQs + matching question (15 marks)
  - Section B: 7 structured questions with a/b/c/d subparts (70 marks)
  - Section C: 1 essay question (15 marks)

- **Divinity Exams (Advanced Level)**
  - Subject code: 114/1 (Form 5) or 114/2 (Form 6)
  - Duration: 3:00 Hours
  - Section A: 6 short-answer questions with a/b/c/d subparts (60 marks)
  - Section B: 3 essay questions, answer 2 (40 marks)

- **Smart Question Selection**
  - MCQ answers shuffled randomly
  - Matching List B shuffled with letters reassigned
  - No self-answering questions
  - No thematic overlap between questions in the same exam
  - 100% cross-exam uniqueness within each set

## Deployment (Netlify)

1. Fork or clone this repository
2. Connect to Netlify
3. Build settings are configured in `netlify.toml`
4. Deploy — the app is ready to use

## Usage

1. Enter school name, exam type, and date
2. Select class level (Form 1, 2, 5, or 6)
3. Select topic scope
4. Click "Generate Exam Paper"
5. Preview the exam in the browser
6. Click "Download PDF" to print/save

## Topics Covered

### Bible Knowledge (Form 1-2)
- **Form 1:** Concept of Bible, God's Creation, Fall of Man, Formation of Patriarchs
- **Form 2:** God's Love & Compassion, Sinai Covenant, Statistics & Census, Leadership, Patriotism

### Divinity (Form 5-6)
- **Form 5:** Introduction to Divinity, Governance, Courage & Decision-Making, Isaiah, Social Justice (Amos), Compassion (Hosea), Responsibility (Haggai & Zechariah)
- **Form 6:** Overview of NT Books, Gospel of Matthew, Gospel of John, Letter to the Romans, Epistle of James

## Environment Variables

Set the following in Netlify dashboard (Site Settings → Environment Variables):
- `GITHUB_TOKEN` - GitHub access token (for repo access if needed)

## License

MIT
