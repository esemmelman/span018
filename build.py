"""Generate the buildless study sheet from spa017's verb bank."""
from pathlib import Path
import re
import html

source = Path('../span017/index.html').read_text(encoding='utf-8')
bank = re.search(r'<div class="verb-bank"[^>]*>(.*?)</div>', source).group(1)
verbs = re.findall(r'<span>(.*?)</span>', bank)
meanings = ['to travel', 'to bathe', 'to wake up', 'to drink', 'to speak', 'to live', 'to sell', 'to study', 'to eat', 'to watch', 'to take off', 'to write', 'to spend', 'to run', 'to sing']
subjects = ['yo', 'tú', 'él / ella / usted', 'nosotros / nosotras', 'vosotros / vosotras', 'ellos / ellas / ustedes']
pronouns = ['me', 'te', 'se', 'nos', 'os', 'se']
present = {'ar': ['o','as','a','amos','áis','an'], 'er': ['o','es','e','emos','éis','en'], 'ir': ['o','es','e','imos','ís','en']}
past = {'ar': ['é','aste','ó','amos','asteis','aron'], 'er': ['í','iste','ió','imos','isteis','ieron'], 'ir': ['í','iste','ió','imos','isteis','ieron']}
cards = []
for number, (verb, meaning) in enumerate(zip(verbs, meanings), 1):
    reflexive = verb.endswith('se')
    base = verb[:-2] if reflexive else verb
    stem, ending = base[:-2], base[-2:]
    columns = []
    for tense, endings in [('Present', present), ('Preterite', past)]:
        rows = []
        for i, subject in enumerate(subjects):
            root = 'despiert' if verb == 'despertarse' and tense == 'Present' and i not in (3,4) else stem
            form = root + endings[ending][i]
            if reflexive:
                form = pronouns[i] + ' ' + form
            rows.append(f'<li><span class="subject">{subject}</span><strong>{form}</strong></li>')
        columns.append(f'<section class="tense {tense.lower()}" aria-label="{verb}: {tense}"><h3>{tense}<small>{"Presente" if tense == "Present" else "Pretérito"}</small></h3><ul lang="es">{"".join(rows)}</ul></section>')
    note = '<p class="note">Present: e → ie, except nosotros and vosotros. Preterite: no stem change.</p>' if verb == 'despertarse' else ''
    cards.append(f'<article class="verb" data-search="{verb} {meaning}"><header><span class="number">{number:02}</span><div><h2 lang="es">{verb}</h2><p>{meaning}</p></div></header><div class="columns">{"".join(columns)}</div>{note}</article>')

page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>span018 · Present &amp; Preterite</title><meta name="description" content="All 15 infinitives from spa017, with present and preterite conjugations side by side.">
<style>
:root{font-family:system-ui,-apple-system,sans-serif;color:#182c42;background:#f3f6fa}*{box-sizing:border-box}body{margin:0}main{max-width:1000px;margin:auto;padding:42px 20px}h1{font-size:clamp(32px,5vw,52px);letter-spacing:-.035em;line-height:1.12;margin:12px 0 16px}.eyebrow{font-size:14px;text-transform:uppercase;letter-spacing:.15em;font-weight:750;color:#42657f}.intro{font-size:20px;line-height:1.6;color:#516478;max-width:720px}.tools{display:flex;gap:16px;align-items:end;flex-wrap:wrap;margin:28px 0}label{flex:1;min-width:200px;font-weight:650}input{display:block;width:100%;margin-top:8px;padding:14px;border:1px solid #afc1d0;border-radius:10px;font:inherit;background:white}button{font:inherit;padding:14px 20px;border:1px solid #183e59;border-radius:10px;background:#183e59;color:white;cursor:pointer}input:focus-visible,button:focus-visible,a:focus-visible{outline:3px solid #df9722;outline-offset:3px}#count{color:#516478}.verb{background:white;border:1px solid #d9e3ec;border-radius:18px;margin:22px 0;overflow:hidden;box-shadow:0 5px 18px #182c4206}.verb>header{display:flex;gap:18px;align-items:center;padding:24px 28px;border-bottom:1px solid #e5ebf1}.number{color:#54718a;background:#edf3f8;border-radius:10px;padding:10px;font-size:16px;font-weight:700}h2{font-size:34px;margin:0;line-height:1.2}.verb header p{margin:6px 0 0;color:#516478;font-size:18px}.columns{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.tense{padding:22px 28px}.present{border-right:1px solid #e5ebf1}.preterite{background:#faf7f1}h3{font-size:24px;color:#1d6375;margin:0 0 18px}.preterite h3{color:#986026}h3 small{display:block;font-size:14px;font-weight:500;margin-top:4px}ul{list-style:none;padding:0;margin:0}li{padding:10px 0;border-bottom:1px solid #e7ebef}li:last-child{border:0}.subject{display:block;font-size:14px;color:#586b7d;margin-bottom:4px}strong{font-size:clamp(20px,3vw,28px);font-weight:650}.note{padding:16px 28px;margin:0;background:#edf6f9;color:#24536a;line-height:1.5}footer{margin-top:30px;color:#516478;font-size:15px;line-height:1.7}a{color:#245d83}[hidden]{display:none!important}@media(max-width:500px){main{padding:25px 12px}.tense{padding:18px 12px}.verb>header{padding:20px 16px;gap:12px}h3{font-size:21px}.subject{font-size:12px}h2{font-size:30px}.note{padding:14px 16px}}@media print{body{background:white}main{padding:0}.tools,#count{display:none}.verb{break-inside:avoid;box-shadow:none;margin:14px 0}h1{font-size:30px}.intro{font-size:14px}.tense{padding:12px 20px}li{padding:5px 0}strong{font-size:20px}footer{font-size:12px}}
</style></head><body><main>
<header><div class="eyebrow">span018 · Spanish study sheet</div><h1>Present &amp; Preterite</h1><p class="intro">The 15 infinitives from spa017. Compare each verb’s present tense with its completed past tense, side by side.</p></header>
<div class="tools"><label for="search">Find a verb<input id="search" type="search" placeholder="Search Spanish or English…" autocomplete="off"></label><button id="print" type="button">Print study sheet</button></div>
<p id="count" role="status">15 verbs</p><div id="verbs">CARDS</div><p id="empty" hidden>No matching verbs. Try another search.</p>
<footer>Includes vosotros / vosotras (used in Spain) and ustedes. Reflexive pronouns are included.<br>Verb bank: <a href="https://esemmelman.github.io/spa017/">spa017</a> · <a href="https://www.spanishdict.com/conjugate/despertarse">Despertarse conjugation reference</a> · Works offline.</footer>
<script>
const cards = [...document.querySelectorAll('.verb')];
const normalize = value => value.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase().trim();
document.querySelector('#search').addEventListener('input', event => {
 const query = normalize(event.target.value);
 let count = 0;
 cards.forEach(card => {card.hidden = !normalize(card.dataset.search).includes(query); if (!card.hidden) count++;});
 document.querySelector('#count').textContent = count + (count === 1 ? ' verb' : ' verbs');
 document.querySelector('#empty').hidden = count !== 0;
});
document.querySelector('#print').addEventListener('click', () => window.print());
</script></main></body></html>'''
assert len(verbs) == 15 and len(cards) == 15
Path('index.html').write_text(page.replace('CARDS', ''.join(cards)), encoding='utf-8')
print('Generated 15 verb cards with 180 conjugations.')
