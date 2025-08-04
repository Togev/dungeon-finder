document.addEventListener('DOMContentLoaded', function() {
    const lookingForPlayersCheckbox = document.getElementById('id_looking_for_players');
    const numPlayersRow = document.getElementById('num-players-row');
    function toggleNumPlayers() {
        if (lookingForPlayersCheckbox && numPlayersRow) {
            if (lookingForPlayersCheckbox.checked) {
                numPlayersRow.style.display = '';
            } else {
                numPlayersRow.style.display = 'none';
            }
        }
    }
    toggleNumPlayers();
    if (lookingForPlayersCheckbox) {
        lookingForPlayersCheckbox.addEventListener('change', toggleNumPlayers);
    }

    const tableSelect = document.getElementById('id_table_select');
    const newTableFields = document.getElementById('new-table-fields');
    function toggleNewTableFields() {
        if (tableSelect) {
            if (tableSelect.value === '__new__') {
                newTableFields.style.display = 'block';
            } else {
                newTableFields.style.display = 'none';
            }
        }
    }
    toggleNewTableFields();
    if (tableSelect) {
        tableSelect.addEventListener('change', toggleNewTableFields);
    }
});