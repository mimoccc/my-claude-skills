---
name: super-promo
description: Use in psippr whenever a capability is added, moved, or reviewed that can HARM ANOTHER PERSON - screenshots of someone else's content, archiving a stranger's identity (contacts, gallery, phone numbers), moderation power, seeing people who hid themselves. Such capabilities belong to SUPER PROMO, never to plain promo/VIP/paid. Also use when touching AppState.superPromo, SuperPromo, SuperPromoStatus, VipStatus or FLAG_SECURE.
---

# Super promo — nejužší role v psippr

Zavedeno 9. 8. 2026 na zadání vlastníka. Promo účtů je víc a jsou to obyčejní lidé
(kamarádi v roli moderátorů). Schopnosti, které umí ublížit **někomu jinému**, proto
nesmí viset na „mám promo kód".

## Definice (jediný zdroj pravdy: `core/SuperPromo.kt`)

Super promo = **promo účet** (promo kód / role `AppRole.PROMO`), který má značku
`psippr`:

1. v **„moje sexualita" (prefs) NA PRVNÍM MÍSTĚ**, a zároveň
2. v **„co hledám" (lookingFor)** kdekoli.

Obojí se dopisuje ručně přes „+" u chipů (`ChipGroup`), takže se to nedá vyplnit
omylem. Odebrání značky roli okamžitě sundá — počítá se za běhu z profilu.

Kód:
- `SuperPromo.matches(promo, prefs, lookingFor)` — čistá funkce, testovatelná.
- `AppState.superPromo: StateFlow<Boolean>` — pro UI (`state.superPromo`).
- `SuperPromoStatus.active` — mirror pro platformní vrstvu (Android `MainActivity`,
  iOS `ScreenshotGuard.ios.kt`, `Contacts.android.kt`).
- Přepočet je na JEDNOM místě: `refreshSuperPromo()` volané z collectoru nad
  `combine(_vip, _myRole, _myProfile)` v `init`. Nepřidávej druhou cestu zápisu.

## Co pod super promo PATŘÍ (a už tam je)

| Schopnost | Kde | Proč |
| --- | --- | --- |
| Snímky obrazovky (Android FLAG_SECURE lift) | `MainActivity` | snímek cizího obsahu |
| Snímky obrazovky (iOS secure vrstva) | `ScreenshotGuard.ios.kt` | totéž |
| Uložit kontakt do adresáře | `SaveContactAction.kt` | sbírá cizí identitu |
| Stažení cizích alb do galerie | `AppState.saveAlbumsToGallery` | cizí fotky na disk |
| Řádek „Otevřít v galerii" v kartě kontaktu | `Contacts.android.kt` | ukazuje na ten archiv |

Debug build má snímky povolené pořád (`isDebugBuild()`), to je záměr.

## Pravidlo pro novou funkci

Než něco pověsíš na `vip` / `hasPaidFeatures`, zeptej se: **může to ublížit někomu
JINÉMU než uživateli, který to spustil?** Pokud ano, patří to na `superPromo`.
Placené funkce (`PaidFeature`) jsou o pohodlí a nikdy nesmí odemykat pravomoc.

## Co super promo NENÍ

- **Není důkaz vůči ostatním klientům.** Je to lokální brána vlastního klienta;
  upravený klient ji obejde. Cokoli, co má platit i pro CIZÍ klienty (spam verdikt,
  otevření cizího alba), musí jít přes podepsaný `RoleCert`.
- **Není náhrada moderace.** Moderační práva (`AppRole.canModerate`, spam verdikty)
  zůstala 9. 8. na promo — zúžení se s vlastníkem neprobralo, nesahat bez zadání.

## Otevřené kandidáty (čeká na rozhodnutí vlastníka)

Vychází z `ethics-review.md` (analýza 7. 8.). NEIMPLEMENTOVAT bez pokynu:

1. Zrušení spam listu / arbitrův verdikt (`removeFromSpamList`, `SpamArbiterCard`) —
   „komunitní hlášení je nejsnáz zneužitelná mechanika v appce".
2. Zobrazení nahlášených pod prahem (`BrowseScreen` spamPending) — seznam podezřelých.
3. Vidět v okolí lidi v inkognitu (`Wire.kt` — inkognito announce vidí promo/VIP klient).
4. Vidět v profilové galerii videa skrytá běžnému divákovi (`Wire.kt`, pokyn 1. 8.).
5. ALERT post s červeným rámečkem (promo autor) — dosah na všechny.

## Související

- `ethics-review.md` v kořeni repa — analýza rizik, ze které se seznam bere.
- memory: `promo-roles-and-vip-security-plan`, `promo-cert-vs-vip-verdict`,
  `contact-save-spec`, `erotic-album-grant-invariant`.
