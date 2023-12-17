function editBookClicked(buttonElement) {
    // Get the row containing the button
    var row = $(buttonElement).closest('tr');

        // Get the book's details from the row
        var bookTitle = row.find('.book-title').text();
        var description = row.find('.book-description').text();
        var authors = row.find('.book-authors').text();
        var status = row.find('.book-status').text();

        console.log(bookTitle)
        console.log(description)
        console.log(authors)
        console.log(status)

        // retrieve book_id from database

        // Create a data object to send as JSON
        var requestData = {
         bookTitle: bookTitle
        };

        // Make an AJAX request to pass the bookTitle to the server-side function
        $.ajax({
          type: 'POST',
          url: '/get_book_id',
          contentType: 'application/json', // Set the content type to JSON
          data: JSON.stringify(requestData), // Convert data to JSON format
          success: function (response) {
          console.log('Server response:', response);
         },
          error: function (error) {
            console.error('Error:', error);
          }
        });

        // Populate the modal with the extracted book details
        $('#edit-book-title').val(bookTitle);
        $('#edit-description-text').val(description);
        $('#edit-author-name').val(authors);
        $('#edit-status').val(status);

        // Show the modal for editing
        $('#edit-book-modal').modal('show');
    }
    $(document).ready(function() {
        // Function to update status button color based on content
        function updateStatusButtonColor(button) {
            var buttonText = $(button).text().trim().toLowerCase();

            switch (buttonText) {
                case "toread":
                    $(button).removeClass("btn-outline-primary btn-outline-success").addClass("btn-outline-warning");
                    break;
                case "complete":
                    $(button).removeClass("btn-outline-warning btn-outline-primary").addClass("btn-outline-success");
                    break;
                case "reading":
                    $(button).removeClass("btn-outline-warning btn-outline-success").addClass("btn-outline-primary");
                    break;
                // Add more cases for other statuses if needed
            }
        }

        // Monitor changes to the status text and update the button color
        $('.book-status').each(function() {
            var button = this;

            // Set up a MutationObserver to watch for changes in the status text
            var observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    // Check if the status text has changed
                    if (mutation.type === 'characterData' && mutation.target === button) {
                        // Update the button color based on the new status text
                        updateStatusButtonColor(button);
                    }
                });
            });

            // Start observing changes in the button's text content
            observer.observe(button, { characterData: true, subtree: true });

            // Call the initial update to set the color based on the initial text
            updateStatusButtonColor(button);
        });
    });

    function deleteBook(buttonElement) {
        if (confirm("Are you sure you want to delete this book?")) {
            // Get the row containing the button
            var row = $(buttonElement).closest('tr');
    
            // Get the book's details from the row
            var bookTitle = row.find('.book-title').text();
            var description = row.find('.book-description').text();
            var authors = row.find('.book-authors').text();
            var status = row.find('.book-status').text();
    
            // Create a data object to send as JSON
            var requestData = {
                bookTitle: bookTitle
            };
    
            // Make an AJAX request to get the bookId from the server
            $.ajax({
                type: 'POST',
                url: '/get_book_id',
                contentType: 'application/json',
                data: JSON.stringify(requestData),
                success: function (response) {
                    console.log('Server response:', response);
    
                    // Extract bookId from the response
                    var bookId = response.book_id;
    
                    // Send an AJAX request to delete the book
                    $.ajax({
                        type: 'DELETE',
                        url: `/delete_book/`,
                        data: JSON.stringify({ bookId: bookId }), // Send the bookId for deletion
                        contentType: 'application/json',
                        success: function (deleteResponse) {
                            alert(deleteResponse.message); // Display success message
                            // Optionally, you can remove the deleted row from the table
                            row.remove();
                        },
                        error: function (deleteError) {
                            console.error('Error:', deleteError);
                            alert('Error deleting book.');
                        }
                    });
                },
                error: function (error) {
                    console.error('Error:', error);
                    alert('Error retrieving bookId.');
                }
            });
        }
    }
    