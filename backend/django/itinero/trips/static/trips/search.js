var debounceTimer;
var cityInput = document.getElementById('cityStateInput');
var cityList = document.getElementById('cityList');

function titleCase(str) {
    return str.toLowerCase().split(' ').map(function(word) {
        return word.replace(word[0], word[0].toUpperCase());
    }).join(' ');
}

function handleInput() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(searchLocations, 300); // Adjust the delay as needed
}

function searchLocations() {
    const inputElement = document.getElementById("cityStateInput");
    const query = inputElement.value;

    if (!query) {
        cityList.innerHTML = "";
        return;
    }

    fetch(`/trips/search_locations/?query=${query}`)
        .then(response => response.json())
        .then(data => {
            cityList.innerHTML = "";  

            data.locations.forEach(location => {
                const li = document.createElement("li");
                li.textContent = titleCase(location.full_name);  // Capitalize the first letter of each word
                li.addEventListener('click', function() {
                    inputElement.value = this.textContent;
                    cityList.innerHTML = ""; // Clear the list
                });
                cityList.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
}


// Listen for input events
cityInput.addEventListener('input', handleInput);

// Add an event listener to hide the list when the input loses focus
cityInput.addEventListener("blur", function () {
    // Hide the list after a short delay to allow for click event to register
    setTimeout(function () {
        cityList.style.display = 'none';
    }, 200); // Delay in milliseconds
});

// Add back the display style when the input is in focus or when there are inputs
cityInput.addEventListener("focus", function () {
    if (cityInput.value.length > 0) {
        cityList.style.display = 'block';
    }
});

cityInput.addEventListener("input", function () {
    if (cityInput.value.length > 0) {
        cityList.style.display = 'block';
    } else {
        cityList.style.display = 'none';
    }
});