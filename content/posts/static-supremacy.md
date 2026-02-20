---
title: "Static Supremacy"
date: 2023-10-30T10:15:00-00:00
draft: false
tags: ["architecture", "hugo"]
---

Dynamic sites are fragile. Databases fail. Servers crash. PHP errors out.

Static sites are diamonds. They are immutable. They are cacheable. They are eternal.

## The Stack

-   **Generator**: Hugo. Written in Go. Compiles in milliseconds.
-   **Host**: GitHub Pages. Edge cached globally.
-   **CI/CD**: GitHub Actions. Automated deployment.

## Zero Runtime

This site has zero server-side runtime. No database queries on page load. No API calls to render content. 

When you request this page, you are downloading a pre-computed file. The server does no work. The database does not exist.

This is the only scalable architecture.
