"""
Generate a Form Five Divinity examination paper (NECTA format) based on
Form 5 Topic 1: Introduction to Divinity.

Format follows the example NECTA Divinity exams:
- Subject code: 114/1 DIVINITY 1
- Time: 3:00 Hours
- Section A (60 marks): 6 questions, answer ALL
- Section B (40 marks): 3 essay questions, answer TWO
- Total: 9 questions
- No MCQs or matching — all open-ended with (a)(b)(c) subparts

Cover page has blank fields for School Name, Examination Type, and Date.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, NextPageTemplate, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ---------- Paths ----------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
COAT_OF_ARMS_PNG = os.path.join(PROJECT_ROOT, "assets", "coat_of_arms_cropped.png")
OUTPUT_PDF = os.path.join(PROJECT_ROOT, "download", "Form5_Divinity_Topic1_Exam.pdf")

# ---------- Font registration ----------
FONT_DIR = "/usr/share/fonts/truetype"
pdfmetrics.registerFont(TTFont('Tinos', f'{FONT_DIR}/liberation/LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Tinos-Bold', f'{FONT_DIR}/liberation/LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Tinos-Italic', f'{FONT_DIR}/liberation/LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Tinos-BoldItalic', f'{FONT_DIR}/liberation/LiberationSerif-BoldItalic.ttf'))
registerFontFamily('Tinos', normal='Tinos', bold='Tinos-Bold',
                   italic='Tinos-Italic', boldItalic='Tinos-BoldItalic')

# ---------- Colors ----------
BLACK = colors.HexColor("#000000")
GRAY = colors.HexColor("#666666")
BG_GRAY = colors.HexColor("#eeeeee")

# ---------- Page geometry ----------
PAGE_W, PAGE_H = A4
MARGIN_L = 18 * mm
MARGIN_R = 18 * mm
MARGIN_T = 14 * mm
MARGIN_B = 14 * mm
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R
CONTENT_H = PAGE_H - MARGIN_T - MARGIN_B

# ---------- Paragraph styles ----------
BODY_FONT = 'Tinos'
BODY_FONT_BOLD = 'Tinos-Bold'
BODY_FONT_ITALIC = 'Tinos-Italic'

style_cover_title = ParagraphStyle(
    'CoverTitle', fontName=BODY_FONT_BOLD, fontSize=14, leading=18,
    alignment=TA_CENTER, textColor=BLACK, spaceAfter=4,
)
style_cover_school = ParagraphStyle(
    'CoverSchool', fontName=BODY_FONT_BOLD, fontSize=14, leading=18,
    alignment=TA_CENTER, textColor=BLACK, spaceAfter=4
)
style_cover_form_line = ParagraphStyle(
    'CoverFormLine', fontName=BODY_FONT_BOLD, fontSize=14, leading=18,
    alignment=TA_CENTER, textColor=BLACK, spaceAfter=4
)
style_cover_meta = ParagraphStyle(
    'CoverMeta', fontName=BODY_FONT_BOLD, fontSize=12, leading=15,
    alignment=TA_CENTER, textColor=BLACK, spaceAfter=2
)
style_candidate_no = ParagraphStyle(
    'CandidateNo', fontName=BODY_FONT_BOLD, fontSize=10, leading=12,
    alignment=TA_RIGHT, textColor=BLACK
)
style_instr_h = ParagraphStyle(
    'InstrH', fontName=BODY_FONT_BOLD, fontSize=11, leading=13,
    alignment=TA_LEFT, textColor=BLACK, spaceAfter=6
)
style_instr_li = ParagraphStyle(
    'InstrLi', fontName=BODY_FONT, fontSize=10.5, leading=14,
    alignment=TA_JUSTIFY, textColor=BLACK, leftIndent=20, bulletIndent=6,
    spaceAfter=4
)
style_section_h = ParagraphStyle(
    'SectionH', fontName=BODY_FONT_BOLD, fontSize=12, leading=15,
    alignment=TA_CENTER, textColor=BLACK, spaceBefore=14, spaceAfter=4
)
style_section_sub = ParagraphStyle(
    'SectionSub', fontName=BODY_FONT, fontSize=10.5, leading=14,
    alignment=TA_CENTER, textColor=BLACK, spaceAfter=8
)
style_qtext = ParagraphStyle(
    'QText', fontName=BODY_FONT, fontSize=11, leading=14.5,
    alignment=TA_JUSTIFY, textColor=BLACK, spaceBefore=12, spaceAfter=4
)
style_subpart = ParagraphStyle(
    'Subpart', fontName=BODY_FONT, fontSize=11, leading=14.5,
    alignment=TA_JUSTIFY, textColor=BLACK, leftIndent=20,
    spaceBefore=4, spaceAfter=3
)


# ---------- Custom Flowables ----------
class DottedLine(Flowable):
    """A single horizontal dotted line for handwritten answers."""
    def __init__(self, width=None, height=20):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        if self.width is None:
            self.width = availWidth
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setDash(1, 2)
        c.setStrokeColor(GRAY)
        c.setLineWidth(0.5)
        c.line(0, 2, self.width, 2)
        c.restoreState()


def add_answer_lines(count, line_height=20):
    """Return a list of dotted line flowables."""
    return [DottedLine(width=CONTENT_W, height=line_height) for _ in range(count)]


# ---------- Build cover page ----------
def build_cover_page():
    """Cover page with coat of arms on the LEFT, three centered headings,
    subject code 114/1 DIVINITY 1, time 3:00 Hours, blank date field,
    instructions, and question table for 9 questions."""
    story = []

    # Candidate Examination Number (top right)
    story.append(Paragraph(
        "Examination Number: __________________________",
        style_candidate_no
    ))
    story.append(Spacer(1, 20))

    # --- Three headings stacked vertically, all 14pt bold, centered ---
    headings_cell = [
        Paragraph("THE UNITED REPUBLIC OF TANZANIA", style_cover_title),
        Spacer(1, 6),
        Paragraph('<u><b>TYPE YOUR SCHOOL NAME HERE</b></u>', style_cover_school),
        Spacer(1, 6),
        Paragraph('FORM FIVE&nbsp;<u><b>TERMINAL/MOCK/PRE-NECTA</b></u>',
                  style_cover_form_line),
    ]

    # --- Load and size the Coat of Arms PNG ---
    coat_img = None
    if os.path.exists(COAT_OF_ARMS_PNG):
        from PIL import Image as PILImage
        pil_img = PILImage.open(COAT_OF_ARMS_PNG)
        iw, ih = pil_img.size
        target_h = 22 * mm
        target_w = target_h * iw / ih
        from reportlab.platypus import Image as RLImage
        coat_img = RLImage(COAT_OF_ARMS_PNG, width=target_w, height=target_h)
        coat_img.hAlign = 'CENTER'

    if coat_img is not None:
        title_tbl = Table(
            [[coat_img, headings_cell, ""]],
            colWidths=[CONTENT_W * 0.20, CONTENT_W * 0.60, CONTENT_W * 0.20]
        )
        title_tbl.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('ALIGN', (2, 0), (2, 0), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(title_tbl)
    else:
        for h in headings_cell:
            story.append(h)

    story.append(Spacer(1, 16))

    # --- Subject code and time line ---
    code_time_tbl = Table(
        [[Paragraph('<b>CODE: 114/1</b>', ParagraphStyle('Code', fontName=BODY_FONT_BOLD,
                                                          fontSize=12, alignment=TA_LEFT)),
          Paragraph('<b>DIVINITY 1</b>', ParagraphStyle('Subj', fontName=BODY_FONT_BOLD,
                                                        fontSize=12, alignment=TA_CENTER)),
          Paragraph('<b>TIME: 3:00 HOURS</b>', ParagraphStyle('Time', fontName=BODY_FONT_BOLD,
                                                              fontSize=12, alignment=TA_RIGHT))]],
        colWidths=[CONTENT_W * 0.33, CONTENT_W * 0.34, CONTENT_W * 0.33]
    )
    code_time_tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEABOVE', (0, 0), (-1, 0), 1.2, BLACK),
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, BLACK),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(code_time_tbl)

    # --- Date line ---
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '<b>Date: ____________________________</b>',
        ParagraphStyle('Date', fontName=BODY_FONT_BOLD, fontSize=12,
                       alignment=TA_RIGHT, textColor=BLACK)
    ))
    story.append(Spacer(1, 14))

    # --- Instructions ---
    story.append(Paragraph("Instructions", style_instr_h))
    instructions = [
        "This paper consists of section A and section B with total of nine (9) questions.",
        "Answer all questions in section A and any two questions in section B.",
        "Cellular phones and any other sort of unauthorized materials are not allowed in the examination room.",
        "Write your examination number on every page of your answer booklet.",
    ]
    for i, ins in enumerate(instructions, 1):
        story.append(Paragraph(f"{i}. {ins}", style_instr_li))
    story.append(Spacer(1, 12))

    # --- Question table (9 questions) ---
    header = ['QUESTION<br/>NUMBER', 'QUESTION<br/>ATTEMPTED<br/>(PUT A TICK ✓)', 'SCORE', "EXAMINER'S<br/>INITIALS"]
    rows = [[Paragraph(h, ParagraphStyle('TH', fontName=BODY_FONT_BOLD, fontSize=9.5,
                                         alignment=TA_CENTER, leading=11))
             for h in header]]
    for n in range(1, 10):
        rows.append([
            Paragraph(str(n), ParagraphStyle('TD', fontName=BODY_FONT, fontSize=10,
                                             alignment=TA_CENTER, leading=12)),
            Paragraph("", style_instr_li),
            Paragraph("", style_instr_li),
            Paragraph("", style_instr_li),
        ])
    rows.append([
        Paragraph('<b>TOTAL MARKS</b>', ParagraphStyle('TD', fontName=BODY_FONT_BOLD,
                                                       fontSize=9.5, alignment=TA_CENTER, leading=11)),
        Paragraph("", style_instr_li),
        Paragraph("", style_instr_li),
        Paragraph("", style_instr_li),
    ])
    rows.append([
        Paragraph('<b>CHECKER\'S INITIALS</b>',
                  ParagraphStyle('TD', fontName=BODY_FONT_BOLD, fontSize=9.5,
                                 alignment=TA_CENTER, leading=11)),
        Paragraph("", style_instr_li),
        Paragraph("", style_instr_li),
        Paragraph("", style_instr_li),
    ])

    q_table = Table(rows, colWidths=[CONTENT_W * 0.18, CONTENT_W * 0.40,
                                      CONTENT_W * 0.20, CONTENT_W * 0.22])
    q_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.6, BLACK),
        ('BACKGROUND', (0, 0), (-1, 0), BG_GRAY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(q_table)

    return story


# ---------- Build Section A ----------
def build_section_a():
    """Section A: 6 short-answer questions (60 marks total, 10 marks each).
    Each question has a), b), c), d) subparts.
    a), b) and sometimes c) are recall/direct questions.
    d) and sometimes c) are competence-based (application to daily life/school/community).
    IMPORTANT: Subparts must NOT ask about something already stated in the lead statement.
    No answer lines — questions only."""
    story = []

    story.append(Paragraph("SECTION A (60 Marks)", style_section_h))
    story.append(Paragraph("Answer <b>all</b> questions in this section.", style_section_sub))

    # Q1 — Origin and meaning of Divinity
    story.append(Paragraph(
        "<b>1.</b> The term \"Divinity\" is derived from the Latin word <i>divinus</i>, which refers to the "
        "state or quality of being divine (holy). Divinity is concerned with God's revelation for the "
        "salvation of humankind and their well-being here on earth.",
        style_qtext
    ))
    story.append(Paragraph("(a) Differentiate between \"divine\" and \"sacred\" as used in theological studies. (02 marks)", style_subpart))
    story.append(Paragraph("(b) Explain the difference between Divinity as a concept and Divinity as an academic discipline. (03 marks)", style_subpart))
    story.append(Paragraph("(c) Give three reasons why the study of Divinity is described as being concerned with \"well-being on earth\" rather than only spiritual matters. (03 marks)", style_subpart))
    story.append(Paragraph("(d) How can the understanding of Divinity help you in your daily life at school? Give two points. (02 marks)", style_subpart))

    # Q2 — Importance of studying Divinity
    story.append(Paragraph(
        "<b>2.</b> The study of Divinity helps the learner to appreciate the presence of the divine being (God) "
        "as the Creator of the universe. It also strengthens faith and helps the learner to live an upright "
        "Christian life.",
        style_qtext
    ))
    story.append(Paragraph("(a) Define the term \"faith\" as used in the study of Divinity. (02 marks)", style_subpart))
    story.append(Paragraph("(b) Explain three ways in which a student can strengthen faith through the study of Divinity. (03 marks)", style_subpart))
    story.append(Paragraph("(c) Describe three characteristics of an \"upright Christian life\" as taught in Divinity. (03 marks)", style_subpart))
    story.append(Paragraph("(d) How can you apply the knowledge gained from studying Divinity to promote national development in your community? Give two points. (02 marks)", style_subpart))

    # Q3 — God's revelation and human welfare
    story.append(Paragraph(
        "<b>3.</b> Divinity is concerned with God's revelation for the salvation of humankind and their "
        "well-being here on earth. Biblical revelation is not only concerned with spiritual matters; "
        "it also addresses the day-to-day welfare of human beings and their environment.",
        style_qtext
    ))
    story.append(Paragraph("(a) Explain three forms through which God has revealed Himself to humanity. (03 marks)", style_subpart))
    story.append(Paragraph("(b) Differentiate between \"spiritual matters\" and \"day-to-day welfare\" as addressed in Biblical revelation. (03 marks)", style_subpart))
    story.append(Paragraph("(c) State two ways in which the environment is part of God's creation that requires human care. (04 marks)", style_subpart))
    story.append(Paragraph("(d) How can the understanding of God's revelation guide you in making moral decisions at home? Give two points. (02 marks)", style_subpart))

    # Q4 — Spiritual formation and intellectual transformation
    story.append(Paragraph(
        "<b>4.</b> In academic discipline, Divinity aims to bring vital spiritual formation and intellectual "
        "transformation, moulding responsible and mature citizens with a strong sense of justice, patriotism "
        "and obedience to timeless truth.",
        style_qtext
    ))
    story.append(Paragraph("(a) Explain the meaning of \"timeless truth\" in the context of Divinity. (02 marks)", style_subpart))
    story.append(Paragraph("(b) Describe three activities that can promote spiritual formation among students. (03 marks)", style_subpart))
    story.append(Paragraph("(c) State two ways in which intellectual transformation differs from spiritual formation. (03 marks)", style_subpart))
    story.append(Paragraph("(d) As a student, how can you apply spiritual formation and intellectual transformation in your community? Give two points. (02 marks)", style_subpart))

    # Q5 — Human dignity and national development
    story.append(Paragraph(
        "<b>5.</b> The study of Divinity develops and promotes self-confidence, respect for human dignity, "
        "human rights and readiness to work hard for self-advancement and national development. "
        "It also enables the learner to understand and uphold the fundamentals of Christianity, the National "
        "Constitution and the enshrined human civic rights, obligations and responsibilities.",
        style_qtext
    ))
    story.append(Paragraph("(a) Define the term \"self-confidence\" as used in the study of Divinity. (02 marks)", style_subpart))
    story.append(Paragraph("(b) Explain three ways in which a student can show readiness to work hard for self-advancement. (03 marks)", style_subpart))
    story.append(Paragraph("(c) Describe three obligations and responsibilities of a Christian citizen according to the National Constitution. (03 marks)", style_subpart))
    story.append(Paragraph("(d) How can you demonstrate respect for human dignity and human rights in your school? Give two points. (02 marks)", style_subpart))

    # Q6 — Divinity and other disciplines
    story.append(Paragraph(
        "<b>6.</b> Divinity is related to several other academic disciplines studied in schools. "
        "Sociology deals with the study of human society, History deals with the development of society, "
        "Geography helps learners identify biblical lands, and Political Science deals with the study of "
        "political and administrative subjects.",
        style_qtext
    ))
    story.append(Paragraph("(a) Define the term \"discipline\" as used in an academic context. (02 marks)", style_subpart))
    story.append(Paragraph("(b) Explain three benefits of studying Divinity alongside other academic disciplines. (03 marks)", style_subpart))
    story.append(Paragraph("(c) Describe two ways in which knowledge of Geography enhances the understanding of Divinity. (03 marks)", style_subpart))
    story.append(Paragraph("(d) How can the relationship between Divinity and Political Science help you become a responsible citizen? Give two points. (02 marks)", style_subpart))

    return story


# ---------- Build Section B ----------
def build_section_b():
    """Section B: 3 essay questions (40 marks total, 20 marks each).
    Each question starts with a statement, then the task, asking for four points.
    IMPORTANT: The question must NOT ask about something already stated in the lead statement.
    No answer lines — questions only."""
    story = []

    story.append(Paragraph("SECTION B (40 Marks)", style_section_h))
    story.append(Paragraph("Answer <b>any two (2)</b> questions from this section.", style_section_sub))

    # Q7
    story.append(Paragraph(
        "<b>7.</b> Divinity is related to several other academic disciplines studied in schools, "
        "including Sociology, History, Geography, and Political Science and Public Administration. "
        "Each of these disciplines shares common concerns with Divinity and contributes to a broader "
        "understanding of God's revelation and human welfare. Explain the challenges that students face "
        "when integrating Divinity with other academic disciplines and suggest how these challenges can "
        "be overcome. Give four (4) points. (20 marks)",
        style_qtext
    ))

    # Q8
    story.append(Paragraph(
        "<b>8.</b> The study of Divinity plays a significant role in the development of an individual "
        "and the nation at large. It helps learners appreciate God as the Creator, strengthens faith, "
        "promotes critical thinking, develops self-confidence, and prepares learners to become responsible "
        "citizens who uphold human dignity and work for national development. Assess the relevance of "
        "studying Divinity in addressing contemporary social problems in Tanzania today. Give four (4) "
        "points. (20 marks)",
        style_qtext
    ))

    # Q9
    story.append(Paragraph(
        "<b>9.</b> Divinity engages the fundamental principles of life as ordained by God through the Bible. "
        "It is concerned with God's revelation for the salvation of humankind and their well-being on earth. "
        "Biblical revelation addresses both spiritual matters and the day-to-day welfare of human beings "
        "and their environment, teaching stewardship of God's creation. Evaluate the role of Divinity in "
        "promoting environmental stewardship and sustainable development in modern society. Give four (4) "
        "points. (20 marks)",
        style_qtext
    ))

    return story


# ---------- Page templates ----------
def on_cover_page(canvas, doc):
    """Cover page: no header/footer."""
    pass


def make_on_content_page(total_pages=None):
    def _on_content_page(canvas, doc):
        canvas.saveState()
        # Top right: examination number
        canvas.setFont(BODY_FONT_BOLD, 10)
        canvas.setFillColor(BLACK)
        canvas.drawRightString(
            PAGE_W - MARGIN_R,
            PAGE_H - MARGIN_T + 6,
            "Examination Number: __________________________"
        )
        # Top left: subject
        canvas.setFont(BODY_FONT, 9)
        canvas.drawString(MARGIN_L, PAGE_H - MARGIN_T + 6, "114/1  DIVINITY 1")
        # Footer: page number
        page_num = canvas.getPageNumber()
        if total_pages:
            footer = f"Page {page_num} of {total_pages}"
        else:
            footer = f"Page {page_num}"
        canvas.setFont(BODY_FONT, 9)
        canvas.drawCentredString(PAGE_W / 2, MARGIN_B - 8, footer)
        canvas.restoreState()
    return _on_content_page


def build_doc():
    os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

    doc = BaseDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title="Form Five Divinity Examination",
        author="Z.ai",
        subject="Form Five Divinity Examination - Topic 1",
        creator="Z.ai PDF Skill",
    )

    cover_frame = Frame(MARGIN_L, MARGIN_B, CONTENT_W, CONTENT_H,
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    content_frame = Frame(MARGIN_L, MARGIN_B + 6, CONTENT_W, CONTENT_H - 18,
                          leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0, id='content')

    cover_template = PageTemplate(id='cover', frames=[cover_frame], onPage=on_cover_page)
    content_template = PageTemplate(id='content', frames=[content_frame],
                                    onPage=make_on_content_page())
    doc.addPageTemplates([cover_template, content_template])

    story = []
    # Cover page
    story.extend(build_cover_page())
    # Force Section A to start on page 2
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())

    # Section A
    story.extend(build_section_a())

    # Section B
    story.extend(build_section_b())

    doc.build(story)

    # Rebuild with correct total page count
    from pypdf import PdfReader
    reader = PdfReader(OUTPUT_PDF)
    total = len(reader.pages)
    _regenerate_with_total(OUTPUT_PDF, total)

    return OUTPUT_PDF, total


def _regenerate_with_total(output_path, total):
    """Rebuild the document with the actual total page count in footers."""
    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title="Form Five Divinity Examination",
        author="Z.ai",
        subject="Form Five Divinity Examination - Topic 1",
        creator="Z.ai PDF Skill",
    )
    cover_frame = Frame(MARGIN_L, MARGIN_B, CONTENT_W, CONTENT_H,
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    content_frame = Frame(MARGIN_L, MARGIN_B + 6, CONTENT_W, CONTENT_H - 18,
                          leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0, id='content')

    cover_template = PageTemplate(id='cover', frames=[cover_frame], onPage=on_cover_page)
    content_template = PageTemplate(id='content', frames=[content_frame],
                                    onPage=make_on_content_page(total))
    doc.addPageTemplates([cover_template, content_template])

    story = []
    story.extend(build_cover_page())
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())
    story.extend(build_section_a())
    story.extend(build_section_b())
    doc.build(story)


if __name__ == "__main__":
    path, pages = build_doc()
    print(f"\nExam PDF generated successfully.")
    print(f"Path:  {path}")
    print(f"Pages: {pages}")
    print(f"Size:  {os.path.getsize(path):,} bytes")
