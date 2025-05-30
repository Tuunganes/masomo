/* frontend/js/scripts.js */

/* ------------------------------------------------------------------
   TAB HANDLER – show / hide .tab-content sections
------------------------------------------------------------------- */
function showSection(sectionId) {
    // hide all sections
    document.querySelectorAll('.tab-content')
             .forEach(s => s.classList.remove('active'));
  
    // show the one we clicked
    const active = document.getElementById(sectionId);
    if (active) active.classList.add('active');
  }
  