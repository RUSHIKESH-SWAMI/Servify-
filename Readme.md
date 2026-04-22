# Servify - Home Services Backend Platform

## 📖 What is this project?
Servify is the backend (the brain and database) for a home services application, similar to apps where you can book an AC repairman or a house cleaner. 

It is built to connect two types of people:
1. **Seekers:** People looking to hire someone for a service.
2. **Providers:** Professionals who offer their services.

This project handles the entire journey: from a user creating an account, to browsing services, booking a professional, completing the job, simulating a payment, and leaving a review.

---

## 🛠️ Tools & Technologies Used
* **Language:** Python
* **Framework:** Django & Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Security/Login:** JSON Web Tokens (JWT)
* **Architecture:** Organized Monolith (Apps are separated cleanly so they can become microservices later).

---

## 📂 Project Structure
The code is split into three main "apps" (folders) to keep everything organized:

1. **`accounts` (User Management & Login)**
   * Handles user sign-ups and secure logins.
   * Gives people specific roles (`SEEKER` or `PROVIDER`) so they only see what they are allowed to see.
2. **`services` (The Catalog)**
   * Holds the list of available jobs (e.g., "AC Repair", "Cleaning").
   * Connects Providers to the services they offer, including their available times.
3. **`bookings` (The Core Engine)**
   * Manages the actual booking request.
   * Tracks the status of a job (`PENDING` ➔ `ACCEPTED` ➔ `COMPLETED`).
   * Creates a bill (Transaction) when the job is done.
   * Allows Seekers to leave a 1-5 star Review at the very end.

---

## 🚀 The API Endpoints (What we built so far)
Below are the 11 URLs that power the application:

**1. Creating Accounts & Logging In**
* `POST /api/accounts/register/` - Create a new Seeker or Provider.
* `POST /api/accounts/login/` - Log in to get your secure access token.
* `POST /api/accounts/login/refresh/` - Keep the user logged in.

**2. Browsing Services (Public)**
* `GET /api/services/` - See all services offered on the app.
* `GET /api/services/<id>/providers/` - See which professionals offer a specific service.

**3. Booking & Working (Secure)**
* `POST /api/bookings/request/` - (Seeker) Ask a Provider to do a job.
* `GET /api/bookings/incoming/` - (Provider) See who wants to hire you.
* `PATCH /api/bookings/<id>/accept/` - (Provider) Say "Yes" to a job request.
* `PATCH /api/bookings/<id>/complete/` - (Provider) Mark the job as finished and generate a bill.

**4. Paying & Reviewing**
* `POST /api/bookings/pay/<transaction_id>/` - (Seeker) Mock payment to verify the bill is paid.
* `POST /api/bookings/<id>/review/` - (Seeker) Rate the Provider 1 to 5 stars.

---

## 💻 How to Run This Locally
If you want to download this code and run it on your own computer, follow these steps:

**1. Clone the repository and enter the folder:**
```bash
git clone <your-github-repo-link>
cd servify
