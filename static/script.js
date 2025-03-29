document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.getElementById("searchForm");
    if (searchForm) {
        searchForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const query = document.getElementById("searchQuery").value;
            
            fetch(`/search?query=${query}`)
                .then(response => response.text())
                .then(data => {
                    document.getElementById("searchResults").innerHTML = data;
                });
        });
    }
});
