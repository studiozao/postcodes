"""Generates the Local economic prosperity microsite as static HTML.
Placeholders in [square brackets] are kept verbatim and highlighted."""
import html, re, os, sys

OUT = sys.argv[1]
from urllib.parse import quote as _q
BOOK = "mailto:chris@studiozao.com?subject=" + _q("Local economic prosperity: 30-minute conversation")
CONNECT = "mailto:marketing@studiozao.com?subject=" + _q("Next Connect")
EMAIL = "marketing@studiozao.com"
os.makedirs(os.path.join(OUT, "case-studies"), exist_ok=True)


def t(s):
    """Escape text and highlight [placeholders]."""
    s = html.escape(s, quote=False)
    return re.sub(r"\[([^\]]+)\]", r'<span class="ph">[\1]</span>', s)


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..900&display=swap" rel="stylesheet">'
         '<link rel="preconnect" href="https://api.fontshare.com">'
         '<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap" rel="stylesheet">')


def head(title, desc, root):
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{FONTS}
<link rel="stylesheet" href="{root}styles.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(root):
    return f"""<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{root}index.html"><img src="{root}assets/studiozao-logo.png" alt="Studio Zao" width="113" height="35"></a>
    <nav aria-label="Main">
      <a href="{root}index.html#how">How we work</a>
      <a href="{root}index.html#what">What we do</a>
      <a href="{root}index.html#value">Social value</a>
      <a class="btn btn-small" href="{root}index.html#contact">Get in touch</a>
    </nav>
  </div>
</header>
"""


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap foot">
    <p><strong>Studio Zao</strong>, London</p>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p><a href="https://studiozao.com">studiozao.com</a></p>
    <p>Looking for Next Steps Studios? Visit <a href="https://nss.studiozao.com">nss.studiozao.com</a></p>
  </div>
</footer>
<script>
(function(){{
  if(!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}})}},{{rootMargin:'0px 0px -8% 0px'}});
  document.querySelectorAll('.reveal').forEach(function(el){{io.observe(el)}});
}})();
</script>
</body>
</html>
"""


STRANDS = [
    {
        "id": "business",
        "name": "Business support",
        "intro": "Programmes that help local businesses start, grow and adopt new tools, including practical AI. Support can be built around a sector or a local cluster of businesses.",
        "cases": [
            {"slug": "impact-torbay", "title": "Impact Torbay",
             "challenge": "[what Torbay needed]",
             "did": "We designed and ran a business support programme for [who] in Torbay [length, format].",
             "changed": "[number of businesses supported; key outcomes]",
             "quote": "[from Gemma, Torbay, if she agrees]"},
            {"slug": "impact-tamworth", "title": "Impact Tamworth",
             "challenge": "[what Tamworth needed]",
             "did": "[programme, length, who it supported]",
             "changed": "[outcomes]",
             "quote": "[from Tamworth, if they agree]"},
        ],
    },
    {
        "id": "skills",
        "name": "Employment, skills and jobs",
        "intro": "Programmes that build entrepreneurial skills and connect people to employers and real work.",
        "cases": [
            {"slug": "next-steps-studios", "title": "Next Steps Studios, South London",
             "challenge": "Many recent graduates in South London are unsure what comes next.",
             "did": "We ran a free, three-week, in-person programme at Clapham Junction from 22 June to 10 July 2026. Teams built and tested business ideas on real briefs from Peabody, Unilever and EY Foundation, used AI tools throughout, and pitched to partners and employers at a showcase. Supported by the South London Partnership and the Mayor of London.",
             "changed": "[number of participants; outcomes]",
             "link": ("See the programme", "https://nss.studiozao.com")},
            {"slug": "tower-hamlets", "title": "Tower Hamlets",
             "challenge": "[from Sara]",
             "did": "[from Sara]",
             "changed": "[from Sara]",
             "quote": "[from Sara]"},
        ],
    },
    {
        "id": "community",
        "name": "Community engagement and co-design",
        "intro": "Engagement that brings residents into the design of services, places and plans, and leaves something behind.",
        "cases": [
            {"slug": "slp-retrofit-roadmap", "title": "South London Partnership retrofit roadmap",
             "challenge": "[what SLP needed on green retrofit]",
             "did": "We brought people together through a roundtable and a hack, and turned what we heard into a roadmap report [confirm scope].",
             "changed": "[outcome]",
             "link_ph": "[report, if public]"},
            {"slug": "torbay-community-hack", "title": "Community hack, Torbay",
             "challenge": "[what the community needed]",
             "did": "We ran a community hack around stand-up paddleboarding [confirm name and details].",
             "changed": "[the community-led outcomes]",
             "quote": "[if available]"},
        ],
    },
]


def proof(c, root, on_page=False):
    if "link" in c:
        label, href = c["link"]
        return f'<a class="ext" href="{href}">{t(label)} <span aria-hidden="true">&#8599;</span></a>'
    if "link_ph" in c:
        return f'<p class="proof"><span class="k">Link</span> {t(c["link_ph"])}</p>'
    return f'<blockquote class="proof"><span class="k">Quote</span> {t(c["quote"])}</blockquote>'


def card(c, strand):
    return f"""<article class="card reveal">
  <h4><a href="case-studies/{c['slug']}.html">{t(c['title'])}</a></h4>
  <dl>
    <dt>The challenge</dt><dd>{t(c['challenge'])}</dd>
    <dt>What we did</dt><dd>{t(c['did'])}</dd>
    <dt>What changed</dt><dd>{t(c['changed'])}</dd>
  </dl>
  {proof(c, '')}
  <a class="more" href="case-studies/{c['slug']}.html" aria-label="Read the full case study: {html.escape(c['title'])}">Read the case study <span aria-hidden="true">&rarr;</span></a>
