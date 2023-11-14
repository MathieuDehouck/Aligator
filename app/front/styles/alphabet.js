// Récupérer le prenom en API
var textField = document.getElementById('prenom-api');

// Gestionnaire d'événements pour le clavier
var keyboard = document.getElementById('keyboard');
keyboard.addEventListener('click', function(event) {
	var clickedElement = event.target;

	// Si l'élément cliqué est bien un bouton
	if (clickedElement.matches('li')) {
		var character = clickedElement.textContent;

		// Insérer le caractère dans le champ texte cible
		insertCharacter(character);
	}
});

// Fonction pour insérer le caractère dans le champ texte cible
function insertCharacter(character) {
	var start = textField.selectionStart;
	var end = textField.selectionEnd;

	var text = textField.value;
	var newText = text.substring(0, start) + character + text.substring(end);

	textField.value = newText;

	// Rétablir la position du curseur après l'insertion
	var newCursorPosition = start + character.length;
	textField.setSelectionRange(newCursorPosition, newCursorPosition);
}

// Récupérer le clavier virtuel
var keyboard = document.getElementById('keyboard');

// Tableau de caractères de l'alphabet phonétique international en français avec caractères diacritiques et accents nasaux
var phoneticAlphabet = ['b', 'd', 'f', 'ɡ', 'k', 'l', 'm', 'n', 'ŋ', 'ɲ', 'p', 'ʁ', 's', 'ʃ', 't', 'v', 'z', 'ʒ',
'j', 'w', 'ɥ',
'a', 'ɑ', 'e', 'ə', 'ɛ', 'i', 'o', 'ɔ', 'ø', 'œ', 'u', 'y',
'~'];
//var phoneticAlphabet = ['ɑ', 'b', 'd', 'ə', 'ɛ', 'f', 'ɡ', 'i', 'k', 'l', 'm', 'n', 'ɔ', 'o', 'p', 'ʁ','s', 'ʃ', 't', 'u', 'v', 'w', 'j', 'z','æ', 'ø', 'œ', 'ɥ', 'ɲ', 'ç', 'ʒ', 'ŋ','ã', 'ẽ', 'ĩ', 'õ', 'ũ'];

// Générer les boutons pour chaque caractère et les ajouter au clavier virtuel
phoneticAlphabet.forEach(function(character) {
	var button = document.createElement('li');
	button.textContent = character;
	keyboard.appendChild(button);
});
