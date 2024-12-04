# SubscriberCount-IEP(TierSync)  
A sleek Django web application for managing and analyzing subscriber memberships across different tiers with a Netflix-inspired design.  

 **About the Project** 
 
TierSync is designed to efficiently handle subscriber memberships across three tiers: *Basic*, *VIP*, and *Premium*. It leverages the *Inclusion-Exclusion Principle* to calculate unique subscriber counts and provides insights into shared memberships between tiers.  

The interface features a modern, Netflix-like theme with a dark background, red buttons, and stylish fonts, ensuring an engaging user experience.  

 **Key Features**  
 
*Add Subscribers*: Easily register subscribers and assign them to a membership tier.  
*View Results*: Analyze membership statistics, including unique and overlapping memberships across tiers.  
*MySQL Database*: The application stores all subscriber and membership data securely in a **MySQL** database.  

**Technologies Used** 

*Backend*: Django Framework  
*Frontend*: HTML & CSS with Netflix-inspired styling  
*Database*: MySQL  

**How to Run the Project**  
1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/coder-riya/SubscriberCount-IEP
   cd SubscriberCount-IEP
   ```

2. **Install Dependencies**:  
   Make sure you have Python and Django installed. Then run:  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:  
   Configure your MySQL database settings in `settings.py` and apply migrations:  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the Development Server**:  
   Start the server and access the app in your browser:  
   ```bash
   python manage.py runserver
   ```

5. **Explore the App**:  
   - Access the homepage at `http://127.0.0.1:8000/`.  
   - Use the "Add Subscriber" and "View Results" options to interact with the app.  

---

### **Acknowledgments**  
The project combines mathematical principles with modern design aesthetics, inspired by Netflix's theme, to deliver a user-friendly experience.  
