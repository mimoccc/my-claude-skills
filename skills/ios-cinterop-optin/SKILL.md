---
name: ios-cinterop-optin
description: Use whenever touching iosMain / Kotlin-Native code in this repo (or before any macOS CI run). Platform (cinterop) calls need @OptIn(ExperimentalForeignApi) — without it the macOS build fails with "This declaration needs opt-in", which is only discovered after a paid macOS run. Also documents what can and cannot be verified from Linux.
---

# iOS: opt-in u cinterop volání

Tahle chyba shodila macOS build **opakovaně** (naposled v1.0.111,
`Contacts.ios.kt`). Přijde vždycky až z placeného macOS běhu, protože z Linuxu
se iosMain type-checknout nedá — proto je levnější ji nedělat.

## Pravidlo

Každý soubor v `*/src/iosMain/**`, který sahá na platformní API přes cinterop,
má **na začátku souboru**:

```kotlin
@file:OptIn(ExperimentalForeignApi::class)
```

Ne na jednotlivé funkce. Anotace na funkci pokryje jen ji, takže při příští
editaci (nová funkce vedle) chyba spadne znovu — přesně tak se to stalo tady:
`buildContact` opt-in měl, `saveDirectly` přidaný později ne.

Když je v souboru i Obj-C konstrukce (`NSObject` subclass, delegát), přidá se
vedle `BetaInteropApi`:

```kotlin
@file:OptIn(ExperimentalForeignApi::class, kotlinx.cinterop.BetaInteropApi::class)
```

## Co opt-in vyžaduje (podle čeho to poznat)

Není to jen `CPointer` a `memScoped`. Opt-in chce i tohle, což vypadá jako
obyčejné volání:

- Obj-C metody s `NSError**` parametrem — v Kotlinu poslední argument `null`:
  `store.executeSaveRequest(request, null)`, `store.groupsMatchingPredicate(null, null)`
- `NSData`/`CFData` a převody přes `bytes`, `refTo`, `usePinned`, `toKString`
- `CValue<*>`, `useContents { }`, `readValue()`, `cValue { }`
- `interpretObjCPointer`, `objcPtr()`, `rawValue`
- `platform.posix.*`

## Ověření PŘED pushem

Na Linuxu (zadarmo, vteřiny) — najde soubory, které na tohle sahají a opt-in
nemají:

```bash
for f in $(git ls-files '*/src/iosMain/**/*.kt'); do
  grep -qE 'executeSaveRequest|groupsMatchingPredicate|memScoped|CPointer|useContents|refTo|usePinned|toKString|readValue\(\)|cValue|objcPtr|interpretObjCPointer|platform\.posix' "$f" || continue
  grep -q 'ExperimentalForeignApi' "$f" || echo "CHYBI OPT-IN: $f"
done
```

### Past: anotace na souboru bez importu

Když se `@file:OptIn(...)` doplňuje hromadně, MUSÍ se ke krátkému názvu doplnit i
import — jinak macOS build spadne na `Unresolved reference 'BetaInteropApi'`
a `Annotation argument must be a compile-time constant` (stalo se v1.0.112,
`ImagePicker.ios.kt` a `IosP2PEngine.kt`, které anotaci uvnitř používaly plně
kvalifikovaně a import neměly). Nejjistější je psát ji rovnou plně kvalifikovaně:

```kotlin
@file:OptIn(kotlinx.cinterop.ExperimentalForeignApi::class, kotlinx.cinterop.BetaInteropApi::class)
```

Kontrola (najde krátký název bez odpovídajícího importu):

```bash
for f in $(git ls-files '*/src/iosMain/**/*.kt'); do
  h=$(head -1 "$f"); case "$h" in @file:OptIn*) ;; *) continue;; esac
  for a in ExperimentalForeignApi BetaInteropApi; do
    echo "$h" | grep -q "[^.]$a::class" || continue
    grep -q "^import kotlinx.cinterop.$a" "$f" || echo "CHYBI IMPORT $a: $f"
  done
done
```

Type-check iosMain na Linuxu **NEJDE** a nemá smysl to zkoušet:
`:shared:compileIosMainKotlinMetadata` závisí na `:phone`, jehož iosMain
potřebuje `WebRTC.xcframework` cinterop — a ten se staví jen na macOS
(`webrtc.gradle.kts`: `onlyIf { os.name contains "Mac" }`), protože Kotlin/Native
Apple targety z Linuxu nepodporuje. Selže to na `Unresolved reference
'addRenderer'`, což NENÍ chyba v kódu.

Skutečný type-check jede přes workflow **`ios-check.yml`** (jen překlad, bez
archivace a podpisu) — pouštět ho **před** plným Release, ať se drahé macOS
minuty nespotřebují na překlepovou chybu:

```bash
gh workflow run ios-check.yml --ref main
```

## Proč to nejde vypnout globálně

Opt-in by šlo nasypat do `freeCompilerArgs` (`-opt-in=kotlinx.cinterop.ExperimentalForeignApi`)
pro všechny iOS targety. Záměrně to tu není: anotace v souboru je zároveň
značka „tady se sahá na nativní paměť", což se při čtení kódu hodí. Kdyby se
to někdy rozhodlo jinak, musí se to udělat v `shared.gradle.kts` i `phone`
a `webrtc` naráz, jinak se chyba přesune jen o modul dál.
