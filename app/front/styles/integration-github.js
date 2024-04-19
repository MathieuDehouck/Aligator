fetch('https://raw.githubusercontent.com/MathieuDehouck/Aligator/main/README.md')
  .then(response => {
    if (!response.ok) {
      throw new Error('La requête n\'a pas abouti. Assurez-vous que le dépôt Github et le fichier README existent et sont publics.');
    }
    return response.text();
  })
  .then(data => {
    // On utilise marked.js pour convertir le Markdown en HTML
     const htmlContent = marked.parse(data);

    // On affiche le contenu HTML dans la page HTML
    document.getElementById('readme').innerHTML = htmlContent;
  })
  .catch(error => {
    console.error('Erreur lors de la récupération du README :', error);
    // Gestion de l'erreur ici : affichage d'un message d'erreur sur la page
    document.getElementById('readme-content').innerHTML = 'Erreur : Impossible de charger le README.';
  });
