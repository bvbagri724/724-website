#!/usr/bin/env python3
"""Builds the 724.uk.com website from apps.json.

To add a new app: add it to apps.json (and, if it needs its own privacy text, a
function in PRIVACY below), run `python3 build.py`, then upload the changed files
to GitHub. Every app automatically gets:
  /apps/<id>/                 about + support page
  /apps/<id>/privacy.html     privacy policy (the link the App Store / Google Play ask for)
  /apps/<id>/delete-account.html   how to delete an account (Google Play asks for this link)
"""
import json, os, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(ROOT, 'apps.json')))
P = D['publisher']
UPDATED = '18 November 2026'
e = html.escape

BRANDS = [
    ('bunz', 'Bunz', 'Burgers & chicken', '🍔', 'Smash burgers, crispy fried chicken and breakfast favourites, made with patties we press ourselves.'),
    ('kebabox', 'Kebabox', 'Kebabs & wraps', '🥙', 'Grilled kebabs, loaded boxes and wraps, generous and freshly made to order.'),
    ('pizzoria', 'Pizzoria', 'Pizza & pasta', '🍕', 'One size only: a full 15-inch pizza, plus comforting pasta dishes.'),
    ('woomi', 'Woomi', 'Indo-Chinese', '🍜', 'Noodles, fried rice and popular Indian dishes, cooked fast and full of flavour.'),
    ('brew', 'Brew Koffee', 'Coffee & drinks', '☕', 'Hot and iced coffee in one generous 400ml size, and tea from £1.'),
    ('tubble', 'Tubble', 'Bubble tea', '🧋', 'Bubble tea in one big 700ml cup, made by our automated tea machine for the same taste every time.'),
    ('bazic', 'BAZIC', 'Everyday essentials', '🛒', 'A tight range of no-frills essentials that comes in the same bag as your food.'),
]


def page(title, body, desc, depth=0, active=''):
    up = '../' * depth
    nav = ''.join(f'<a href="{up}{h}"{" style=\"color:var(--gold2)\"" if active == k else ""}>{t}</a>' for k, h, t in [
        ('home', 'index.html#brands', 'Our brands'), ('724', 'index.html#seven24', '724'), ('apps', 'apps/', 'Apps'), ('contact', 'index.html#contact', 'Contact')])
    return f'''<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/style.css"></head><body>
<header class="top"><div class="wrap"><a class="brand" href="{up}index.html"><img src="{up}assets/favicon.svg" width="34" height="34" alt=""><span><b>BVBAGRI</b><small>FOOD FAMILY</small></span></a>
<nav class="menu">{nav}</nav></div></header>
{body}
<footer><div class="wrap">
<div><b style="font-family:Fraunces,Georgia,serif;font-size:20px;letter-spacing:.06em">BVBAGRI FOOD FAMILY</b><p style="margin-top:8px">One family. Many brands. Same promise.<br>Real food. Real people. Real value. Every time.</p></div>
<div><b>Company</b><br><a href="{up}index.html#brands">Our brands</a><br><a href="{up}index.html#seven24">724 delivery</a><br><a href="{up}index.html#contact">Contact</a></div>
<div><b>Apps &amp; legal</b><br><a href="{up}apps/">Our apps &amp; support</a><br><a href="{up}privacy.html">Privacy notice</a><br><a href="mailto:{P['support']}">{P['support']}</a></div>
<div class="legal">{e(P['name'])} · Registered in England and Wales, company number {P['number']} · Registered office: {e(P['office'])} · ICO registration {P['ico']}</div>
</div></footer></body></html>'''


def w(path, text):
    full = os.path.join(ROOT, path); os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    open(full, 'w', encoding='utf-8').write(text)


