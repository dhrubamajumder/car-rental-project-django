# 🚗 Rental Car System

A full-stack web application for managing car rentals where users can browse cars, book rentals, and track bookings, while admins manage cars, bookings, and revenue through a powerful dashboard.

---

## 📌 Project Overview

The Rental Car System is a Django-based web application designed to simplify car rental operations. It supports user booking, admin management, payment handling, and analytics.

---

# 👤 User Side (Customer Panel)

## 🔐 Authentication System
- User Registration (Email / Phone)
- Login / Logout
- Password Reset
- Profile Management

---

## 🚘 Car Browsing System
- View available cars
- Advanced filtering:
  - Price range filter
  - Brand filter
  - Fuel type (Petrol / Diesel / EV)
  - Transmission (Auto / Manual)
- Search cars by name or location
- Sort by price (Low → High / High → Low)

---

## 🚗 Car Details Page
- Image gallery for each car
- Full specifications:
  - Brand & Model
  - Seating capacity
  - Fuel type
  - Mileage
  - Rent per day/hour
- Availability calendar
- Ratings & reviews
- Book Now button

---

## 📅 Booking System
- Select rental start and end date
- Auto price calculation:
  - Total = Days × Price per day
- Optional services:
  - Driver service
  - Insurance
  - GPS
- Booking confirmation page
- Payment status:
  - Cash
  - Online
  - Pending

---

## 📖 Booking History
- View past bookings
- Active bookings
- Booking statuses:
  - Pending
  - Approved
  - Rejected
  - Completed
  - Cancelled

---

## 👤 User Profile
- Update personal information
- Upload driving license
- Profile picture
- Manage saved addresses

---

## 🔔 Notifications
- Booking approval/rejection alerts
- Payment confirmation alerts
- Admin messages

---

# 🛠️ Admin Side (Control Panel)

## 🚗 Car Management
- Add new cars
- Update car details
- Delete cars
- Upload multiple images
- Set car status:
  - Available
  - Booked
  - Maintenance

---

## 📋 Booking Management
- View all bookings
- Filter bookings:
  - Pending
  - Approved
  - Cancelled
- Approve / Reject bookings
- Assign car availability
- Add admin notes

---

## 💰 Revenue Dashboard
- Total revenue overview
- Monthly revenue chart
- Daily earnings tracking
- Top rented cars
- Pending payments list

---

## 👥 User Management
- View all users
- Block / unblock users
- View user booking history

---

## 📊 Analytics Dashboard
- Total cars count
- Total bookings
- Active rentals
- Conversion rate (views → bookings)

---

## 🔔 Admin Notifications
- New booking alerts
- Cancel request alerts
- Payment received alerts

---

# ⭐ Advanced Features (Portfolio Level)

## 🧠 Smart Features
- Car recommendation system (based on user behavior)
- Dynamic pricing (weekend/holiday pricing)
- Automatic availability check (no date conflict)

---

## 📍 Location Features
- Pickup & drop location selection
- Nearby cars filtering

---

## 💳 Payment System
- Stripe / SSLCommerz / bKash integration
- Payment history tracking
- Invoice generation (PDF)

---

## 🧾 Invoice System
- Download booking invoice
- Booking summary in PDF format

---

## ⭐ Reviews & Ratings
- Users can rate cars after rental
- Admin moderation for reviews

---

## 📱 UI/UX Features
- Fully responsive design
- Dark mode support (optional)
- Charts using Chart.js

---

# 🧱 Database Structure (Main Models)

- User (Custom User Model)
- Car
- CarImage
- Booking
- Payment
- Review
- Notification
- Driver (Optional)
- Location

---

# 🔁 Booking Workflow

1. User selects a car
2. Chooses rental dates
3. System checks availability
4. Calculates total price
5. Booking created (status = Pending)
6. Admin approves/rejects booking
7. Notification sent to user
8. Payment processed
9. Booking completed

---

# 🧑‍💻 Admin Dashboard Overview

## 📊 Dashboard Widgets
- Total Cars
- Total Bookings
- Total Revenue

## 📈 Charts
- Monthly earnings graph
- Booking statistics

## 🚗 Latest Activity
- Recent bookings list
- Recent user activity

## 🔔 Notifications Panel
- New bookings
- Pending approvals
- Payment updates

---

# 🚀 Tech Stack (Optional Suggestion)

- Backend: Django / Django REST Framework
- Frontend: HTML, CSS, Bootstrap
- Database: PostgreSQL / SQLite
- Charts: Chart.js
- Payment: Stripe / bKash / SSLCommerz

---

# 🎯 Project Goal

To build a real-world car rental management system that demonstrates full-stack development skills, including authentication, booking logic, admin dashboard, and payment integration.

---

# 📌 Future Improvements

- Mobile App (React Native / Flutter)
- AI-based car recommendations
- Live tracking system
- Chat system between user & admin