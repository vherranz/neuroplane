---
# Leave the homepage title empty to use the site title
title:
date: 2024-01-01
type: landing

sections:
  - block: hero
    content:
      title: |
        NeuroPlaNe Lab
        Neurogénesis y Plasticidad Neural
      text: ""
      cta: []
    design:
      spacing:
        padding: ["6rem","0","4rem","0"]
      background:
        gradient_start: "#4f51e8"
        gradient_end: "#00c2ff"
        gradient_angle: 135

  - block: markdown
    content:
      title: ""
      text: |
        NeuroPlaNe is a neuroscience research group at the **Universitat de València** (Valencia, Spain).
        We investigate neural stem cells and populations of immature neurons with prolonged maturation, using comparative approaches across mammalian species.
        Based at the **Institut Cavanilles** (Campus Burjassot-Paterna), we combine histology, molecular methods, and advanced microscopy to study brain development, circuit plasticity, and neurodevelopmental disorders.

    design:
      columns: '1'

  - block: collection
    content:
      title: Latest news
      count: 3
      filters:
        page_type: post
      order: desc
    design:
      view: card
      columns: '1'
---
