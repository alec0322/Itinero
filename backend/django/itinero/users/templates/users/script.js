const searchInput = document.getElementById('search-input');
const resultsList = document.getElementById('results-list');

// Load the JSON data
fetch('cities.json')
    .then(response => response.json())
    .then(data => {
        // Store the city data
        const cities = data;

        // Listen for input in the search field
        searchInput.addEventListener('input', () => {
            const searchTerm = searchInput.value.trim().toLowerCase();
            displayResults(searchTerm);
        });

        // Display search results based on the search term
        function displayResults(searchTerm) {
            resultsList.innerHTML = ''; // Clear previous results

            // Filter cities based on the search term
            const filteredCities = cities.filter(city => city.city_ascii.toLowerCase().includes(searchTerm));

            // Populate the results list
            filteredCities.forEach(city => {
                const listItem = document.createElement('li');
                listItem.textContent = city.city;
                listItem.addEventListener('click', () => {
                    searchInput.value = city.city;
                    resultsList.style.display = 'none';
                });
                resultsList.appendChild(listItem);
            });

            // Show or hide the results list
            if (filteredCities.length > 0) {
                resultsList.style.display = 'block';
            } else {
                resultsList.style.display = 'none';
            }
        }
    });