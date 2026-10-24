"""
SMART BUS TICKET BOOKING & RESERVATION SYSTEM
Python 3 | Built-in libraries only | In-memory data (no database)
Run: python main.py
"""

from datetime import datetime

ROUTES = [
    {
        "route_id": "R101",
        "source": "Karachi",
        "destination": "Hyderabad",
        "departure": "08:00 AM",
        "fare": 1200,
        "total_seats": 40,
        "available_seats": 40,
    },
    {
        "route_id": "R102",
        "source": "Karachi",
        "destination": "Sukkur",
        "departure": "09:30 AM",
        "fare": 2000,
        "total_seats": 36,
        "available_seats": 36,
    },
    {
        "route_id": "R103",
        "source": "Hyderabad",
        "destination": "Mirpur Khas",
        "departure": "11:00 AM",
        "fare": 800,
        "total_seats": 32,
        "available_seats": 32,
    },
    {
        "route_id": "R104",
        "source": "Karachi",
        "destination": "Lahore",
        "departure": "07:00 PM",
        "fare": 5000,
        "total_seats": 45,
        "available_seats": 45,
    },
    {
        "route_id": "R105",
        "source": "Sukkur",
        "destination": "Hyderabad",
        "departure": "02:00 PM",
        "fare": 1500,
        "total_seats": 30,
        "available_seats": 30,
    },
]

BOOKINGS = []
next_booking_number = 1001


def line(char="-", width=78):
    print(char * width)


def heading(title):
    print()
    line("=")
    print(title.center(78))
    line("=")


def money(amount):
    return f"Rs. {amount:,}"


def get_route(route_id):
    """Return the route matching an ID, or None if it does not exist."""
    for route in ROUTES:
        if route["route_id"].lower() == route_id.strip().lower():
            return route
    else:
        return None


def display_routes(routes=None):
    if routes is None:
        routes = ROUTES

    if not routes:
        print("\nNo routes found.")
        return

    print()
    line()
    print(f"{'ID':<7} {'FROM':<16} {'TO':<18} {'DEPARTURE':<13} "
          f"{'FARE':<12} {'SEATS':<8}")
    line()
    for route in routes:
        print(
            f"{route['route_id']:<7} "
            f"{route['source']:<16} "
            f"{route['destination']:<18} "
            f"{route['departure']:<13} "
            f"{money(route['fare']):<12} "
            f"{route['available_seats']}/{route['total_seats']:<5}"
        )
    line()


def view_routes():
    heading("AVAILABLE BUS ROUTES")
    display_routes()


def search_route():
    heading("SEARCH ROUTE")
    source = input("Enter departure city (or press Enter to skip): ").strip()
    destination = input("Enter destination city (or press Enter to skip): ").strip()

    matches = []
    for route in ROUTES:
        source_matches = not source or source.lower() in route["source"].lower()
        destination_matches = (
            not destination
            or destination.lower() in route["destination"].lower()
        )
        if source_matches and destination_matches:
            matches.append(route)
            continue

    display_routes(matches)


