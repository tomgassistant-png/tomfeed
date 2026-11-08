# Curiosities

Single source of truth for TomFeed. Edit this file when interests or must-checks change.
The daily Grok Bot reads **this document**, then builds and publishes the feed page.

Public site: https://tomgassistant-png.github.io/tomfeed/

---

## Daily rules

1. Read this whole file before searching or publishing.
2. **Must-check every day** first (section below) — append anything new that is not already on the feed / ever-seen.
3. Then **search** across **≥5** topic sections below for **15–20** strong recent pieces (last 2–4 weeks). Prefer longform / essays / Substack; ~10–20% YouTube lectures or long interviews. Avoid breaking-news churn and YouTube Shorts.
4. Quality first — never pad with weak items to hit a quota; never drop a strong piece only for diversity math.
5. Soft balance: aim ≤3 mainstream outlets and ≤3 from one outlet when comparable alternatives exist.
6. Keep the live list around **~48 items** and about a **5-day** window (prune older/surplus after adding).
7. Skip URLs already on the feed or in the ever-seen list (normalize www / tracking / near-dup titles).
8. Set `published_at` from the piece; set `added_at` to now (ISO UTC). Newest first.
9. **Excluded outlets — never add:** History Today (`historytoday.com`), Foreign Affairs (`foreignaffairs.com`), War on the Rocks (`warontherocks.com`), Lawfare (`lawfaremedia.org`), New York Review of Books (`nybooks.com`).
10. Publish the static page to GitHub Pages. Do not use OpenClaw/Telegram for the daily refresh.
11. **Keep the site unindexed:** always ship `robots.txt` with `User-agent: *` / `Disallow: /`, and put `<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">` in every HTML page (including regenerated `index.html`). Never submit a sitemap.
12. **Page chrome (every build):** rebuild `index.html` with `python3 generate.py` from `feed.json`. Do not rewrite ordinary feed items for a chrome-only change. The script always puts an edition line at the very top, above weather/markets, from the same generation timestamp as the footer, in Asia/Jerusalem — `Edition: Sun, Nov 8, 2026, 7:33 AM Israel time (05:33 UTC)`. It sets the root font size to 120% so all text scales together. It links **Edit interests (curiosities.md)** to `https://github.com/tomgassistant-png/tomfeed/edit/main/curiosities.md` next to that edition line and in the footer beside the curiosities.md note. On that same run it applies the Off Leash rule: show a new update only in the edition that first adds it, then remove it; never insert a placeholder.

### Selective topic filters

- **Cursor and Grok Bot:** prefer official Cursor/xAI announcements, docs/changelogs, credible tech press on material changes. Exclude lifestyle/promo fluff, “how I use…” blogs, tips listicles, sales spam.
- **Victorian era — arts, culture, science:** prefer serious history/culture/science essays (Works in Progress–level and peers). Exclude shallow listicles and pop fluff.
- **Marginal Revolution:** check when relevant; add posts that map to a topic below or look like a future curiosity. Skip link dumps, EV cohort lists, generic paper plugs. Soft cap ~1–2 per day unless several are unusually strong across different topics.

---

## Must-check every day

Fixed sources. Check these every refresh; do not leave them to general search alone. Recent window ~21 days unless noted. Public/RSS items only where that applies. Do not historically backfill.

### Substack / RSS

| Name | Feed / site | Notes |
|------|-------------|--------|
| Magenta Notebooks (Bronze Age Pervert) | https://www.bronzeagepervert.yoga/feed | Every new public RSS item (no tip cap) — essays + Caribbean Rhythms |
| Wandervogel (Gildhelm) | https://www.wandervogel.art/feed | Recent public posts |
| Psychobabble (Hannah Spier, MD) | https://hannahspier.substack.com/feed | Recent public posts (essays + podcast) |
| The Matter with Things (Iain McGilchrist) | https://iainmcgilchrist.substack.com/feed | Recent public posts |
| It's Noon In Israel (Amit Segal) | https://newsletter.amitsegal.net/feed | **Max 1** — newest issue only |
| Amphora (LEO CAESARIS) | https://amphora.substack.com/feed | Recent public posts |
| Inside Bordeaux (Jane Anson) | https://janeanson.com/feed | Recent posts |
| Cultural Capital (James Marriott) | https://jmarriott.substack.com/feed | Recent public posts |
| Beyond the Ideological (Zineb Riboua) | https://www.zinebriboua.com/feed | **Max 1** — newest only |
| MTS (Monitoring the Situation) | https://mtslive.substack.com/feed | **Max 1** — newest only |
| Theo Jaffee | https://www.theojaffee.com/feed | Recent public posts |
| Effort | https://www.effort.news/feed.xml | Every recent item (no tip cap) |

