/* frontend/js/scripts.js */

document.addEventListener('DOMContentLoaded', () => {
    const message = document.createElement('p');
    message.textContent = 'Welcome to your Django app!';
    document.body.appendChild(message);
});
// Fonction pour afficher la section correspondante lorsqu'on clique sur un onglet
function showSection(sectionId) {
    // Masquer toutes les sections
    const sections = document.querySelectorAll('.tab-content');
    sections.forEach(section => section.classList.remove('active'));

    // Afficher la section sélectionnée
    const activeSection = document.getElementById(sectionId);
    activeSection.classList.add('active');
}