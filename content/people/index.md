---
title: People
date: 2026-03-20
type: landing

sections:
  # =============================
  # LAB MEMBERS / ALUMNI (CARDS)
  # =============================
  - block: people
    content:
      title: People

      user_groups:
        - Lab Members
        - Alumni

      sort_by: Params.weight
      sort_ascending: true

    design:
      show_interests: false
      show_role: true
      show_social: false

  # =============================
  # COLLABORATORS (LIST)
  # =============================
  - block: markdown
    content:
      title: Collaborators
      text: |
        <ul class="collaborators-list">
          <li><a href="https://www.ucsf.edu/" target="_blank" rel="noopener noreferrer">Arturo Álvarez-Buylla</a> (University of California San Francisco)</li>
          <li><a href="https://www.doshisha.ac.jp/en/" target="_blank" rel="noopener noreferrer">Naoko Kaneko</a> (Doshisha University)</li>
          <li><a href="https://www.ucsf.edu/" target="_blank" rel="noopener noreferrer">Mercedes Paredes</a> (University of California San Francisco)</li>
          <li><a href="https://english.nagoya-cu.ac.jp/" target="_blank" rel="noopener noreferrer">Kazunobu Sawamoto</a> (Nagoya City University)</li>
          <li><a href="https://www.sorrellslab.com/" target="_blank" rel="noopener noreferrer">Shawn Sorrells</a> (University of Pittsburgh)</li>
        </ul>

    design:
      columns: "1"
    advanced:
      css_class: "collaborators-section"
---