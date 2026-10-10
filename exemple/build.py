#!/usr/bin/env python3
"""Vidéo « Combien ça m'a coûté » (version complète).
Usage depuis un dossier de travail : python3 build.py mots.json
Produit proj/storyboard.json et proj/index.html. Les événements sont indexés sur les mots."""
import json, sys, html

W = json.load(open(sys.argv[1]))
import os
CEN = json.load(open("center.json")) if os.path.exists("center.json") else {}
LEAD = 0.08
def t(i): return round(max(0, W[i]["start"] - LEAD), 2)
END = round(W[-1]["end"] + 0.8, 2)          # fin : dernier mot + 0,8 s

LOGO_MISS = '<span class="lg miss" style="width:34px;height:34px">LOGO<br>REQUIS</span>'
def logo(name, size=24):
    return f'<span class="lg real" style="width:{size}px;height:{size}px"><img src="logos/{name}.svg" alt="{name}"></span>'
FLAG = ('<svg viewBox="0 0 30 20" style="width:30px;height:20px;border:2px solid var(--ink);border-radius:4px;flex:none">'
        '<rect width="30" height="10" fill="#EF2B2D"/><rect y="10" width="30" height="10" fill="#009E49"/>'
        '<path d="M15 6.2l1.1 3.3h3.4l-2.8 2 1.1 3.3-2.8-2-2.8 2 1.1-3.3-2.8-2h3.4z" fill="#FCD116"/></svg>')

# ---------- scènes : (id, mot de début, composant, html, événements) ----------
# événement : (élément, index du mot, options)  — options : accent, pose, logo, text, typing, to (déplacement), show_only
S = []

S.append(("s1", 0, "PunchTitle", """
<div class="t" id="s1-l1" style="top:150px">Combien ça m'a</div>
<div class="t" id="s1-l2" style="top:192px;font-size:52px"><em>coûté</em> ?</div>
""", [("s1-l1", 0, {}), ("sticker", 0, {"pose": "money", "until": 6}), ("s1-l2", 3, {"accent": True})]))

S.append(("s2", 6, "PhoneScreen", f"""
<div class="cap" id="s2-c1" style="top:60px">une appli de <em>transfert</em></div>
<div class="cap" id="s2-c2" style="top:60px">des <em>milliers</em> de transactions</div>
<div class="phone a" id="s2-phone" style="left:80px;top:122px;width:200px;height:390px">
 <div class="scr" style="padding:34px 14px 14px;display:flex;flex-direction:column;gap:14px">
  <div class="row" style="gap:8px;padding-bottom:12px;border-bottom:2px solid var(--ink)"><b style="flex:1;font:900 15px var(--fd)">NANAPAY</b><span id="s2-bf">{FLAG}</span></div>
  <div style="display:flex;flex-direction:column;gap:6px"><span style="font:700 9px var(--fb);letter-spacing:.4px;color:var(--soft)">ENVOYER</span>
   <b style="font:900 28px/1 var(--fd);letter-spacing:-.6px">25 000 F</b></div>
  <div style="display:flex;flex-direction:column;gap:6px"><span style="font:700 9px var(--fb);letter-spacing:.4px;color:var(--soft)">À</span>
   <div class="row" style="height:36px;gap:10px;padding:0 10px;border:2px solid var(--ink);border-radius:calc(var(--rs) * .7)">
    <span class="av" style="width:22px;height:22px"></span><span style="flex:1;display:flex;flex-direction:column;gap:5px"><span class="ln k" style="width:70%"></span><span class="ln" style="width:50%"></span></span></div></div>
  <div class="row" style="justify-content:space-between;font:800 11px var(--fb)"><span style="color:var(--soft)">FRAIS</span><b>0 F</b></div>
  <span class="btn" style="margin-top:auto;height:36px;font-size:14px">Envoyer</span>
  <div id="s2-list" style="position:absolute;inset:0;padding:34px 14px 14px;background:var(--tile);display:flex;flex-direction:column;gap:12px">
   <div class="row" style="padding-bottom:12px;border-bottom:2px solid var(--ink)"><b style="font:900 15px var(--fd)">REÇUS</b></div>
   <div class="row" id="s2-n1" style="height:36px;gap:10px;padding:0 12px;background:var(--tile);border:2.5px solid var(--ink);border-radius:var(--rs);box-shadow:var(--shadow-small);font:800 13px var(--fb)"><span class="bd" style="background:var(--yes)">✓</span>+15 000 F</div><div class="row" id="s2-n2" style="height:36px;gap:10px;padding:0 12px;background:var(--tile);border:2.5px solid var(--ink);border-radius:var(--rs);box-shadow:var(--shadow-small);font:800 13px var(--fb)"><span class="bd" style="background:var(--yes)">✓</span>+5 000 F</div><div class="row" id="s2-n3" style="height:36px;gap:10px;padding:0 12px;background:var(--tile);border:2.5px solid var(--ink);border-radius:var(--rs);box-shadow:var(--shadow-small);font:800 13px var(--fb)"><span class="bd" style="background:var(--yes)">✓</span>+40 000 F</div>
   <span class="tg" id="s2-tx" style="position:static;margin-top:auto;align-self:center;height:28px;font-size:11px">1 000+ transactions</span>
  </div>
 </div>
</div>
""", [("s2-c1", 6, {}), ("s2-phone", 7, {}), ("s2-bf", 12, {}),
      ("s2-c2", 16, {}), ("s2-list", 17, {}), ("s2-n1", 17, {"delay": .1}), ("s2-n2", 17, {"delay": .35}), ("s2-n3", 17, {"delay": .6}),
      ("s2-tx", 19, {"accent": True})]))

