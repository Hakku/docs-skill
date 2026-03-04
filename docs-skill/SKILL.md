---
name: docs
description: >
  Dokumentaation laatujärjestelmä. Soveltaa silmäiltävyys-, selkeys-
  ja saavutettavuusperiaatteita markdown-dokumentteihin ja ajaa
  automaattisen kielitarkistuksen humanizer-skillillä.
  Käytä kun kirjoitat tai parannat README:tä, guidea tai OS-dokumentaatiota.
allowed-tools: Read Write Edit Glob Grep AskUserQuestion Skill
metadata:
  author: Hakku
  version: 1.0.0
---
# Documentation Quality System

## Not for

- **CC:n sisäiset tiedostot** — CLAUDE.md, context.md, memory.md, ARCHITECTURE.md, SKILL.md-tiedostot. Nämä ovat konfiguraatiota, eivät dokumentaatiota.
- **Koodidokumentaatio** — docstringit, JSDoc, inline-kommentit. Ne elävät koodin kanssa.
- **Muiden skillien korvaaminen** — /review tekee koodiarvion, /verify tarkistaa spec-fidelityn. /docs käsittelee lukijakokemusta.

## Workflow

Suorita nämä vaiheet järjestyksessä kohdetiedostolle ($ARGUMENTS):

### 1. Lue kohdetiedosto

Lue $ARGUMENTS kokonaan. Jos tiedostoa ei löydy, ilmoita ja lopeta.

Jos tiedosto on CC:n sisäinen (CLAUDE.md, context.md, memory.md, ARCHITECTURE.md, SKILL.md, tai sijaitsee `~/.claude/`-hakemistossa), kieltäydy: "Tämä tiedosto on CC:n sisäinen konfiguraatio, ei dokumentaatio. /docs ei käsittele näitä."

### 2. Lue periaatteet

Lue `references/principles.md` (suhteessa tämän skillin hakemistoon). Nämä ohjaavat arviointia.
Täysi viittaus: see references/principles.md

### 3. Arvioi periaatteiden mukaan

Käy kohdetiedosto läpi kolmella akselilla:

**Silmäiltävyys:**
- Onko sisältö jaettu osioihin informatiivisilla otsikoilla?
- Onko sisällysluettelo (pitkissä dokumenteissa)?
- Ovatko kappaleet lyhyitä?
- Aloittavatko kappaleet aihevirkkeellä joka toimii itsenäisesti?
- Ovatko avainsanat virkkeen alussa?
- Onko tärkein tieto nostettu alkuun?
- Hyödynnetäänkö luetteloita, taulukoita ja lihavointia?

**Kirjoituslaatu:**
- Ovatko virkkeet yksinkertaisia ja yksiselitteisiä?
- Onko pitkiä substantiiviketjuja?
- Onko vasemmalle haarautuvia virkkeitä?
- Onko epämääräisiä pronomineja ("tämä", "se") ilman viittauskohdetta?
- Onko johdonmukaisuus kunnossa (otsikointitapa, välimerkit, nimeäminen)?

**Saavutettavuus:**
- Onko kieli tarpeettoman monimutkaista?
- Onko avaamattomia lyhenteitä?
- Ovatko koodiesimerkit itsenäisiä ja siirrettäviä?
- Käsitelläänkö yleisimmät ongelmat ensin?
- Aloitetaanko aiheet laajalla kehyksellä ennen yksityiskohtia?

### 4. Paranna

Tee muutokset arvioinnin perusteella:

- **Kosmeettinen** (sanamuodot, kappalejako, otsikot, lihavoinnit) → käytä Edit-työkalua
- **Rakenteellinen** (järjestyksen muutos, osioiden yhdistäminen/jakaminen, merkittävä uudelleenkirjoitus) → käytä Write-työkalua

Säilytä aina:
- Koodilohkot (```` ``` ````) muuttumattomina — älä muokkaa koodin sisältöä
- Taulukot rakenteellisesti ehjinä — voit muokata solujen tekstiä mutta älä riko taulukkorakennetta
- Linkit, kuvaviittaukset ja muut tekniset elementit

### 5. Kielitarkistus humanizer-skillillä

Tunnista kohdetiedoston dominoiva kieli proosakappaleista (ei koodilohkoista tai teknisistä termeistä).

Kutsu Skill-työkalulla oikea humanizer:
- **Suomi** → `skill: "finnish-humanizer", args: "<tiedostopolku>"`
- **Englanti** → `skill: "english-humanizer", args: "<tiedostopolku>"`

Jos Skill-työkalu ei ole käytettävissä (permission denied tai muu virhe):
- **Suomi** → ohjeista käyttäjää: "Aja seuraavaksi: `/finnish-humanizer <tiedosto>`"
- **Englanti** → ohjeista käyttäjää: "Aja seuraavaksi: `/english-humanizer <tiedosto>`"

### 6. Yhteenveto

Näytä lopuksi mitä muutettiin ja miksi:

```
## /docs yhteenveto

**Kohde:** <tiedosto>
**Kieli:** <FI/EN>

### Tehdyt muutokset
- [muutos 1]: [perustelu periaatteista]
- [muutos 2]: [perustelu periaatteista]
- ...

### Humanizer
- [kutsuttu/ohjeistettu] <skill-nimi>
```

## Constraints

- **Yksi tiedosto kerrallaan.** $ARGUMENTS on yksittäinen tiedostopolku.
- **Älä lisää sisältöä.** Parannat olemassa olevaa — et keksi uusia osioita tai väitteitä.
- **Periaatteet ohjaavat, eivät pakota.** Osio "Riko sääntöjä vain syystä" pätee. Jos jokin periaate on ristiriidassa dokumentin tarkoituksen kanssa, ohita se ja selitä miksi yhteenvedossa.
- **Koodia ei kosketa.** Fenced code blocks ja inline code säilyvät byte-identtisinä.
