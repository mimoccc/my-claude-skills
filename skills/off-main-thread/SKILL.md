---
name: off-main-thread
description: Use whenever writing, reviewing or debugging code in ANY project that touches coroutines, suspend functions or UI - everything that does not belong on the UI thread must run in a different coroutine context (Dispatchers.Default/IO). Also use when the app stutters, jank is reported, "Too much work on main thread"/ANR appears, or a composable/state holder calls disk, DB, crypto, image decoding or network.
---

# Na UI vlákně jen UI

Uživatel to hlásí opakovaně jako „seká se to". Pokaždé to bylo totéž: práce,
která nemá s kreslením nic společného, běžela na hlavním vlákně.

## Pravidlo

Na UI vlákně smí zůstat JEN:

- skládání UI (Compose kompozice, měření, kreslení),
- čtení/zápis stavu, který UI hned vykresluje,
- spuštění coroutine, která tu práci předá jinam.

Všechno ostatní jde do jiného kontextu:

```kotlin
// špatně — suspend funkce v rememberCoroutineScope běží na Main
scope.launch { importAppData(zip) }

// dobře
scope.launch { withContext(Dispatchers.Default) { importAppData(zip) } }
```

- CPU práce (parsování, CBOR, komprese, hashe, podpisy, dekódování obrázků,
  skenování alb/timeline) → `Dispatchers.Default`
- disk, DB, síť, souborové operace → `Dispatchers.IO` (na KMP tam, kde existuje;
  jinak `Dispatchers.Default`)
- výsledek zpátky do stavu až po `withContext` — flow/StateFlow se aktualizuje
  z libovolného vlákna, UI se překreslí samo

## Co musí platit v kódu

1. **Suspend funkce nesmí být „main-safe až u volajícího".** Funkce, která sahá
   na disk/DB/CPU, si přepnutí kontextu udělá SAMA (`withContext` uvnitř) —
   volající pak nemůže nic pokazit.
2. **V composable se nic nedekóduje ani nepočítá.** Dekódování obrázků a jiné
   drahé výpočty patří mimo kompozici a přes `remember`/cache, ne do každé
   rekompozice.
3. **Ve ViewModelu/state holderu žádný `scope.launch { }` bez kontextu**, pokud
   uvnitř není jen změna stavu.
4. **Žádný `runBlocking` na UI vlákně.** Nikdy.
5. **Platformní zpětná volání** (Android receivery, service callbacky, iOS
   delegáti) běží na hlavním vlákně — práci z nich hned předej dál.

## Jak to hlídat

- Android: logcat `Choreographer: Skipped N frames` / `Too much work on main
  thread` / ANR trace = přímý důkaz; hledej podle názvu funkce v traceu.
- Rychlý audit v repu (kandidáti na kontrolu):
  ```bash
  grep -rn "scope.launch {" --include=*.kt | grep -v withContext
  grep -rn "rememberCoroutineScope()" --include=*.kt
  grep -rn "runBlocking" --include=*.kt
  ```
  Každý nález projdi: dělá to jen změnu stavu (OK), nebo pracuje (přesunout)?
- Po opravě se do komentáře píše PROČ (jaký příznak to řešilo), ne co ten řádek
  dělá.

## Historie v psippr

- ANR při přesunu profilu: `requestTakeover` včetně `importAppData` běžel
  z `rememberCoroutineScope` (Main) → `withContext(Dispatchers.Default)`.
- „Too much work on main thread" při otevření tabu Alba: `receivedAlbums`,
  `timelineOf`, `timelinePageOf`, `phonesFromChat`, `cachedPublicAlbums`,
  `loadAlbumVideo`, `loadAlbumPhoto` skenovaly data na Main.
- ~40 volání `decodeImage` přímo v kompozici bez `remember`.