def read_positive_integer(prompt, minimum=1, maximum=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if value < minimum:
            print(f"Enter a number of at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Enter a number no greater than {maximum}.")
            continue
        return value


def book_ticket():
    global next_booking_number
    heading("BOOK A TICKET")
    display_routes()

    route_id = input("\nEnter route ID (e.g. R101): ").strip()
    route = get_route(route_id)
    if route is None:
        print("Invalid route ID. Booking was not created.")
        return

    passenger_name = input("Passenger full name: ").strip()
    if len(passenger_name) < 2 or not any(ch.isalpha() for ch in passenger_name):
        print("Please enter a valid passenger name (at least 2 characters).")
        return

    age = read_positive_integer("Passenger age (1-120): ", 1, 120)
    if age < 1 or age > 120:
        print("Invalid age. Booking was not created.")
        return

    if route["available_seats"] == 0:
        print("Sorry, this route is fully booked.")
        return

    seat_count = read_positive_integer(
        f"Number of seats (available {route['available_seats']}): ",
        1,
        route["available_seats"],
    )

    # Only update seats after all input and availability checks succeed.
    total_fare = route["fare"] * seat_count
    booking = {
        "booking_id": f"B{next_booking_number}",
        "passenger_name": passenger_name,
        "age": age,
        "route_id": route["route_id"],
        "source": route["source"],
        "destination": route["destination"],
        "departure": route["departure"],
        "seats": seat_count,
        "fare_per_seat": route["fare"],
        "total_fare": total_fare,
        "status": "Confirmed",
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    BOOKINGS.append(booking)
    route["available_seats"] -= seat_count
    next_booking_number += 1

    print("\nBOOKING CONFIRMED!")
    line()
    print(f"Booking ID     : {booking['booking_id']}")
    print(f"Passenger      : {booking['passenger_name']}")
    print(f"Age            : {booking['age']}")
    print(f"Route          : {booking['source']} to {booking['destination']}")
    print(f"Departure      : {booking['departure']}")
    print(f"Seats          : {booking['seats']}")
    print(f"Fare per seat  : {money(booking['fare_per_seat'])}")
    print(f"Total fare     : {money(booking['total_fare'])}")
    print(f"Status         : {booking['status']}")
    line()


def view_bookings():
    heading("ALL BOOKINGS")
    if not BOOKINGS:
        print("No bookings have been made yet.")
        return

    line()
    print(f"{'BOOKING ID':<13} {'PASSENGER':<20} {'ROUTE':<9} "
          f"{'SEATS':<7} {'TOTAL FARE':<14} {'STATUS':<12}")
    line()
    for booking in BOOKINGS:
        route_text = booking["route_id"]
        print(
            f"{booking['booking_id']:<13} "
            f"{booking['passenger_name'][:19]:<20} "
            f"{route_text:<9} "
            f"{booking['seats']:<7} "
            f"{money(booking['total_fare']):<14} "
            f"{booking['status']:<12}"
        )
    line()


def cancel_booking():
    heading("CANCEL BOOKING")
    booking_id = input("Enter booking ID (e.g. B1001): ").strip().upper()

    for booking in BOOKINGS:
        if booking["booking_id"].upper() == booking_id:
            if booking["status"] == "Cancelled":
                print("This booking has already been cancelled.")
                return

            route = get_route(booking["route_id"])
            if route is not None:
                route["available_seats"] += booking["seats"]

            booking["status"] = "Cancelled"
            booking["cancelled_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Booking {booking['booking_id']} cancelled successfully.")
            print(f"{booking['seats']} seat(s) have been released.")
            return
    else:
        print("Booking ID not found.")


def seat_availability():
    heading("SEAT AVAILABILITY")
    display_routes()
    route_id = input("\nEnter route ID to check (or press Enter for all): ").strip()

    if not route_id:
        return

    route = get_route(route_id)
    if route is None:
        print("Invalid route ID.")
        return

    reserved = route["total_seats"] - route["available_seats"]
    print(f"\nRoute: {route['source']} to {route['destination']}")
    print(f"Total seats     : {route['total_seats']}")
    print(f"Reserved seats  : {reserved}")
    print(f"Available seats : {route['available_seats']}")


def booking_report():
    heading("BOOKING REPORT")
    total_bookings = len(BOOKINGS)
    confirmed = [booking for booking in BOOKINGS if booking["status"] == "Confirmed"]
    cancelled = [booking for booking in BOOKINGS if booking["status"] == "Cancelled"]
    reserved_seats = sum(booking["seats"] for booking in confirmed)
    revenue = sum(booking["total_fare"] for booking in confirmed)

    print(f"Total booking records : {total_bookings}")
    print(f"Confirmed bookings   : {len(confirmed)}")
    print(f"Cancelled bookings   : {len(cancelled)}")
    print(f"Currently reserved seats: {reserved_seats}")
    print(f"Revenue (confirmed only): {money(revenue)}")

    print("\nROUTE-WISE SEAT SUMMARY")
    line()
    print(f"{'ROUTE':<8} {'JOURNEY':<35} {'RESERVED':<10} {'AVAILABLE':<10}")
    line()
    for route in ROUTES:
        reserved = route["total_seats"] - route["available_seats"]
        journey = f"{route['source']} to {route['destination']}"
        print(f"{route['route_id']:<8} {journey:<35} {reserved:<10} "
              f"{route['available_seats']:<10}")
    line()


def show_menu():
    print()
    line("=")
    print("SMART BUS TICKET BOOKING & RESERVATION SYSTEM".center(78))
    line("=")
    print("1. View all routes")
    print("2. Search route by city")
    print("3. Book a ticket")
    print("4. View all bookings")
    print("5. Cancel a booking")
    print("6. Check seat availability")
    print("7. Booking report")
    print("8. Exit")
    line("=")


def main():
    print("\nWelcome to the Smart Bus Ticket Booking System!")
    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            view_routes()
        elif choice == "2":
            search_route()
        elif choice == "3":
            book_ticket()
        elif choice == "4":
            view_bookings()
        elif choice == "5":
            cancel_booking()
        elif choice == "6":
            seat_availability()
        elif choice == "7":
            booking_report()
        elif choice == "8":
            print("\nThank you for using the Smart Bus Ticket Booking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")

        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main()
