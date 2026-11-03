from pathlib import Path
import re
p=Path('/mnt/data/fixwork/index.html')
s=p.read_text()
# filenames -> appropriate existing visual asset; avoid clinical consultation images as therapy photos
img={
'abhyanga':'therapy-photo-01.jpg','acupressure':'therapy-photo-08.jpg','akshitarpan':'therapy-photo-02.jpg','ark-swedana':'therapy-photo-03.jpg','basti':'therapy-photo-04.jpg',
'castor-oil-wrap':'therapy-photo-11.jpg','cupping-therapy':'therapy-photo-07.jpg','dip-diet':'health-photo-10.jpg','hdt-head-down-tilt':'therapy-photo-12.jpg','hot-water-immersion':'therapy-photo-09.jpg',
'hridaya-basti':'therapy-photo-10.jpg','janu-basti':'therapy-photo-08.jpg','kashayadhara-pinda':'therapy-photo-16.jpg','kati-basti':'therapy-photo-10.jpg','leech-therapy':'leech-therapy.svg','lepan':'therapy-photo-06.jpg',
'lower-leg-hot-water-immersion':'therapy-photo-09.jpg','mud-therapy':'therapy-photo-06.jpg','nabhi-basti':'therapy-photo-11.jpg','nasya':'therapy-photo-05.jpg','naturopathy':'health-photo-16.jpg','neem-kerala-therapy':'therapy-photo-01.jpg',
'panchakarma':'therapy-photo-13.jpg','potali':'therapy-photo-16.jpg','raktmokshana':'therapy-photo-06.jpg','shashtishali-pinda-swedana':'therapy-photo-16.jpg','swedana-nadi-swedana':'therapy-photo-03.jpg','takradhara':'therapy-photo-02.jpg','udwartan':'therapy-photo-01.jpg','vamana':'therapy-photo-04.jpg','yoga':'therapy-photo-14.jpg','zero-volt-therapy':'health-photo-12.jpg'}
# Create a distinct accurate illustrative asset for leech therapy rather than a mismatched doctor consultation photo.
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 620"><defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#203b2f"/><stop offset="1" stop-color="#10241c"/></linearGradient></defs><rect width="840" height="620" fill="url(#bg)"/><rect x="55" y="95" width="730" height="430" rx="34" fill="#d6b18b" stroke="#f0d5b4" stroke-width="8"/><path d="M90 315 Q230 265 360 315 T750 315" fill="none" stroke="#b88968" stroke-width="24" opacity=".55"/><g fill="#29372c" stroke="#17251c" stroke-width="8" stroke-linecap="round"><path d="M250 205 C280 150 345 155 360 215 C375 270 330 330 290 355 C255 380 220 345 240 315 C260 285 275 260 250 205Z"/><path d="M470 250 C500 195 565 200 580 260 C595 315 550 375 510 400 C475 425 440 390 460 360 C480 330 495 305 470 250Z"/></g><g fill="#d9c4a3"><circle cx="276" cy="210" r="9"/><circle cx="496" cy="255" r="9"/></g><text x="420" y="570" text-anchor="middle" font-family="Arial,sans-serif" font-size="28" fill="#e9d6b6" letter-spacing="5">LEECH THERAPY</text></svg>'''
(p.parent/'images/page-images/leech-therapy.svg').write_text(svg)
# extract card article blocks
start=s.index('<section class="section therapy-directory"')
end=s.index('</section>', start)+len('</section>')
section=s[start:end]
# categorize by enclosing accordion in order and renumber sequentially
# Replace per article based on href slug
counter=0
for m in list(re.finditer(r'<article class="directory-card visual-directory-card reveal">.*?</article>',section,re.S))[::-1]:
    block=m.group(0)
    hm=re.search(r'href="/therapies/([^./]+)\.html"',block)
    if not hm: continue
    slug=hm.group(1)
    counter+=1
    if slug in img:
        block=re.sub(r'<img src="/images/page-images/[^\"]+" alt="[^\"]*"',f'<img src="/images/page-images/{img[slug]}" alt="{slug.replace("-"," ").title()}: therapy procedure image"',block,count=1)
    block=re.sub(r'<div class="directory-card-top"><span>\d+</span>',f'<div class="directory-card-top"><span>{counter:02d}</span>',block,count=1)
    # normalize selected visible names/title spellings and case
    names={
      'akshitarpan':'Akshitarpan','ark-swedana':'Ark Swedana','leech-therapy':'Leech Therapy','kashayadhara-pinda':'Kashayadhara Pinda','swedana-nadi-swedana':'Swedana / Nadi Swedana','dip-diet':'DIP Diet','hdt-head-down-tilt':'HDT (Head Down Tilt)','neem-kerala-therapy':'Neem Kerala Therapy','raktmokshana':'Raktmokshana','shashtishali-pinda-swedana':'Shashtishali Pinda Swedana','zero-volt-therapy':'Zero Volt Therapy','lower-leg-hot-water-immersion':'Lower-leg hot water immersion','hot-water-immersion':'Hot water immersion','castor-oil-wrap':'Castor oil wrap','cupping-therapy':'Cupping Therapy','yoga':'Yoga'}
    name=names.get(slug,slug.replace('-',' ').title())
    block=re.sub(r'(<h3><a href="/therapies/[^\"]+">).*?(</a></h3>)',lambda x:x.group(1)+name+x.group(2),block,count=1,flags=re.S)
    block=re.sub(r'aria-label="Read about [^"]+"',f'aria-label="Read about {name}"',block,count=1)
    # substitute block at original location
    section=section[:m.start()]+block+section[m.end():]
# update counts and overall total
section=section.replace('31 therapies','31 therapies')
# set category count labels according to actual known counts
section=section.replace('<small>19 therapies</small>','<small>19 therapies</small>')
section=section.replace('<small>8 therapies</small>','<small>8 therapies</small>')
s=s[:start]+section+s[end:]
p.write_text(s)
print('patched cards',counter)