# ---------------- home page ----------------
brandbar = '<div class="brandbar">' + ''.join(f'<i style="background:var(--{b[0]})"></i>' for b in BRANDS) + '</div>'
cards = ''.join(f'''<div class="bcard" style="--c:var(--{k})"><div class="ic">{ic}</div><h3>{e(n)}</h3><div class="what">{e(what)}</div><p>{e(t)}</p></div>''' for k, n, what, ic, t in BRANDS)
apps_cards = ''.join(f'''<a class="card app" href="apps/{a['id']}/" style="text-decoration:none"><div class="ai" style="background:{a['colour']}">{e(a['icon'])}</div><div><h3 style="margin-bottom:2px">{e(a['name'])}</h3>
<span class="badge">{e(a['status'])}</span><p style="color:var(--muted);font-size:15px;margin:10px 0 0">{e(a['summary'])}</p></div></a>''' for a in D['apps'])
home = f'''
<section class="hero"><div class="wrap">
<span class="eyebrow">BVBAGRI Food Family</span>
<h1>Real food. Real people.<br><span>Real value.</span> Every time.</h1>
<p class="lead">BVBAGRI is a family of UK takeaway and delivery brands — burgers, kebabs, pizza, Indo-Chinese, coffee, bubble tea and everyday essentials — all ordered through one app and delivered by our own team.</p>
<div class="ctas"><a class="btn gold" href="#brands">Meet the brands</a><a class="btn line" href="#seven24">How 724 works</a></div>
</div></section>{brandbar}

<section id="brands"><div class="wrap">
<span class="eyebrow">One family. Many brands.</span><h2>Seven brands, one basket</h2>
<p class="lead">Each brand keeps a short menu of the dishes people love most. Because they share one kitchen and many of the same fresh ingredients, we can keep portions generous and prices low.</p>
<div class="grid g4" style="margin-top:36px">{cards}
<div class="bcard" style="--c:var(--olive);background:var(--olive);color:#fff"><div class="ic" style="background:var(--gold);color:var(--olive)">★</div><h3>£1 · £2 · £3</h3><div class="what" style="color:var(--gold2)">Value menu</div><p style="color:rgba(255,255,255,.8)">A shared value menu across every brand — full-size items, never shrunk to hit a price.</p></div>
</div></div></section>

<section id="seven24" class="alt"><div class="wrap split">
<div><span class="eyebrow">Our own ordering &amp; delivery</span><h2>724 — open 7am to midnight</h2>
<p class="lead">724 is our own app. Order from any of our brands in one basket, add essentials from BAZIC, and our own riders bring it to your door.</p>
<div class="grid" style="gap:22px;margin-top:28px">
<div class="pr"><div class="n">1</div><div><h3>One basket, every brand</h3><p>Mix a pizza, a bubble tea and a pint of milk in a single order and a single delivery.</p></div></div>
<div class="pr"><div class="n">2</div><div><h3>Low everyday prices</h3><p>No inflated prices with fake discounts — the price you see is the everyday price.</p></div></div>
<div class="pr"><div class="n">3</div><div><h3>Delivery fees and tips go to the team</h3><p>The money from delivery charges and tips is paid out to the people who make and deliver your food.</p></div></div>
<div class="pr"><div class="n">4</div><div><h3>Halal, no pork</h3><p>We use halal suppliers and there is no pork on any of our menus.</p></div></div>
</div></div>
<div class="panel724"><div class="big">7·24</div><p style="color:rgba(255,255,255,.75);margin-top:8px">Our first store is opening in Pitsea, Essex.</p>
<ul><li><b>7</b><span>We start delivering at 7am</span></li><li><b>24</b><span>…and keep going until midnight</span></li><li><b>£</b><span>Low delivery charge, set by distance</span></li><li><b>⟳</b><span>Order in the app, or collect from the shop</span></li></ul>
<p style="margin:22px 0 0"><span class="badge">App coming soon</span></p></div>
</div></section>

<section id="apps"><div class="wrap">
<span class="eyebrow">Apps</span><h2>Apps published by BVBAGRI</h2>
<p class="lead">BVBAGRI publishes apps for its own brands, for businesses in its group and for UK higher education. Each app has its own support, privacy and account deletion page.</p>
<div class="grid g2" style="margin-top:32px">{apps_cards}</div>
<p style="margin-top:22px"><a class="btn dark" href="apps/">All apps &amp; support →</a></p>
</div></section>

<section id="contact" class="contact"><div class="wrap">
<span class="eyebrow">Contact</span><h2 style="color:#fff">Talk to us</h2>
<div class="grid g3" style="margin-top:28px">
<div class="card"><h3 style="color:#fff">General enquiries</h3><p>Suppliers, partners, press and anything else.</p><a class="mail" href="mailto:{P['general']}">{P['general']}</a></div>
<div class="card"><h3 style="color:#fff">App support</h3><p>Help with any of our apps, privacy questions and account deletion.</p><a class="mail" href="mailto:{P['support']}">{P['support']}</a></div>
<div class="card"><h3 style="color:#fff">Registered office</h3><p style="color:#fff">{e(P['name'])}<br>{e(P['office']).replace(', ', '<br>')}</p><p>Company number {P['number']}</p></div>
</div></div></section>'''
w('index.html', page('BVBAGRI Food Family — burgers, kebabs, pizza, bubble tea & more, delivered by 724', home, 'BVBAGRI FOODS CORPORATION LIMITED — a family of UK takeaway and delivery brands ordered through our own 724 app.', 0, 'home'))

