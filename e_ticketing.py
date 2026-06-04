print("Starting...")
import customtkinter as ctk
from tkinter import messagebox, ttk
import random
import csv
import os
from datetime import datetime, timedelta

# Set appearance mode to dark for modern look
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BookMyShowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BookMyShow - E-Ticketing")
        self.root.geometry("800x700")
        self.root.configure(bg="#000000")

        # Predefined data
        self.event_categories = ["Movies", "Concerts", "Sports", "Theatre"]
        self.movies = [
            {"name": "Avengers: Endgame", "dates": ["2023-10-15", "2023-10-16"], "times": ["10:00 AM", "2:00 PM", "6:00 PM"]},
            {"name": "Inception", "dates": ["2023-10-17", "2023-10-18"], "times": ["11:00 AM", "3:00 PM", "7:00 PM"]},
            {"name": "The Dark Knight", "dates": ["2023-10-19", "2023-10-20"], "times": ["12:00 PM", "4:00 PM", "8:00 PM"]}
        ]
        self.concerts = [
            {"name": "Taylor Swift", "dates": ["2023-10-21", "2023-10-22"], "times": ["7:00 PM", "9:00 PM"]},
            {"name": "Ed Sheeran", "dates": ["2023-10-23", "2023-10-24"], "times": ["8:00 PM", "10:00 PM"]}
        ]
        self.sports = [
            {"name": "Football Match", "dates": ["2023-10-25"], "times": ["5:00 PM"]},
            {"name": "Basketball Game", "dates": ["2023-10-26"], "times": ["6:00 PM"]}
        ]
        self.theatre = [
            {"name": "Hamlet", "dates": ["2023-10-27"], "times": ["7:30 PM"]},
            {"name": "Romeo and Juliet", "dates": ["2023-10-28"], "times": ["8:00 PM"]}
        ]

        self.selected_category = None
        self.selected_event = None
        self.selected_date = None
        self.selected_time = None
        self.selected_seats = []

        # Frames for different screens
        self.home_frame = ctk.CTkFrame(root, fg_color="#1a1a1a")
        self.event_frame = ctk.CTkFrame(root, fg_color="#1a1a1a")
        self.details_frame = ctk.CTkFrame(root, fg_color="#1a1a1a")
        self.records_frame = ctk.CTkFrame(root, fg_color="#1a1a1a")

        self.root.lift()

        # Create all widgets once in __init__
        self.create_home_widgets()
        self.create_event_widgets()
        self.create_details_widgets()
        self.create_records_widgets()

        self.show_home()

    def create_home_widgets(self):
        self.home_title = ctk.CTkLabel(self.home_frame, text="BookMyShow", font=("Arial", 28, "bold"), text_color="#FF4500")
        self.home_title.pack(pady=20)

        self.home_subtitle = ctk.CTkLabel(self.home_frame, text="Select an Event Category", font=("Arial", 16), text_color="#FFFFFF")
        self.home_subtitle.pack(pady=10)

        # Category buttons
        self.category_buttons = []
        for category in self.event_categories:
            btn = ctk.CTkButton(self.home_frame, text=category, command=lambda c=category: self.show_events(c), width=200, height=50, fg_color="#8A2BE2", hover_color="#9932CC")
            btn.pack(pady=10)
            self.category_buttons.append(btn)

        # View Records button
        self.view_records_btn = ctk.CTkButton(self.home_frame, text="View Records", command=self.show_records, width=200, height=50, fg_color="#00FF00", hover_color="#32CD32")
        self.view_records_btn.pack(pady=20)

    def create_event_widgets(self):
        self.event_title = ctk.CTkLabel(self.event_frame, text="", font=("Arial", 24, "bold"), text_color="#00FF00")
        self.event_title.pack(pady=20)

        self.event_listbox = ctk.CTkScrollableFrame(self.event_frame, width=600, height=300)
        self.event_listbox.pack(pady=10)

        self.event_back_btn = ctk.CTkButton(self.event_frame, text="Back", command=self.show_home, fg_color="#FF6347")
        self.event_back_btn.pack(pady=10)

    def create_details_widgets(self):
        self.details_title = ctk.CTkLabel(self.details_frame, text="", font=("Arial", 24, "bold"), text_color="#FFD700")
        self.details_title.pack(pady=20)

        # Date selection
        self.date_label = ctk.CTkLabel(self.details_frame, text="Select Date:", font=("Arial", 14), text_color="#00BFFF")
        self.date_label.pack()
        self.date_combobox = ctk.CTkComboBox(self.details_frame, values=[], width=300)
        self.date_combobox.pack(pady=5)

        # Time selection
        self.time_label = ctk.CTkLabel(self.details_frame, text="Select Time:", font=("Arial", 14), text_color="#FF4500")
        self.time_label.pack()
        self.time_combobox = ctk.CTkComboBox(self.details_frame, values=[], width=300)
        self.time_combobox.pack(pady=5)

        # Seats
        self.seats_label = ctk.CTkLabel(self.details_frame, text="Number of Seats:", font=("Arial", 14), text_color="#00FF00")
        self.seats_label.pack()
        self.seats_entry = ctk.CTkEntry(self.details_frame, placeholder_text="Enter number of seats", width=300)
        self.seats_entry.pack(pady=5)

        # User details
        self.name_label = ctk.CTkLabel(self.details_frame, text="Name:", font=("Arial", 14), text_color="#FF1493")
        self.name_label.pack()
        self.name_entry = ctk.CTkEntry(self.details_frame, placeholder_text="Enter your name", width=300)
        self.name_entry.pack(pady=5)

        self.phone_label = ctk.CTkLabel(self.details_frame, text="Phone Number:", font=("Arial", 14), text_color="#FFD700")
        self.phone_label.pack()
        self.phone_entry = ctk.CTkEntry(self.details_frame, placeholder_text="Enter your phone number", width=300)
        self.phone_entry.pack(pady=5)

        # Book button
        self.book_btn = ctk.CTkButton(self.details_frame, text="Book Ticket", command=self.book_ticket, fg_color="#8A2BE2", hover_color="#9932CC")
        self.book_btn.pack(pady=20)

        self.details_back_btn = ctk.CTkButton(self.details_frame, text="Back", command=self.show_events_back, fg_color="#FF6347")
        self.details_back_btn.pack()

    def create_records_widgets(self):
        self.records_title = ctk.CTkLabel(self.records_frame, text="Booking Records", font=("Arial", 24, "bold"), text_color="#00BFFF")
        self.records_title.pack(pady=20)

        # Use Treeview for proper table display
        self.records_tree = ttk.Treeview(self.records_frame, columns=("Ticket ID", "Name", "Phone", "Event", "Date", "Time", "Seats", "Total Cost"), show="headings", height=15)
        self.records_tree.pack(pady=10, fill="both", expand=True)

        # Define headings
        for col in ("Ticket ID", "Name", "Phone", "Event", "Date", "Time", "Seats", "Total Cost"):
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=100, anchor="center")

        # Scrollbars
        self.records_scrollbar = ttk.Scrollbar(self.records_frame, orient="vertical", command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=self.records_scrollbar.set)
        self.records_scrollbar.pack(side="right", fill="y")

        self.records_back_btn = ctk.CTkButton(self.records_frame, text="Back", command=self.show_home, fg_color="#FF6347")
        self.records_back_btn.pack(pady=10)

    def clear_frames(self):
        self.home_frame.pack_forget()
        self.event_frame.pack_forget()
        self.details_frame.pack_forget()
        self.records_frame.pack_forget()

    def show_home(self):
        self.clear_frames()
        self.home_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_events(self, category):
        self.selected_category = category
        self.clear_frames()
        self.event_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.event_title.configure(text=f"Select {category}")

        # Clear previous event buttons
        for widget in self.event_listbox.winfo_children():
            widget.destroy()

        # Get events for category
        events = getattr(self, category.lower())

        for event in events:
            event_btn = ctk.CTkButton(self.event_listbox, text=event["name"], command=lambda e=event: self.select_event(e), width=500, height=40, fg_color="#FF1493", hover_color="#FF69B4")
            event_btn.pack(pady=5)

    def show_events_back(self):
        if self.selected_category:
            self.show_events(self.selected_category)
        else:
            self.show_home()

    def select_event(self, event):
        self.selected_event = event
        self.show_details()

    def show_details(self):
        self.clear_frames()
        self.details_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.details_title.configure(text=f"Book {self.selected_event['name']}")
        self.date_combobox.configure(values=self.selected_event["dates"])
        self.time_combobox.configure(values=self.selected_event["times"])

        # Clear user input fields to prevent auto-filling from previous records
        self.name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.seats_entry.delete(0, 'end')
        self.date_combobox.set('')
        self.time_combobox.set('')

    def show_records(self):
        self.clear_frames()
        self.records_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Clear existing items
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        if os.path.isfile("bookings.csv"):
            with open("bookings.csv", mode="r") as file:
                reader = csv.reader(file)
                records = list(reader)
                if len(records) > 1:  # Has header and data
                    for row in records[1:]:
                        self.records_tree.insert("", "end", values=row)
                else:
                    # No data, insert a message
                    self.records_tree.insert("", "end", values=("No records found.", "", "", "", "", "", "", ""))
        else:
            self.records_tree.insert("", "end", values=("No records file found.", "", "", "", "", "", "", ""))

    def book_ticket(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        date = self.date_combobox.get()
        time = self.time_combobox.get()
        seats = self.seats_entry.get()

        if not all([name, phone, date, time, seats]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            num_seats = int(seats)
        except ValueError:
            messagebox.showerror("Error", "Number of seats must be a valid integer.")
            return

        ticket_id = random.randint(100000, 999999)
        total_cost = num_seats * 50

        ticket_details = f"""
        ========================================
                BOOKING CONFIRMATION
        ========================================
        Ticket ID: {ticket_id}
        Event: {self.selected_event['name']}
        Date: {date}
        Time: {time}
        Seats: {num_seats}
        Name: {name}
        Phone: {phone}
        Total Cost: ${total_cost}
        ========================================
        Enjoy the show!
        """

        messagebox.showinfo("Booking Successful", ticket_details)

        self.save_record(ticket_id, name, phone, self.selected_event['name'], date, time, num_seats, total_cost)

        self.show_home()

    def save_record(self, ticket_id, name, phone, event, date, time, seats, cost):
        file_exists = os.path.isfile("bookings.csv")
        with open("bookings.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Ticket ID", "Name", "Phone", "Event", "Date", "Time", "Seats", "Total Cost"])
            writer.writerow([ticket_id, name, phone, event, date, time, seats, cost])

if __name__ == "__main__":
    root = ctk.CTk()
    app = BookMyShowApp(root)
    root.mainloop()
