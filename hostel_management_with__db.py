import mysql.connector
from datetime import date
class guest:
    def __init__(self,name,members):
        self.name=name
        self.members=members
class hotel:
    def __init__(self,total_rooms,dbconfig):
        self.total_rooms=total_rooms
        self.conn=mysql.connector.connect(**dbconfig)
        self.cursor=self.conn.cursor()
        
    def add_guest(self,guest):
        add_guest_query=("INSERT INTO guest(name,members) VALUES (%s,%s)")
        val=(guest.name,guest.members)
        self.cursor.execute(add_guest_query,val)
        self.conn.commit()
        return self.cursor.lastrowid
    def book_guests(self,guest,check_in,check_out,rooms_booked):
        if self.chk_availability(check_in,check_out,rooms_booked):
            guest_id=self.add_guest(guest)
            add_booking_query=("INSERT INTO bookings(guest_id,check_in,check_out,rooms_booked) VALUES(%s,%s,%s,%s)")
            val=(guest_id,check_in,check_out,rooms_booked)
            self.cursor.execute(add_booking_query,val)
            self.conn.commit()
            print(f"Rooms successfully booked for {guest.name} ")
        else:
            print("Not enough rooms available in given date")
    def chk_availability(self,check_in,check_out,room_needed):
        query=("SELECT SUM(rooms_booked) FROM bookings "
                "WHERE check_in < %s AND check_out > %s")
        vals=(check_out,check_in)
        self.cursor.execute(query,vals)
        total_booked_rooms=self.cursor.fetchone()[0] or 0
        remaining=self.total_rooms-total_booked_rooms
        if remaining>=room_needed:
            return True
        else:
            return False
    def get_availability(self):
        query=("SELECT SUM(rooms_booked) FROM bookings")
    
        self.cursor.execute(query)
        total_booked_rooms=self.cursor.fetchone()[0] or 0
        available=self.total_rooms-total_booked_rooms
        print(f"{available} room are available out of {self.total_rooms}")
    def close(self):
        self.cursor.close()
        self.conn.close()
        
dbconfig={
        'user':"root",
        'password':'admin',
        'host': '127.0.0.1',
        'database': 'hotel_management_system',
        
    }
h1 = hotel(10, dbconfig)
g1 = guest("Zaeem", 5)
h1.book_guests(g1, date(2024, 10, 12), date(2024, 10, 14), 2)  # Booking from 12th to 14th October
h1.get_availability()
g2 = guest("Ali", 10)
h1.book_guests(g2, date(2024, 10, 14), date(2024, 10, 16), 3)  # Booking from 14th to 16th October
h1.get_availability()
h1.close()