# ---------------- website privacy notice ----------------
priv = f'''<div class="page"><div class="wrap"><span class="eyebrow">Legal</span><h1 style="font-size:44px">Privacy notice</h1><p class="lead">For this website and for emails you send us. Last updated {UPDATED}.</p>
<h2>Who we are</h2><p>{e(P['name'])} (company number {P['number']}, registered office {e(P['office'])}) runs this website. We are registered with the UK Information Commissioner's Office, registration number {P['ico']}.</p>
<h2>What this website collects</h2><p>This website has no sign-up, no forms, no advertising and no analytics or tracking cookies. Our web host and the font service (Google Fonts) receive your device's IP address and browser details, because every website needs them to send the page to you.</p>
<h2>When you email us</h2><p>If you email {P['general']} or {P['support']}, we receive your name, email address and whatever you write. We use it only to reply and to deal with your request, and we keep it for as long as we need to for that and for our legal and accounting records.</p>
<h2>Our apps</h2><p>Each of our apps has its own privacy policy, listed on the <a href="apps/">apps page</a>.</p>
<h2>Your rights</h2><p>Under UK data protection law you can ask for a copy of your data, ask us to correct or delete it, or object to how we use it. Email <a href="mailto:{P['support']}">{P['support']}</a>. We reply within one month. You can also complain to the Information Commissioner's Office at <a href="https://ico.org.uk/make-a-complaint/">ico.org.uk/make-a-complaint</a>.</p>
</div></div>'''
w('privacy.html', page('Privacy notice — BVBAGRI', priv, 'Privacy notice for the BVBAGRI website.', 0))


# ---------------- per-app privacy text ----------------
def privacy_pending(a):
    return f'''<div class="note"><b>{e(a['name'])} is not yet on the App Store or Google Play.</b> Its full privacy policy will be published on this page before it is released there.</div>
<p>The organisation responsible for personal data in {e(a['name'])} (the controller) will be {e(a['controller'])}. The app is published by {e(P['name'])}, United Kingdom (ICO registration {P['ico']}). Questions: <a href="mailto:{P['support']}">{P['support']}</a>.</p>'''