### Podcast / radio

| Name | Where | Notes |
|------|-------|--------|
| The Piano Matters (David Dubal) | https://www.wwfm.org/show/the-piano-matters-with-david-dubal | WWFM; no public RSS — check listings for new episodes |

### YouTube (no Shorts)

| Channel | URL | Notes |
|---------|-----|--------|
| Israel Update (Michael Doran & Gadi Taub) | https://www.youtube.com/channel/UCG7Vh-hy0I0N5g3ZVpdwXmQ | Latest 1–2 full episodes |
| All-In Podcast | https://www.youtube.com/@allin | Latest 1–2 full episodes (≥20 min); never Shorts |
| The Critical Drinker (Will Jordan) | https://www.youtube.com/@TheCriticalDrinker | Latest 1–2; skip Shorts; main channel only |
| The Students | https://www.youtube.com/@the_students_media | Latest 1–2; skip Shorts |

### X

| Account | Handle | Notes |
|---------|--------|--------|
| Erik Prince (Off Leash) | [@realErikDPrince](https://x.com/realErikDPrince) | **Only** posts whose first line starts with “Off Leash update”. Max 1 (newest). Keep the full post body for inline display. Pin below weather/markets when those exist. Shown once, in the edition where it first appears, then removed; no placeholder. `generate.py` records that edition and drops the item once `generated_at` moves on. Do not alert on Telegram if missing. |
| Yonatan Adler | [@AdlerYonatan](https://x.com/AdlerYonatan) | Max 1 serious archaeology/history post; also surface him in general search across platforms |

---

## Topics to search

Broad subjects — topics, not individual articles. Rotate across sections; do not cluster on one niche.

### Current affairs & geopolitics

- [ ] Israel's security environment
- [ ] Lebanon, Hezbollah, Iran, and Syria — regional dynamics
- [ ] US–Iran diplomacy and its interaction with regional conflict
- [ ] Maritime chokepoints and supply-chain vulnerability (e.g. Strait of Hormuz)
- [ ] Private military and security contractors — law, deployment, and geopolitical impact
- [ ] Technology trade policy — EV imports, advanced tech, and security screening
- [ ] Diplomacy and international organizations
- [ ] How bureaucracies function behind the scenes
- [ ] Israel domestic politics and elections
- [ ] Negev infrastructure — data centers, water, energy
- [ ] Sinai and border-region security
- [ ] Lebanon post-conflict recovery and reconstruction
- [ ] Latin American politics (incl. Colombia)
- [ ] Arctic and Greenland — sovereignty, security, resources, and great-power interest
- [ ] Rare earth minerals — geology, supply chains, processing, and geopolitics

### History

#### Bible — history, literature, theology

- [ ] Hebrew prophets and prophetic literature
- [ ] How the New Testament uses the Old Testament
- [ ] Bible translation — original languages vs English versions
- [ ] Biblical archaeology
- [ ] Ancient Israel and Judah as historical kingdoms

#### Yonatan Adler

- [ ] Yonatan Adler — person to follow / surface material by or about him wherever it appears. Prefer serious scholarship and longform on archaeological-historical dating of Torah observance among ordinary Judeans; *The Origins of Judaism*. Exclude fluff and promotional noise.
- [ ] When Judaism as a lived way of life begins — earliest evidence for dietary laws, ritual purity, circumcision, Sabbath, and festivals
- [ ] Material markers of Torah practice — mikva’ot, chalk vessels, tefillin, mezuzot, pig and scaleless-fish remains, figural art
- [ ] Hasmonean and Hellenistic context — whether widespread Torah observance emerges under foreign rule or after Judean autonomy

#### Everyday life, literacy & education

- [ ] Literacy and ordinary people in pre-modern societies
- [ ] Daily life — work, writing, manners, social customs
- [ ] History of reading, writing, and numeracy
- [ ] Philosophy in national education systems

#### Places, eras & civilizations

- [ ] English history — Restoration and early modern
- [ ] History of science — especially Victorian era
- [ ] The Victorian era — arts, culture, science (see selective filter above)
- [ ] Ernst Haeckel — evolution, monism, *Kunstformen der Natur*, German Darwinism, recapitulation, legacy and controversy
- [ ] Jewish history
- [ ] Religion and politics
- [ ] Japan and Chinese cultural exchange
- [ ] Tibet
- [ ] Mesoamerica and pre-Columbian urban history
- [ ] Neolithic astronomy and ceremonial landscapes
- [ ] Arctic and Greenland — history, society, and indigenous cultures
- [ ] American Civil War memory and historic sites
- [ ] Local and suburban history (US Northeast)
- [ ] Edwardian and Victorian literary culture

#### War, intelligence & 20th-century geopolitics

- [ ] Espionage and intelligence history
- [ ] World War Two in Asia
- [ ] Cold War in Africa, East Asia, and Latin America

### Languages & China

- [ ] Language change and etymology
- [ ] Spelling reform and branded spellings
- [ ] French, Quebec French, Hebrew, and English usage
- [ ] Chinese languages — family, dialects, and script
- [ ] Learning and using Chinese
- [ ] Travel in China — visas, logistics, practical tools

### Science, technology & space

#### AI, agents & local infrastructure

- [ ] How large language models work
- [ ] Comparing AI models and their tradeoffs
- [ ] AI bias — causes and measurement
- [ ] Self-hosted and local LLM infrastructure (e.g. Ollama)
- [ ] AI agent frameworks and workflow automation
- [ ] AI-assisted coding and human–AI collaboration
- [ ] Cursor and Grok Bot (see selective filter above)
- [ ] Structured markdown and AI-augmented development environments
- [ ] AI industry and startup economics

#### Spaceflight

- [ ] Space launch economics and engineering
- [ ] Reusable rockets and deep-space exploration
- [ ] Military and civilian space programs

### Arts & culture

#### Literature & film

- [ ] 20th-century modernist literature — structure and theme (Eliot, Proust, and peers)
- [ ] Film — history, production, influences, soundtracks
- [ ] *The Gentlemen* (Netflix) — Guy Ritchie crime comedy series

#### Music & piano

- [ ] lives of composers
- [ ] International Chopin and His Europe Festival (Warsaw)

#### Food, drink & other

- [ ] Wine — regions, criticism, and historical writing
- [ ] Cocktails, spirits, and aperitifs
- [ ] Cooking and recipe development
- [ ] Gemology — stone identification and trade

### Society, mind & daily life

#### Cognition, belief & society

- [ ] Why people believe what they believe
- [ ] Political and national identity
- [ ] How narratives form and spread
- [ ] Philosophy of religion
- [ ] US progressive politics
- [ ] Psychology of dreams
- [ ] Reinventing oneself later in life
- [ ] How societies change
- [ ] Which expert narratives age badly
- [ ] Mental health trends in younger generations

#### Iain McGilchrist

- [ ] Iain McGilchrist — divided brain and two kinds of attention; *The Master and His Emissary* and *The Matter with Things*
- [ ] Hemisphere hypothesis — left-hemisphere grasp vs right-hemisphere attention
- [ ] The sacred and the thinning of reality
- [ ] Institutions under left-hemisphere capture

#### Nick Land

- [ ] Nick Land — accelerationism, post-Kant critical philosophy, the Outside
- [ ] Retrochronicity — history as future-driven assembly; capitalism as retrochronic AI; hyperstition
- [ ] Gnostic Calvinism — Terminator vs Matrix in AI culture
- [ ] Capitalism-as-intelligence — machinic desire, providence metaphors, Anglo-Protestant Whig endgame

#### Productivity & cognitive architecture

- [ ] Getting Things Done — externalized commitment tracking
- [ ] Weekly review and maintaining clear digital workspaces
- [ ] Productivity systems and life organization

#### Health, nutrition & longevity

- [ ] Body composition and sustainable weight loss
- [ ] High-protein, low-carb nutrition
- [ ] Appliance-assisted meal prep for restricted diets

#### Personal admin

- [ ] Retirement and housing options
- [ ] Personal finance and investing

### Transport & infrastructure

- [ ] Electric vehicles — engineering, brands, and market dynamics
- [ ] Transportation systems and logistics
- [ ] Aviation history and engineering
- [ ] Supersonic passenger flight (Concorde and successors)
- [ ] Airports and global logistics

### Knowledge, research & writing

- [ ] Historical method and how historians work
- [ ] Historiography and narrative technique in popular history
- [ ] Research archives and permanent knowledge repositories
- [ ] Note-taking and personal knowledge management
- [ ] Long-form writing, blogging, and publishing
- [ ] Organizing information into useful structures
- [ ] 19th-century historical writing and memoirs

---

## How to edit

- Change a topic or must-check → edit this file on GitHub (or ask the Bot to edit it).
- Add a must-check source → add a row under **Must-check every day** with URL/feed and any max/filter notes.
- The Bot should consult this file at the start of every daily build.