</article>"""


HOW = [
    ("Business-led", "We start from what local businesses and residents need, then design the programme around them."),
    ("Local and in person", "Our team is on the ground in the places we work, running sessions and mentoring people directly."),
    ("Co-designed", "Residents, businesses and partners shape the programme with us from the start."),
    ("Adaptable", "We test, learn and adjust while a programme runs."),
    ("AI to make things happen", "We use AI in our own delivery, and help businesses and teams put it to practical use."),
    ("Accessible", "We design for people who don't usually take part."),
]

PLACES = ["Torbay", "Tamworth", "Tower Hamlets", "East Sussex", "South London"]

# ---------- index ----------
p = [head("Local economic prosperity | Studio Zao",
          "Studio Zao helps councils and strategic authorities design and deliver business support, skills and community programmes that work on the ground.", ""),
     header("")]

p.append(f"""<main id="main">
<section class="hero">
  <div class="wrap">
    <p class="label">Local economic prosperity</p>
    <h1>Growth in any postcode.</h1>
    <p class="lede">We help councils and strategic authorities design and deliver business support, skills and community programmes that work on the ground. We take them from brief to launch, and we use AI to move faster.</p>
    <div class="actions">
      <a class="btn" href="{BOOK}">Book a conversation</a>
      <a class="btn btn-ghost" href="{CONNECT}">Ask about our next Connect</a>
    </div>
  </div>
</section>

<section class="section" id="who">
  <div class="wrap split">
    <h2 class="reveal">Who we are</h2>
    <div class="reveal">
      <p class="big">Studio Zao is a London innovation and growth studio. For councils, we are the team that turns a plan into a programme people can use. We design it with local businesses and residents, run it in person, and adapt it as we learn.</p>
      <p>We have delivered programmes in Torbay, Tamworth, Tower Hamlets, East Sussex and South London, for councils, partnerships and the people they serve.</p>
      <ul class="places" aria-label="Places we have worked">{''.join(f'<li>{x}</li>' for x in PLACES)}</ul>
    </div>
  </div>
</section>

<section class="section tint" id="how">
  <div class="wrap">
    <h2 class="reveal">How we work</h2>
    <ol class="how">
      {''.join(f'<li class="reveal"><h3>{t(a)}</h3><p>{t(b)}</p></li>' for a, b in HOW)}
    </ol>
  </div>
</section>