S.append(("s3", 20, "CodeEditor", """
<div class="cap" id="s3-c1" style="top:126px">je suis <em>développeur</em></div>
<div class="bx a" id="s3-win" style="left:30px;top:188px;width:300px;height:150px;overflow:hidden">
 <div class="wbar"><span class="dots"><i></i><i></i><i></i></span>moi.dart</div>
 <div class="code" style="padding:16px 16px"><span id="s3-k">final metier =</span>
  <span class="s" id="s3-v" style="display:inline-block;white-space:pre">"développeur";</span></div>
</div>
""", [("s3-c1", 20, {}), ("s3-win", 20, {}), ("s3-v", 22, {"typing": '"développeur";'}),
      ("s3-v", 25, {"accent": True, "pulse": True})]))

# Frise : carte en colonne (padding 20, 16 entre rangées) ; 6 points répartis, trait d'un centre à l'autre
nodes = "".join(f'<span id="s4-d{k}" style="position:absolute;left:calc({k} * (100% - 20px) / 5);top:0;width:20px;height:20px;border-radius:50%;'
                f'border:2.5px solid var(--ink);background:{"var(--acc)" if k==0 else "var(--tile)"}"></span>' for k in range(6))
S.append(("s4", 26, "Timeline", f"""
<div class="cap" id="s4-c1" style="top:124px">il y a <em>5 mois</em></div>
<div class="bx a" id="s4-card" style="left:30px;top:186px;width:300px;padding:22px 20px 20px;display:flex;flex-direction:column;gap:16px">
 <div style="position:relative;height:20px"><span style="position:absolute;left:10px;right:10px;top:8px;height:4px;background:var(--ink);border-radius:2px"></span>{nodes}</div>
 <div class="row" style="justify-content:space-between">
  <span class="tg" id="s4-l0" style="position:static;height:26px;padding:0 12px;font-size:11px">Lancement</span>
  <span class="tg w" id="s4-l5" style="position:static;height:26px;padding:0 12px;font-size:11px">Aujourd'hui</span></div>
 <div class="row" id="s4-app" style="gap:8px;font:900 11px var(--fd);text-transform:uppercase">{FLAG}transfert d'argent</div>
</div>
""", [("s4-c1", 26, {}), ("s4-card", 26, {})] + [(f"s4-d{k}", 29, {"delay": .12*k}) for k in range(6)]
     + [("s4-l0", 32, {"accent": True}), ("s4-app", 35, {}), ("s4-l5", 41, {})]))

S.append(("s5", 42, "Sticker", """
<div class="cap" id="s5-c1" style="top:126px">Moi c'est <em>Abdoul</em></div>
<div class="cap" id="s5-c2" style="top:126px">vivre de <em>mes apps</em></div>
<div class="big" id="s5-big" style="top:176px">+1 an</div>
""", [("s5-c1", 42, {}), ("sticker", 42, {"pose": "wave", "until": 57}), ("s5-big", 49, {"accent": True}),
      ("s5-c2", 53, {})]))

