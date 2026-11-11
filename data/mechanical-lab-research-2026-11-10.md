# Mechanical engineering lab research

Research date: 10 November 2026. This is a source-backed starting sample, not a ranking or a complete audit of the 13 universities.

## Project context

The project builds a Korean-language mechanical engineering research atlas. `scripts/build_rosters.py` converts captured university directories into PI rosters; `scripts/openalex_fetch.py` resolves authors and retrieves publications since 2022; `scripts/aggregate.py` classifies publications and produces `site/data.json`. `site/template.html` contains the directory interface, and `site/index.html` is the populated site.

The existing dataset reports 816 PI entries across 13 universities, 20,589 unique papers in the aggregation, 704 entries treated as reliable author matches, and 633 entries passing its mechanical-engineering scope filter. These are project-generated counts, not independently verified lab totals. A PI entry may stand in for a research group. The 61 KAIST entries come from publication affiliations rather than an official faculty roster; their `unofficial` status is included in the project's reliable-author count.

## Browser method and limitation

Read the Aside skill and ran `aside guide`. Attempted `aside exec` for official-site lab research, but it failed before starting: `Failed to request daemon auth challenge ... connect EPERM 127.0.0.1:21420`. The sandbox denied access to Aside's local service. The sources below were therefore researched with the available web search/fetch tool, not Aside. No site data, source scripts, or existing rosters were changed.

## Official-source lab sample

| University | Lab / PI | Research topics supported by sources | Evidence and access limits |
| --- | --- | --- | --- |
| KAIST | [Dynamic Robot Control & Design Lab](https://www.dynamicrobot.kaist.ac.kr/) — Hae-Won Park | Legged robots, actuator/mechanism design, dynamic control and learning-based locomotion | Lab homepage directly readable. [KAIST faculty introduction](https://ilp.kaist.ac.kr/english/sub0302/view/page/2/id/70) links the lab and describes its work; [KAIST researcher profile](https://pure.kaist.ac.kr/en/persons/hae-won-park/) confirms Mechanical Engineering affiliation. |
| KAIST | [AiM⁴ Lab — Laboratory for AI-powered Modeling in Mechanics, Materials, and Manufacturing](https://sites.google.com/site/seunghwalab/) — Seunghwa Ryu | Physics-informed AI, surrogate models, generative design, inverse design, engineering optimization | Current lab homepage names Ryu and describes these directions. [KAIST Space Institute profile](https://ksi.kaist.ac.kr/em01_05/8) confirms Mechanical Engineering affiliation and links this same site, although it describes the older multiscale mechanics focus. |
| Seoul National University | [Bioinspired Embodied Intelligence Robotics Laboratory](https://www.biorobotics.snu.ac.kr/) — Kyu-Jin Cho | Soft and bioinspired robotics, wearable assistance, prosthetic hands, deployable robots | Lab homepage directly readable. [SNU Robotics directory](https://robotics.snu.ac.kr/) confirms Cho's Mechanical Engineering affiliation. Homepage lists a January 2025 Science Robotics result on a hyperelastic torque-reversal mechanism for soft joints. |
| MIT | [Design Computation and Digital Engineering (DeCoDE) Lab](https://decode.mit.edu/) — Faez Ahmed | AI-driven engineering design, generative models, optimization, multimodal representations and human–AI design tools | Direct lab homepage identifies Ahmed and MIT Mechanical Engineering. [Lab publication listing](https://web.mit.edu/decode/www/publications/) supplies research-level detail; distinguish papers from patent applications when importing records. |
| MIT | [Device Research Lab](https://drl.mit.edu/) — Evelyn N. Wang | Heat/mass transport, thermal management, solar thermal systems, water harvesting and desalination | Search-indexed official lab content identifies Wang and Mechanical Engineering affiliation, supported by [MIT profile](https://oge.mit.edu/profiles/evelyn-wang/). Direct homepage fetch returned 502 in this session. Administrative titles in older profiles may be stale; no current department-head claim is made here. |
| Stanford | [Living Matter Lab](https://livingmatter.stanford.edu/) — Ellen Kuhl | Computational biomechanics, physics-based modeling and machine learning for living systems | Lab homepage directly readable. [Stanford faculty profile](https://bioengineering.stanford.edu/people/ellen-kuhl) confirms Mechanical Engineering affiliation and living-matter research. [Full Stanford profile](https://cap.stanford.edu/profiles/frdActionServlet?choiceId=printerprofile&profileId=9528&profileversion=full) describes constitutive neural networks and automated model discovery. |
| Stanford | [Mani Research Lab](https://web.stanford.edu/~alimani/) — Ali Mani | Turbulent transport, fluid flow, high-fidelity numerical simulation and predictive modeling | [Official Mechanical Engineering lab directory](https://me.stanford.edu/research-impact/labs) identifies the lab, PI and scope. [Stanford profile](https://cap.stanford.edu/profiles/frdActionServlet?choiceId=printerprofile&profileId=47677&profileversion=full) confirms affiliation and direct lab URL. Direct lab fetch returned no readable text, so research details rely on the directory/profile. |

## KAIST roster evidence

- The [department homepage](https://me.kaist.ac.kr/) returned no readable text through the web fetch tool. This does not establish that the website is down in an interactive browser. A current full official faculty directory was not verified.
- The search index exposes an official [2024 Mechanical Engineering Biennial Report](https://me.kaist.ac.kr/download/2024%20KAIST%20ME_Biennial%20Report.pdf) with professor/lab tables and research summaries. It is a historical reconciliation source, not a current roster. The PDF was located through indexed excerpts, not fully audited page by page.
- That report calls Ryu's group “Multiscale Mechanics and Materials Modeling Laboratory”; the currently readable lab site uses AiM⁴ Lab. Preserve the former name as a source-dated alias if enriching the dataset.
- The [KAIST College of Engineering faculty statistics](https://engineering.kaist.ac.kr/content?menu=75) report 58 Mechanical Engineering faculty as of February 2026. This differs from the project's 61 inferred author entries. The dates and populations differ, so the difference alone does not identify incorrect entries.

## Implications for the directory

1. Store official lab names and direct lab URLs separately from PI profile URLs; preserve aliases and source dates.
2. Keep author-match confidence separate from verified faculty membership and verified lab identity. The present “reliable” count should not be read as independently confirmed laboratories.
3. Reconcile KAIST entries against official faculty evidence individually before replacing its unofficial-roster flag.
4. Retain publication-derived area classifications as inferred metadata. Official lab descriptions can supply complementary topics and reveal changes in research direction.

This note provides candidate enrichment evidence only; it does not alter rankings, paper counts, or existing lab classifications.
