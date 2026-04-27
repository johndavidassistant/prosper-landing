import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, Image
)

NAVY  = HexColor('#0F1B2D')
GOLD  = HexColor('#C8952E')
CREAM = HexColor('#F6F1E9')
MUTED = HexColor('#5B6E8A')
BODY_C = HexColor('#1A2942')
WHITE = HexColor('#FFFFFF')

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
        leading=26, spaceAfter=6, spaceBefore=14)
    s['cta_title'] = ParagraphStyle('cta_title',
        fontName='Helvetica-Bold', fontSize=22, textColor=NAVY,
        alignment=TA_CENTER, leading=30, spaceAfter=8, spaceBefore=14)
    s['step_num'] = ParagraphStyle('step_num',
        fontName='Helvetica-Bold', fontSize=48, textColor=GOLD,
        leading=52, spaceAfter=0, spaceBefore=20)
    s['step_title'] = ParagraphStyle('step_title',
        fontName='Helvetica-Bold', fontSize=20, textColor=NAVY,
        leading=24, spaceAfter=4, spaceBefore=4)
    s['step_sub'] = ParagraphStyle('step_sub',
        fontName='Helvetica-Oblique', fontSize=12, textColor=MUTED,
        leading=16, spaceAfter=10, spaceBefore=0)
    s['section_head'] = ParagraphStyle('section_head',
        fontName='Helvetica-Bold', fontSize=13, textColor=NAVY,
        leading=17, spaceAfter=8, spaceBefore=18)
    s['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=11.5, textColor=BODY_C,
        leading=19, spaceAfter=8, spaceBefore=4)
    s['body_bold'] = ParagraphStyle('body_bold',
        fontName='Helvetica-Bold', fontSize=11.5, textColor=NAVY,
        leading=19, spaceAfter=8, spaceBefore=4)
    s['body_strong'] = ParagraphStyle('body_strong',
        fontName='Helvetica-Bold', fontSize=13, textColor=NAVY,
        leading=19, spaceAfter=10, spaceBefore=6)
    s['body_italic'] = ParagraphStyle('body_italic',
        fontName='Helvetica-Oblique', fontSize=11, textColor=MUTED,
        leading=17, spaceAfter=6, spaceBefore=4)
    s['bullet'] = ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=11, textColor=BODY_C,
        leading=18, spaceAfter=7, spaceBefore=4,
        leftIndent=20)
    s['callout'] = ParagraphStyle('callout',
        fontName='Helvetica-Bold', fontSize=11.5, textColor=NAVY,
        leading=18, spaceAfter=10, spaceBefore=10,
        leftIndent=16, rightIndent=8,
        backColor=CREAM, borderPad=10)
    s['pull_quote'] = ParagraphStyle('pull_quote',
        fontName='Helvetica-Oblique', fontSize=12, textColor=CREAM,
        leading=20, spaceAfter=12, spaceBefore=12,
        leftIndent=20, rightIndent=20,
        backColor=NAVY, borderPad=14)
    s['action_label'] = ParagraphStyle('action_label',
        fontName='Helvetica-Bold', fontSize=9, textColor=GOLD,
        leading=12, spaceAfter=4, spaceBefore=14,
        leftIndent=12, backColor=CREAM)
    s['action_item'] = ParagraphStyle('action_item',
        fontName='Helvetica', fontSize=11, textColor=BODY_C,
        leading=18, spaceAfter=4, spaceBefore=4,
        leftIndent=28, backColor=CREAM)
    s['compliance'] = ParagraphStyle('compliance',
        fontName='Helvetica-Oblique', fontSize=9, textColor=MUTED,
        leading=14, spaceAfter=6, spaceBefore=16)
    s['transition'] = ParagraphStyle('transition',
        fontName='Helvetica-Oblique', fontSize=10.5, textColor=MUTED,
        leading=16, spaceAfter=8, spaceBefore=14)
    s['welcome_body'] = ParagraphStyle('welcome_body',
        fontName='Helvetica', fontSize=12, textColor=BODY_C,
        leading=22, spaceAfter=10, spaceBefore=6)
    s['sig_name'] = ParagraphStyle('sig_name',
        fontName='Helvetica-Bold', fontSize=12, textColor=NAVY,
        leading=16, spaceAfter=2, spaceBefore=20)
    s['sig_brand'] = ParagraphStyle('sig_brand',
        fontName='Helvetica', fontSize=11, textColor=GOLD,
        leading=15, spaceAfter=8)
    s['step_index'] = ParagraphStyle('step_index',
        fontName='Helvetica', fontSize=12, textColor=NAVY,
        leading=19, spaceAfter=4, spaceBefore=4,
        leftIndent=12, backColor=CREAM)
    s['cta_body'] = ParagraphStyle('cta_body',
        fontName='Helvetica', fontSize=13, textColor=BODY_C,
        alignment=TA_CENTER, leading=22, spaceAfter=10, spaceBefore=6)
    s['cta_btn'] = ParagraphStyle('cta_btn',
        fontName='Helvetica-Bold', fontSize=14, textColor=WHITE,
        alignment=TA_CENTER, leading=24,
        backColor=GOLD, borderPad=16, spaceAfter=10, spaceBefore=10)
    return s