# Reçu : colonne flex, pas régulier (padding 14, 14 entre groupes, 6 entre libellé et ligne) ; la carte épouse son contenu
RB = 'display:flex;flex-direction:column;gap:14px;padding:14px'
def brand(bid=""):
    i = f' id="{bid}"' if bid else ""
    return (f'<div class="row"{i} style="gap:10px;padding-bottom:14px;border-bottom:2px solid var(--ink)">'
            f'<b style="font:900 16px var(--fd)">NANAPAY</b></div>')
def group(gid, label, rid, lg, name, aid, amount=""):
    gi = f' id="{gid}"' if gid else ""
    return (f'<div{gi} style="display:flex;flex-direction:column;gap:6px">'
            f'<span style="font:700 9px var(--fb);letter-spacing:.4px;color:var(--soft)">{label}</span>'
            f'<div class="row" id="{rid}" style="height:36px;gap:10px;padding:0 10px;border:2px solid var(--ink);border-radius:calc(var(--rs) * .7)">'
            f'{logo(lg)}<b style="flex:1;font:900 12px var(--fd);text-transform:uppercase">{name}</b>'
            f'<span id="{aid}" style="font:900 14px var(--fd)">{amount}</span></div></div>')
def total(tid="", on=True):
    i = f' id="{tid}"' if tid else ""
    st = "background:var(--acc);color:var(--on-acc);" if on else "background:var(--tile);"
    return (f'<div class="row"{i} style="height:36px;padding:0 12px;gap:8px;{st}border:2.5px solid var(--ink);border-radius:var(--rs)">'
            f'<b style="flex:1;font:900 13px var(--fd)">TOTAL</b><b style="font:900 16px var(--fd)">? $</b></div>')

S.append(("s7", 60, "Receipt", f"""
<div class="cap" id="s7-c1" style="top:112px">ce que ça a <em>coûté</em></div>
<div class="bx a" id="s7-card" style="left:30px;top:172px;width:300px;overflow:hidden">
 <div class="wbar"><span class="dots"><i></i><i></i><i></i></span>Coût du lancement</div>
 <div style="{RB}">{brand("s7-brand")}{group("s7-g1", "DÉVELOPPEMENT", "s7-r1", "claude", "Claude Code", "s7-a1")}{total("s7-tot")}</div>
</div>
""", [("s7-c1", 61, {}), ("s7-card", 61, {}), ("s7-brand", 64, {}), ("s7-tot", 67, {"accent": True}),
      ("s7-g1", 73, {}), ("s7-a1", 78, {"text": "…"}), ("s7-a1", 81, {"text": "20 $ × 2"})]))

S.append(("s8", 87, "BigNumber", """
<div class="cap" id="s8-c1" style="top:126px">ça revient à</div>
<div class="big" id="s8-big" style="top:170px">40 $</div>
<div class="cap" id="s8-c2" style="top:240px"><em>20 $</em> par mois</div>
""", [("s8-c1", 87, {}), ("s8-big", 87, {"accent": True}), ("sticker", 87, {"pose": "star_eyes", "until": 93}),
      ("s8-c2", 90, {})]))

S.append(("s9", 93, "Receipt", f"""
<div class="cap" id="s9-c1" style="top:112px">pour <em>publier</em> l'app</div>
<div class="bx a" style="left:30px;top:172px;width:300px;overflow:hidden">
 <div class="wbar"><span class="dots"><i></i><i></i><i></i></span>Coût du lancement</div>
 <div style="{RB}">{brand()}{group("", "DÉVELOPPEMENT", "s9-r1", "claude", "Claude Code", "s9-a1", "40 $")}{group("s9-g2", "PUBLICATION", "s9-r2", "appstore", "App Store", "s9-a2")}<div class="row" id="s9-r3" style="height:36px;gap:10px;padding:0 10px;margin-top:-6px;border:2px solid var(--ink);border-radius:calc(var(--rs) * .7)">{logo("googleplay")}<b style="flex:1;font:900 12px var(--fd);text-transform:uppercase">Play Store</b><span id="s9-a3" style="font:900 14px var(--fd)"></span></div>{total(on=False)}</div>
</div>
""", [("s9-c1", 94, {}), ("s9-g2", 100, {}), ("s9-a2", 104, {"text": "99 $ / an"}), ("s9-r3", 111, {}), ("s9-a3", 115, {"text": "25 $ unique", "accent": True})]))


