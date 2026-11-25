from django.shortcuts import render
from django.http import Http404


PROJECTS = [
    {
        "slug": "airxpress-eats",
        "name": "AirXpress Eats",
        "category": "Food ordering and delivery platform",
        "description": (
            "A multi-business food ordering and delivery platform that connects "
            "customers, restaurants and delivery drivers through one digital system."
        ),
        "problem": (
            "Independent restaurants and food businesses can struggle to manage "
            "orders, customer communication, delivery coordination and driver "
            "operations across separate channels. This can lead to delays, "
            "manual administration and a fragmented customer experience."
        ),
        "solution": (
            "AirXpress Eats brings the ordering and delivery process into one "
            "platform. Customers can discover participating food businesses, "
            "browse menus and place orders, while restaurant teams and drivers "
            "use dedicated operational workflows to manage fulfilment."
        ),
        "features": [
            "Customer-facing food business and menu browsing",
            "Shopping cart and customer order submission",
            "Customer contact details and delivery instructions",
            "Address search and verification using Mapbox",
            "Delivery distance and delivery-fee calculation",
            "Restaurant order management and order status updates",
            "Driver assignment and delivery workflow",
            "Order history and operational reporting",
            "Business and platform management dashboards",
            "Online payment integration",
        ],
        "technology": [
            "Python",
            "Django",
            "HTML, CSS and JavaScript",
            "Mapbox integration",
            "PostgreSQL for production database hosting",
            "Gunicorn",
            "WhiteNoise",
            "Railway deployment",
        ],
        "business_value": (
            "The platform helps food businesses organise orders, coordinate "
            "drivers and manage daily operations. It also gives customers a "
            "more structured way to order and follow the fulfilment process."
        ),
        "live_url": "https://web-production-81fc2.up.railway.app/",
        "technology_note": (
            "The production technology list reflects the documented project "
            "stack. Payment provider configuration can be confirmed separately."
        ),
    },
    {
        "slug": "amlo-shoes",
        "name": "AMLO Shoes",
        "category": "Footwear retail and e-commerce",
        "description": (
            "A digital footwear retail experience designed to present shoe "
            "products online and make it easier for customers to explore a collection."
        ),
        "problem": (
            "Customers may have limited access to a retailer's product range "
            "when products are presented only through in-store visits or scattered "
            "social media posts. This can make product discovery and enquiries "
            "less convenient."
        ),
        "solution": (
            "AMLO Shoes provides a dedicated online presence for showcasing "
            "footwear. It gives customers a central place to explore product "
            "presentations and engage with the business."
        ),
        "features": [
            "Online footwear product presentation",
            "Product catalogue and browsing experience",
            "Dedicated business website",
            "Customer product discovery",
            "Customer enquiry pathway",
        ],
        "technology": [
            "Django-based web application",
            "Python",
            "HTML",
            "CSS",
            "JavaScript",
            "Railway hosting",
        ],
        "business_value": (
            "The website gives the footwear business a dedicated digital "
            "showcase, supports product visibility and provides an online "
            "starting point for customer enquiries."
        ),
        "live_url": "https://web-production-6630.up.railway.app/",
        "technology_note": (
            "The exact database, payment and checkout integrations have not "
            "yet been confirmed, so they are not advertised as implemented features."
        ),
    },
    {
        "slug": "injabulo-clinic",
        "name": "Injabulo Clinic",
        "category": "Healthcare website and appointment platform",
        "description": (
            "A clinic website and management platform that brings together "
            "service information, appointment requests, clinic content and "
            "staff-facing administration."
        ),
        "problem": (
            "Clinics need a convenient way to communicate their services and "
            "clinic information while handling appointment requests and keeping "
            "website content current. Relying entirely on manual communication "
            "can increase administrative work."
        ),
        "solution": (
            "Injabulo Clinic provides a public-facing website with appointment "
            "booking and information pages, supported by a staff dashboard for "
            "managing website content and clinic activities."
        ),
        "features": [
            "Online appointment booking",
            "Clinic services management",
            "Gallery and event management",
            "Homepage content management",
            "Staff dashboard",
            "Appointment administration",
            "Appointment history and monthly reporting",
            "Role-based access for clinic staff and administrators",
            "Mobile-friendly website experience",
            "Progressive Web App installation support",
        ],
        "technology": [
            "Python",
            "Django",
            "HTML",
            "CSS",
            "JavaScript",
            "SQLite during development",
            "Railway deployment",
            "Progressive Web App technologies",
        ],
        "business_value": (
            "The platform gives patients an online route to clinic information "
            "and appointment requests, while helping clinic staff manage content "
            "and appointment administration from a central dashboard."
        ),
        "live_url": "https://injabulo-clinic-website-production.up.railway.app/",
        "technology_note": (
            "The project uses Django. The production database configuration "
            "should be checked before naming a production database in marketing material."
        ),
    },
    {
        "slug": "triple-s-safety-solutions",
        "name": "Triple S Safety Solutions",
        "category": "Corporate website and business services",
        "description": (
            "A business website presenting Triple S Safety Solutions and its "
            "safety-related and business service offering."
        ),
        "problem": (
            "Businesses need a clear and credible online presence where potential "
            "customers can understand what the company offers and find a way to "
            "make contact. Without a central website, information can be difficult "
            "to discover and share."
        ),
        "solution": (
            "The website gives Triple S Safety Solutions a dedicated digital "
            "presence to introduce the business, communicate its offering and "
            "provide a channel for business enquiries."
        ),
        "features": [
            "Company and service presentation",
            "Safety solutions information",
            "Medical billing and credit control service information",
            "Business enquiry pathway",
            "Dedicated company web presence",
        ],
        "technology": [
            "Django-based web application",
            "Python",
            "HTML",
            "CSS",
            "JavaScript",
            "Railway hosting",
            "Custom domain support",
        ],
        "business_value": (
            "The website strengthens the company's online presence, makes "
            "business information easier to access and gives prospective "
            "customers a direct way to enquire."
        ),
        "live_url": "https://triplesafety.co.za/",
        "technology_note": (
            "The service descriptions follow the existing portfolio content. "
            "The full repository documentation and implementation details still "
            "need confirmation."
        ),
    },
    {
        "slug": "carwash-connect",
        "name": "Carwash Connect",
        "category": "Car wash operations and management platform",
        "description": (
            "A car wash management platform that helps operators register "
            "customers and vehicles, manage a live wash queue, record payments "
            "and monitor daily business activity."
        ),
        "problem": (
            "Car wash businesses can rely on paper records and informal "
            "communication to track vehicles, queues, wash progress and payments. "
            "This makes it harder to monitor operations, maintain accurate "
            "records and understand daily revenue."
        ),
        "solution": (
            "Carwash Connect digitises key car wash workflows. Staff can register "
            "vehicles, manage the queue, update wash progress and record payments, "
            "while management can monitor activity and review business reports."
        ),
        "features": [
            "Customer and vehicle registration",
            "Live car wash queue",
            "Vehicle wash status tracking",
            "Staff authentication",
            "Customer WhatsApp notifications",
            "Payment recording",
            "Daily revenue reporting",
            "Car wash operational dashboard",
            "Multi-car-wash support",
            "Platform administration and activity monitoring",
            "Mobile-friendly interface",
        ],
        "technology": [
            "Python",
            "Django",
            "HTML",
            "CSS",
            "JavaScript",
            "SQLite during development",
            "PostgreSQL for production",
            "Gunicorn",
            "WhiteNoise",
            "Railway deployment",
        ],
        "business_value": (
            "The platform helps car wash operators organise their daily workflow, "
            "keep vehicle and payment records, communicate with customers and "
            "monitor revenue and operational activity."
        ),
        "live_url": "https://web-production-bf460.up.railway.app/",
        "technology_note": (
            "The features and technology are based on the project's available "
            "documentation."
        ),
    },
    {
        "slug": "auto-tracker",
        "name": "Auto Tracker",
        "category": "Vehicle management solution",
        "description": (
            "A vehicle-focused digital solution intended to bring vehicle "
            "information and management tools into one accessible application."
        ),
        "problem": (
            "Vehicle-related information can become difficult to organise when "
            "records and updates are kept in separate places. A central digital "
            "system can make vehicle information easier to access and manage."
        ),
        "solution": (
            "Auto Tracker provides a dedicated application for vehicle-related "
            "information and management. Its detailed tracking capabilities "
            "should be confirmed against the current deployed application."
        ),
        "features": [
            "Vehicle-focused application",
            "Vehicle information management",
            "Centralised vehicle-related tools",
        ],
        "technology": [
            "Django-based web application",
            "Python",
            "HTML",
            "CSS",
            "JavaScript",
            "Railway hosting",
        ],
        "business_value": (
            "The project demonstrates how a dedicated digital application can "
            "help bring vehicle-related information and management workflows "
            "together. Specific operational benefits depend on the features "
            "available in the deployed version."
        ),
        "live_url": "https://edvance-auto-tracker-production.up.railway.app/",
        "technology_note": (
            "The repository documentation was not available for verification. "
            "The technology list is a provisional description and should be "
            "checked against the project's current settings and dependencies."
        ),
    },
]


def project_list(request):
    return render(
        request,
        "portfolio/project_list.html",
        {"projects": PROJECTS},
    )


def project_detail(request, slug):
    project = next(
        (item for item in PROJECTS if item["slug"] == slug),
        None,
    )

    if project is None:
        raise Http404("Project not found")

    return render(
        request,
        "portfolio/project_detail.html",
        {"project": project},
    )
