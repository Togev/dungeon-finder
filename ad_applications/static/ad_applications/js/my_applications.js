document.addEventListener('click', function(e) {
    const tab = e.target.closest('.tab-btn');
    const pageLink = e.target.closest('.pagination-link');

    if (tab) {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active-tab'));
        tab.classList.add('active-tab');

        const type = tab.dataset.type;
        loadApplications(type, 1);
    }

    if (pageLink) {
        e.preventDefault();
        const type = pageLink.dataset.type;
        const page = pageLink.dataset.page;
        loadApplications(type, page);
    }
});

function loadApplications(type, page) {
    fetch(`/applications/my_applications/ajax/?type=${type}&page=${page}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('application-list').innerHTML = data.html;
        })
        .catch(error => {
            console.error('Error loading applications:', error);
            document.getElementById('application-list').innerHTML = '<p>Error loading data.</p>';
        });
}