<section class="section" id="why">
  <div class="wrap split">
    <h2 class="reveal">Why the three strands belong together</h2>
    <div class="reveal">
      <p class="big">Councils often fund business support, skills and community engagement from separate budgets and teams. Residents and businesses experience them as one place.</p>
      <ul class="links">
        <li><span class="from">Skills</span><span class="arrow" aria-hidden="true">&rarr;</span><span>A skills programme can produce new founders.</span></li>
        <li><span class="from">Community</span><span class="arrow" aria-hidden="true">&rarr;</span><span>Community engagement shows which support people will actually use.</span></li>
        <li><span class="from">Business</span><span class="arrow" aria-hidden="true">&rarr;</span><span>Business support creates the jobs that skills programmes prepare people for.</span></li>
      </ul>
      <p>We work across all three, so whichever strand you start with, we design it to connect to the others.</p>
    </div>
  </div>
</section>

<section class="section tint" id="what">
  <div class="wrap">
    <h2 class="reveal">What we do</h2>
""")
for i, s in enumerate(STRANDS, 1):
    p.append(f"""    <div class="strand" id="{s['id']}">
      <div class="strand-head reveal">
        <p class="num">0{i}</p>
        <h3>{t(s['name'])}</h3>
        <p>{t(s['intro'])}</p>
      </div>
      <div class="cards">
        {''.join(card(c, s) for c in s['cases'])}
      </div>
    </div>
""")
p.append(f"""  </div>
</section>

<section class="section" id="value">
  <div class="wrap split">
    <h2 class="reveal">What our work leaves behind</h2>
    <div class="reveal">
      <p class="big">Our programmes leave more in a place than the contract asks for: community-led projects, new local networks, and people taking part who usually don't.</p>
      <p>{t('[One or two examples from Torbay or Tamworth, with a figure if we have one.]')}</p>
    </div>
  </div>
</section>

<section class="cta" id="contact">
  <div class="wrap">
    <h2>Let's talk about your area</h2>
    <p class="lede">Tell us what you want to change locally. We will tell you honestly whether we can help, and what has worked elsewhere.</p>
    <div class="actions">
      <a class="btn btn-light" href="{BOOK}">Book a 30-minute conversation</a>
      <a class="btn btn-ghost-light" href="{CONNECT}">Ask about our next Connect</a>
    </div>
    <p class="small">Connects are small, invite-only roundtables for council and partnership leads, each on one topic.</p>
  </div>
</section>
</main>
""")
p.append(footer())
open(os.path.join(OUT, "index.html"), "w").write("".join(p))

# ---------- case study pages ----------
for s in STRANDS:
    for c in s["cases"]:
        q = [head(f"{c['title']} | Local economic prosperity | Studio Zao",
                  f"Case study: {c['title']}. {s['name']} by Studio Zao.", "../"),
             header("../")]
        q.append(f"""<main id="main">
<section class="hero hero-case">
  <div class="wrap">
    <p class="label"><a href="../index.html#{s['id']}">{t(s['name'])}</a></p>
    <h1>{t(c['title'])}</h1>
  </div>
</section>
<section class="section">
  <div class="wrap case">
    <h2>The challenge</h2><p>{t(c['challenge'])}</p>
    <h2>What we did</h2><p>{t(c['did'])}</p>
    <h2>What changed</h2><p>{t(c['changed'])}</p>
    {('<h2>See more</h2><p>' + proof(c, '../') + '</p>') if 'link' in c else ''}
    {('<h2>Report</h2><p>' + t(c['link_ph']) + '</p>') if 'link_ph' in c else ''}
    {('<h2>In their words</h2><blockquote class="pull">' + t(c['quote']) + '</blockquote>') if 'quote' in c else ''}
    <p class="back"><a href="../index.html#what">&larr; Back to all our work</a></p>
  </div>
</section>
<section class="cta">
  <div class="wrap">
    <h2>Let's talk about your area</h2>
    <p class="lede">Tell us what you want to change locally. We will tell you honestly whether we can help, and what has worked elsewhere.</p>
    <div class="actions"><a class="btn btn-light" href="{BOOK}">Book a 30-minute conversation</a></div>
  </div>
</section>
</main>
""")
        q.append(footer())
        open(os.path.join(OUT, "case-studies", c["slug"] + ".html"), "w").write("".join(q))

open(os.path.join(OUT, ".nojekyll"), "w").write("")
print("built")
