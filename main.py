import json
from collections import namedtuple
from http.server import BaseHTTPRequestHandler, HTTPServer

CityPopulation = namedtuple("City", ["name", "population"])

CITIES = [
    CityPopulation("Helsinki", 658761),
    CityPopulation("Espoo", 292896),
    CityPopulation("Tampere", 244016),
    CityPopulation("Vantaa", 241093),
    CityPopulation("Oulu", 209827),
]

CityAverageExpense = namedtuple("City", ["name", "average_expense"])

CitiesAverageExpenses = [
    CityAverageExpense("Helsinki", 2500),
    CityAverageExpense("Espoo", 2200),
    CityAverageExpense("Tampere", 2000),
    CityAverageExpense("Vantaa", 2100),
    CityAverageExpense("Oulu", 2000),
]


class CityRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Server is running!")
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

        # Get the method name from the request path
        method_name = self.path.strip("/")

        # LIST OF CITIES IN FINLAND
        if method_name == "get_cities":
            # Convert the list of cities to JSON format
            cities_json = json.dumps([city._asdict() for city in CITIES])
            self.wfile.write(cities_json.encode())

        # AVERAGE LIVING EXPENSE OF A CITY IN FINLAND
        elif method_name == "get_average_expense":
            # Retrieve city name from request data
            request_data = self.rfile.read(int(self.headers['Content-Length']))
            city_name = json.loads(request_data)["city_name"]
            # Find the city's average expense
            city_expense = next(
                (city for city in CitiesAverageExpenses if city.name == city_name),
                None
            )
            if city_expense:
                # Return the average expense in JSON format
                self.wfile.write(json.dumps({"average_expense": city_expense.average_expense}).encode())
            else:
                self.send_error(404, f"City not found: {city_name}")
        # IF METHOD DOES NOT EXIST
        else:
            self.send_error(404, "Method not found")


if __name__ == "__main__":
    server_address = ("localhost", 8080)
    httpd = HTTPServer(server_address, CityRequestHandler)
    print(f"Server running on http://{server_address[0]}:{server_address[1]}")
    httpd.serve_forever()
