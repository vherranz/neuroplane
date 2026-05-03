---
title: People
date: 2026-03-20
type: landing

sections:
  # =============================
  # LAB MEMBERS
  # =============================
  - block: people
    content:
      title: Lab Members
      user_groups:
        - Lab Members
      sort_by: Params.weight
      sort_ascending: true

    design:
      show_interests: false
      show_role: true
      show_social: false
      spacing:
        padding: ["3rem", "0", "1rem", "0"]

  # =============================
  # ALUMNI
  # =============================
  - block: people
    content:
      title: Alumni
      user_groups:
        - Alumni
      sort_by: Params.weight
      sort_ascending: true

    design:
      show_interests: false
      show_role: true
      show_social: false
      spacing:
        padding: ["1rem", "0", "1rem", "0"]

  # =============================
  # COLLABORATORS
  # =============================
  - block: markdown
    content:
      title: Collaborators
      text: |
        <ul class="collaborators-list">
          <li><a href="https://ablab.ucsf.edu" target="_blank" rel="noopener noreferrer">Arturo Álvarez-Buylla</a> <span>University of California San Francisco</span></li>
          <li><a href="https://www.uv.es/persona/pavon" target="_blank" rel="noopener noreferrer">Carmen Agustín Pavón</a> <span>Universitat de València</span></li>
          <li><a href="https://reitergroup.ucsf.edu/" target="_blank" rel="noopener noreferrer">Jeremy Reiter</a> <span>University of California San Francisco</span></li>
          <li><a href="https://k-sawamoto.com/#" target="_blank" rel="noopener noreferrer">Kazunobu Sawamoto</a> <span>Nagoya City University</span></li>
          <li><a href="https://www.uv.es/doreal/index.html" target="_blank" rel="noopener noreferrer">Lucía Hipólito Cubedo</a> <span>Universitat de València</span></li>
          <li><a href="http://vicentresearchlab.com/" target="_blank" rel="noopener noreferrer">María Jesús Vicent</a> <span>Centro de Investigación Príncipe Felipe</span></li>
          <li><a href="https://paredeslab.ucsf.edu" target="_blank" rel="noopener noreferrer">Mercedes Paredes</a> <span>University of California San Francisco</span></li>
          <li><a href="https://brainscience.doshisha.ac.jp/br/en/introduction/pat/nr.html" target="_blank" rel="noopener noreferrer">Naoko Kaneko</a> <span>Doshisha University</span></li>
          <li><a href="https://sites.google.com/view/sorrells-lab/home" target="_blank" rel="noopener noreferrer">Shawn Sorrells</a> <span>University of Pittsburgh</span></li>
          <li><a href="https://www.cabimer.es/en/vivian-capilla-gonzalez/" target="_blank" rel="noopener noreferrer">Vivian Capilla González</a> <span>CABIMER</span></li>
        </ul>

    design:
      columns: "1"
      spacing:
        padding: ["1rem", "0", "2rem", "0"]

    advanced:
      css_class: "collaborators-section"
---
