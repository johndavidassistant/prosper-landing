from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib import colors

# ── Palette ──────────────────────────────────────────────────
NAVY   = HexColor('#0F1B2D')
GOLD   = HexColor('#C8952E')
CREAM  = HexColor('#F6F1E9')
MUTED  = HexColor('#5B6E8A')
BODY_C = HexColor('#1A2942')
WHITE  = HexColor('#FFFFFF')

# ── Styles ───────────────────────────────────────────────────
def make_styles():
    s = {}
    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=30, textColor=GOLD,
        alignment=TA_CENTER, leading=36, spaceAfter=10)
    s['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='Helvetica', fontSize=15, textColor=CREAM,
        alignment=TA_CENTER, leading=20, spaceAfter=6)
    s['cover_sub2'] = ParagraphStyle('cover_sub2',
        fontName='Helvetica-Oblique', fontSize=12, textColor=CREAM,
        alignment=TA_CENTER, leading=16, spaceAfter=4)
    s['cover_url'] = ParagraphStyle('cover_url',
        fontName='Helvetica', fontSize=10, textColor=MUTED,
        alignment=TA_CENTER, leading=14)
    s['page_title'] = ParagraphStyle('page_title',
        fontName='Helvetica-Bold', fontSize=20, textColor=NAVY,
        leading=24, spaceAfter=4, spaceBefore=12)
    s['step_num'] = ParagraphStyle('step_num',
        fontName='Helvetica-Bold', fontSize=48, textColor=GOLD,
        leading=52, spaceAfter=0, spaceBefore=20)
    s['step_title'] = ParagraphStyle('step_title',
        fontName='Helvetica-Bold', fontSize=20, textColor=NAVY,
        leading=24, spaceAfter=4, spaceBefore=4)
    s['step_sub'] = ParagraphStyle('step_sub',
        fontName='Helvetica-Oblique', fontSize=12, textColor=MUTED,
        leading=16, spaceAfter=8, spaceBefore=0)
    s['section_head'] = ParagraphStyle('section_head',
        fontName='Helvetica-Bold', fontSize=13, textColor=NAVY,
        leading=16, spaceAfter=4, spaceBefore=12)
    s['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=11.5, textColor=BODY_C,
        leading=18, spaceAfter=6, spaceBefore=3)
    s['body_bold'] = ParagraphStyle('body_bold',
        fontName='Helvetica-Bold', fontSize=11.5, textColor=NAVY,
        leading=18, spaceAfter=6, spaceBefore=3)
    s['body_strong'] = ParagraphStyle('body_strong',
        fontName='Helvetica-Bold', fontSize=13, textColor=NAVY,
        leading=18, spaceAfter=8, spaceBefore=4)
    s['body_italic'] = ParagraphStyle('body_italic',
        fontName='Helvetica-Oblique', fontSize=11, textColor=MUTED,
        leading=16, spaceAfter=4, spaceBefore=2)
    s['bullet'] = ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=11, textColor=BODY_C,
        leading=17, spaceAfter=3, spaceBefore=2,
        leftIndent=20, firstLineIndent=0)
    s['callout'] = ParagraphStyle('callout',
        fontName='Helvetica-Bold', fontSize=11.5, textColor=NAVY,
        leading=17, spaceAfter=6, spaceBefore=6,
        leftIndent=16, rightIndent=8,
        backColor=CREAM, borderPad=8)
    s['pull_quote'] = ParagraphStyle('pull_quote',
        fontName='Helvetica-Oblique', fontSize=12, textColor=CREAM,
        leading=18, spaceAfter=8, spaceBefore=8,
        leftIndent=20, rightIndent=20,
        backColor=NAVY, borderPad=12)
    s['action_label'] = ParagraphStyle('action_label',
        fontName='Helvetica-Bold', fontSize=9, textColor=GOLD,
        leading=12, spaceAfter=2, spaceBefore=10,
        leftIndent=12, backColor=CREAM)
    s['action_item'] = ParagraphStyle('action_item',
        fontName='Helvetica', fontSize=11, textColor=BODY_C,
        leading=17, spaceAfter=2, spaceBefore=2,
        leftIndent=28, backColor=CREAM)
    s['compliance'] = ParagraphStyle('compliance',
        fontName='Helvetica-Oblique', fontSize=9, textColor=MUTED,
        leading=13, spaceAfter=4, spaceBefore=12)
    s['transition'] = ParagraphStyle('transition',
        fontName='Helvetica-Oblique', fontSize=10.5, textColor=MUTED,
        leading=15, spaceAfter=6, spaceBefore=10)
    s['welcome_body'] = ParagraphStyle('welcome_body',
        fontName='Helvetica', fontSize=12, textColor=BODY_C,
        leading=20, spaceAfter=6, spaceBefore=4)
    s['sig_name'] = ParagraphStyle('sig_name',
        fontName='Helvetica-Bold', fontSize=12, textColor=NAVY,
        leading=16, spaceAfter=2, spaceBefore=16)
    s['sig_brand'] = ParagraphStyle('sig_brand',
        fontName='Helvetica', fontSize=11, textColor=GOLD,
        leading=15, spaceAfter=6)
    s['step_index'] = ParagraphStyle('step_index',
        fontName='Helvetica', fontSize=12, textColor=NAVY,
        leading=18, spaceAfter=2, spaceBefore=2,
        leftIndent=12, backColor=CREAM)
    return s

