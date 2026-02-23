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
      text: |
        The NeuroPlaNe Lab investigates neural stem cells and populations of immature neurons with prolonged maturation in the mammalian brain.

        Our research integrates developmental neurobiology, comparative neuroscience, and translational approaches to better understand human brain development and neurological disorders.

        Based at the Universitat de València, we combine histological, molecular, and advanced imaging strategies to study neural progenitors, amygdala organization, and neurodevelopmental pathologies such as Rett syndrome.

  - block: markdown
    content:
      title: Research Areas
      text: |
        **Human Brain Development**  
        Development of neural progenitors arising from the caudal ganglionic eminence and their contribution to cortical and limbic circuitry.

        **Paralaminar Nucleus of the Amygdala**  
        Comparative and functional organization of the paralaminar nucleus across species.

        **Immature Neurons and Rett Syndrome**  
        Protracted neuronal maturation and its vulnerability in neurodevelopmental disorders.
    design:
      columns: '1'

  - block: collection
    content:
      title: Latest News
      count: 3
      filters:
        page_type: post
      order: desc
    design:
      view: card
      columns: '1'

  - block: collection
    content:
      title: Selected Publications
      count: 5
      filters:
        folders:
          - publication
    design:
      view: citation
      columns: '1'

  - block: markdown
    content:
      text: |
        {{% cta cta_link="./people/" cta_text="Meet the team →" %}}
    design:
      columns: '1'
---