def gold_rule():
    return HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=8, spaceBefore=4)

def sp(h=8):
    return Spacer(1, h)

def callout_p(text, S):
    return Paragraph(text, S['callout'])

def pull_quote_p(text, S):
    return Paragraph(f'"{text}"', S['pull_quote'])

def action_box(items, S, subtext=None):
    elems = []
    elems.append(Paragraph('SUA AÇÃO PARA ESTE PASSO', S['action_label']))
    if subtext:
        sub_s = ParagraphStyle('action_sub', parent=S['action_item'],
                               fontName='Helvetica', fontSize=11, textColor=BODY_C)
        elems.append(Paragraph(subtext, sub_s))
    for item in items:
        elems.append(Paragraph(f'&#9634;  {item}', S['action_item']))
    return elems

def build():
    out = '/Users/miriampalma/AI-OS/projects/prosper-landing/public/assets/prosper_in_america_guia_pt.pdf'
    doc = SimpleDocTemplate(out, pagesize=letter,
                            leftMargin=1.1*inch, rightMargin=1.1*inch,
                            topMargin=1.0*inch, bottomMargin=0.9*inch)
    W, H = letter
    S = make_styles()
    story = []

    # ── CAPA ────────────────────────────────────────────────
    cover_img_path = '/Users/miriampalma/Documents/ARCHIVE/ProsperInAmerica Guia/cover - 5Passos.png'

    def cover_bg(canvas, doc):
        canvas.saveState()
        if os.path.exists(cover_img_path):
            canvas.drawImage(cover_img_path, 0, 0, width=W, height=H, preserveAspectRatio=False)
        else:
            canvas.setFillColor(NAVY)
            canvas.rect(0, 0, W, H, fill=1, stroke=0)
        canvas.restoreState()

    story.append(Spacer(1, 0.1))
    story.append(PageBreak())

    # ── CARTA DA WELLEN ──────────────────────────────────────
    story.append(Paragraph('Uma Nota da Wellen', S['page_title']))
    story.append(gold_rule())
    story.append(sp(14))

    for line in [
        "Você não veio pra cá pra ficar no mesmo lugar.",
        "Eu também não.",
        "Quando eu cheguei aqui, eu não sabia como abrir uma conta.",
        "Não entendia crédito.",
        "Não sabia nem por onde começar.",
        "Aprendi errando.",
        "Eu sei o que é trabalhar duro e não sair do lugar.",
        "Esse guia existe por um motivo:",
        "Te dar clareza.",
        "Te dar direção.",
        "E te ajudar a não pagar o preço dos erros que ninguém te explicou.",
        "Leia isso com atenção.",
        "E mais importante:",
        "bota em prática.",
        "Se quiser ajuda pra aplicar isso na sua realidade,",
        "fala com a gente direto no WhatsApp.",
    ]:
        story.append(Paragraph(line, S['welcome_body']))

    story.append(sp(16))
    story.append(Paragraph('— Wellen', S['sig_name']))
    story.append(Paragraph('Prosper In America', S['sig_brand']))
    story.append(PageBreak())

    # ── COMO USAR ────────────────────────────────────────────
    story.append(Paragraph('Como Usar Este Guia', S['page_title']))
    story.append(gold_rule())
    story.append(sp(10))

    story.append(Paragraph("Este guia tem 5 passos essenciais.", S['body']))
    story.append(sp(8))
    story.append(Paragraph("Eles seguem uma sequência, mas você não precisa começar do início.", S['body']))
    story.append(sp(10))
    story.append(Paragraph("Se você já tem conta no banco, pule para o Passo 3.", S['body']))
    story.append(Paragraph("Se crédito é o seu maior gap, comece pelo Passo 4.", S['body']))
    story.append(Paragraph("Se você está preocupado com a proteção da sua família, vá direto para o Passo 5.", S['body']))
    story.append(sp(12))
    story.append(Paragraph('Encontre onde você está.', S['body_bold']))
    story.append(Paragraph('Comece por aí.', S['body_bold']))
    story.append(sp(12))
    story.append(Paragraph("Depois da base, vêm as próximas fases:", S['body']))
    story.append(Paragraph("aumentar sua renda e construir algo que dure.", S['body_italic']))
    story.append(sp(16))

    story.append(Paragraph('Passos deste guia', S['section_head']))
    for num, title in [
        ('01', 'Por Que a Maioria dos Imigrantes Fica Parada no Lugar'),
        ('02', 'Coloque Seus Números em Ordem'),
        ('03', 'Abra a Conta Certa'),
        ('04', 'Construa Seu Crédito'),
        ('05', 'Proteja o Que Você Está Construindo'),
    ]:
        story.append(Paragraph(f'<font color="#C8952E"><b>{num}</b></font>  {title}', S['step_index']))
    story.append(PageBreak())

    # ── PASSO 1 ──────────────────────────────────────────────
    story.append(Paragraph('01', S['step_num']))
    story.append(Paragraph('Por Que a Maioria dos Imigrantes Fica Parada no Lugar', S['step_title']))
    story.append(Paragraph('Não é falta de esforço. É falta de estrutura.', S['step_sub']))
    story.append(gold_rule())
    story.append(sp(10))

    story.append(Paragraph("Você trabalha muito.", S['body']))
    story.append(Paragraph("Isso nunca foi o problema.", S['body']))
    story.append(sp(12))
    story.append(Paragraph("O problema é não saber o que fazer com o que você ganha.", S['body']))
    story.append(sp(12))
    story.append(Paragraph("Você veio pra construir algo.", S['body']))
    story.append(Paragraph("Mas os anos passam — e nada muda.", S['body']))
    story.append(sp(10))
    story.append(Paragraph("O dinheiro entra.", S['body']))
    story.append(Paragraph("O dinheiro sai.", S['body']))
    story.append(Paragraph("Nada fica.", S['body']))
    story.append(sp(12))
    story.append(Paragraph("Isso não é falta de esforço.", S['body_bold']))
    story.append(sp(8))
    story.append(Paragraph("É falta de direção.", S['body_bold']))
    story.append(sp(16))

    story.append(Paragraph('Ninguém te deu o mapa.', S['section_head']))
    story.append(Paragraph("O sistema financeiro aqui não se explica.", S['body']))
    story.append(Paragraph("Ele espera que você já saiba tudo.", S['body']))
    story.append(sp(10))
    story.append(Paragraph("Se você não sabia — você foi aprendendo no escuro.", S['body']))
    story.append(sp(14))

    story.append(Paragraph('Você decidiu baseado no que apareceu:', S['section_head']))
    for line in [
        "o que alguém falou,",
        "o que viu no WhatsApp,",
        "o que parecia fazer sentido na hora.",
    ]:
        story.append(Paragraph(f'&nbsp;&nbsp;&nbsp;{line}', S['bullet']))
    story.append(sp(12))
    story.append(Paragraph("E algumas dessas decisões já estão te custando.", S['body_bold']))
    story.append(sp(8))
    story.append(Paragraph("Você só ainda não percebeu o quanto.", S['body_bold']))
    story.append(sp(16))

    story.append(Paragraph('O que muda quando você tem a informação certa', S['section_head']))
    for line in [
        "Você para de tomar decisões com base no medo ou em suposições.",
        "Você sabe qual passo vem primeiro — e por quê.",
        "Você para de perder tempo com as coisas erradas.",
        "O caminho fica claro.",
    ]:
        story.append(Paragraph(line, S['body']))
    story.append(sp(12))

    story.append(pull_quote_p("A diferença quase nunca é esforço. Quase sempre é informação — e saber em qual ordem agir.", S))
    story.append(sp(14))

    story.extend(action_box([
        'Conta bancária', 'Histórico de crédito', 'Declaração de imposto',
        'Proteger minha família', 'Construir renda',
    ], S, subtext='Identifique a área em que você se sente mais atrasado:'))
    story.append(sp(10))
    story.append(Paragraph('Quando você entende onde está, o próximo passo é descobrir o que você realmente tem acesso.', S['transition']))
    story.append(PageBreak())

    # ── PASSO 2 ──────────────────────────────────────────────
    story.append(Paragraph('02', S['step_num']))
    story.append(Paragraph('Coloque Seus Números em Ordem', S['step_title']))
    story.append(Paragraph('ITIN e SSN — o que cada um é e o que cada um abre.', S['step_sub']))
    story.append(gold_rule())
    story.append(sp(10))

    story.append(Paragraph("Você sabe que precisa de um número pra começar.", S['body']))
    story.append(Paragraph("Só não sabe ao certo o que cada um te abre.", S['body']))
    story.append(sp(16))

    story.append(Paragraph('SSN — Social Security Number', S['section_head']))
    story.append(Paragraph("Emitido pela Social Security Administration para pessoas autorizadas a trabalhar nos EUA.", S['body']))
    story.append(sp(6))
    story.append(Paragraph("Se você tem autorização de trabalho — por visto, green card ou outro status — você pode ser elegível para solicitá-lo.", S['body']))
    story.append(sp(6))
    story.append(Paragraph("Se você não tem autorização de trabalho, não vai conseguir um SSN.", S['body']))
    story.append(Paragraph("É aí que entra o ITIN.", S['body']))
    story.append(sp(14))

    story.append(Paragraph('ITIN — Individual Taxpayer Identification Number', S['section_head']))
    story.append(Paragraph("Emitido pelo IRS.", S['body']))
    story.append(Paragraph("É um número de processamento fiscal — não é prova de status imigratório, não é autorização de trabalho, e não é um caminho para benefícios por si só.", S['body']))
    story.append(sp(6))
    story.append(Paragraph("Existe para pessoas que têm obrigação de declarar imposto nos EUA mas não são elegíveis para o SSN.", S['body']))
    story.append(sp(12))

    story.append(Paragraph('Para que o ITIN é comumente usado:', S['section_head']))
    for item in [
        'Abrir certas contas bancárias',
        'Declarar imposto de renda',
        'Construir histórico de crédito em algumas instituições',
        'Solicitar certos produtos financeiros',
    ]:
        story.append(Paragraph(f'•  {item}', S['bullet']))
    story.append(sp(12))

    story.append(Paragraph('Como funciona o pedido, de forma geral:', S['section_head']))
    story.append(Paragraph("Você preenche o formulário W-7 do IRS.", S['body']))
    story.append(Paragraph("Envia junto com sua declaração de imposto e documentos de identidade.", S['body']))
    story.append(sp(6))
    story.append(Paragraph("Agentes certificados — chamados Certifying Acceptance Agents (CAAs) — podem ajudar no processo.", S['body']))
    story.append(Paragraph("Muitas empresas contábeis e organizações sem fins lucrativos oferecem esse serviço.", S['body']))
    story.append(sp(6))
    story.append(Paragraph("O tempo de processamento varia. Consulte o site do IRS para estimativas atuais.", S['body']))
    story.append(sp(14))

    story.append(Paragraph('O que isso significa pra você', S['section_head']))
    story.append(Paragraph("Se você tem SSN — você já tem uma vantagem.", S['body']))
    story.append(Paragraph("Entenda o que ele abre — e o que não abre.", S['body']))
    story.append(sp(8))
    story.append(Paragraph("Se você tem ITIN — você tem um ponto de partida real.", S['body']))
    story.append(Paragraph("Muitos bancos, credores e serviços aceitam.", S['body']))
    story.append(sp(8))
    story.append(Paragraph("Se você não tem nenhum dos dois — descubra se o ITIN se aplica à sua situação.", S['body']))
    story.append(Paragraph("É o ponto de partida para muitas pessoas sem autorização de trabalho.", S['body']))
    story.append(sp(10))

    story.append(callout_p("Não espere ter o SSN pra começar a construir. Para muitas pessoas nessa situação, o ITIN é o que abre as primeiras portas de verdade.", S))
    story.append(sp(12))

    story.extend(action_box([
        'Confirme se você tem SSN ou ITIN',
        'Se não tiver nenhum, pesquise o processo do ITIN — um contador ou CAA pode te orientar',
        'Anote para que você quer usar o número (banco, crédito, declaração)',
    ], S))
    story.append(sp(8))
    story.append(Paragraph('Observação: A elegibilidade para o ITIN e SSN depende do status imigratório individual. Informação geral apenas — consulte um profissional especializado em tributos ou imigração.', S['compliance']))
    story.append(Paragraph('Com o número certo em mãos, o próximo passo é onde seu dinheiro vai morar.', S['transition']))
    story.append(PageBreak())

    # ── PASSO 3 ──────────────────────────────────────────────
    story.append(Paragraph('03', S['step_num']))
    story.append(Paragraph('Abra a Conta Certa', S['step_title']))
    story.append(gold_rule())
    story.append(sp(12))

    story.append(Paragraph("Se a sua conta está errada, tudo o que vem depois fica mais difícil.", S['body_strong']))
    story.append(sp(8))
    story.append(Paragraph("Você não consegue construir crédito nos EUA sem uma conta.", S['body']))
    story.append(Paragraph("Não dá pra pagar aluguel, contas e seguro de forma confiável sem uma.", S['body']))
    story.append(sp(6))
    story.append(Paragraph("E se você abriu a conta errada — ou pulou esse passo — está pagando um preço que talvez ainda não tenha percebido.", S['body']))
    story.append(sp(14))

    story.append(Paragraph('Por que a conta errada atrasa tudo', S['section_head']))
    story.append(Paragraph("Nem toda conta bancária é igual.", S['body']))
    story.append(Paragraph("Algumas foram feitas pra quem já está estabelecido.", S['body']))
    story.append(Paragraph("Elas cobram tarifas mensais, exigem saldo mínimo e têm multas que vão drenando o que você está tentando construir.", S['body']))
    story.append(sp(8))
    story.append(Paragraph("Para um imigrante começando do zero, uma conta com tarifa mensal de $15 e saldo mínimo de $500 não é só inconveniente.", S['body']))
    story.append(sp(4))
    story.append(callout_p("Isso não é tarifa. Isso é um vazamento.", S))
    story.append(sp(10))

    story.append(Paragraph('O que procurar', S['section_head']))
    for label, text in [
        ('Aceita seus documentos:', 'Muitos bancos aceitam ITIN, passaporte e comprovante de endereço nos EUA — sem SSN obrigatório. Confirme diretamente antes de solicitar.'),
        ('Sem tarifas mensais:', 'Algumas contas cobram só por existir. Procure uma sem tarifa, ou que seja facilmente dispensada.'),
        ('Sem saldo mínimo:', 'Se você está começando do zero, não deveria ser penalizado por ter saldo baixo.'),
        ('Acesso online e pelo celular:', 'Básico. Se a conta não oferece, continue procurando.'),
        ('Caminho para crédito:', 'Alguns bancos oferecem produtos de construção de crédito para clientes existentes. Isso importa mais do que a maioria das pessoas percebe.'),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(12))

    story.append(Paragraph('O que evitar', S['section_head']))
    for label, text in [
        ('Cartão pré-pago como substituto de conta:', 'Não reporta ao bureau de crédito. Não constrói histórico bancário. É um recurso emergencial, não uma base.'),
        ('Contas com tarifas empilhadas:', 'Tarifa mensal + taxa de cheque especial + ATM fora da rede. Leia o resumo de tarifas antes de abrir qualquer conta.'),
        ('Esperar até ter SSN:', 'Em muitos casos, ITIN e passaporte são suficientes. Esperar custa tempo que você não precisa perder.'),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(12))

    story.append(Paragraph('Documentos normalmente solicitados', S['section_head']))
    for item in [
        'Passaporte (válido)',
        'ITIN ou SSN (quando exigido)',
        'Comprovante de endereço nos EUA — contrato de aluguel, conta de luz ou correspondência oficial',
    ]:
        story.append(Paragraph(f'•  {item}', S['bullet']))
    story.append(sp(8))
    story.append(Paragraph("Sempre ligue ou consulte o site da instituição antes de ir.", S['body_italic']))
    story.append(Paragraph("As exigências podem variar entre agências do mesmo banco.", S['body_italic']))
    story.append(sp(12))

    story.append(pull_quote_p("A conta certa não impressiona ninguém. Ela simplesmente funciona — sem tirar dinheiro enquanto faz isso.", S))
    story.append(sp(10))

    story.append(Paragraph('Se esse passo estiver errado, tudo o que vem depois fica mais lento, mais caro e mais difícil de corrigir.', S['body_bold']))
    story.extend(action_box([
        'Pesquise 2–3 opções de conta que aceitam seus documentos atuais',
        'Compare as tarifas — procure o resumo completo, não só os benefícios anunciados',
        'Confirme os requisitos diretamente com a instituição antes de solicitar',
        'Abra uma conta que não te cobre nada pra existir',
    ], S))
    story.append(sp(8))
    story.append(Paragraph('Observação: A elegibilidade para abertura de conta varia por instituição e estado. Confirme os requisitos diretamente com o banco ou cooperativa de crédito antes de solicitar.', S['compliance']))
    story.append(Paragraph('Com a conta certa aberta, o sistema começa a olhar para o seu histórico de crédito.', S['transition']))
    story.append(PageBreak())

    # ── PASSO 4 ──────────────────────────────────────────────
    story.append(Paragraph('04', S['step_num']))
    story.append(Paragraph('Construa Seu Crédito', S['step_title']))
    story.append(gold_rule())
    story.append(sp(10))

    story.append(Paragraph("Todo o seu histórico financeiro no Brasil não vale nada aqui.", S['body_strong']))
    story.append(Paragraph("Você começa do zero.", S['body_strong']))
    story.append(sp(8))

    story.append(Paragraph("Muitos imigrantes chegam sem nenhum histórico de crédito nos EUA.", S['body']))
    story.append(Paragraph("Não crédito ruim. Nenhum crédito.", S['body']))
    story.append(Paragraph("Aos olhos do sistema financeiro, você ainda não existe.", S['body']))
    story.append(sp(8))
    story.append(Paragraph("É por isso que as pessoas ficam presas por mais tempo do que esperavam.", S['body']))
    story.append(sp(8))
    story.append(Paragraph("Você não pode apressar o histórico de crédito.", S['body']))
    story.append(Paragraph("O que dá pra fazer: evitar os erros que te obrigam a recomeçar.", S['body']))
    story.append(Paragraph("E dar os passos certos cedo o suficiente pra que o tempo trabalhe a seu favor.", S['body']))
    story.append(sp(14))

    story.append(Paragraph('O que realmente importa — os três fatores', S['section_head']))
    for label, text in [
        ('Histórico de pagamentos:', 'O fator mais importante. Pague em dia, sempre. Um atraso pode ficar no seu relatório por anos.'),
        ('Utilização do crédito:', 'Quanto da sua linha disponível você está usando. Alta utilização sinaliza pressão financeira. Mantenha os saldos baixos.'),
        ('Tempo de histórico:', 'Contas mais antigas ajudam. Fechar sua primeira conta pra fazer upgrade costuma ser um erro.'),
    ]:
        story.append(Paragraph(f'<b><font color="#C8952E">{label}</font></b>  {text}', S['bullet']))
    story.append(sp(8))
    story.append(Paragraph('Todo o resto — consultas de crédito, mix de produtos — importa menos. Foque nesses três primeiro.', S['body_italic']))
    story.append(sp(14))

    story.append(Paragraph('Como imigrantes costumam começar a construir crédito', S['section_head']))
    for label, text in [
        ('Cartão de crédito garantido (secured):', 'Um depósito vira seu limite. Use, pague em dia. O comportamento de pagamento constrói o histórico — não o depósito.'),
        ('Virar usuário autorizado:', 'Alguém de confiança te adiciona no cartão dele. O histórico deles pode aparecer no seu relatório — uma das formas mais rápidas de estabelecer uma pontuação inicial.'),
        ('Empréstimo para construção de crédito:', 'Oferecido por alguns bancos e cooperativas. Pagamentos mensais fixos reportados ao bureau. Pesquise disponibilidade onde você tem conta.'),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(14))

    story.append(Paragraph('O que evitar', S['section_head']))
    for label, text in [
        ('Atrasar um pagamento — mesmo uma vez:', 'Configure pagamento mínimo automático. Um atraso pode ficar no seu histórico por até sete anos.'),
        ('Maximizar o cartão:', 'Alta utilização prejudica sua pontuação mesmo que você pague depois. Mantenha os saldos bem abaixo do seu limite.'),
        ('Solicitar vários produtos de uma vez:', 'Cada pedido gera uma consulta. Pesquise primeiro, solicite uma vez.'),
        ('Achar que seu histórico financeiro do Brasil vale aqui:', 'Não vale. O sistema americano não tem acesso a ele. Isso não é punição — é como o sistema funciona.'),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(8))

    story.append(callout_p("Quem descobre isso tarde, olha pra trás e vê anos que não consegue recuperar.", S))
    story.append(sp(12))
    story.append(pull_quote_p("Você não pode apressar o histórico de crédito. O que você pode fazer é evitar os erros que te obrigam a recomeçar.", S))
    story.append(sp(12))

    story.extend(action_box([
        'Verifique se você tem histórico de crédito nos EUA em annualcreditreport.com (gratuito)',
        'Pesquise um cartão garantido ou produto de construção de crédito adequado à sua situação',
        'Configure pagamento automático em todas as contas existentes',
        'Identifique alguém de confiança que possa te adicionar como usuário autorizado — e tenha essa conversa',
    ], S))
    story.append(sp(8))
    story.append(Paragraph('Observação: Pontuação de crédito e decisões de crédito dependem de muitos fatores individuais. Informação educacional apenas — não é aconselhamento financeiro. Consulte um profissional financeiro qualificado.', S['compliance']))
    story.append(Paragraph('Enquanto seu histórico financeiro começa a se construir, a próxima pergunta é: o que acontece se tudo parar?', S['transition']))
    story.append(PageBreak())

    # ── PASSO 5 ──────────────────────────────────────────────
    story.append(Paragraph('05', S['step_num']))
    story.append(Paragraph('Proteja o Que Você Está Construindo', S['step_title']))
    story.append(Paragraph('Muitos imigrantes passam anos construindo — e não protegem nada disso.', S['body_strong']))
    story.append(gold_rule())
    story.append(sp(10))

    story.append(Paragraph("Esse é o passo que as pessoas mais deixam pra depois.", S['body']))
    story.append(sp(6))
    story.append(Paragraph("Não porque não se importam com a família.", S['body']))
    story.append(Paragraph("Porque estão focadas em sobreviver agora — e a proteção parece algo pra resolver depois, quando as coisas estiverem mais estáveis.", S['body']))
    story.append(sp(6))
    story.append(Paragraph("Essa lógica é comum.", S['body']))
    story.append(Paragraph("E é exatamente assim que famílias acabam em crise.", S['body']))
    story.append(sp(14))

    story.append(Paragraph('Como o risco realmente parece', S['section_head']))
    step5_img_path = '/Users/miriampalma/Documents/ARCHIVE/ProsperInAmerica Guia/Step 5 Protection subtle family.png'
    if os.path.exists(step5_img_path):
        img5 = Image(step5_img_path, width=4.2*inch, height=2.8*inch, kind='proportional')
        img5.hAlign = 'CENTER'
        story.append(img5)
        story.append(sp(10))
    scenario_style = ParagraphStyle('scenario', fontName='Helvetica', fontSize=11.5,
                                    textColor=BODY_C, leading=20, spaceAfter=6, spaceBefore=6,
                                    leftIndent=12, rightIndent=12, backColor=CREAM, borderPad=14)
    story.append(Paragraph("Você é quem sustenta a casa.", scenario_style))
    story.append(sp(8))
    story.append(Paragraph("Você trabalha.", scenario_style))
    story.append(Paragraph("Paga o aluguel.", scenario_style))
    story.append(Paragraph("Manda dinheiro pro Brasil.", scenario_style))
    story.append(sp(8))
    story.append(Paragraph("Todo mês, é você.", scenario_style))
    story.append(sp(12))
    story.append(Paragraph("Agora pensa comigo:", scenario_style))
    story.append(sp(10))
    story.append(Paragraph("Se você parar por 6 meses —", scenario_style))
    story.append(Paragraph("quem segura tudo?", scenario_style))
    story.append(sp(8))
    story.append(Paragraph("Se algo acontecer com você —", scenario_style))
    story.append(Paragraph("quem sustenta sua família?", scenario_style))
    story.append(sp(8))
    story.append(Paragraph("E a família no Brasil que depende de você?", scenario_style))
    story.append(sp(14))
    story.append(Paragraph("Isso não é sobre medo.", S['body_bold']))
    story.append(sp(8))
    story.append(Paragraph("É sobre responsabilidade.", S['body_bold']))
    story.append(sp(8))
    story.append(Paragraph("E responsabilidade exige preparação.", S['body_bold']))
    story.append(sp(14))

    story.append(Paragraph('O que proteção realmente significa', S['section_head']))
    for label, text in [
        ('Seguro de vida:', "Uma apólice paga um valor determinado à sua família se você falecer. É uma estrutura simples: você paga uma mensalidade, e se o pior acontecer, sua família recebe um valor que pode cobrir despesas finais, renda perdida e tempo pra se reorganizar."),
        ('Plano de saúde:', "Dívida médica é uma das principais causas de colapso financeiro nos EUA — mesmo para famílias que trabalham. Uma única internação sem cobertura pode apagar anos de poupança."),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(14))

    story.append(Paragraph('Seguro de vida e status imigratório', S['section_head']))
    story.append(Paragraph("Muitas famílias assumem que precisam de SSN pra se qualificar para seguro de vida.", S['body']))
    story.append(Paragraph("Essa suposição custa anos de cobertura que elas poderiam ter tido.", S['body']))
    story.append(sp(8))
    story.append(Paragraph("Algumas apólices aceitam solicitantes com ITIN.", S['body']))
    story.append(Paragraph("O processo de análise varia por apólice e operadora.", S['body']))
    story.append(Paragraph("Mas a opção existe.", S['body']))
    story.append(sp(8))
    story.append(callout_p("Se você tem esperado até ter seu SSN, descubra o que você já pode ser elegível agora.", S))
    story.append(sp(14))

    story.append(Paragraph('O que evitar', S['section_head']))
    for label, text in [
        ('Esperar até se sentir estável:', 'Não existe estável. Estabilidade se constrói, não se espera. Quem espera o momento perfeito, espera para sempre.'),
        ('Achar que não vai se qualificar:', 'Muita gente nunca verifica. Essa suposição está errada com mais frequência do que as pessoas imaginam.'),
        ('Escolher cobertura só pelo preço:', 'A opção mais barata e a opção certa nem sempre são a mesma coisa.'),
        ('Deixar essa conversa pra quando algo forçar:', 'A hora de pensar em proteger sua família não é durante uma crise. É antes.'),
    ]:
        story.append(Paragraph(f'<b>{label}</b>  {text}', S['bullet']))
    story.append(sp(12))

    story.append(pull_quote_p("Proteção não é o que você constrói depois que está estável. Faz parte do que torna a estabilidade possível.", S))
    story.append(sp(10))

    story.append(Paragraph("Esse passo quase sempre é adiado até que algo force a decisão.", S['body_bold']))
    story.append(Paragraph("Quando isso acontece, as opções são menores.", S['body_bold']))
    story.extend(action_box([
        'Pergunte a si mesmo: se eu não pudesse trabalhar por 6 meses, o que aconteceria com minha família?',
        'Pesquise opções de plano de saúde — comece pelo healthcare.gov ou um assistente local',
        'Verifique se seus documentos atuais permitem solicitar seguro de vida',
        'Converse com um profissional licenciado — não pra comprar nada, mas pra entender o que existe',
    ], S))
    story.append(sp(8))
    story.append(Paragraph('Observação: A elegibilidade para seguros, coberturas e programas de saúde varia por circunstâncias, status imigratório e estado. Conteúdo informacional apenas — não é aconselhamento de seguros. Consulte um profissional de seguros ou saúde licenciado.', S['compliance']))

    story.append(sp(22))
    story.append(HRFlowable(width='40%', thickness=1, color=GOLD, spaceAfter=16, spaceBefore=12))
    story.append(Paragraph("Até aqui, você organizou a base.", S['body_bold']))
    story.append(sp(10))
    story.append(Paragraph("É aqui que a maioria para.", S['body']))
    story.append(sp(12))
    story.append(Paragraph("Mas quem realmente avança entende duas coisas:", S['body']))
    story.append(sp(10))
    story.append(Paragraph("Como aumentar a renda…", S['body']))
    story.append(Paragraph("E como construir algo que não dependa só do seu tempo.", S['body']))
    story.append(sp(12))
    story.append(Paragraph("Essas são as próximas fases.", S['body']))
    story.append(sp(10))
    story.append(Paragraph("Mas elas só funcionam quando a base está certa.", S['body_bold']))

    # ── SE VOCÊ CONTINUAR ───────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph('Se você continuar como está…', S['page_title']))
    story.append(gold_rule())
    story.append(sp(16))

    story.append(Paragraph("Se nada mudar, daqui a 1 ano sua vida vai estar igual.", S['body']))
    story.append(sp(12))
    story.append(Paragraph("Mais trabalho.", S['body']))
    story.append(Paragraph("Mais esforço.", S['body']))
    story.append(Paragraph("E a mesma sensação de que algo está faltando.", S['body']))
    story.append(sp(18))

    story.append(Paragraph("Não é porque você não tenta.", S['body']))
    story.append(sp(12))
    story.append(Paragraph("É porque ninguém te mostrou a ordem certa.", S['body']))
    story.append(sp(18))

    story.append(Paragraph("E esse é o ponto que a maioria das pessoas trava.", S['body']))
    story.append(sp(12))
    story.append(Paragraph("Elas entendem.", S['body']))
    story.append(sp(4))
    story.append(Paragraph("Mas não fazem nada com isso.", S['body']))
    story.append(sp(22))

    story.append(Paragraph("Você tem duas opções agora:", S['body_strong']))
    story.append(sp(16))
    story.append(Paragraph("Fechar esse guia… e continuar exatamente onde você está hoje.", S['body']))
    story.append(sp(12))
    story.append(Paragraph("Ou usar isso como ponto de virada.", S['body_bold']))
    story.append(sp(22))

    story.append(Paragraph("Você não precisa resolver tudo hoje.", S['body']))
    story.append(sp(12))
    story.append(Paragraph("Mas precisa decidir se vai continuar no mesmo caminho —<br/>ou começar a ajustar isso de forma intencional.", S['body']))

    # ── PÁGINA CTA ───────────────────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1, 1.8*inch))
    story.append(Paragraph('Quer conversar sobre a sua situação?', S['cta_title']))
    story.append(gold_rule())
    story.append(sp(24))
    story.append(Paragraph('Se esse guia fez sentido pra você, não para aqui.', S['cta_body']))
    story.append(sp(8))
    story.append(Paragraph('A maioria das pessoas entende isso…', S['cta_body']))
    story.append(Paragraph('e não faz nada.', S['cta_body']))
    story.append(sp(8))
    story.append(Paragraph('Se você quiser clareza sobre a sua situação,', S['cta_body']))
    story.append(Paragraph('manda uma mensagem no WhatsApp e me fala onde você está hoje.', S['cta_body']))
    story.append(sp(8))
    story.append(Paragraph('A gente olha junto.', S['cta_body']))
    story.append(sp(8))
    story.append(Paragraph('Sem pressão.', S['cta_body']))
    story.append(Paragraph('Sem promessa.', S['cta_body']))
    story.append(Paragraph('Só direção.', S['cta_body']))
    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph(
        '<a href="https://wa.me/13526303930" color="white">Quero conversar no WhatsApp →</a>',
        S['cta_btn']
    ))
    story.append(sp(14))
    story.append(Paragraph('wa.me/13526303930', S['cover_url']))
    story.append(sp(12))
    story.append(Paragraph('Se você leu até aqui, você não é a maioria.', S['body_italic']))
    story.append(Spacer(1, 0.4*inch))
    story.append(HRFlowable(width='30%', thickness=1, color=GOLD, spaceAfter=10, spaceBefore=10))
    story.append(Paragraph('prosperinamerica.com  |  @prosperinamerica', S['cover_url']))

    doc.build(story, onFirstPage=cover_bg, onLaterPages=lambda c, d: None)
    print(f'PDF salvo: {out}')

build()
