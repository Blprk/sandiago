---
title: "The 10KB Budget"
date: 2023-10-29T14:30:00-00:00
draft: false
tags: ["performance", "optimization"]
---

I set a hard limit for this site: **10KB** for all critical assets. 

If it doesn't fit, it doesn't ship.

## The Breakdown

1.  **HTML**: < 2KB (Gzipped). Semantics only. No wrapper div soup.
2.  **CSS**: < 3KB. Inline critical styles. Variables for theming. No frameworks.
3.  **JS**: < 1KB. Search logic only. Lazy loaded on interaction.
4.  **Images**: SVG where possible. WebP compression for rasters.

## Why 10KB?

Because TCP slow start. 

The first round-trip of a TCP connection sends about 14KB of data. If your site fits in that first packet, you achieve instant rendering. You beat the speed of light (latency).

Performance isn't a feature. It's the baseline.