def privacy_nobel(a):
    return f'''<p class="lead">Nobel Export Factory is a private workplace app. Accounts are created only by Nobel Export Company for its own staff, managers and invited business clients.</p>
<h2>Who is responsible</h2>
<table><tr><th>Data fiduciary (controller)</th><td>Nobel Export Company, Tiruppur, Tamil Nadu, India — the employer that decides what the app is used for. Contact: <a href="mailto:nobel151013@gmail.com">nobel151013@gmail.com</a></td></tr>
<tr><th>App publisher and service provider</th><td>{e(P['name'])}, United Kingdom (company number {P['number']}). We build and run the app for Nobel Export Company and use the data only on its instructions. Contact: <a href="mailto:{P['support']}">{P['support']}</a></td></tr></table>
<h2>What the app collects, and why</h2>
<table>
<tr><th>Staff record</th><td>Name (in English and Tamil), photo, phone number, department, shift, joining date, pay details and bank details.</td><td>To employ you, plan work and pay you.</td></tr>
<tr><th>Face and voice check</th><td>A face template (a set of numbers made from photos of your face), a short voice sample, and photos taken at the factory gate tablet or gate cameras.</td><td>To record attendance — who came in and went out, and when — and to stop anyone marking attendance for someone else.</td></tr>
<tr><th>Location</th><td>Your device's location at the moment you check in or out.</td><td>To confirm you were at the factory. It is not tracked at other times.</td></tr>
<tr><th>Work records</th><td>Attendance times, time spent out of the factory, extra work, leave, production entries, salary advances (with your signature) and payslips.</td><td>To run the factory and to work out pay correctly.</td></tr>
<tr><th>Messages</th><td>WhatsApp messages and voice notes exchanged with the factory's WhatsApp number.</td><td>To ask about and record reasons (for example, time out of the factory) and to send reminders.</td></tr>
<tr><th>Visitors</th><td>Photos of people at the factory gate who are not staff, with the time.</td><td>Security of the factory and its staff.</td></tr>
<tr><th>Business clients</th><td>Contact details, orders and messages.</td><td>To take and deliver orders.</td></tr>
</table>
<p>The app does not show advertising and does not sell or share personal data for marketing.</p>
<h2>Who else handles the data</h2><p>Only service providers that the app needs in order to work, each under contract:</p>
<ul><li><b>Render</b> — hosts the app and its database.</li><li><b>Meta (WhatsApp) through Kapso</b> — sends and receives WhatsApp messages.</li><li><b>Anthropic (Claude)</b> — reads documents and photos that managers upload (for example a staff sheet) and writes Tamil versions of names.</li></ul>
<p>These providers may process data outside India, including in the United Kingdom, the European Union and the United States.</p>
<h2>How long it is kept</h2><p>Personal data is kept while you work with Nobel Export Company and afterwards only for as long as it is needed for pay, tax and employment records under Indian law. Gate photos of visitors are kept only as long as they are needed for security.</p>
<h2>Your rights</h2><p>Under India's Digital Personal Data Protection Act, 2023 you can ask for a summary of your data, ask for it to be corrected or erased, nominate someone to act for you, and raise a grievance. Ask the factory office, or email <a href="mailto:nobel151013@gmail.com">nobel151013@gmail.com</a> or <a href="mailto:{P['support']}">{P['support']}</a>. To delete your account, see <a href="delete-account.html">delete my account</a>.</p>
<h2>Children</h2><p>The app is for adults only. It is not used by anyone under 18.</p>
<h2>Security</h2><p>Each person sees only what their role allows. Passwords and PINs are stored scrambled (hashed), all connections are encrypted (HTTPS), and the factory owner approves important changes.</p>'''


def delete_pending(a):
    return f'''<div class="note"><b>{e(a['name'])} is not yet on the App Store or Google Play.</b> When it is, you will be able to delete your account inside the app, or by emailing us as below.</div>
<p>Email <a href="mailto:{P['support']}?subject=Delete%20my%20{e(a['name'])}%20account">{P['support']}</a> with the subject “Delete my {e(a['name'])} account”, from the email address or phone number on your account.</p>'''


def delete_nobel(a):
    return f'''<p class="lead">Nobel Export Factory accounts belong to Nobel Export Company's staff and invited clients.</p>
<h2>How to ask</h2><ol><li>Tell the factory office (the General Manager), <b>or</b></li>
<li>Email <a href="mailto:{P['support']}?subject=Delete%20my%20Nobel%20Export%20Factory%20account">{P['support']}</a> with the subject “Delete my Nobel Export Factory account”, giving your name and the phone number on your account.</li></ol>
<p>We confirm who you are before deleting anything, and we reply within 30 days.</p>
<h2>What is deleted</h2><ul><li>Your login and PIN or password</li><li>Your face template, voice sample and photos</li><li>Your phone number and WhatsApp messages</li></ul>
<h2>What is kept, and for how long</h2><p>Attendance, salary, advance and payslip records are kept by Nobel Export Company for as long as Indian wage, tax and employment law requires, and are then deleted.</p>'''