S.append(("s10", 119, "BigNumber", """
<div class="cap" id="s10-c1" style="top:126px">dit comme ça</div>
<div class="big" id="s10-big" style="top:166px">164 $</div>
<div class="cap" id="s10-c2" style="top:248px">c'est <em>pas cher</em></div>
""", [("s10-c1", 119, {}), ("s10-big", 120, {"accent": True}), ("sticker", 119, {"pose": "thumbs_up", "until": 125}), ("s10-c2", 122, {})]))

S.append(("s11", 125, "PunchTitle", """
<div class="t" id="s11-l1" style="top:270px">Mais ce n'est</div>
<div class="t" id="s11-l2" style="top:308px;font-size:52px">pas <em>tout</em></div>
""", [("s11-l1", 127, {}), ("s11-l2", 128, {"accent": True})]))

S.append(("s12", 130, "CalcCards", """
<div class="cap" id="s12-c1" style="top:150px">pour qu'une app <em>réussisse</em></div>
<div class="bx a" id="s12-k1" style="left:30px;top:212px;width:300px;height:52px;display:flex;align-items:center;gap:12px;padding:0 16px"><span class="ck" style="background:var(--yes)">✓</span><b style="font:900 17px var(--fd)">LE CODE</b></div>
<div class="bx a" id="s12-k2" style="left:30px;top:276px;width:300px;height:52px;display:flex;align-items:center;gap:12px;padding:0 16px"><b style="font:900 22px var(--fd);width:22px;text-align:center">+</b><b style="font:900 17px var(--fd)">LE MARKETING</b></div>
<div class="bx on a" id="s12-k3" style="left:30px;top:340px;width:300px;height:52px;display:flex;align-items:center;gap:12px;padding:0 16px"><b style="font:900 22px var(--fd);width:22px;text-align:center">=</b><b style="font:900 17px var(--fd)">UNE APP QUI MARCHE</b></div>
""", [("s12-c1", 130, {}), ("s12-k1", 132, {}), ("s12-k2", 138, {}), ("s12-k3", 138, {"accent": True, "delay": .6})]))

S.append(("s13", 139, "PunchTitle", """
<div class="t" id="s13-l1" style="top:150px">Pas de</div>
<div class="t" id="s13-l2" style="top:188px;font-size:52px"><em>négociation</em></div>
""", [("s13-l1", 145, {}), ("sticker", 142, {"pose": "arms_crossed", "until": 148}), ("s13-l2", 147, {"accent": True})]))

S.append(("s14", 148, "GoalProgress", """
<div class="cap" id="s14-c1" style="top:170px">tu mises <em>tout</em></div>
<div class="bx a" id="s14-card" style="left:30px;top:232px;width:300px;padding:16px;display:flex;flex-direction:column;gap:14px">
 <b class="u" style="font:900 15px var(--fd)">Ton budget</b>
 <div class="pg" style="height:28px"><i id="s14-bar" style="width:100%"></i></div>
 <div class="row" style="justify-content:space-between"><span style="font:700 11px var(--fb);color:var(--soft)">0 %</span><span class="tg" id="s14-tag" style="position:static;height:28px;font-size:12px">100 % marketing</span></div>
</div>
""", [("s14-c1", 148, {}), ("s14-card", 149, {}), ("s14-bar", 150, {"grow": "100%"}), ("s14-tag", 158, {"accent": True})]))

