document.addEventListener('DOMContentLoaded', function() {
    const lookingForPlayersCheckbox = document.getElementById('id_looking_for_players');
    const numPlayersRow = document.getElementById('num-players-row');

    function toggleNumPlayers() {
        if (lookingForPlayersCheckbox.checked) {
            numPlayersRow.style.display = '';
        } else {
            numPlayersRow.style.display = 'none';
        }
    }
    toggleNumPlayers();
    lookingForPlayersCheckbox.addEventListener('change', toggleNumPlayers);
});