PRIVACY = {'pending': privacy_pending, 'nobel': privacy_nobel}
DELETE = {'pending': delete_pending, 'nobel': delete_nobel}

# ---------------- apps pages ----------------
rows = ''.join(f'''<div class="card app"><div class="ai" style="background:{a['colour']}">{e(a['icon'])}</div><div style="flex:1"><h3 style="margin-bottom:2px">{e(a['name'])}</h3><span class="badge">{e(a['status'])}</span>
<p style="color:var(--muted);margin:10px 0">{e(a['summary'])}</p><p style="margin:0;font-size:15px"><a href="{a['id']}/">Support</a> · <a href="{a['id']}/privacy.html">Privacy policy</a> · <a href="{a['id']}/delete-account.html">Delete my account</a></p></div></div>''' for a in D['apps'])
w('apps/index.html', page('Apps & support — BVBAGRI', f'''<div class="page"><div class="wrap" style="max-width:960px"><span class="eyebrow">Apps</span><h1 style="font-size:44px">Our apps &amp; support</h1>
<p class="lead">Every app published by {e(P['name'])} on the App Store and Google Play. For help with any of them, email <a href="mailto:{P['support']}">{P['support']}</a>.</p>
<div class="grid" style="margin-top:28px">{rows}</div></div></div>''', 'Apps published by BVBAGRI FOODS CORPORATION LIMITED, with support, privacy and account deletion.', 1, 'apps'))

for a in D['apps']:
    sub = lambda t: f'<p style="font-size:14px"><a href="../">← All apps</a> · <a href="./">{e(a["name"])}</a></p>'
    about = f'''<div class="page"><div class="wrap">{sub('')}<div class="app" style="margin:10px 0 20px"><div class="ai" style="background:{a['colour']};width:76px;height:76px;font-size:36px">{e(a['icon'])}</div><div><h1 style="font-size:42px;margin:0">{e(a['name'])}</h1><span class="badge">{e(a['status'])}</span></div></div>
<p class="lead">{e(a['summary'])}</p><table><tr><th>Who it is for</th><td>{e(a['for'])}</td></tr><tr><th>Published by</th><td>{e(P['name'])}, United Kingdom</td></tr><tr><th>Support</th><td><a href="mailto:{P['support']}?subject={e(a['name'])}%20support">{P['support']}</a> — we reply within 2 working days</td></tr></table>
<p><a class="btn dark" href="privacy.html">Privacy policy</a> &nbsp; <a class="btn dark" href="delete-account.html" style="background:#7a2d1e">Delete my account</a></p></div></div>'''
    w(f'apps/{a["id"]}/index.html', page(f'{a["name"]} — support', about, a['summary'], 2, 'apps'))
    w(f'apps/{a["id"]}/privacy.html', page(f'{a["name"]} — privacy policy', f'''<div class="page"><div class="wrap">{sub('')}<span class="eyebrow">Privacy policy</span><h1 style="font-size:40px">{e(a['name'])}</h1><p class="muted">Last updated {UPDATED}</p>{PRIVACY[a['privacy']](a)}</div></div>''', f'Privacy policy for the {a["name"]} app.', 2, 'apps'))
    w(f'apps/{a["id"]}/delete-account.html', page(f'{a["name"]} — delete my account', f'''<div class="page"><div class="wrap">{sub('')}<span class="eyebrow">Account deletion</span><h1 style="font-size:40px">Delete my {e(a['name'])} account</h1>{DELETE[a['privacy']](a)}</div></div>''', f'How to delete your {a["name"]} account.', 2, 'apps'))

w('404.html', page('Page not found — BVBAGRI', '<div class="page"><div class="wrap"><h1 style="font-size:44px">Page not found</h1><p class="lead">That page does not exist. <a href="/">Go to the home page</a>.</p></div></div>', 'Page not found', 0))
print('built', len(D['apps']), 'apps')
