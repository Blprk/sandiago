(function() {
    const input = document.getElementById('search-input');
    const results = document.getElementById('search-results');
    let data = [];

    async function loadData() {
        if (data.length === 0) {
            const response = await fetch('/index.json');
            data = await response.json();
        }
    }

    input.addEventListener('focus', loadData);

    input.addEventListener('input', function(e) {
        const term = e.target.value.toLowerCase();
        results.innerHTML = '';
        if (term.length < 2) return;

        const matches = data.filter(item => 
            item.title.toLowerCase().includes(term) || 
            (item.tags && item.tags.some(tag => tag.toLowerCase().includes(term)))
        ).slice(0, 5);

        matches.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="${item.permalink}">${item.title} <small>${item.date}</small></a>`;
            results.appendChild(li);
        });
    });

    document.addEventListener('click', function(e) {
        if (e.target !== input && e.target !== results) {
            results.innerHTML = '';
        }
    });
})();
