from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "pdf" / "cs179g_backend_testing_guide.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#176B87")
TEAL = colors.HexColor("#1D8A7A")
LIGHT_BLUE = colors.HexColor("#EAF3F7")
LIGHT_TEAL = colors.HexColor("#EAF7F4")
LIGHT_GRAY = colors.HexColor("#F4F6F8")
MID_GRAY = colors.HexColor("#617184")
TEXT = colors.HexColor("#17212B")
CODE_BG = colors.HexColor("#1F2933")
CODE_TEXT = colors.HexColor("#F4F7FA")


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="GuideTitle",
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideSubtitle",
        fontName="Helvetica",
        fontSize=11.5,
        leading=17,
        textColor=MID_GRAY,
        spaceAfter=18,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="Subsection",
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=BLUE,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyGuide",
        fontName="Helvetica",
        fontSize=9.8,
        leading=14.2,
        textColor=TEXT,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="BulletGuide",
        parent=styles["BodyGuide"],
        leftIndent=14,
        firstLineIndent=-8,
        bulletIndent=2,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="StepNumber",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.white,
    )
)
styles.add(
    ParagraphStyle(
        name="StepText",
        fontName="Helvetica",
        fontSize=9.8,
        leading=14,
        textColor=TEXT,
    )
)
styles.add(
    ParagraphStyle(
        name="GuideCode",
        fontName="Courier",
        fontSize=8.2,
        leading=11.2,
        textColor=CODE_TEXT,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=MID_GRAY,
    )
)


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = letter
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor("#DCE4EA"))
        canvas.setLineWidth(0.6)
        canvas.line(0.72 * inch, height - 0.55 * inch, width - 0.72 * inch, height - 0.55 * inch)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(NAVY)
        canvas.drawString(0.72 * inch, height - 0.42 * inch, "CS179G N-Gram Website")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MID_GRAY)
        canvas.drawRightString(width - 0.72 * inch, height - 0.42 * inch, "Backend Testing Guide")

    canvas.setStrokeColor(colors.HexColor("#DCE4EA"))
    canvas.line(0.72 * inch, 0.52 * inch, width - 0.72 * inch, 0.52 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MID_GRAY)
    canvas.drawString(0.72 * inch, 0.34 * inch, "Group 3 - Local development guide")
    canvas.drawRightString(width - 0.72 * inch, 0.34 * inch, f"Page {doc.page}")
    canvas.restoreState()


def code_block(text):
    block = Table([[Preformatted(text.strip(), styles["GuideCode"])]], colWidths=[6.75 * inch])
    block.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#111820")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return block


def callout(title, text, color=LIGHT_BLUE):
    content = Paragraph(f"<b>{title}</b><br/>{text}", styles["BodyGuide"])
    box = Table([[content]], colWidths=[6.75 * inch])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), color),
                ("LINEBEFORE", (0, 0), (0, -1), 4, TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return box


def step(number, title, body):
    number_cell = Table(
        [[Paragraph(str(number), styles["StepNumber"])]],
        colWidths=[0.32 * inch],
        rowHeights=[0.32 * inch],
    )
    number_cell.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BLUE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    text = Paragraph(f"<b>{title}</b><br/>{body}", styles["StepText"])
    row = Table([[number_cell, text]], colWidths=[0.48 * inch, 6.27 * inch])
    row.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return row


story = []

# Cover and quick-start page
story.append(Spacer(1, 0.35 * inch))
story.append(Paragraph("CS179G Backend Testing Guide", styles["GuideTitle"]))
story.append(
    Paragraph(
        "A beginner-friendly walkthrough for testing the MySQL-to-Express integration "
        "and connecting the React frontend to the N-gram chart data.",
        styles["GuideSubtitle"],
    )
)

summary = Table(
    [
        [Paragraph("FRONTEND", styles["Small"]), Paragraph("BACKEND", styles["Small"]), Paragraph("DATABASE", styles["Small"])],
        [Paragraph("React<br/><b>localhost:3000</b>", styles["BodyGuide"]), Paragraph("Express API<br/><b>localhost:5000</b>", styles["BodyGuide"]), Paragraph("MySQL<br/><b>ngram_db</b>", styles["BodyGuide"])],
    ],
    colWidths=[2.25 * inch] * 3,
)
summary.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, 1), LIGHT_GRAY),
            ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#CBD5DE")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5DE")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