S.append(("s15", 159, "BarChart", f"""
<div class="cap" id="s15-c1" style="top:120px">avec <em>NanaPay</em></div>
<div class="cap" id="s15-c2" style="top:120px">tout marche <em>bien</em></div>
<div class="bx a" id="s15-card" style="left:30px;top:182px;width:300px;overflow:hidden">
 <div class="wbar"><span class="dots"><i></i><i></i><i></i></span>NanaPay · transactions</div>
 <div style="padding:16px;display:flex;flex-direction:column;gap:12px">
  <div style="display:flex;gap:10px;align-items:flex-end;border-bottom:2.5px solid var(--ink)"><div style="flex:1;height:150px;display:flex;align-items:flex-end"><span id="s15-b0" style="display:block;width:100%;height:22%;background:var(--tile);border:2.5px solid var(--ink);border-radius:6px 6px 0 0"></span></div><div style="flex:1;height:150px;display:flex;align-items:flex-end"><span id="s15-b1" style="display:block;width:100%;height:34%;background:var(--tile);border:2.5px solid var(--ink);border-radius:6px 6px 0 0"></span></div><div style="flex:1;height:150px;display:flex;align-items:flex-end"><span id="s15-b2" style="display:block;width:100%;height:48%;background:var(--tile);border:2.5px solid var(--ink);border-radius:6px 6px 0 0"></span></div><div style="flex:1;height:150px;display:flex;align-items:flex-end"><span id="s15-b3" style="display:block;width:100%;height:66%;background:var(--tile);border:2.5px solid var(--ink);border-radius:6px 6px 0 0"></span></div><div style="flex:1;height:150px;display:flex;align-items:flex-end"><span id="s15-b4" style="display:block;width:100%;height:92%;background:var(--acc);border:2.5px solid var(--ink);border-radius:6px 6px 0 0"></span></div></div>
  <div class="row" style="justify-content:space-between;font:700 10px var(--fb);color:var(--soft)"><span>MOIS 1</span><span>MOIS 5</span></div>
 </div>
</div>
""", [("s15-c1", 160, {}), ("s15-card", 160, {})] + [(f"s15-b{i}", 166, {"growh": h, "delay": .18*i}) for i, h in enumerate(["22%","34%","48%","66%","92%"])]
     + [("s15-c2", 170, {})]))

S.append(("s16", 173, "BigNumber", """
<div class="cap" id="s16-c1" style="top:126px">on fait</div>
<div class="big" id="s16-big" style="top:166px">1 000+</div>
<div class="cap" id="s16-c2" style="top:248px"><em>transactions</em></div>
""", [("s16-c1", 173, {}), ("s16-big", 176, {"accent": True}), ("sticker", 175, {"pose": "chart_up", "until": 179}), ("s16-c2", 178, {})]))

S.append(("s17", 179, "Versus", """
<div class="cap" id="s17-c1" style="top:130px">retiens bien</div>
<div class="cap" id="s17-c2" style="top:130px">ce qui change <em>tout</em></div>
<div class="bx a" id="s17-l" style="left:30px;top:192px;width:144px;height:190px;padding:16px 12px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;text-align:center">
 <b style="font:900 15px/1.1 var(--fd)">CRÉER<br>UNE APP</b><span class="tg w" id="s17-cheap" style="position:static;height:28px;font-size:11px">Pas cher</span><span class="tg k" id="s17-y" style="position:static;height:22px;font-size:10px">en 2026</span></div>
<div class="bx on a" id="s17-r" style="left:186px;top:192px;width:144px;height:190px;padding:16px 12px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;text-align:center">
 <b id="s17-m" style="font:900 15px/1.1 var(--fd)">LE<br>MARKETING</b><b style="font:900 18px var(--fd)" id="s17-plus">+</b><b id="s17-d" style="font:900 15px/1.1 var(--fd)">LA<br>DISTRIBUTION</b></div>
""", [("s17-c1", 180, {}), ("s17-l", 181, {}), ("s17-cheap", 186, {}), ("s17-y", 192, {}), ("s17-c2", 196, {}),
      ("s17-l", 196, {"slide": 78}), ("s17-r", 196, {"accent": True, "delay": .2}), ("s17-m", 200, {}), ("s17-plus", 202, {}), ("s17-d", 203, {})]))

