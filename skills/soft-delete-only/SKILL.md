# Soft delete only — NIKDY fyzicky nemazat uživatelský obsah

Závazný diktát vlastníka (27. 8. 21:2x, doslovně zopakován a zpřísněn 1. 9. večer
po nevratném výmazu skupinových chatů a dat tabu Práce):

> Nebudeš nikdy fyzicky nic mazat. Položka, která je smazána v kódu nebo
> uživatelem, se OZNAČÍ jako smazaná — nesmaže se a neposílá se, pokud není
> potřeba. Pokud je potřeba (výmaz uživatelem), výmaz se samozřejmě odešle všem
> a u nich se také označí jako vymazáno a přestane delegovat do UI.

## Pravidla

1. **Žádný SQL DELETE na uživatelský obsah.** Zprávy, posty, jízdy, inzeráty,
   karty, alba, média, profily — smazání je VŽDY `UPDATE … SET deleted…`
   (flag/timestamp), nikdy odstranění řádku.
2. **Označené se nezobrazuje a nereplikuje**, pokud není potřeba — UI i sync
   filtrují `deleted`.
3. **Výmaz uživatelem se propaguje**: peerům odejde událost výmazu; u nich se
   položka TAKÉ jen označí a přestane delegovat do UI.
4. **TTL/úklid = označení**, ne DELETE. Fyzický úklid označených nejdřív po
   30 dnech (zadání 27. 8.) a JEN cestou, která prošla suchým během s diffem
   (skill backup-data-before-risky-change).
5. **Technický stav není obsah**: přebité online/offline eventy a čistě servisní
   záznamy smí úklid odstranit (výslovně schváleno 1. 9. ráno) — ale cokoli, co
   nese obsah od uživatele, NIKDY.
6. Před KAŽDOU změnou dotýkající se mazací cesty: přečíst tento skill + memory
   `never-touch-user-data`, najít VŠECHNY písaře (grep DELETE/delete v .sq a
   stores) a každý zvlášť obhájit proti pravidlům 1–5.

## Proč skill existuje

1. 9. jsem tvrdým DELETE v novém úklidu nevratně zničil 306+ zpráv skupinových
chatů a všechna data tabu Práce, přestože pravidlo o soft-delete platilo od
27. 8. Pravidlo v žurnálu nestačilo — proto skill, který se čte při každé práci
s mazáním.