story.append(summary)
story.append(Spacer(1, 0.16 * inch))
story.append(callout("Current status", "The API connection has been verified. If an endpoint returns an empty <font name='Courier'>data</font> array, the integration is working but the related Part 2 table does not contain processed rows yet.", LIGHT_TEAL))
story.append(Paragraph("Quick test", styles["Section"]))
story.append(step(1, "Start MySQL", "Use MySQL Workbench or the Windows Services application and confirm the MySQL server is running."))
story.append(step(2, "Start the backend", "Open PowerShell in the project&apos;s <font name='Courier'>backend</font> folder and run the commands below. Keep the terminal open."))
story.append(code_block("npm install\nnpm start"))
story.append(Spacer(1, 0.1 * inch))
story.append(step(3, "Open the health endpoint", "Visit <font name='Courier'>http://localhost:5000/api/health</font> in a browser."))
story.append(code_block('{ "database": "connected" }'))
story.append(step(4, "Test chart data", "Open the trend and decade endpoints shown on the next page. A non-error JSON response confirms that React can call the API."))

# Database and endpoint testing
story.append(PageBreak())
story.append(Paragraph("1. Confirm the MySQL tables", styles["Section"]))
story.append(Paragraph("Open PowerShell and connect to MySQL. The password is typed at the prompt and should never be placed in frontend code.", styles["BodyGuide"]))
story.append(code_block("mysql -u root -p"))
story.append(Spacer(1, 0.08 * inch))
story.append(Paragraph("Run these SQL statements:", styles["BodyGuide"]))
story.append(code_block("USE ngram_db;\nSHOW TABLES;\nSELECT COUNT(*) FROM word_year_stats;\nSELECT COUNT(*) FROM decade_top_words;\nexit;"))
story.append(Paragraph("2. Test every API route", styles["Section"]))

