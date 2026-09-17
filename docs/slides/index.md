# Presentations

**No presentation is published yet.** Each session's slides are supplied by the
person who gives it, and appear on the site as soon as the file is in place.

---

## How a presentation appears

Every session already has an empty placeholder waiting for it, named after the
session itself:

```
docs/downloads/Day1/1400_ai-infrastructure_EN-inactif.pdf
```

Name your file exactly the same, **minus `-inactif`**, drop it in that folder, and
rebuild. A download button appears under the session on its day page.

```bash
python tools/downloads.py            # the name expected for every session
python tools/downloads.py --missing  # only what is still needed
python tools/build_site.py           # publish what you have dropped
```

PDF and PowerPoint are both accepted, in English and in French, and any subset is
fine. Several files for one session are distinguished by a number — the full
convention is in `docs/downloads/HOW-TO-ADD-FILES.txt`.

---

## Where the buttons show up

Not here. A presentation belongs to a session, so its buttons appear on the day
page, directly under the session it supports:

[Day 1](../day1/index.md){ .md-button } [Day 2](../day2/index.md){ .md-button }
[Day 3](../day3/index.md){ .md-button } [Day 4](../day4/index.md){ .md-button }
[Day 5](../day5/index.md){ .md-button }

This page stays as the entry point and will list the decks once they exist.

---

## Notes for facilitators

!!! info "The built reveal.js decks are switched off"

    The repository also carries a small slide system that builds browser decks
    from bilingual sources under `slides/decks/`. It is disabled while the
    workshop runs on supplied presentations:

    ```yaml
    # config/workshop.yml
    site:
      publish_slides: false
    ```

    Set it to `true` and run `python tools/build_slides.py` to publish them. The
    sources are untouched — nothing was deleted.

!!! tip "Presenting without a network"

    A supplied PDF or PowerPoint needs nothing but the file itself. If you use
    the built decks instead, run `python tools/vendor_reveal.py` beforehand so
    they do not depend on a CDN; the venue network is not a safe assumption.