# ── Flowables ────────────────────────────────────────────────
def gold_rule():
    return HRFlowable(width='100%', thickness=1, color=GOLD,
                      spaceAfter=6, spaceBefore=2)

def sp(h=8):
    return Spacer(1, h)

def body_p(text, style):
    return Paragraph(text, style)

def action_box(items, styles, subtext=None):
    elems = []
    elems.append(Paragraph('YOUR ACTION FOR THIS STEP', styles['action_label']))
    if subtext:
        p = ParagraphStyle('action_sub', parent=styles['action_item'],
                           fontName='Helvetica', fontSize=11, textColor=BODY_C)
        elems.append(Paragraph(subtext, p))
    for item in items:
        elems.append(Paragraph(f'☐  {item}', styles['action_item']))
    return elems

def callout_p(text, styles):
    return Paragraph(text, styles['callout'])

def pull_quote_p(text, styles):
    return Paragraph(f'"{text}"', styles['pull_quote'])

# ── Cover page background ─────────────────────────────────────
class NavyBackground(Flowable):
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height
    def draw(self):
        self.canv.setFillColor(NAVY)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)

# ── Document builder ─────────────────────────────────────────
def build():
    out = '/Users/miriampalma/AI-OS/projects/prosper-landing/public/assets/prosper_in_america_guide.pdf'
    doc = SimpleDocTemplate(out, pagesize=letter,
                            leftMargin=1.1*inch, rightMargin=1.1*inch,
                            topMargin=1.0*inch, bottomMargin=0.9*inch)
    W, H = letter
    S = make_styles()
    story = []

    # ── PAGE 1: COVER ────────────────────────────────────────
    def cover_background(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        canvas.restoreState()

    story.append(Spacer(1, 2.2*inch))
    story.append(Paragraph('PROSPER IN AMERICA', S['cover_title']))
    story.append(Paragraph('The Immigrant Financial Starter Guide', S['cover_sub']))
    story.append(Paragraph('7 Steps to Building Your Life in America', S['cover_sub2']))
    story.append(Spacer(1, 3.0*inch))
    story.append(Paragraph('prosperinamerica.com', S['cover_url']))
    story.append(PageBreak())

    # ── PAGE 2: WELCOME ──────────────────────────────────────
    story.append(Paragraph('A Note Before You Start', S['page_title']))
    story.append(gold_rule())
    story.append(sp(10))
    for line in [
        "You didn't come here to stay in the same place.",
        "Neither did I.",
        "When I arrived in America, no one handed me a roadmap. I figured things out slowly — sometimes the hard way — and I spent years learning things that should have taken weeks.",
        "This guide is what I wish someone had given me in my first year.",
        "It won't answer every question. But it will give you the right starting point — and help you stop making the decisions that cost people the most time and money.",
        "Read it. Use it. And if you want to apply it to your specific situation, I'm available for a free conversation. No pressure. No agenda.",
    ]:
        story.append(Paragraph(line, S['welcome_body']))
        story.append(sp(4))
    story.append(sp(10))
    story.append(Paragraph('— John David', S['sig_name']))
    story.append(Paragraph('Prosper In America', S['sig_brand']))
    story.append(PageBreak())

    # ── PAGE 3: HOW TO USE ───────────────────────────────────
    story.append(Paragraph('How to Use This Guide', S['page_title']))
    story.append(gold_rule())
    story.append(sp(8))
    story.append(Paragraph("This guide has 7 steps. They follow a sequence — but you don't have to start at the beginning.", S['body']))
    story.append(sp(4))
    story.append(Paragraph("If you already have a bank account, skip to Step 3. If credit is your biggest gap, start at Step 4. If you're worried about your family's protection, go straight to Step 5.", S['body']))
    story.append(sp(4))
    story.append(Paragraph('Find where you are. Start there.', S['body_bold']))
    story.append(sp(14))
    story.append(Paragraph('Steps in this guide', S['section_head']))
    for num, title in [
        ('01', 'Why Most Immigrants Stay Stuck'),
        ('02', 'Get Your Numbers Right'),
        ('03', 'Open the Right Account'),
        ('04', 'Build Your Credit'),
        ('05', "Protect What You're Building"),
        ('06', 'Increase Your Income'),
        ('07', 'Build Something That Lasts'),
    ]:
        story.append(Paragraph(f'<font color="#C8952E"><b>{num}</b></font>  {title}', S['step_index']))
    story.append(PageBreak())

    # ── STEP 1 ───────────────────────────────────────────────
    story.append(Paragraph('01', S['step_num']))
    story.append(Paragraph('Why Most Immigrants Stay Stuck', S['step_title']))
    story.append(Paragraph("It's not a lack of effort. It's a lack of structure.", S['step_sub']))
    story.append(gold_rule())
    story.append(sp(8))
    story.append(Paragraph("You work hard. That's not the problem.", S['body']))
    story.append(Paragraph("You didn't come here to stay in the same place.", S['body']))
    story.append(Paragraph("And still — years pass without real progress.", S['body']))
    story.append(Paragraph("The money comes in. The money goes out. Nothing builds.", S['body']))
    story.append(sp(10))
    story.append(Paragraph('No one gave you the map.', S['section_head']))
    story.append(Paragraph("The US financial system does not explain itself. It assumes you already know how credit works, which banks to use, what forms to file, what you qualify for, and in what order to do things.", S['body']))
    story.append(sp(4))
    story.append(Paragraph("If you arrived without that knowledge — or without someone who had it — you've been navigating blind.", S['body']))
    story.append(sp(8))
    story.append(Paragraph("You've been making decisions based on incomplete information.", S['section_head']))
    for line in ["What someone at church mentioned.", "What you found in a WhatsApp group.",
                 "What you assumed was the same as Brazil.", "What you were afraid to ask about."]:
        story.append(Paragraph(f'&nbsp;&nbsp;&nbsp;{line}', S['bullet']))
    story.append(sp(4))
    story.append(Paragraph("Some of those decisions have consequences you haven't fully felt yet.", S['body']))
    story.append(sp(10))
    story.append(Paragraph('Small mistakes compound.', S['section_head']))
    for line in ["The credit you didn't build in year one is costing you more in year three.",
                 "The account you opened because it was easy might be the wrong account.",
                 "The filing you skipped — that's a gap in your record."]:
        story.append(Paragraph(f'&nbsp;&nbsp;&nbsp;{line}', S['bullet']))
    story.append(sp(4))
    story.append(Paragraph("None of this is your fault. It's the result of operating without a system in a system that expects you to already have one.", S['body']))
    story.append(sp(12))
    story.append(Paragraph('What changes when you have the right information', S['section_head']))
    for line in ["You stop making decisions from fear or guesswork.",
                 "You know which step comes first — and why.",
                 "You stop wasting time on the wrong things.", "The path gets clear."]:
        story.append(Paragraph(line, S['body']))
    story.append(sp(10))
    story.append(pull_quote_p("The gap is almost never effort. It's almost always information — and knowing in what order to act on it.", S))
    story.append(sp(12))
    story.extend(action_box([
        'Banking and accounts', 'Credit history', 'Taxes and filing',
        'Protecting my family', 'Building income'
    ], S, subtext='Identify the one area where you feel most behind:'))
    story.append(sp(8))
    story.append(Paragraph('Once you understand where you stand, the next step is knowing what you actually have access to.', S['transition']))
    story.append(PageBreak())

    # ── STEP 2 ───────────────────────────────────────────────
    story.append(Paragraph('02', S['step_num']))
    story.append(Paragraph('Get Your Numbers Right', S['step_title']))
    story.append(Paragraph('ITIN vs. SSN — what each one is and what each one opens.', S['step_sub']))
    story.append(gold_rule())
    story.append(sp(8))
    story.append(Paragraph("You arrive knowing you need something to start — but not knowing exactly what it is or what it opens.", S['body']))
    story.append(sp(12))
    story.append(Paragraph('SSN — Social Security Number', S['section_head']))
    story.append(Paragraph("Issued by the Social Security Administration to people authorized to work in the US.", S['body']))
    story.append(Paragraph("If you have work authorization — through a visa, green card, or other status — you may be eligible to apply for one.", S['body']))
    story.append(Paragraph("If you don't have work authorization, you won't qualify for an SSN. That's where the ITIN comes in.", S['body']))
    story.append(sp(8))
    story.append(Paragraph('ITIN — Individual Taxpayer Identification Number', S['section_head']))
    story.append(Paragraph("Issued by the IRS. A tax processing number — not proof of immigration status, not work authorization, and not a path to benefits on its own.", S['body']))
    story.append(Paragraph("It exists for people who have a US tax filing requirement but are not eligible for an SSN.", S['body']))
    story.append(sp(6))
    story.append(Paragraph('What the ITIN is commonly used for:', S['section_head']))
    for item in ['Opening certain bank accounts', 'Filing a US tax return',
                 'Building a credit history at some institutions', 'Applying for certain financial products']:
        story.append(Paragraph(f'•  {item}', S['bullet']))
    story.append(sp(8))
    story.append(Paragraph('How the application generally works:', S['section_head']))
    story.append(Paragraph("You complete IRS Form W-7 and submit it with your federal tax return and identity documents. Certifying Acceptance Agents (CAAs) can assist — many accounting firms and nonprofits offer this service. Processing times vary. Check the IRS website for current estimates.", S['body']))
    story.append(sp(10))
    story.append(Paragraph('What this means for you', S['section_head']))
    for line in ["If you have an SSN — you're already ahead. Make sure you know what it does and doesn't give you access to.",
                 "If you have an ITIN — you have a real starting point. Many banks, lenders, and services accept it.",
                 "If you have neither — find out whether the ITIN applies to your situation. It's the starting point for many people without work authorization."]:
        story.append(Paragraph(line, S['body']))
        story.append(sp(3))
    story.append(sp(4))
    story.append(callout_p("Don't wait for the SSN to start building. For many people in this situation, the ITIN is what opens the first real doors.", S))
    story.append(sp(10))
    story.extend(action_box([
        'Confirm whether you currently have an SSN or ITIN',
        'If neither, look into the ITIN process — an accountant or CAA can walk you through it',
        'Write down what you need the number for (banking, credit, filing)',
    ], S))
    story.append(sp(8))
    story.append(Paragraph('Note: ITIN eligibility, SSN eligibility, and application requirements depend on individual immigration status and circumstances. General information only — consult a qualified tax professional or immigration specialist.', S['compliance']))
    story.append(Paragraph('Once your number is in place, the next thing that matters is where your money actually lives.', S['transition']))
    story.append(PageBreak())

    # ── STEP 3 ───────────────────────────────────────────────
    story.append(Paragraph('03', S['step_num']))
    story.append(Paragraph('Open the Right Account', S['step_title']))
    story.append(gold_rule())
    story.append(sp(10))
    story.append(Paragraph("If your account is wrong, everything that comes after gets harder.", S['body_strong']))
    story.append(Paragraph("You can't build US credit without one.", S['body']))
    story.append(Paragraph("You can't pay rent, utilities, or insurance reliably without one.", S['body']))
    story.append(Paragraph("And if you opened the wrong one — or skipped this step entirely — it's costing you more than you probably realize.", S['body']))
    story.append(sp(10))
    story.append(Paragraph('Why the wrong account slows everything down', S['section_head']))
    story.append(Paragraph("Not all bank accounts are equal. Some are designed for people who are already established. They come with monthly fees, minimum balance requirements, and penalties that quietly drain what you're trying to build.", S['body']))
    story.append(sp(4))
    story.append(Paragraph("For an immigrant starting from zero, an account with a $15 monthly fee and a $500 minimum balance isn't just inconvenient.", S['body']))
    story.append(sp(2))
    story.append(callout_p("That's not a fee. That's a leak.", S))
    story.append(sp(6))
    story.append(Paragraph('What to look for', S['section_head']))
    for label, text in [
        ('Accepts your documents:', 'Many banks accept an ITIN, passport, and proof of US address — no SSN required. Verify directly before applying.'),
        ('No monthly maintenance fees:', "Some accounts charge you just for existing. Look for no monthly fee, or one that's easily waived."),
        ('No minimum balance requirement:', "If you're building from zero, you shouldn't be penalized for a low balance."),
        ('Online and mobile access:', "Baseline. If an account doesn't offer it, keep looking."),
        ('A path to a credit product:', 'Some banks offer credit-builder products to existing customers. This matters more than most people realize.'),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(8))
    story.append(Paragraph('What to avoid', S['section_head']))
    for label, text in [
        ("Prepaid debit cards:", "Don't report to credit bureaus. Don't build a banking history. A workaround, not a foundation."),
        ("Accounts with stacked fees:", 'Monthly maintenance + overdraft + ATM fees. Read the fee schedule before opening anything.'),
        ("Waiting until you have an SSN:", "In many cases, an ITIN and passport are enough. Waiting costs time you don't need to lose."),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(8))
    story.append(Paragraph('What documents are typically requested', S['section_head']))
    for item in ['Passport (valid, unexpired)', 'ITIN or SSN (where required)',
                 'Proof of US address — lease, utility bill, or official letter']:
        story.append(Paragraph(f'•  {item}', S['bullet']))
    story.append(sp(10))
    story.append(pull_quote_p("The right account doesn't impress anyone. It just works — without taking money from you while it does.", S))
    story.append(sp(8))
    story.append(Paragraph('If this step is wrong, everything that follows gets slower, more expensive, and harder to fix later.', S['body_bold']))
    story.extend(action_box([
        'Research 2–3 account options that accept your current documents',
        'Compare fee structures — look for the fee schedule, not just advertised features',
        'Confirm requirements directly with the institution before applying',
        'Open an account that charges you nothing to exist',
    ], S))
    story.append(sp(8))
    story.append(Paragraph('Note: Account eligibility and document requirements vary by institution and state. Verify requirements directly with any bank or credit union before applying.', S['compliance']))
    story.append(Paragraph('Once your account is set up correctly, the system starts looking at your credit history.', S['transition']))
    story.append(PageBreak())

    # ── STEP 4 ───────────────────────────────────────────────
    story.append(Paragraph('04', S['step_num']))
    story.append(Paragraph('Build Your Credit', S['step_title']))
    story.append(gold_rule())
    story.append(sp(8))
    story.append(Paragraph("Your entire financial history in Brazil counts for nothing here. You start at zero.", S['body_strong']))
    story.append(Paragraph("Many immigrants arrive with no US credit history. Not bad credit. No credit. In the eyes of the financial system, you don't exist yet.", S['body']))
    story.append(sp(4))
    story.append(Paragraph("This is why people stay stuck longer than they expect.", S['body']))
    story.append(sp(4))
    story.append(Paragraph("You can't rush credit history. What you can do is avoid the mistakes that force you to start over — and take the right steps early enough that time works for you.", S['body']))
    story.append(sp(12))
    story.append(Paragraph('What actually matters — the three factors', S['section_head']))
    for label, text in [
        ('Payment history:', 'The single most important factor. Pay on time, every time. One missed payment can stay on your report for years.'),
        ('Credit utilization:', "How much of your available limit you're using. High utilization signals financial pressure. Keep balances low."),
        ('Length of history:', 'Older accounts help. Closing your first account to upgrade is often a mistake.'),
    ]:
        story.append(Paragraph(f'<b><font color="#C8952E">{label}</font></b>  {text}', S['bullet']))
    story.append(sp(4))
    story.append(Paragraph('Everything else — new inquiries, credit mix — matters less. Focus on these three first.', S['body_italic']))
    story.append(sp(10))
    story.append(Paragraph('How immigrants typically start building credit', S['section_head']))
    for label, text in [
        ('Secured credit cards:', "A deposit becomes your credit limit. Use it, pay on time. The payment behavior builds the history — not the deposit."),
        ('Becoming an authorized user:', "Someone you trust adds you to their card. Their history can appear on your report — one of the faster ways to establish a starting score."),
        ('Credit-builder loans:', "Offered by some banks and credit unions. Fixed monthly payments reported to bureaus. Research availability where you bank."),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(10))
    story.append(Paragraph('What to avoid', S['section_head']))
    for label, text in [
        ('Missing a payment — even once:', 'Set up automatic minimum payments as a safety net. One late payment stays on record for up to seven years.'),
        ('Maxing out a card:', 'High utilization damages your score even if you pay it off. Keep balances well below your limit.'),
        ('Applying for multiple products at once:', 'Each application creates an inquiry. Research first, apply once.'),
        ("Assuming your Brazilian credit history transfers:", "It doesn't. The US system has no access to it. That's not a penalty — it's how the system works."),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(4))
    story.append(callout_p("Those who figure it out late often look back on years they can't recover.", S))
    story.append(sp(10))
    story.append(pull_quote_p("You can't rush credit history. What you can do is avoid the mistakes that force you to start over.", S))
    story.append(sp(10))
    story.extend(action_box([
        'Check existing US credit history at annualcreditreport.com (free)',
        'Research one secured card or credit-builder product that fits your situation',
        'Set up automatic payments on all existing accounts',
        'Identify someone who might add you as an authorized user — and have that conversation',
    ], S))
    story.append(sp(8))
    story.append(Paragraph('Note: Credit scoring and lending decisions depend on many individual factors. General educational information only — not financial advice. Consult a qualified financial professional.', S['compliance']))
    story.append(Paragraph('As your financial record starts to build, the next question becomes: what happens if everything stops?', S['transition']))
    story.append(PageBreak())

    # ── STEP 5 ───────────────────────────────────────────────
    story.append(Paragraph('05', S['step_num']))
    story.append(Paragraph("Protect What You're Building", S['step_title']))
    story.append(Paragraph('Many immigrants spend years building — and nothing protecting it.', S['body_strong']))
    story.append(gold_rule())
    story.append(sp(8))
    story.append(Paragraph("This is the step people most often skip.", S['body']))
    story.append(sp(4))
    story.append(Paragraph("Not because they don't care about their family. Because they're focused on surviving right now, and protection feels like something you deal with later.", S['body']))
    story.append(sp(4))
    story.append(Paragraph("That logic is common. It's also how families end up in crisis.", S['body']))
    story.append(sp(10))
    story.append(Paragraph('What the risk actually looks like', S['section_head']))
    scenario_style = ParagraphStyle('scenario', fontName='Helvetica', fontSize=11.5,
                                    textColor=BODY_C, leading=18, spaceAfter=6, spaceBefore=4,
                                    leftIndent=12, rightIndent=12, backColor=CREAM, borderPad=12)
    story.append(Paragraph("You're the one holding the household together. You work. You send money home. You pay rent. You're the structure.<br/><br/>Now picture that stopping tomorrow.<br/><br/>If you couldn't work for six months — what happens? If you died this year — what happens to your spouse, your children, your family back in Brazil?", scenario_style))
    story.append(sp(6))
    story.append(Paragraph("Many families in this situation have no answer to that question. Not because they haven't thought about it — because they haven't put anything in place.", S['body']))
    story.append(sp(4))
    story.append(Paragraph("That gap is what protection is for. This is where years of work are either protected — or exposed.", S['body_bold']))
    story.append(sp(8))
    story.append(Paragraph('What protection actually means', S['section_head']))
    for label, text in [
        ('Life insurance:', "A policy pays a designated amount to your family if you die. It's a simple structure: monthly premium, and if the worst happens, your family has coverage for final expenses, lost income, and time to stabilize."),
        ('Health coverage:', "Medical debt is one of the leading causes of financial collapse for working families. Options to research: Medicaid, CHIP, ACA marketplace plans. Eligibility varies by immigration status, income, and state."),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(10))
    story.append(Paragraph('Life insurance and immigration status', S['section_head']))
    story.append(Paragraph("Many families in this situation assume they need an SSN to qualify. That assumption costs them years of coverage they could have had.", S['body']))
    story.append(sp(4))
    story.append(Paragraph("Some life insurance policies accept applicants with an ITIN. The underwriting process varies by policy and provider. But the option exists.", S['body']))
    story.append(sp(4))
    story.append(callout_p("If you've been waiting until you have your SSN, find out what you may be eligible for now.", S))
    story.append(sp(10))
    story.append(Paragraph('What to avoid', S['section_head']))
    for label, text in [
        ('Waiting until you feel stable:', 'There is no stable. Stability is built, not arrived at. People who wait for the right time often wait too long.'),
        ("Assuming you don't qualify:", 'Many people never check. The assumption is wrong more often than they expect.'),
        ('Choosing coverage based only on price:', 'The cheapest option and the right option are not always the same.'),
        ('Leaving this conversation until something forces it:', "The time to think about protecting your family is not during a crisis. It's before one."),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(10))
    story.append(pull_quote_p("Protection is not what you build after you're stable. It's part of what makes stability possible.", S))
    story.append(sp(8))
    story.append(Paragraph("This step is almost always delayed until something forces the decision. By then, the options are fewer.", S['body_bold']))
    story.extend(action_box([
        "Ask honestly: if I couldn't work for 6 months, what would happen to my family?",
        'Research health coverage — start with healthcare.gov or a local navigator',
        'Look into whether your documents allow you to apply for life insurance',
        "Speak with a licensed professional — not to buy anything, but to understand what's available",
    ], S))
    story.append(sp(8))
    story.append(Paragraph('Note: Insurance eligibility, coverage terms, and health program eligibility vary by circumstances, immigration status, and state. General informational content only — not insurance advice. Consult a licensed insurance or healthcare professional.', S['compliance']))

    # ── Build with cover background ──────────────────────────
    def on_first_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        canvas.restoreState()

    def on_later_pages(canvas, doc):
        pass

    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f'PDF saved: {out}')

build()