route_data = [
    ["Purpose", "Address", "Chart use"],
    ["Database health", "/api/health", "Connection status"],
    ["Keyword trend", "/api/trends?keyword=database", "Line chart"],
    ["Filtered trend", "/api/trends?keyword=database&startYear=1900&endYear=2009", "Line chart"],
    ["Available decades", "/api/decades", "Dropdown"],
    ["Top words", "/api/top-words?decade=1990&limit=10", "Bar chart"],
]
routes = Table(route_data, colWidths=[1.28 * inch, 4.12 * inch, 1.35 * inch], repeatRows=1)
routes.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.4),
            ("TEXTCOLOR", (1, 1), (1, -1), BLUE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
            ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#CCD6DF")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
story.append(routes)
story.append(Paragraph("Expected trend response", styles["Subsection"]))
story.append(code_block('''{
  "keyword": "database",
  "data": [
    { "year": 1980, "match_count": 55 },
    { "year": 1981, "match_count": 8255 }
  ]
}'''))
story.append(Paragraph("Expected top-words response", styles["Subsection"]))
story.append(code_block('''{
  "decade": 1990,
  "data": [
    { "word": "the", "total_matches": 500000, "rank": 1 }
  ]
}'''))

# Optional sample data
story.append(PageBreak())
story.append(Paragraph("3. Optional end-to-end test data", styles["Section"]))
story.append(Paragraph("Use this only when the Part 2 tables are empty. These records use a distinctive test word and a decade outside the Google Books dataset, making them easy to remove afterward.", styles["BodyGuide"]))
story.append(callout("Before inserting", "Connect to MySQL, select <font name='Courier'>ngram_db</font>, and make sure you are working in the intended local database."))
story.append(Paragraph("Insert temporary rows", styles["Subsection"]))
story.append(code_block("""INSERT INTO word_year_stats
    (word, year, match_count, page_count, volume_count)
VALUES
    ('backendtestword', 2000, 10, 5, 2),
    ('backendtestword', 2001, 25, 12, 4),
    ('backendtestword', 2002, 40, 20, 8);

INSERT INTO decade_top_words
    (decade, word, total_matches, word_rank)
VALUES
    (2090, 'backendtestword', 1000, 1),
    (2090, 'sampleword', 800, 2);"""))
story.append(Paragraph("Test the inserted rows", styles["Subsection"]))
story.append(code_block("http://localhost:5000/api/trends?keyword=backendtestword\nhttp://localhost:5000/api/top-words?decade=2090"))
story.append(Paragraph("Remove the temporary rows", styles["Subsection"]))
story.append(code_block("""DELETE FROM word_year_stats
WHERE word = 'backendtestword';

DELETE FROM decade_top_words
WHERE decade = 2090;"""))
story.append(Spacer(1, 0.12 * inch))
story.append(callout("Real data dependencies", "The trend route reads <font name='Courier'>word_year_stats</font>, which is produced by <font name='Courier'>src/process_ngrams.py</font>. The decade route reads <font name='Courier'>decade_top_words</font>, which is produced by <font name='Courier'>src/process_decade_top.py</font> or <font name='Courier'>src/process_ngrams.py</font>.", LIGHT_TEAL))

# Frontend handoff
story.append(PageBreak())
story.append(Paragraph("4. Frontend handoff", styles["Section"]))
story.append(Paragraph("The frontend must call Express. It must never connect directly to MySQL or contain a database password.", styles["BodyGuide"]))
story.append(Paragraph("Run both applications", styles["Subsection"]))

terminals = Table(
    [
        ["Terminal 1 - backend", "Terminal 2 - frontend"],
        [Preformatted("cd backend\nnpm start", styles["GuideCode"]), Preformatted("cd frontend\nnpm start", styles["GuideCode"])],
        [Paragraph("http://localhost:5000", styles["Small"]), Paragraph("http://localhost:3000", styles["Small"])],
    ],
    colWidths=[3.375 * inch, 3.375 * inch],
)
terminals.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, 1), CODE_BG),
            ("BACKGROUND", (0, 2), (-1, 2), LIGHT_GRAY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5DE")),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
story.append(terminals)
story.append(Paragraph("React keyword request", styles["Subsection"]))
story.append(code_block("""async function getWordTrend(keyword) {
  const url = 'http://localhost:5000/api/trends?keyword=' +
    encodeURIComponent(keyword);
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error('Could not load the word trend');
  }

  const result = await response.json();
  return result.data;
}"""))
story.append(Paragraph("Line-chart mapping", styles["Subsection"]))
story.append(code_block("const labels = data.map(item => item.year);\nconst values = data.map(item => item.match_count);"))
story.append(Paragraph("Popular-words request", styles["Subsection"]))
story.append(code_block("""async function getTopWords(decade) {
  const response = await fetch(
    `http://localhost:5000/api/top-words?decade=${decade}&limit=10`
  );
  if (!response.ok) throw new Error('Could not load popular words');
  const result = await response.json();
  return result.data;
}"""))
story.append(Paragraph("Bar-chart mapping", styles["Subsection"]))
story.append(code_block("const labels = data.map(item => item.word);\nconst values = data.map(item => item.total_matches);"))

# Troubleshooting and rules
story.append(PageBreak())
story.append(Paragraph("5. Frontend rules and troubleshooting", styles["Section"]))
story.append(Paragraph("Frontend rules", styles["Subsection"]))
for text in [
    "Use <font name='Courier'>encodeURIComponent(keyword)</font> before adding user text to a URL.",
    "Check <font name='Courier'>response.ok</font> before reading chart data.",
    "Treat an empty <font name='Courier'>data</font> array as a valid result and show a clear 'No data found' message.",
    "For a line chart, use <font name='Courier'>year</font> as labels and <font name='Courier'>match_count</font> as values.",
    "For a bar chart, use <font name='Courier'>word</font> as labels and <font name='Courier'>total_matches</font> as values.",
    "Never copy <font name='Courier'>backend/.env</font> into React or commit it to Git.",
]:
    story.append(Paragraph(f"- {text}", styles["BulletGuide"]))

story.append(Paragraph("Common problems", styles["Subsection"]))
problems = [
    ["Problem", "What to check"],
    ["Database says disconnected", "Start MySQL and check the values in backend/.env."],
    ["The browser cannot reach port 5000", "Keep npm start running in the backend terminal."],
    ["The API returns data: []", "The query worked, but the Part 2 table has no matching rows."],
    ["React reports a CORS error", "Use React on port 3000 or update FRONTEND_URL in backend/.env."],
    ["A teammate cannot use localhost", "localhost refers to that teammate's computer, not yours."],
]
problem_table = Table(problems, colWidths=[2.05 * inch, 4.70 * inch], repeatRows=1)
problem_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.7),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
            ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#CBD5DE")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
story.append(problem_table)
story.append(Spacer(1, 0.15 * inch))
story.append(callout("Working on separate computers", "The current project uses local databases. Each teammate must run MySQL and the backend locally, or the group must later deploy one shared backend. A React app on another computer cannot reach your <font name='Courier'>localhost</font> address.", LIGHT_TEAL))
story.append(Spacer(1, 0.14 * inch))
story.append(Paragraph("Final verification checklist", styles["Subsection"]))
for text in [
    "MySQL is running.",
    "The backend health route says connected.",
    "The required Part 2 tables contain rows.",
    "Trend and top-word endpoints return JSON.",
    "React uses port 3000 and the backend uses port 5000.",
    "No database password appears in frontend code or Git.",
]:
    story.append(Paragraph(f"[ ] {text}", styles["BulletGuide"]))


doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=letter,
    rightMargin=0.75 * inch,
    leftMargin=0.75 * inch,
    topMargin=0.72 * inch,
    bottomMargin=0.68 * inch,
    title="CS179G Backend Testing Guide",
    author="CS179G Group 3",
    subject="Testing the MySQL, Express, and React integration",
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
