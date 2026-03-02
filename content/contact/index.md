---
title: Contact
date: 2022-10-24
type: landing

sections:
  - block: markdown
    content:
      title: Contact
      text: |
        **Vicente Herranz Pérez**  
        Jeroni Muñoz Research Building — Lab 1.63  
        Universitat de València  
        Av. Vicent Andrés Estellés, 19  
        46100 Burjassot (Valencia)  
        Spain

        **E-mail:** <a id="email-link" href="#" rel="nofollow">click to reveal</a>  
        **Tel:** +34 9635 44637

        <script>
          (function () {
            const user = "vicente.herranz";
            const domain = "uv.es";
            const email = user + "@" + domain;
            const a = document.getElementById("email-link");
            if (a) {
              a.href = "mailto:" + email;
              a.textContent = email;
            }
          })();
        </script>
    design:
      columns: "1"
      background:
        image:
          filename: contact.jpg
          filters:
            brightness: 1
          parallax: false
          position: center
          size: cover
          text_color_light: true
      spacing:
        padding: ["20px", "0", "20px", "0"]
      css_class: fullscreen
---