S.append(("s18", 204, "PhoneScreen", """
<div class="cap" id="s18-c1" style="top:60px"><em>personne</em> ne l'utilise</div>
<div class="phone a" id="s18-phone" style="left:80px;top:122px;width:200px;height:390px">
 <div class="scr" style="padding:34px 14px 14px;display:flex;flex-direction:column;gap:14px">
  <div class="row" style="gap:8px;padding-bottom:12px;border-bottom:2px solid var(--ink)"><b style="flex:1;font:900 15px var(--fd)">TON APP</b></div>
  <div style="display:flex;flex-direction:column;gap:6px"><span style="font:700 9px var(--fb);letter-spacing:.4px;color:var(--soft)">UTILISATEURS</span>
   <b id="s18-zero" style="font:900 56px/1 var(--fd);letter-spacing:-.05em;color:var(--acc)">0</b></div>
  <div style="display:flex;flex-direction:column;gap:8px"><span class="ln" style="width:85%"></span><span class="ln" style="width:60%"></span><span class="ln" style="width:72%"></span></div>
 </div>
</div>
""", [("s18-c1", 206, {}), ("s18-phone", 206, {}), ("s18-zero", 207, {"accent": True})]))

S.append(("s19", 210, "PunchTitle", """
<div class="t" id="s19-l1" style="top:250px">Temps perdu</div>
<div class="t" id="s19-l2" style="top:292px;font-size:52px"><em>argent</em> perdu</div>
""", [("s19-l1", 213, {}), ("s19-l2", 218, {"accent": True})]))

S.append(("s20", 219, "EndCard", """
<div class="a" id="s20-bg" style="left:0;top:0;width:360px;height:640px;background:var(--acc)"></div>
<div class="t" id="s20-l1" style="top:160px;font-size:26px;color:var(--on-acc)">d'autres conseils ?</div>
<div class="t" id="s20-l2" style="top:196px;font-size:52px;color:var(--on-acc)">Abonne-toi</div>
""", [("s20-l1", 223, {}), ("sticker", 220, {"pose": "hands_heart", "until": None}), ("s20-l2", 228, {"accent": True})]))

# ---------- storyboard + timeline ----------
starts = [t(s[1]) if k else 0.0 for k, s in enumerate(S)]
scenes, tweens, clips = [], [], []
captions_by_scene = {}
for k, (sid, w0, comp, body, evs) in enumerate(S):
    st, en = starts[k], (starts[k + 1] if k + 1 < len(S) else END)
    ev_out = []
    for el, wi, o in evs:
        tt = round(max(st, t(wi)) + o.get("delay", 0), 2)
        e = {"t": tt, "el": "sticker" if el == "sticker" else el.split("-", 1)[1], "word": W[wi]["word"]}
        if o.get("accent"): e["accent"] = True
        if "logo" in o: e["logo"] = o["logo"]
        if o.get("typing"): e["typing"] = True; e["text"] = o["typing"]
        if el == "sticker":
            e["pose"] = o["pose"]; e["until"] = round(en if o["until"] is None else min(en, t(o["until"])), 2)
            clips.append((o["pose"], tt, e["until"]))
        elif o.get("typing"):
            tweens.append(f'typ("#{el}",{len(o["typing"])},{tt});')
        elif o.get("text"):
            tweens.append(f'txt("#{el}",{json.dumps(o["text"])},{tt});')
        elif o.get("grow"):
            tweens.append(f'tl.fromTo("#{el}",{{width:"0%"}},{{width:"{o["grow"]}",duration:.9,ease:"power2.out"}},{tt});')
        elif o.get("growh"):
            tweens.append(f'tl.fromTo("#{el}",{{height:"0%"}},{{height:"{o["growh"]}",duration:.6,ease:"back.out(1.6)"}},{tt});')
        elif o.get("slide") is not None:
            tweens.append(f'tl.set("#{el}",{{x:{o["slide"]}}},0);tl.to("#{el}",{{x:0,duration:.45,ease:"power3.inOut"}},{tt});')
        elif o.get("pulse"):
            tweens.append(f'pulse("#{el}",{tt});')
        elif __import__("re").fullmatch(r"c\d+", el.split("-")[1]):           # sous-titres : un seul visible à la fois
            captions_by_scene.setdefault(sid, []).append((el, tt))
        else:
            tweens.append(f'pop("#{el}",{tt});')
        ev_out.append(e)
    ev_out.sort(key=lambda e: e["t"])
    scenes.append({"id": sid, "start": st, "end": en, "component": comp,
                   "say": " ".join(x["word"] for x in W[w0:(S[k + 1][1] if k + 1 < len(S) else len(W))]), "events": ev_out})
