---
name: no-inline-fqn
description: Use whenever writing or editing code in ANY project - never reference a type, function or constant by its fully qualified name inline (org.foo.bar.Baz in the middle of an expression). Always add an import; when the short name would collide with something already in the file, import it with an alias.
---

# Žádné plně kvalifikované názvy v těle kódu

Uživatel to opakovaně odmítá jako „hnusný kód" — a má pravdu: FQN uprostřed
výrazu je nečitelný, rozbíjí zarovnání a schovává skutečnou závislost souboru,
protože se neobjeví v import bloku.

## Pravidlo

**ŠPATNĚ**

```kotlin
const val MY_PROFILE_KEY = org.mjdev.psippr.data.MY_PROFILE_NODE

androidx.compose.foundation.layout.BoxWithConstraints(Modifier.fillMaxWidth()) { … }

scope.launch { org.mjdev.psippr.core.AppForeground.resumed.collect { … } }
```

**SPRÁVNĚ**

```kotlin
import org.mjdev.psippr.data.MY_PROFILE_NODE

const val MY_PROFILE_KEY = MY_PROFILE_NODE
```

Platí pro VŠECHNO: třídy, funkce, konstanty, anotace, rozšíření. Bez výjimky
pro „je to jen jednou" — jedno použití je přesně ten případ, kdy se import píše
nejsnáz.

## Konflikt jmen → alias, ne FQN

Když se krátké jméno bije s něčím, co už v souboru existuje (typicky konstanta
vystavená znovu pod stejným jménem v `companion object`), importuje se
s aliasem:

```kotlin
// alias: companion níž vystavuje konstantu pod stejným jménem, přímý import by kolidoval
import org.mjdev.psippr.data.LAST_FIX_KEY as LAST_FIX_STORE_KEY

companion object {
    const val LAST_FIX_KEY = LAST_FIX_STORE_KEY
}
```

Alias pojmenovat podle toho, ODKUD hodnota je (`…_STORE_KEY`, `…Platform`,
`…Android`), ne `X2` nebo `XAlias`. K aliasu patří krátký komentář, proč
existuje — jinak ho někdo při úklidu importů „opraví" zpět na kolizi.

## Kdy si toho všimnout

- při psaní nového kódu (nikdy FQN nezačínat),
- při editaci cizího řádku, který FQN má — přepsat na import je součást té
  editace, ne samostatný úkol,
- při revizi čistoty kódu spolu s [[one-class-per-file]] a úklidem
  nepoužitých importů (viz [[agent-edit-lint]]).

Hromadné přepisování celého repa se ale nedělá bez zadání — pravidlo se
uplatňuje na kód, kterého se stejně dotýkáš.
