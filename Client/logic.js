var user_id = -1;
var book_id = -1;

user_id = getParameterByName('user');

async function attemptLogin() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'username': username,
                'password': password
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const responseData = await response.json();
        console.log('Response Data:', responseData);

        user_id = responseData['user_id'];
        alert(user_id);

        // Save the response data to a variable or perform other actions
        alert('POST request successful! Check the console for response data.');

        window.location.href = 'home.html?user=' + user_id;

    } catch (error) {
        console.error('Error:', error);
        alert('Error occurred. Check the console for details.');
    }
}

async function borrowBook() {
     if (book_id == -1) {
        alert('No book selected.');
        return;
    }
     // Make a POST request to the server to add the user
    fetch('http://127.0.0.1:5000/borrow_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
       body: JSON.stringify({
            'user_id': user_id,
            'book_id': book_id
       }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // You can perform additional actions upon successful borrow addition
    })
    .catch(error => {
        alert('Error adding borrow. Check the console for details.');
        console.error('Error:', error);
    });

}

async function returnBook() {
     if (book_id == -1) {
        alert('No book selected.');
        return;
    }
     // Make a POST request to the server to add the user
    fetch('http://127.0.0.1:5000/return_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
       body: JSON.stringify({
            'user_id': user_id,
            'book_id': book_id
       }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // You can perform additional actions upon successful borrow addition
    })
    .catch(error => {
        alert('Error returning book. Check the console for details.');
        console.error('Error:', error);
    });

}

async function getBorrowedBooks() {
    try {
        const response = await fetch('http://127.0.0.1:5000/get_borrowed_books_by_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'user_id': user_id
            }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const responseData = await response.json();

        const books = responseData['books'];

        // Display the books on the page
        displayBooks(books);

    } catch (error) {
        console.error('Error:', error);
        alert('Error occurred. Check the console for details.');
    }
}

async function getBooks() {

    var author_id = document.getElementById('author_id').value;

    alert(user_id);

    try {
        const response = await fetch('http://127.0.0.1:5000/get_books_by_author', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'author_id': author_id
            }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const responseData = await response.json();

        const books = responseData['books'];

        // Display the books on the page
        displayBooks(books);

    } catch (error) {
        console.error('Error:', error);
        alert('Error occurred. Check the console for details.');
    }
}

function displayBooks(books) {
    const bookListContainer = document.getElementById('bookList');

    // Clear previous content
    bookListContainer.innerHTML = '';

    // Create a table
    const table = document.createElement('table');
    table.style.width = '80%';  // Set the width of the table
    table.border = '1';

    // Create table headers
    const headers = ['Title','Author','Genre','Year'];
    const headerRow = document.createElement('tr');

    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.textContent = headerText;
        headerRow.appendChild(th);
    });

    table.appendChild(headerRow);

    // Populate the table with book information
    books.forEach(book => {
        const row = document.createElement('tr');

        // Save the book ID as a data attribute
        row.setAttribute('book_id', book.book_id);

        const titleCell = document.createElement('td');
        titleCell.textContent = book.title;
        row.appendChild(titleCell);

        const authorIdCell = document.createElement('td');
        authorIdCell.textContent = book.author_id;
        row.appendChild(authorIdCell);

        const genreCell = document.createElement('td');
        genreCell.textContent = book.genre;
        row.appendChild(genreCell);

        const publishYearCell = document.createElement('td');
        publishYearCell.textContent = book.publish_year;
        row.appendChild(publishYearCell);

        table.appendChild(row);
    });

    // Append the table to the container
    bookListContainer.appendChild(table);

    // Add an event listener to the table to handle row clicks
    table.addEventListener('click', handleRowClick);
}

// Function to handle row clicks
function handleRowClick(event) {
    const targetRow = event.target.closest('tr');

    if (targetRow) {
        book_id = targetRow.getAttribute('book_id');
        alert(`Clicked on book with ID: ${book_id}`);
    }
}

function changePageToUpdateUser(){
    window.location.href = 'update_user.html?user=' + user_id;
}

function updateUser() {
    var username = document.getElementById('update_username').value;
    var password = document.getElementById('update_password').value;
    var full_name = document.getElementById('update_full_name').value;
    var email = document.getElementById('update_email').value;

    alert(user_id);

    // Dummy data for demonstration purposes
    var userData = {
        user: {
            user_id: user_id,
            username: username,
            password: password,
            full_name: full_name,
            email: email
        }
    };

    // Make a POST request to the server to add the user
    fetch('http://127.0.0.1:5000/user', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // You can perform additional actions upon successful user addition
    })
    .catch(error => {
        alert('Error adding user. Check the console for details.');
        console.error('Error:', error);
    });
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}