for sid, caps in captions_by_scene.items():
    for j, (el, tt) in enumerate(caps):
        tweens.append(f'pop("#{el}",{tt});')
        if j + 1 < len(caps): tweens.append(f'tl.set("#{el}",{{opacity:0}},{caps[j+1][1]});')
sfx = [st for (_, st, _) in clips] + [starts[0]]
sb = {"video": "combien-ca-coute-30s", "fps": 30, "duration": END, "audio": "voix.mp3", "scenes": scenes}
json.dump(sb, open("proj/storyboard.json", "w"), ensure_ascii=False, indent=1)

clip_html = "\n".join(
    f'<div id="{sid}" class="clip" data-start="{scenes[k]["start"]}" data-duration="{round(scenes[k]["end"]-scenes[k]["start"],2)}" data-track-index="1">'
    f'<div class="ad-scene is-full"><div class="ad-stage" data-cy="{190 if any(e[0]=="sticker" for e in evs) else 320}" style="transform:translate({CEN.get(sid,[0,0])[0]}px,{CEN.get(sid,[0,0])[1]}px)">{body}</div></div></div>' for k, (sid, w0, comp, body, evs) in enumerate(S))
stk_html = "\n".join(
    f'<img id="stk{i}" class="clip sticker edged" src="poses/{p}.webp" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="2" '
    f'style="left:150px;bottom:-30px;width:780px;height:auto;top:auto">' for i, (p, a, b) in enumerate(clips))
# sons : pilotés par sfx.config.json (enabled, sons, déclencheurs) — rien en dur
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts")); import sfx_eleven
_cfg = sfx_eleven.load("sfx.config.json") if os.path.exists("sfx.config.json") else {"enabled": False}
SFX = sfx_eleven.plan(_cfg, sb)
sfx_html = "\n".join(f'<audio id="sfx{i}" src="{p["file"]}" data-start="{p["t"]}" data-duration="1" data-track-index="{3+i}" data-volume="{p["volume"]}"></audio>'
                     for i, p in enumerate(SFX))

import re as _re
page_fix = lambda h: _re.sub(r'class="cap" id="([^"]+)" style="top:([\d.]+)px"', lambda m: f'class="cap" id="{m.group(1)}" style="top:auto;bottom:{640-float(m.group(2))-30:g}px"', h)
clip_html = page_fix(clip_html)
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=1080, height=1920">
<style>
@font-face{{font-family:Satoshi;src:url(fonts/Satoshi-Medium.woff2) format("woff2");font-weight:500}}
@font-face{{font-family:Satoshi;src:url(fonts/Satoshi-Bold.woff2) format("woff2");font-weight:600 700}}
@font-face{{font-family:Satoshi;src:url(fonts/Satoshi-Black.woff2) format("woff2");font-weight:800 900}}
</style>
<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="bundle.css">
<script src="gsap.min.js"></script>
<style>html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:var(--paper)}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--paper)}}
.clip{{position:absolute;left:0;top:0}} div.clip{{width:1080px;height:1920px}}
.clip .ad-scene{{transform:scale(3)}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
<audio id="voix" src="voix.mp3" data-start="0" data-duration="{END}" data-track-index="0"></audio>
{clip_html}
{stk_html}
{sfx_html}
</div>
<script>
const tl=gsap.timeline({{paused:true}});
const pop=(s,t)=>tl.fromTo(s,{{opacity:0,y:12,scale:.86}},{{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(2)"}},t);
const txt=(s,v,t)=>tl.set(s,{{textContent:v}},t);
const pulse=(s,t)=>tl.fromTo(s,{{backgroundColor:"rgba(0,0,0,0)"}},{{backgroundColor:"var(--accent-tint)",duration:.2}},t);
const typ=(s,n,t)=>tl.fromTo(s,{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:n/25,ease:`steps(${{n}})`}},t);
document.querySelectorAll('[id^="stk"]').forEach(el=>pop(el,+el.dataset.start));
{chr(10).join(tweens)}
window.__timelines=window.__timelines||{{}};window.__timelines["main"]=tl;tl.seek(0);
</script></body></html>"""
open("proj/index.html", "w").write(page)
print(f"{len(scenes)} scènes, {len(clips)} apparitions, durée {END} s")
