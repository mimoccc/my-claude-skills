---
name: about-thanks-list
description: Use whenever a dependency is added, removed, or replaced in ANY gradle file of this repo (psippr) — libs.versions.toml, *.gradle.kts, vendored modules, or Rust crates used via FFI. The About screen has a "Thanks to:" section listing the project's libraries with links (licenses require attribution and it is fair); keep that list in sync with reality.
---

# About „Thanks to:" — údržba seznamu knihoven

Obrazovka Nastavení → About má pod tlačítkem Aktualizovat sekci **Thanks to:**
se seznamem knihoven a odkazy. Seznam žije v
`shared/src/commonMain/kotlin/org/mjdev/psippr/ui/components/ThanksTo.kt`
(`THANKS_LIBS`, pár `jméno to url`).

## Pravidla

1. **Při každé změně závislostí** (přidání/odebrání/náhrada v
   `gradle/libs.versions.toml`, kterémkoli `*.gradle.kts`, vendorovaném modulu
   jako `:webrtc`, nebo Rust crate v `gossip/rust/Cargo.toml` viditelné ve
   funkcích appky) uprav ve STEJNÉM commitu i `THANKS_LIBS`.
2. **Kurátorovaný, ne generovaný**: jedna položka na PROJEKT, ne na artefakt
   (všechny `io.ktor:*` = jedna položka „Ktor"; androidx = jedna položka
   „AndroidX / Jetpack"). Interní/build-time věci (ktlint, gradle pluginy)
   do seznamu nepatří — jen co appka opravdu používá za běhu.
3. **Odkaz vede na domov projektu** (GitHub repo nebo oficiální web), ne na
   Maven souřadnice.
4. U knihoven od jednotlivců uveď autora v závorce — např.
   „Reorderable (Calvin Liang)" — poděkování má mířit na člověka.
5. Odebraná závislost = odebrat řádek (mrtvé poděkování je horší než žádné).

## Kontrola (občas, ne při každém buildu)

```bash
grep -E 'module = ' gradle/libs.versions.toml | sed 's/.*module = "//;s/".*//' | sort -u
grep -rhoE 'implementation\("[^"]+"\)' shared/shared.gradle.kts phone/*.gradle.kts androidApp/*.gradle.kts | sort -u
```

a porovnat s `THANKS_LIBS`. Chybějící doplnit, přebývající smazat.

## Poznámka

Zvažovaná alternativa: AboutLibraries (mikepenz) umí seznam generovat z gradle
metadat včetně licencí; zatím nenasazeno (další plugin + riziko nekompatibility
Kotlin metadat — viz Coil 3.5 vs Kotlin 2.2.20). Kdyby seznam začal zaostávat,
je to cesta.
