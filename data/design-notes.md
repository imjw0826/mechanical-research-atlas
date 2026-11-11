# Design notes for a data-heavy research directory

Inspected 9 November 2026. These notes distinguish live visual observations, computed browser values, displayed code, and recommendations. Desktop inspection only; this was not a full accessibility, responsive, or performance audit.

## 1. transitions.dev

Official site: https://transitions.dev/
Library inspected: https://transitions.dev/library.html

### Observed visual language

- **Typography:** Inter body text with a Saans heading stack. Computed body size 16px; detail-page heading 36px, weight 500. Clean sans-serif, large restrained headings, smaller gray supporting labels.
- **Palette/theme:** inspected light presentation uses near-white background (#fdfdfd), near-black text (#0d0d0d), pale gray preview surfaces and muted metadata. Color is subordinate to the demos. A dark presentation was not inspected.
- **Spacing/density:** generous page margins and gaps; desktop library is a four-column preview grid. Each card dedicates substantial space to one isolated interaction, followed by a title/description. Documentation uses a narrow navigation rail beside a large preview/code area. This is a demonstration gallery, not a dense directory layout.
- **Radius/borders:** library articles measured 24px radius, without a conventional border. Rounded light-gray preview panels and pill controls dominate. The tabs recipe specifies a 48px radius; tooltip recipe specifies 8px with a faint outline/elevation shadow.
- **Components:** preview cards, category tabs (All, Essential, AI Agents, Effects, Texts, Pro), sort control, a Search/⌘K entry point, and Preview/CSS/React tabs on detail pages. No data table or faceted research filter was inspected. The search entry was observed, not its resulting command dialog.

### Concrete motion recipes

These values were read from the site's displayed **CSS tabs**, not inferred from appearance. The common easing below is **cubic-bezier(0.22, 1, 0.36, 1)**.

- [Card resize](https://transitions.dev/detail.html?t=card-resize): width and height tween over **300ms**, common easing.
- [Menu dropdown](https://transitions.dev/detail.html?t=menu-dropdown): origin-aware scale plus opacity; **250ms open / 150ms close**, common easing. Starts at **0.97** scale; closes toward **0.99**. Supports top/bottom, left/center/right origins.
- [Modal open/close](https://transitions.dev/detail.html?t=modal-open-close): centered opacity/scale transition, **0.96 to 1**, **250ms open / 150ms close**, common easing.
- [Panel reveal](https://transitions.dev/detail.html?t=panel-reveal): Y translation, opacity and **2px to 0 blur** together; **400ms open / 350ms close**, common easing. Default travel is **calc(187px * 0.5)**, not a universal panel distance.
- [Tabs sliding](https://transitions.dev/detail.html?t=tabs-sliding): active white pill changes horizontal position and width in **250ms**, common easing; text color uses the same clock. Recipe specifies 3px bar padding/gap and 30px tab height. Initial positioning should snap without animation.
- [Skeleton loader and reveal](https://transitions.dev/detail.html?t=skeleton-loader-and-reveal): **1000ms** pulse, **one** cycle by default, opacity down to **0.5**; then **400ms** cross-fade/cross-blur using **ease-in-out**, with **2px** blur. Skeleton and content share the same coordinates to avoid layout movement.
- [Accordion](https://transitions.dev/detail.html?t=accordion): grid rows **0fr to 1fr**, opacity/unblur, and a vertically flipping chevron; **250ms expand, collapse and chevron**, common easing.
- [Tooltip open/close](https://transitions.dev/detail.html?t=tooltip-open-close): **80ms appearance delay**, **150ms in / 50ms out**, both **ease-out**; scale **0.98 to 1**. A shared tooltip travels/resizes between triggers in **160ms**, common easing. The label says “instant out,” but the CSS actually specifies 50ms and no exit delay.
- [Toast open/close](https://transitions.dev/detail.html?t=toast-open-close): rises **16px**, fades/unblurs from **2px**, scales **0.97 to 1**; **350ms open / 250ms close**, common easing.

All nine inspected recipes include a prefers-reduced-motion rule disabling their transitions/animations. Several clicked preview controls did not visibly change state in this browser; these are verified displayed recipes, not a claim of successful playback or measured runtime timing. Other library entries, including confetti, gooey menus and 3D counters, were visible in the catalog but not code-audited.

**Directory direction:** borrow tab-indicator movement, anchored-menu transitions, loading cross-fades and brief confirmation toasts. Avoid celebratory effects, rolling result counts, and repeated blur/stagger on research rows. Keep comparison content stable.

## 2. shadcn/ui

Official site: https://ui.shadcn.com/
Inspected homepage, component index, and these live documentation pages:
- https://ui.shadcn.com/docs/components/base/data-table
- https://ui.shadcn.com/docs/components/base/command
- https://ui.shadcn.com/docs/components/base/tabs

### Observed visual language

- **Typography:** computed Geist body and headings. Table text **14px**. Strong hierarchy comes from weight, size and muted labels rather than decorative typography.
- **Palette/theme:** predominantly white, black and neutral gray. Light mode has faint gray borders and muted surfaces; dark mode was toggled and inspected, with near-black background, pale text and low-contrast dark surfaces. Dark border token is white at 10% opacity. No strong brand accent is necessary for the basic controls.
- **Spacing/density:** spacious documentation shell but compact actual controls. Table rows measured about **40.5px**, filter input **32px** high; sampled cell padding **8px 0 8px 8px**. Distinguish the roomy docs layout from the usable component density.
- **Radius/borders:** thin neutral outlines and horizontal rules; rounded input/button/card surfaces rather than heavy shadows. Sampled filter input radius **10px**; root radius token **0.625rem**. Homepage mixes outlined controls with rounded financial-summary and form cards.
- **Cards:** modular title/description/body/action compositions. Homepage examples combine balances, progress indicators, forms, charts and secondary metadata without large colored backgrounds.
- **Tables/filters:** live payment table includes selection checkboxes, status text, sortable Email header, right-aligned currency, row overflow actions, a Columns visibility menu, selection count and pagination controls. Typing “ken99” actually reduced five rows to one. Columns opened checked status/email/amount options. This is a text-column filter, not an inspected multi-facet directory filter.
- **Tabs:** muted rounded segmented track with a light active tab, plus documented/live underline, vertical, icon and disabled variants. Switching Overview to Analytics changed both selected state and panel content.
- **Command menus:** opened the Command Palette demo. Search above grouped Suggestions/Settings, leading icons, muted group labels, right-aligned keyboard shortcuts and a highlighted selected row. The command list sits in a rounded modal over a dimmed page.

**Directory direction:** strongest baseline for a comparison-first interface: table, persistent search/filter toolbar, visible sorting and selection, neutral status labels, optional contextual tabs and keyboard jump search. The Data Table page is a composition guide using TanStack Table, not a single turnkey large-directory component.

## 3. Arc UI: identity is ambiguous

Two distinct official projects were found and visited. I cannot determine which was intended from the name alone:

- **Arc UI, React library:** https://uiarc.dev/
- **ARC UI, ARC Radiant Components, Lit library:** https://arcui.dev/

The React library is the closer match to the accompanying shadcn/ui and affectUI references, so it received the deeper component inspection. Their features and styles must not be conflated.

### Arc UI at uiarc.dev: observed

Inspected:
- https://uiarc.dev/components/button
- https://uiarc.dev/components/sortable-data-table
- https://uiarc.dev/components/filter-toolbar
- https://uiarc.dev/components/tabs
- https://uiarc.dev/components/card
- Site-wide command search, opened from the documentation shell.

- **Typography:** Inter body **16px/22.4px**; Geist documentation heading **40px**, weight **500**, letter-spacing **-1.2px**. Table cells **14px/19.6px**.
- **Palette/theme:** quiet monochrome light UI, white surfaces, near-black text, gray rules and restrained status treatments. Dark mode was tested: charcoal background, slightly lighter table surface, pale type and subtle gray borders. Light mode was restored.
- **Spacing/density:** comfortable, not maximum density. Sample table rows **52px**, sampled cell padding **0 16px 0 8px**. Documentation has searchable left navigation, central examples and right contents rail.
- **Radius/borders:** table enclosure **18px** radius with **1px oklch(0.935 0 0)** border; row dividers **1px oklch(0.965 0 0)**. Demo card **26px** radius, **20px** content padding, **340px** wide. Tab buttons **36px** high, 12px horizontal padding, sampled radius **15px**.
- **Table:** “Project health” with Project, Owner, Status, Due and Score; checkbox selection, dot/text status pills and record-count footer. Clicking Project actually sorted alphabetically and announced ascending order. Documentation explicitly says this table is **not virtualized** and uses client-side sorting.
- **Filters:** removable “Status · In review” and “Owner · Emma Collins” chips, Add filter and Clear all. Opened a two-stage field/value menu: Status/Owner/Due date/Priority, then Urgent/High/Medium/Low. This separate demo was not proven connected to the table.
- **Tabs:** Overview/Activity/Settings; switching to Activity changed selection and content.
- **Command search:** working site palette with search, Esc close, descriptive result snippets and Pages/Docs/Components/Blocks groupings. Searching “table” returned ten results. Measured dialog wrapper width **620px**.
- **Cards:** media/title/description/byline/status/Save composition. Clicking “Lobby lounge” opened a contextual dialog. Media showed fallback text, so an actual photo was not successfully verified. Documented spring/hover effects were not timing-measured.

**Directory direction:** use its removable query chips, categorized command results and contextual quick-look dialog. Prefer denser rows than its 52px sample when comparing many records. Pro data grids and tree tables appeared in navigation/search but were not inspected.

### Separate ARC UI at arcui.dev: homepage only

- **Typography:** Host Grotesk; computed body **17px/28.9px**; queried heading **34px/34px**, weight **700**. More geometric and emphatic than the React library.
- **Palette/theme:** pale lavender-gray background **rgb(242,242,248)**, gray text **rgb(76,79,99)**, blue **#2756d7** and teal **#0f766e** accent values shown in its playground. Glow is part of its stated visual positioning. Auto-theme control was present; dark mode was not tested here.
- **Spacing/density:** homepage playground exposes **Compact / Default / Roomy** choices, not tested. Samples include segmented Day/Week/Month controls, badges, progress and pagination.
- **Radius/borders/components:** compact rounded controls were visible; exact radius/border tokens were not measured. No dedicated table, filter or command-menu implementation was inspected for this separate library.

**Directory direction:** explicit density settings are useful inspiration. Do not attribute them to uiarc.dev.

## 4. Affect UI / affectUI

Official site identified and visited: https://www.affectui.com/
Inspected live demos, all in the default **Clean** style:
- https://www.affectui.com/components/data-table
- https://www.affectui.com/components/filter-menu
- https://www.affectui.com/components/segmented-control
- https://www.affectui.com/components/command-menu
- https://www.affectui.com/components/project-card

### Observed visual language

- **Typography:** Inter/InterVariable. Homepage heading **56px/60px**, weight **500**, letter-spacing **-2px**. Component/table/filter text **13px/20px**; table headers **12px/16px**, weight **500**, muted black at 61% opacity.
- **Palette/theme:** white, near-black and gray, with small colored category/status pills, logos and avatars. Dark mode was actually inspected on Segmented Control and Command Menu: charcoal surfaces, pale text and subtle separators.
- **Spacing/density:** homepage is spacious; product components are notably tighter. Table rows **40px**, headers **36px**, filter option rows approximately **35.2px**.
- **Radius/borders:** table surface **10px** radius, no conventional border; a **0.5px shadow outline** and very faint elevation define its edge. Filter options have **6px** radius. Overall softer and less heavily boxed than an enterprise spreadsheet.
- **Table:** “Design Stack” with selection, Tool, Category, Website and Renewal date; tool logos, colored category pills, understated links, muted header band, fine row separators, Add row footer and undo/redo controls. Clicking Tool actually sorted Figma, Framer, Linear, Loom and Vercel alphabetically. Editing/clipboard/undo behavior was not tested.
- **Filters:** grouped Stage/Deal size/Region sections with checkboxes, counts, chevrons, removable chips and Clear all. Selecting Proposal sent updated the checkbox, Stage count and chips; overflow compacted to “+1.”
- **Tabs:** Segmented Control demonstrates dashboard chips with a notification count, an icon/label layout tray, and underline billing switch. Active state is a quiet gray fill or raised light pill. Selecting Analytics changed selection; this example did not render associated dashboard content.
- **Command menu:** search above grouped commands, app icons, secondary descriptions, shortcut keycaps and a gray active row. Typing “report” returned Reports and an assistant suggestion, “Ask assistant about ‘report’.” Actual matches and AI suggestions coexist.
- **Cards:** Project Card combines progress ring, title, status pill, due date and overlapping initial avatars. Summary click revealed five checklist items and Open; choosing Done in the status menu updated the summary. Expansion grows downward instead of opening a separate detail panel.

Main demos were accessible. Table, Command Menu and Project Card source/additional examples were Pro-gated; unseen paid examples are not part of these observations. Classic style and mobile layouts were not tested. The small table demo is not evidence of large-dataset readiness; its documentation recommends virtualization, filtering and server paging for thousands of rows.

**Directory direction:** borrow its compact table scale, grouped faceted filters and quiet selected states. Keep every important active filter discoverable rather than concealed behind +N. Separate matching records from assistant suggestions. Avoid downward-growing cards in a tightly aligned comparison grid.

## Recommended combined direction

These are proposed design decisions, not facts claimed about all four sites:

1. **Foundation:** shadcn-style neutral, comparison-first table; default around 40px rows, 13-14px text, optional comfortable density. Use a readable sans-serif and tabular numerals for numeric comparisons.
2. **Layout:** persistent directory navigation, a compact query toolbar, results count and table, with optional right-side record details. Cards are an alternate browse mode, not the only way to compare records.
3. **Query UI:** Arc's removable field/value chips plus Affect's grouped checkbox facets; visible reset and unambiguous active-filter counts. Preserve search/filter state when viewing a record.
4. **Surfaces:** fine gray separators, modest 8-12px control/panel radii and minimal elevation. Avoid applying 24-26px showcase-card radii to every dense table region.
5. **Color:** neutral background and typography; reserve restrained accent/status colors for meaning, and always include text labels. Support a deliberately tuned dark theme rather than simply inverting colors.
6. **Navigation:** contextual tabs and categorized command search as secondary accelerators, not replacements for visible navigation or primary record search.
7. **Motion:** use 150-250ms menu/tab feedback as the starting point, specific verified recipes where useful, immediate stable results, no decorative row choreography, and reduced-motion support. The 400ms reveal recipes are references, not mandatory delays before showing data.
8. **Scale:** separately implement and test server-side queries, pagination or virtualization, sorting semantics, keyboard behavior, loading/empty/error states and accessible focus handling. Polished five-row demos do not establish those capabilities.
