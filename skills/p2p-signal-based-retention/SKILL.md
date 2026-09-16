---
name: p2p-signal-based-retention
description: Load before designing or reviewing any feature that shares content between peers (posts, profiles, group chat, POIs, guides, business listings, group boards, ...). Default retention/propagation model for the whole app; check any deviation against it.
---

# Default retention model: peer-held signals, 30 days, no central timer

**Pravidlo (vlastník projektu, 2026-09-16):** „zapis ze se posty i uzivatel
ktery je offline a vse co napsal, krome privatniho chatu, smaze po dobe 30
dni... je to na zaklade signalu ktere drzi 30 dni kazdy peer... a peers
sharuju a synchronizuju zmeny mezi sebou, takze peer nemusi byt online aby
zmeny jeho profilu byli akceptovane... a to si i dej jako skill, vse tak musi
fungovat, krome specifickych detailu."

## Jak to funguje (a musí fungovat u nového veřejného/sdíleného obsahu)

1. **Žádné centrální mazání timerem.** Nic se neposílá na server a nic se tam
   nemaže — appka nemá server. Obsah (post, profil, oznámení, ...) prostě
   PŘESTANE BÝT DOSTUPNÝ, jakmile ho žádný peer už nemá koho poprosit o
   předání dál.
2. **Peeři si navzájem sdílejí a synchronizují signály o sobě** (announce,
   profil, veřejný obsah) — autor NEMUSÍ být online, aby jeho data zůstávala v
   oběhu. Stačí, že je má aspoň jeden jiný peer a ten je ochotný je předat dál
   (viz `AppState.kt` — sdílení peerů/profilů přes `peers_ask/list/req/rec` a
   `profiles_ask/list/req/rec`).
3. **Každý takový signál má u sebe na zařízení TTL 30 dní** (`PEER_HISTORY_TTL_MS`,
   `PEER_HISTORY_GRID_MAX_AGE_MS`, `PUBLIC_DELETE_KEEP_MS` v `AppState.kt` —
   konkrétní konstanta se liší podle druhu signálu, ale řád je stejný: 30 dní).
   Po 30 dnech bez obnovy peer signál zahodí.
4. **Důsledek:** pokud se autor k síti vůbec nepřipojí 30 dní, ŽÁDNÝ peer už
   jeho signál nedrží → nemá ho od koho dostat → autor i všechno VEŘEJNÉ, co
   napsal, ze sítě zmizí samo, bez jakékoli explicitní mazací akce.
5. **Výjimka: soukromý chat.** Zprávy 1:1 jdou přímo mezi dvěma zařízeními,
   NEŠÍŘÍ se přes další peery a NEPODLÉHAJÍ žádné z lhůt níže — zůstávají,
   dokud je někdo z účastníků sám nesmaže.
6. **Výjimka: veřejná zeď má VLASTNÍ, kratší lhůtu — 24 hodin** (`PUBLIC_POST_TTL_MS`
   v `WireLimits.kt`, `25L * 60 * 60 * 1000`). Je to úmyslně krátkodobá
   nástěnka toho, co se děje TEĎ v okolí, ne archiv — příspěvek zestárne a
   přestane se šířit/zobrazovat po 24 hodinách bez ohledu na 30denní
   peer-signal mechanismus výše (ten platí pro profil/oznámení, ne pro
   obsah zdi).

## Jak to použít u nové featury

- Nová sdílená/veřejná featura (skupinový board, guides, business listing,
  cokoli, kde obsah vidí víc lidí než autor) **defaultně dědí tenhle model**:
  šíří se přes peer-signály, drží se ~30 dní bez obnovy, mizí samo, když ho
  nikdo nedrží.
- Odchylka (jiná délka TTL, jiný mechanismus, žádná expirace) je možná, ale
  jen se SPECIFICKÝM zdůvodněním u dané featury (jako u soukromého chatu výš)
  — ne mlčky.
- Marketing/copy (web, guide, privacy policy) musí tenhle mechanismus popisovat
  přesně takhle — ne jako „server po 30 dnech smaže data" (žádný server není)
  a ne jako věčné uchovávání veřejného obsahu bez zmínky o 30denním okně.
