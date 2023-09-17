
---

# Virtual Book Shelf

## Overview

The **Virtual Book Shelf** is a web application designed to help users manage their reading list and track the status of books. This project serves as a personal book collection organizer, emphasizing simplicity and usability.

## Key Features

- **User-friendly Interface**: The application employs Bootstrap to create an intuitive and visually appealing user interface.
- **Book Management**: Users can easily add, edit, and delete books from their virtual bookshelves.
- **Status Tracking**: Keep track of your reading progress by setting book statuses to "To Read," "Reading," or "Complete."
- **Description Notes**: Add brief descriptions for each book to remember what they're about.
- **Author Management**: Store one or more authors for each book, making it easy to search for works by your favorite writers.

## Getting Started

To run the application locally, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine using `git clone`.

2. **Set Up Environment Variables**: Create a `.env` file in the project root directory and add the following environment variables:

    ```env
    DATABASE_NAME=YourDatabaseName
    DATABASE_URI=YourMongoDBURI
    SECRET_KEY=YourSecretKey
    ```

3. **Install Dependencies**: Run `pip install -r requirements.txt` to install the required Python packages.

4. **Run the Application**: Execute `python app.py` to start the Flask development server.

5. **Access the Application**: Open a web browser and navigate to `http://localhost:5000` to access the Virtual Book Shelf.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

- Fork the repository on GitHub.
- Create a new branch with a descriptive name for your feature or bug fix.
- Make your changes and commit them with clear, concise commit messages.
- Push your changes to your fork on GitHub.
- Create a pull request (PR) to the main repository.


## Acknowledgments

This project was developed by Adebawojo Mosopefoluwa as a personal project for learning the  Python Flask framework.

## Credits

- [YouTube Video: Design Inspiration](https://youtu.be/sY1lLGe7ECA) - This project took inspiration from a design tutorial on YouTube that helped shape the user interface and layout.

---
