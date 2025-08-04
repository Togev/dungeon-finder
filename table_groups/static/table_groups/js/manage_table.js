document.addEventListener('DOMContentLoaded', function() {
    const dropdown = document.getElementById('memberDropdown');
    if (dropdown) {
        const actionBlocks = document.querySelectorAll('.member-actions-block');
        actionBlocks.forEach(block => block.style.display = 'none');
        dropdown.addEventListener('change', function() {
            actionBlocks.forEach(block => {
                block.style.display = (block.id === dropdown.value) ? 'block' : 'none';
            });
        });
    }
});