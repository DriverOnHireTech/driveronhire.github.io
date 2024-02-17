from datetime import date
from .models import Driverappstatus

class DriverPackageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if the user is a driver and has a package
            if hasattr(request.user, 'driver') and hasattr(request.user.driver, 'package'):
                driver_package = request.user.driver.package
                if driver_package.expiry_date and driver_package.expiry_date < date.today():
                    # Update driver status to inactive if package expired
                    driver_package.status = 'inactive'
                    driver_package.save()

        response = self.get_response(request)
        return response
