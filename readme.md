# Lab 4 
# Book Search and Filter App

## Overview
This application is designed to allow users to search and filter books scraped from a fictional bookstore website. It provides functionality to view all books, search by title, filter by rating, and sort by either rating or price in ascending or descending order. This data-driven application uses PostgreSQL for storage and management of book data and Streamlit for an interactive web interface.

## Features
- View a list of all books in the database.
- Search books by title.
- Filter books by their star rating.
- Sort books by rating or price in ascending or descending order.
- Responsive and user-friendly web interface.

## Technology Stack
- Python
- Streamlit
- PostgreSQL
- BeautifulSoup
- Pandas

## Project Setup

### Requirements
- Python 3.8+
- PostgreSQL

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Jaclynjw/technic510-lab4.git
   cd technic510-lab4
2. Install dependencies:
    ```
    pip install -r requirements.txt
### Running the Application
To run the application, execute the following command in the terminal:
    ```
    streamlit run scraper.py
    ```

Visit http://localhost:8501 in your web browser to view the app.

## Lessons Learned

### Data Management
- **Database Design**: The importance of thoughtful database schema design was evident, particularly how unique constraints and indexes can impact data integrity and performance.
- **Data Scraping Nuances**: Dealing with dynamic data from scraping taught us about the variability and unpredictability of source data. Handling exceptions and ensuring data quality are crucial for robust applications.

### Development Practices
- **Modular Code**: Developing the application in a modular fashion (e.g., separating scraping logic from database management and user interface code) made the code easier to manage and debug.
- **Version Control**: Regular commits and clear commit messages proved invaluable in maintaining the project history and made it easier to track changes and revert to previous versions when necessary.

### Streamlit Deployment
- **User Interface Design**: Streamlit provided a rapid way to build a user interface, but also highlighted the need for careful design choices to ensure usability and functionality.
- **Handling User Inputs**: Ensuring the application handles user inputs safely and efficiently without compromising performance was a key learning point.

## Future Improvements

### Scalability
- **Database Optimization**: Implementing more sophisticated SQL queries and possibly migrating to a more scalable database solution as the dataset grows.
- **Load Balancing**: Consider deploying the application in a load-balanced environment to handle increased traffic and data processing demands.

### Features
- **Advanced Search Capabilities**: Adding more search filters and options, such as searching by author or ISBN, could enhance the user experience.
- **Recommendation Engine**: Implement a recommendation system that suggests books based on user preferences and browsing history.

### User Experience
- **Interactive Elements**: Incorporate more interactive elements into the Streamlit app, such as sliders for price ranges, interactive book previews, or user ratings and reviews.
- **Mobile Responsiveness**: Optimizing the application for mobile devices to reach a broader audience.

### Technical Debt
- **Code Refactoring**: Continual refactoring of the codebase to improve maintainability and readability, particularly focusing on reducing redundancy and enhancing modular architecture.
- **Testing**: Expanding the test suite to cover more edge cases and ensure that new features do not break existing functionality.


