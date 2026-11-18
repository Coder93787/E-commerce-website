"""
Seeds Mega Flipkart-Style Catalogue in Indian Rupees (₹) for SoapSphere Store.
Features latest editions requested by user:
- Mobiles: iPhone 15, 16 Pro, 17 Concept, 18 Ultra, Samsung S24/S25 Ultra, Redmi, Realme, Oppo, Vivo, Motorola
- 2 Wheelers: Royal Enfield Bullet, Pulsar NS400Z, TVS Apache, Hero Glamour, Ola S1 Pro, Ather 450X
- Fashion: Tactical Cargo Pants, Shirts, Full/Half T-Shirts, Winter Puffer Jacket, Leather Biker Jacket
- Footwear & Slippers: Nike, Air Jordan, Puma, Adidas, Red Tape (Sneakers & Slides)
- Laptops: MacBook Air M1, M2, M3, MacBook Pro M4, HP, Dell, Acer, Asus
- Appliances & Fans: BLDC Smart Fans, Pedestal Table Fans, Mixer Grinders, Steam Irons
- Furniture & Tables: Study Desk, Solid Wood Dining Table, Bar Stools, Office Chairs, Coffee Tables
- Luggage & Trolleys: 3-Piece Hard-Side Spinner Trolleys, Cabin Suitcases, Laptop Backpacks
- Electronics & Audio: AirPods Pro 2, Sony WH-1000XM5, OnePlus Buds Pro, boAt, JBL Bluetooth Speaker, Anker Power Banks
- Stationery: Classmate Pulse Notebooks, Parker Pen, Faber-Castell Highlighters, Camlin Markers
- Food & Oil: Fortune Sunflower Oil, Parachute Pure Coconut Oil, Peanut Butter, Tata Tea Gold, Whey Protein
- Beauty, Toys, Baby, Auto Accessories, Sports & Ball, Books
"""
from database import init_db, create_user, get_db

PRODUCTS = [
    # =========================================================================
    # 1. MOBILES (All Latest Versions & Requested Brands)
    # =========================================================================
    {
        "title": "Apple iPhone 15 (Black, 128 GB)",
        "description": "Dynamic Island, 48MP Main Camera with 2x Telephoto, A16 Bionic chip, durable color-infused glass and aluminum design with USB-C connector.",
        "price": 58999.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=800&q=80",
        "stock": 25,
        "rating": 4.8,
        "rating_count": 9400,
        "is_featured": 1
    },
    {
        "title": "Apple iPhone 16 Pro (Natural Titanium, 256 GB)",
        "description": "Next-gen A18 Pro Bionic chip, dedicated Camera Control tactile button, 48MP Fusion Camera, Grade 5 Titanium frame, 4K 120 fps Dolby Vision recording.",
        "price": 119900.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=800&q=80",
        "stock": 15,
        "rating": 4.9,
        "rating_count": 4200,
        "is_featured": 1
    },
    {
        "title": "Apple iPhone 17 Pro Max (Desert Titanium, 512 GB)",
        "description": "A19 Bionic 2nm architecture, under-display FaceID sensor, 10x periscope optical zoom, ultra-slim bezel LTPO ProMotion 144Hz display.",
        "price": 149900.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02560?auto=format&fit=crop&w=800&q=80",
        "stock": 10,
        "rating": 5.0,
        "rating_count": 1800,
        "is_featured": 1
    },
    {
        "title": "Apple iPhone 18 Ultra Futuristic Edition (Liquid Glass, 1 TB)",
        "description": "True all-screen zero-notch quantum OLED display, Apple Neural Engine X2, holographic FaceTime audio, solid-state haptic volume buttons.",
        "price": 189900.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1530319067432-f2a729c03db5?auto=format&fit=crop&w=800&q=80",
        "stock": 5,
        "rating": 5.0,
        "rating_count": 890,
        "is_featured": 1
    },
    {
        "title": "Samsung Galaxy S24 Ultra 5G (Titanium Gray, 256 GB, 12 GB RAM)",
        "description": "Built-in S-Pen, 200MP camera with Quad Telephoto system, Galaxy AI live translate, Snapdragon 8 Gen 3 for Galaxy, titanium armor frame.",
        "price": 109999.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=800&q=80",
        "stock": 18,
        "rating": 4.9,
        "rating_count": 6120,
        "is_featured": 1
    },
    {
        "title": "Samsung Galaxy S25 Ultra 5G (Titanium Phantom Black, 512 GB)",
        "description": "Next-gen Snapdragon 8 Elite SoC, upgraded 50MP ultra-wide sensor, seamless satellite messaging, anti-reflective Gorilla Armor glass.",
        "price": 124999.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1580910051074-3eb694886505?auto=format&fit=crop&w=800&q=80",
        "stock": 12,
        "rating": 4.9,
        "rating_count": 2340,
        "is_featured": 1
    },
    {
        "title": "Redmi Note 14 Pro+ 5G (Midnight Black, 12GB RAM, 512GB)",
        "description": "200MP OIS camera with 4x lossless in-sensor zoom, 1.5K 120Hz curved AMOLED, 120W HyperCharge (0-100% in 19 mins), IP68 water resistance.",
        "price": 29999.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=800&q=80",
        "stock": 35,
        "rating": 4.7,
        "rating_count": 7820,
        "is_featured": 0
    },
    {
        "title": "Realme GT 6 5G (Fluid Silver, 16GB RAM, 512GB)",
        "description": "Snapdragon 8s Gen 3, industry-brightest 6000 nits Ultra Bright Display, 120W SuperVOOC flash charge, 50MP Sony LYT-808 with OIS.",
        "price": 38999.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=800&q=80",
        "stock": 25,
        "rating": 4.8,
        "rating_count": 3410,
        "is_featured": 0
    },
    {
        "title": "Oppo Reno 12 Pro 5G (Sunset Gold, 12GB RAM, 512GB)",
        "description": "Quad-curved infinite display with splash touch, AI Studio & AI Eraser 2.0, 50MP portrait telephoto camera, aerospace-grade high-strength alloy.",
        "price": 36999.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?auto=format&fit=crop&w=800&q=80",
        "stock": 20,
        "rating": 4.7,
        "rating_count": 2980,
        "is_featured": 0
    },
    {
        "title": "Vivo X100 Pro 5G (Asteroid Black, 16GB RAM, 512GB)",
        "description": "ZEISS 1-inch main sensor with APO floating telephoto lens, Dimensity 9300 flagship chip, custom Vivo V3 imaging chip, 100W FlashCharge.",
        "price": 89999.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1575695342320-d2d2d2f9b73f?auto=format&fit=crop&w=800&q=80",
        "stock": 14,
        "rating": 4.9,
        "rating_count": 2100,
        "is_featured": 1
    },
    {
        "title": "Motorola Edge 50 Ultra (Nordic Wood Finish, 16GB, 512GB)",
        "description": "Real FSC-certified Nordic wood back, Pantone-validated camera & display, 125W TurboPower charging with 50W wireless, IP68 water resistance.",
        "price": 54999.0,
        "category": "Mobiles",
        "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=800&q=80",
        "stock": 16,
        "rating": 4.8,
        "rating_count": 1820,
        "is_featured": 0
    },

    # =========================================================================
    # 2. TWO WHEELERS & MOTOR BIKES (Bullet, Pulsar, Apache, Glamour, EV)
    # =========================================================================
    {
        "title": "Royal Enfield Bullet 350 (Standard Black, Dual Channel ABS)",
        "description": "Iconic hand-painted pinstripes on fuel tank, 349cc J-series smooth air-oil cooled single-cylinder engine, characteristic thump, wide single bench seat.",
        "price": 173562.0,
        "category": "2 Wheelers",
        "image_url": "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80",
        "stock": 6,
        "rating": 4.9,
        "rating_count": 12400,
        "is_featured": 1
    },
    {
        "title": "Bajaj Pulsar NS400Z (Glossy Ebony Black, 373cc DOHC)",
        "description": "Biggest Pulsar ever built! 373cc liquid-cooled DOHC engine producing 40 PS power, 43mm USD front forks, 4 ride modes, switchable traction control.",
        "price": 185000.0,
        "category": "2 Wheelers",
        "image_url": "https://images.unsplash.com/photo-1609630875171-b1321377ee65?auto=format&fit=crop&w=800&q=80",
        "stock": 8,
        "rating": 4.8,
        "rating_count": 4890,
        "is_featured": 1
    },
    {
        "title": "TVS Apache RTR 160 4V (Matte Black Special Edition, Dual Disc ABS)",
        "description": "159.7cc oil-cooled 4-valve race tuned engine, SmartXonnect Bluetooth cluster with voice assist, 3 ride modes (Urban, Rain, Sport), bullpup exhaust.",
        "price": 124870.0,
        "category": "2 Wheelers",
        "image_url": "https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?auto=format&fit=crop&w=800&q=80",
        "stock": 10,
        "rating": 4.8,
        "rating_count": 6420,
        "is_featured": 0
    },
    {
        "title": "Hero Glamour XTEC 125 (Candy Blazing Red, Bluetooth Navigation)",
        "description": "125cc fuel-injected engine with i3S idle stop-start system, full digital instrument console with turn-by-turn navigation, integrated USB phone charger.",
        "price": 89990.0,
        "category": "2 Wheelers",
        "image_url": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=800&q=80",
        "stock": 12,
        "rating": 4.7,
        "rating_count": 8900,
        "is_featured": 0
    },
    {
        "title": "Ola S1 Pro Gen 2 Electric Scooter (Midnight Blue, 195 km Range)",
        "description": "11 kW peak power motor with 120 km/h top speed, 0 to 40 km/h in 2.6s, MoveOS 4 smart display navigation, cruise control, hypercharging.",
        "price": 129999.0,
        "category": "2 Wheelers",
        "image_url": "https://images.unsplash.com/photo-1558981420-87aa9dad1c89?auto=format&fit=crop&w=800&q=80",
        "stock": 7,
        "rating": 4.8,
        "rating_count": 3840,
        "is_featured": 1
    },
    {
        "title": "Ather 450X Gen 3 Smart Electric Scooter (Lunar Grey, 111 km Range)",
        "description": "Aluminum chassis with precision balanced 50:50 weight distribution, 7-inch touchscreen dashboard with Google Maps, AutoHold hill assist.",
        "price": 139999.0,
        "category": "2 Wheelers",
        "image_url": "https://images.unsplash.com/photo-1558980664-3a031cf67ea8?auto=format&fit=crop&w=800&q=80",
        "stock": 5,
        "rating": 4.9,
        "rating_count": 2910,
        "is_featured": 0
    },

    # =========================================================================
    # 3. LAPTOPS (MacBook M1/M2/M3/M4, HP, Dell, Acer, Asus)
    # =========================================================================
    {
        "title": "Apple MacBook Air 13-inch (M1 Chip, 8GB Unified RAM, 256GB SSD)",
        "description": "Revolutionary Apple Silicon M1 chip, completely silent fanless design, up to 18 hours battery life, 13.3-inch Retina display with P3 wide color.",
        "price": 64990.0,
        "category": "Laptops",
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80",
        "stock": 25,
        "rating": 4.9,
        "rating_count": 18200,
        "is_featured": 1
    },
    {
        "title": "Apple MacBook Air 13.6-inch (M2 Chip, Midnight, 16GB RAM, 512GB SSD)",
        "description": "Redesigned ultra-slim aluminum unibody, MagSafe 3 charging port, 1080p FaceTime HD camera, Liquid Retina display with 500 nits brightness.",
        "price": 99900.0,
        "category": "Laptops",
        "image_url": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=800&q=80",
        "stock": 20,
        "rating": 4.9,
        "rating_count": 6800,
        "is_featured": 1
    },
    {
        "title": "Apple MacBook Air 15.3-inch (M3 Chip, Space Grey, 16GB RAM, 512GB)",
        "description": "Powerful 3nm M3 chip with hardware-accelerated ray tracing, support for up to two external displays, Wi-Fi 6E, immersive six-speaker sound system.",
        "price": 124900.0,
        "category": "Laptops",
        "image_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=800&q=80",
        "stock": 15,
        "rating": 4.9,
        "rating_count": 3100,
        "is_featured": 1
    },
    {
        "title": "Apple MacBook Pro 14-inch (M4 Pro Chip, Space Black, 24GB RAM, 1TB)",
        "description": "Blazing fast M4 Pro processor engineered for AI workloads, Liquid Retina XDR display with nano-texture option, Thunderbolt 5 ports, 24-hour battery.",
        "price": 199900.0,
        "category": "Laptops",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=80",
        "stock": 8,
        "rating": 5.0,
        "rating_count": 1240,
        "is_featured": 1
    },
    {
        "title": "HP OMEN 16 Gaming Laptop (Intel Core i7 14th Gen, RTX 4070 8GB, 16GB/1TB)",
        "description": "16.1-inch QHD 240Hz gaming display with 3ms response, OMEN Tempest Cooling technology, per-key RGB backlit keyboard, Bang & Olufsen audio.",
        "price": 134990.0,
        "category": "Laptops",
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=800&q=80",
        "stock": 12,
        "rating": 4.8,
        "rating_count": 2180,
        "is_featured": 0
    },
    {
        "title": "Dell XPS 15 (Core i9 13th Gen, 3.5K OLED Touch, RTX 4060, 32GB/1TB)",
        "description": "Machined aluminum chassis with carbon fiber palm rest, 15.6-inch 3.5K InfinityEdge OLED display with 100% DCI-P3 color gamut, quad-speaker design.",
        "price": 178990.0,
        "category": "Laptops",
        "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=800&q=80",
        "stock": 10,
        "rating": 4.9,
        "rating_count": 1420,
        "is_featured": 1
    },
    {
        "title": "Asus ROG Zephyrus G16 (Intel Core Ultra 9, RTX 4080, 2.5K 240Hz OLED)",
        "description": "CNC-machined aluminum body under 1.85kg, ROG Slash Lighting matrix, 2.5K ROG Nebula OLED panel with G-SYNC, 2nd Gen Arc Flow Fans.",
        "price": 194990.0,
        "category": "Laptops",
        "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80",
        "stock": 7,
        "rating": 4.9,
        "rating_count": 980,
        "is_featured": 0
    },
    {
        "title": "Acer Predator Helios 16 (Core i7 13th Gen, RTX 4060, 165Hz WQXGA, 16GB/1TB)",
        "description": "Custom engineered 5th Gen AeroBlade 3D metal fans, liquid metal thermal grease, Mini-LED per-key RGB keyboard, Killer DoubleShot Pro networking.",
        "price": 114990.0,
        "category": "Laptops",
        "image_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=800&q=80",
        "stock": 14,
        "rating": 4.7,
        "rating_count": 3120,
        "is_featured": 0
    },

    # =========================================================================
    # 4. FASHION & CLOTHING (Cargo Pants, Shirts, T-Shirts Full/Half, Jackets)
    # =========================================================================
    {
        "title": "Ripstop Tactical Military Cargo Pants (6 Deep Pockets, Olive Green)",
        "description": "Heavy-duty 280 GSM ripstop cotton fabric with Teflon water-resistant finish, articulated knee seams, deep snap-closure cargo pockets, relaxed straight fit.",
        "price": 1799.0,
        "category": "Fashion",
        "image_url": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?auto=format&fit=crop&w=800&q=80",
        "stock": 45,
        "rating": 4.8,
        "rating_count": 7820,
        "is_featured": 1
    },
    {
        "title": "Urban Commuter Multi-Pocket Cargo Pants (Matte Obsidian Black)",
        "description": "Modern tapered streetwear silhouette with elasticated drawcord cuffs, FIDLOCK magnetic side buckle straps, and breathable stretch cotton twill.",
        "price": 1999.0,
        "category": "Fashion",
        "image_url": "https://images.unsplash.com/photo-1517445312882-bc9910d016b7?auto=format&fit=crop&w=800&q=80",
        "stock": 35,
        "rating": 4.7,
        "rating_count": 4210,
        "is_featured": 0
    },
    {
        "title": "Levi's Men's 511 Slim Fit Stretch Denim Jeans (Dark Indigo Wash)",
        "description": "Classic modern slim-cut jeans made with Levi's Flex stretch technology for all-day comfort and long-lasting shape retention.",
        "price": 2499.0,
        "category": "Fashion",
        "image_url": "https://images.unsplash.com/photo-1542272604-780c96856592?auto=format&fit=crop&w=800&q=80",
        "stock": 40,
        "rating": 4.8,
        "rating_count": 6420,
        "is_featured": 1
    },
    {
        "title": "Allen Solly Men's Slim Fit 100% Combed Cotton Casual Shirt (Sky Blue)",
        "description": "Tailored cutaway spread collar with curved hemline and contrast inner cuff detailing, breathable soft combed cotton.",
        "price": 1199.0,
        "category": "Fashion",
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=80",
        "stock": 50,
        "rating": 4.6,
        "rating_count": 3850,
        "is_featured": 0
    },
    {
        "title": "Raymond Fine Linen Formal Full-Sleeve Luxury Shirt (Crisp White)",
        "description": "Woven from 100% pure European flax linen. Natural breathability, mother-of-pearl buttons, stiffened dress collar for boardroom meetings.",
        "price": 2899.0,
        "category": "Fashion",
        "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=80",
        "stock": 30,
        "rating": 4.9,
        "rating_count": 1940,
        "is_featured": 1
    },
    {
        "title": "Bewakoof Heavyweight 240 GSM Oversized Drop-Shoulder Half T-Shirt",
        "description": "Boxy streetwear cut made from 100% pre-shrunk super-combed cotton. High-density ribbed crew neck with minimal chest typography.",
        "price": 699.0,
        "category": "Fashion",
        "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=800&q=80",
        "stock": 80,
        "rating": 4.7,
        "rating_count": 12400,
        "is_featured": 0
    },
    {
        "title": "U.S. Polo Assn. Solid Cotton Full-Sleeve Henley T-Shirt (Navy Blue)",
        "description": "3-button placket waffle knit henley shirt, ribbed cuffs, embroidered heritage chest crest, perfect transitional autumn/spring layering.",
        "price": 1099.0,
        "category": "Fashion",
        "image_url": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?auto=format&fit=crop&w=800&q=80",
        "stock": 60,
        "rating": 4.6,
        "rating_count": 4820,
        "is_featured": 0
    },
    {
        "title": "Winter Thermal Hooded Puffer Down Jacket (Wind & Water Repellent)",
        "description": "90/10 duck down insulation with 650 fill power. Thermal reflective interior lining, storm-flap dual front zipper, and fleece-lined zip pockets.",
        "price": 3499.0,
        "category": "Fashion",
        "image_url": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?auto=format&fit=crop&w=800&q=80",
        "stock": 28,
        "rating": 4.8,
        "rating_count": 5120,
        "is_featured": 1
    },
    {
        "title": "Genuine Lambskin Leather Biker Motorcycle Jacket (Heavy Brass Zips)",
        "description": "Handcrafted from 100% authentic full-grain lambskin leather. Asymmetrical front zip, snap-down notch lapels, zippered cuffs, satin diamond quilted lining.",
        "price": 7999.0,
        "category": "Fashion",
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=80",
        "stock": 18,
        "rating": 4.9,
        "rating_count": 1840,
        "is_featured": 1
    },

    # =========================================================================
    # 5. FOOTWEAR & SLIPPERS (Nike, Jordan, Puma, Adidas, Red Tape, Slides)
    # =========================================================================
    {
        "title": "Nike Air Jordan 1 Retro High OG (Chicago Red / White / Black)",
        "description": "Iconic high-top basketball sneaker in premium full-grain leather, encapsulated Air-Sole heel unit, signature Wings logo, perforated toe box.",
        "price": 16995.0,
        "category": "Footwear",
        "image_url": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=800&q=80",
        "stock": 14,
        "rating": 5.0,
        "rating_count": 15800,
        "is_featured": 1
    },
    {
        "title": "Nike Air Max 270 React Running Shoes (Triple Black)",
        "description": "Features Nike's biggest heel Air unit yet for a super-soft ride, lightweight layered no-sew mesh upper, full rubber outsole coverage.",
        "price": 12995.0,
        "category": "Footwear",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80",
        "stock": 22,
        "rating": 4.8,
        "rating_count": 8900,
        "is_featured": 1
    },
    {
        "title": "Puma Nitro Deviate Carbon Plate Running Shoes (Emerald Fast)",
        "description": "Dual-layer NITRO Elite foam infused with nitrogen gas, full-length INNOPLATE carbon fiber propulsion plate, PUMAGRIP high-traction rubber.",
        "price": 8999.0,
        "category": "Footwear",
        "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=800&q=80",
        "stock": 18,
        "rating": 4.9,
        "rating_count": 3410,
        "is_featured": 0
    },
    {
        "title": "Adidas Ultraboost Light Running Shoes (Core White / Solar Red)",
        "description": "Lightest Boost cushioning foam ever created with 30% lighter material, Linear Energy Push system on the sole, Primeknit+ foot-hugging upper.",
        "price": 14999.0,
        "category": "Footwear",
        "image_url": "https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?auto=format&fit=crop&w=800&q=80",
        "stock": 20,
        "rating": 4.9,
        "rating_count": 6700,
        "is_featured": 1
    },
    {
        "title": "Red Tape Classic Casual Lace-Up Sneakers (Pure White & Pine)",
        "description": "Premium PU upper with perforated side panels, cushioned memory foam insole, flexible vulcanized TPR sole providing all-day walking comfort.",
        "price": 1399.0,
        "category": "Footwear",
        "image_url": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=800&q=80",
        "stock": 45,
        "rating": 4.6,
        "rating_count": 18200,
        "is_featured": 0
    },
    {
        "title": "Adidas Adilette Comfort Slides / Slippers (Cloudfoam Footbed)",
        "description": "Pillowy-soft Cloudfoam Plus contoured footbed recharges energy, single-bandage synthetic upper with classic 3-stripes, lightweight EVA outsole.",
        "price": 1999.0,
        "category": "Footwear",
        "image_url": "https://images.unsplash.com/photo-1560769629-975ec94e6a86?auto=format&fit=crop&w=800&q=80",
        "stock": 60,
        "rating": 4.8,
        "rating_count": 9200,
        "is_featured": 0
    },
    {
        "title": "Puma Softride Pro Slides / Slippers (Ultra Cushion EVA Sole)",
        "description": "SOFTRIDE foam technology designed for extreme cushioning and all-day comfort, water-resistant molded synthetic strap with Puma Cat debossing.",
        "price": 1499.0,
        "category": "Footwear",
        "image_url": "https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?auto=format&fit=crop&w=800&q=80",
        "stock": 55,
        "rating": 4.7,
        "rating_count": 5400,
        "is_featured": 0
    },
    {
        "title": "Red Tape Casual Comfort Thong Slippers (Leatherette Grip Footbed)",
        "description": "Ergonomic arch-supporting TPR footbed with textured anti-skid grooves, soft fabric toe post, lightweight durable outdoor flip-flops.",
        "price": 699.0,
        "category": "Footwear",
        "image_url": "https://images.unsplash.com/photo-1535043934128-cf0b28d52f95?auto=format&fit=crop&w=800&q=80",
        "stock": 70,
        "rating": 4.5,
        "rating_count": 7800,
        "is_featured": 0
    },

    # =========================================================================
    # 6. ELECTRONICS & AUDIO (AirPods, Sony, OnePlus, boAt, Speakers, Power Bank)
    # =========================================================================
    {
        "title": "Apple AirPods Pro (2nd Generation with MagSafe USB-C Case)",
        "description": "Apple H2 headphone chip, up to 2x more Active Noise Cancellation, Adaptive Audio & Transparency mode, Personalized Spatial Audio with dynamic head tracking.",
        "price": 22900.0,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?auto=format&fit=crop&w=800&q=80",
        "stock": 30,
        "rating": 4.9,
        "rating_count": 14200,
        "is_featured": 1
    },
    {
        "title": "Sony WH-1000XM5 Wireless Noise Cancelling Over-Ear Headphones",
        "description": "Industry-leading noise cancellation with two processors and 8 microphones, soft-fit synthetic leather, 30-hour battery life with 3-minute quick charge.",
        "price": 26990.0,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
        "stock": 20,
        "rating": 4.9,
        "rating_count": 8900,
        "is_featured": 1
    },
    {
        "title": "OnePlus Buds Pro 2 True Wireless Earbuds (Co-created with Dynaudio)",
        "description": "MelodyBoost dual drivers (11mm woofer + 6mm tweeter), 48dB Smart Adaptive Noise Cancellation, spatial audio with head tracking, 39 hours battery.",
        "price": 9999.0,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80",
        "stock": 35,
        "rating": 4.8,
        "rating_count": 4820,
        "is_featured": 0
    },
    {
        "title": "boAt Airdopes 141 True Wireless Earbuds (42H Playtime, Beast Mode)",
        "description": "8mm dynamic drivers with boAt Signature Sound, ENx technology for noise-free calling, 80ms low-latency Beast Mode for mobile gaming, ASAP charge.",
        "price": 1299.0,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1572536147248-ac59a8abfa4b?auto=format&fit=crop&w=800&q=80",
        "stock": 80,
        "rating": 4.5,
        "rating_count": 45000,
        "is_featured": 0
    },
    {
        "title": "JBL Flip 6 Portable Waterproof Bluetooth Speaker (30W Deep Bass)",
        "description": "2-way speaker system engineered for loud, crystal clear audio with dual passive radiators for deep bass. IP67 waterproof and dustproof, 12 hours playtime.",
        "price": 9999.0,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=800&q=80",
        "stock": 25,
        "rating": 4.8,
        "rating_count": 11200,
        "is_featured": 1
    },
    {
        "title": "Anker 737 Power Bank PowerCore 24000mAh (140W Ultra Fast Charge)",
        "description": "Massive 24000mAh capacity with two-way 140W Power Delivery 3.1. Smart digital display shows real-time output power and recharge time remaining.",
        "price": 11999.0,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1609592426507-b248a3350275?auto=format&fit=crop&w=800&q=80",
        "stock": 30,
        "rating": 4.9,
        "rating_count": 3200,
        "is_featured": 0
    },
    {
        "title": "Cosmic Byte Firefly Mechanical Gaming Keyboard (RGB Outemu Blue)",
        "description": "Compact Tenkeyless (87 keys) form factor, tactile Outemu Blue mechanical switches, customizable per-key RGB backlighting, anti-ghosting keys.",
        "price": 2199.0,
        "category": "Electronics",
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80",
        "stock": 35,
        "rating": 4.6,
        "rating_count": 4120,
        "is_featured": 0
    },

    # =========================================================================
    # 7. APPLIANCES & FANS (Smart BLDC Fans, Table Fans, Mixers, Irons)
    # =========================================================================
    {
        "title": "Atomberg Renesa 1200mm Smart BLDC Ceiling Fan with Remote (White)",
        "description": "Consumes only 28 Watts at top speed (saves up to 65% on electricity bills), 360 RPM high speed delivery, timer and boost mode via smart remote control.",
        "price": 3699.0,
        "category": "Appliances",
        "image_url": "https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=800&q=80",
        "stock": 30,
        "rating": 4.8,
        "rating_count": 18400,
        "is_featured": 1
    },
    {
        "title": "Havells Stealth Air Metallic High-Speed Ceiling Fan (1200mm, Pearl White)",
        "description": "Aerodynamically contoured dust-resistant composite blades delivering silent whisper operation with massive 280 cmm air volume displacement.",
        "price": 4999.0,
        "category": "Appliances",
        "image_url": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?auto=format&fit=crop&w=800&q=80",
        "stock": 22,
        "rating": 4.7,
        "rating_count": 6800,
        "is_featured": 0
    },
    {
        "title": "Crompton High-Speed Oscillating Pedestal / Table Fan (400mm)",
        "description": "Heavy copper-wound motor delivering 2100 RPM hurricane air breeze, wide 90-degree thermal oscillation, height adjustable telescopic stand.",
        "price": 2299.0,
        "category": "Appliances",
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "stock": 25,
        "rating": 4.6,
        "rating_count": 4120,
        "is_featured": 0
    },
    {
        "title": "Prestige Iris 750W Heavy Duty Mixer Grinder (3 SS Jars + Juicer)",
        "description": "750 Watt high-torque motor with overload trip switch, mirror polished stainless steel multipurpose grinding jars, transparent polycarbonate juicer jar.",
        "price": 2899.0,
        "category": "Appliances",
        "image_url": "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?auto=format&fit=crop&w=800&q=80",
        "stock": 28,
        "rating": 4.6,
        "rating_count": 14200,
        "is_featured": 1
    },
    {
        "title": "Pigeon by Stovekraft Cruise 1800W Induction Cooktop",
        "description": "Energy-efficient electromagnetic heating plate with 7 pre-set Indian cooking menus, LED digital display, push-button controls, dual thermal sensor.",
        "price": 1699.0,
        "category": "Appliances",
        "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80",
        "stock": 35,
        "rating": 4.5,
        "rating_count": 21500,
        "is_featured": 0
    },

    # =========================================================================
    # 8. FURNITURE & TABLES (Study Table, Dining Table, Bar Stools, Ergonomic Chairs)
    # =========================================================================
    {
        "title": "Modern Minimalist Solid Teak Wood Computer Study Desk with Drawers",
        "description": "Durable 100% natural seasoned teak wood desktop with chamfered smooth edges, dual pull-out storage drawers, integrated wire management grommet.",
        "price": 7999.0,
        "category": "Furniture",
        "image_url": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=800&q=80",
        "stock": 18,
        "rating": 4.8,
        "rating_count": 3420,
        "is_featured": 1
    },
    {
        "title": "Nilkamal Sheesham Hardwood 4-Seater Dining Table & Chairs Set",
        "description": "Solid Sheesham wood construction with rich natural honey grain finish, 4 ergonomically contoured slat-back chairs, stain-resistant lacquered tabletop.",
        "price": 14999.0,
        "category": "Furniture",
        "image_url": "https://images.unsplash.com/photo-1617806118233-18e1de247200?auto=format&fit=crop&w=800&q=80",
        "stock": 10,
        "rating": 4.7,
        "rating_count": 1420,
        "is_featured": 0
    },
    {
        "title": "Wakefit Ergonomic High-Back Breathable Mesh Office Chair (Lumbar Support)",
        "description": "Adjustable 2D lumbar spine support, pneumatic Class-4 hydraulic gas lift, synchro-tilt locking mechanism, high-density molded seat foam.",
        "price": 5999.0,
        "category": "Furniture",
        "image_url": "https://images.unsplash.com/photo-1580481077195-c3a8a3a0e633?auto=format&fit=crop&w=800&q=80",
        "stock": 25,
        "rating": 4.8,
        "rating_count": 9200,
        "is_featured": 1
    },
    {
        "title": "Luxury Velvet Adjustable Swivel Bar Stool with Chrome Base (Set of 2)",
        "description": "High-density foam padded bucket seat wrapped in soft stain-resistant velvet fabric. 360-degree swivel with hydraulic footrest height adjuster.",
        "price": 4999.0,
        "category": "Furniture",
        "image_url": "https://images.unsplash.com/photo-1503602642458-232111445657?auto=format&fit=crop&w=800&q=80",
        "stock": 20,
        "rating": 4.8,
        "rating_count": 1840,
        "is_featured": 1
    },
    {
        "title": "Sleepyhead Kiki Engineered Wood Center Coffee Table (Walnut)",
        "description": "Modern low-profile living room center table with lower shelf storage for books and remotes, scratch-resistant European melamine coating.",
        "price": 2899.0,
        "category": "Furniture",
        "image_url": "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?auto=format&fit=crop&w=800&q=80",
        "stock": 25,
        "rating": 4.6,
        "rating_count": 2180,
        "is_featured": 0
    },

    # =========================================================================
    # 9. LUGGAGE & TROLLEY BAGS (American Tourister, Safari, Skybags)
    # =========================================================================
    {
        "title": "American Tourister 3-Piece Hard-Sided Spinner Trolley Bag Combo (55/65/75cm)",
        "description": "Complete family luggage set (Small Cabin, Medium & Large Check-In). Ultra-lightweight impact-absorbing polypropylene shell, TSA 3-digit combination lock, 360-degree silent spinner wheels.",
        "price": 9999.0,
        "category": "Luggage & Bags",
        "image_url": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?auto=format&fit=crop&w=800&q=80",
        "stock": 25,
        "rating": 4.9,
        "rating_count": 14200,
        "is_featured": 1
    },
    {
        "title": "Safari Pentagon 55cm Hard-Side Cabin Trolley Suitcase (Cyan Blue)",
        "description": "Scratch-resistant polycarbonate exterior shell with stylish textured geometric pattern, smooth glide dual multi-directional wheels, telescopic iron trolley handle.",
        "price": 2499.0,
        "category": "Luggage & Bags",
        "image_url": "https://images.unsplash.com/photo-1581553680321-4fffae59fccd?auto=format&fit=crop&w=800&q=80",
        "stock": 40,
        "rating": 4.7,
        "rating_count": 8900,
        "is_featured": 0
    },
    {
        "title": "American Tourister 32L Water-Resistant Laptop Backpack (Rain Cover)",
        "description": "High-density 1680D nylon with dedicated padded sleeve for up to 15.6-inch laptops, 3 spacious compartments, ergonomic mesh back padding, bundled neon rain cover.",
        "price": 1399.0,
        "category": "Luggage & Bags",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80",
        "stock": 50,
        "rating": 4.8,
        "rating_count": 9400,
        "is_featured": 0
    },

    # =========================================================================
    # 10. STATIONERY & OFFICE (Notebooks, Parker Pen, Highlighters, Markers)
    # =========================================================================
    {
        "title": "Classmate Pulse Spiral Bound Long Notebooks (Pack of 6, 300 Pages)",
        "description": "Elemental chlorine-free bright white paper with smooth glide writing texture, single-line ruling, micro-perforated tear-off pages, durable poly cover.",
        "price": 549.0,
        "category": "Stationery",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80",
        "stock": 60,
        "rating": 4.8,
        "rating_count": 12400,
        "is_featured": 0
    },
    {
        "title": "Parker Vector Matte Black Rollerball Pen with Chrome Trim (Gift Box)",
        "description": "Timeless iconic design with stainless steel cap and body in sleek matte black finish. Ultra-smooth FreeInk rollerball technology for effortless handwriting.",
        "price": 499.0,
        "category": "Stationery",
        "image_url": "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?auto=format&fit=crop&w=800&q=80",
        "stock": 70,
        "rating": 4.9,
        "rating_count": 8900,
        "is_featured": 1
    },
    {
        "title": "Faber-Castell Pastel Textliner Highlighters (Pack of 8 Aesthetic Shades)",
        "description": "Soft pastel water-based ink that doesn't bleed through thin notebook pages. Chisel tip marks 1mm, 2mm and 5mm line widths for neat study notes.",
        "price": 320.0,
        "category": "Stationery",
        "image_url": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?auto=format&fit=crop&w=800&q=80",
        "stock": 85,
        "rating": 4.8,
        "rating_count": 6420,
        "is_featured": 0
    },
    {
        "title": "Camlin Whiteboard Marker Pens (Pack of 4 Assorted Colors + Eraser)",
        "description": "Bright erasable ink with minimal odor, bold bullet tip for clear presentation writing on whiteboards, easily wipes clean without leaving ghost stains.",
        "price": 160.0,
        "category": "Stationery",
        "image_url": "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?auto=format&fit=crop&w=800&q=80",
        "stock": 90,
        "rating": 4.6,
        "rating_count": 4120,
        "is_featured": 0
    },

    # =========================================================================
    # 11. FOOD, OILS & HEALTH (Sunflower Oil, Coconut Oil, Peanut Butter, Protein)
    # =========================================================================
    {
        "title": "Fortune Sunlite 100% Pure Refined Sunflower Cooking Oil (5 Litre Can)",
        "description": "Enriched with Vitamins A and D. Light and healthy cooking oil with high smoke point, helps maintain healthy cholesterol levels for daily family cooking.",
        "price": 699.0,
        "category": "Food & Health",
        "image_url": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=800&q=80",
        "stock": 60,
        "rating": 4.8,
        "rating_count": 24200,
        "is_featured": 1
    },
    {
        "title": "Parachute 100% Pure Coconut Hair Oil (1000 ml Bottle)",
        "description": "Made from naturally sun-dried coconuts via a 5-stage purification process. 100% pure and unrefined edible coconut oil for deep hair nourishment and healthy scalp.",
        "price": 389.0,
        "category": "Food & Health",
        "image_url": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?auto=format&fit=crop&w=800&q=80",
        "stock": 75,
        "rating": 4.9,
        "rating_count": 31200,
        "is_featured": 1
    },
    {
        "title": "Pintola All-Natural Creamy Peanut Butter (1kg, 30g High Protein)",
        "description": "100% roasted bold peanuts with zero added sugar, zero salt, zero hydrogenated oils, and zero preservatives. Non-GMO, gluten-free vegan fitness fuel.",
        "price": 399.0,
        "category": "Food & Health",
        "image_url": "https://images.unsplash.com/photo-1589733955941-5eeaf752f6dd?auto=format&fit=crop&w=800&q=80",
        "stock": 70,
        "rating": 4.9,
        "rating_count": 21000,
        "is_featured": 0
    },
    {
        "title": "Tata Tea Gold Premium CTC Tea with Gently Rolled Long Leaves (1kg)",
        "description": "Exquisite blend of rich Assam CTC teas combined with gently rolled aromatic long leaves for exceptional fragrance and deep golden liquor taste.",
        "price": 499.0,
        "category": "Food & Health",
        "image_url": "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?auto=format&fit=crop&w=800&q=80",
        "stock": 80,
        "rating": 4.8,
        "rating_count": 14200,
        "is_featured": 0
    },
    {
        "title": "MuscleBlaze Biozyme Performance Whey Protein (Rich Chocolate, 1kg)",
        "description": "Enhanced absorption formula (EAF) certified by US patent. Delivers 25g protein and 5.51g BCAA per scoop with 50% higher protein absorption.",
        "price": 2499.0,
        "category": "Food & Health",
        "image_url": "https://images.unsplash.com/photo-1579722821273-0f6c7d44362f?auto=format&fit=crop&w=800&q=80",
        "stock": 40,
        "rating": 4.8,
        "rating_count": 9400,
        "is_featured": 1
    },

    # =========================================================================
    # 12. BEAUTY & SOAPS
    # =========================================================================
    {
        "title": "SoapSphere Handmade Organic Charcoal & Tea Tree Detox Bar (Pack of 3)",
        "description": "Handmade cold-processed herbal soap infused with bamboo activated charcoal, pure Australian tea tree oil, and organic shea butter. Controls acne and purifies skin.",
        "price": 399.0,
        "category": "Beauty",
        "image_url": "https://images.unsplash.com/photo-1607006314605-feed26116891?auto=format&fit=crop&w=800&q=80",
        "stock": 70,
        "rating": 4.9,
        "rating_count": 1840,
        "is_featured": 1
    },
    {
        "title": "The Derma Co 1% Hyaluronic Sunscreen Aqua Gel SPF 50 PA++++ (50g)",
        "description": "Ultra-lightweight invisible gel formulation with 1% hyaluronic acid and vitamin E. Absorbs within seconds with zero white cast and maximum UV protection.",
        "price": 449.0,
        "category": "Beauty",
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=800&q=80",
        "stock": 60,
        "rating": 4.7,
        "rating_count": 8900,
        "is_featured": 0
    },
    {
        "title": "Khadi Natural Royal Sandalwood & Honey Nourishing Bath Bar (Pack of 4)",
        "description": "Therapeutic Ayurvedic bathing bars crafted with pure Mysore sandalwood oil, raw wild honey, and vegetable glycerin for silky smooth glowing skin.",
        "price": 349.0,
        "category": "Beauty",
        "image_url": "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?auto=format&fit=crop&w=800&q=80",
        "stock": 65,
        "rating": 4.8,
        "rating_count": 3450,
        "is_featured": 0
    },
    {
        "title": "Maybelline New York Superstay Matte Ink Liquid Lipstick (16Hr Wear)",
        "description": "Highly pigmented liquid matte lipstick with precision arrow applicator. Smudge-proof, transfer-resistant formulation that stays flawless up to 16 hours.",
        "price": 549.0,
        "category": "Beauty",
        "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?auto=format&fit=crop&w=800&q=80",
        "stock": 50,
        "rating": 4.6,
        "rating_count": 7820,
        "is_featured": 0
    },

    # =========================================================================
    # 13. TOYS & BABY
    # =========================================================================
    {
        "title": "LEGO Classic Medium Creative Brick Box Building Set (484 Pieces)",
        "description": "Includes a wide range of LEGO bricks in 35 different colors, 18 tires and wheel rims, window frames, eyes and baseplate. Inspires open-ended creative construction.",
        "price": 2499.0,
        "category": "Toys",
        "image_url": "https://images.unsplash.com/photo-1585366119957-e9730b6d0f60?auto=format&fit=crop&w=800&q=80",
        "stock": 30,
        "rating": 4.9,
        "rating_count": 7800,
        "is_featured": 1
    },
    {
        "title": "Hot Wheels 10-Car Gift Pack of Die-Cast Vehicles (1:64 Scale)",
        "description": "Includes 10 authentic 1:64 scale die-cast metal vehicles with realistic details and cool retro and modern decos. Perfect for collectors and car racing enthusiasts.",
        "price": 1299.0,
        "category": "Toys",
        "image_url": "https://images.unsplash.com/photo-1594787318286-3d835c1d207f?auto=format&fit=crop&w=800&q=80",
        "stock": 40,
        "rating": 4.8,
        "rating_count": 5600,
        "is_featured": 0
    },
    {
        "title": "Pampers All Round Protection Pants Diapers (Large, 64 Count)",
        "description": "Anti-rash blanket enriched with lotion containing aloe vera, ultra-absorb magic gel core for up to 12 hours dryness, 360-degree soft stretchy waistband.",
        "price": 999.0,
        "category": "Baby",
        "image_url": "https://images.unsplash.com/photo-1519689680058-324335c77eba?auto=format&fit=crop&w=800&q=80",
        "stock": 60,
        "rating": 4.8,
        "rating_count": 18200,
        "is_featured": 1
    },
    {
        "title": "LuvLap Sunshine Baby Stroller & Pram with Reversible Handle (Navy)",
        "description": "Certified to European safety standards. Features 3-position reclining seat, 5-point safety harness, reversible handlebar, 360-degree swivel front wheels with brake.",
        "price": 4499.0,
        "category": "Baby",
        "image_url": "https://images.unsplash.com/photo-1591088398332-8a7791972843?auto=format&fit=crop&w=800&q=80",
        "stock": 15,
        "rating": 4.7,
        "rating_count": 2840,
        "is_featured": 0
    },

    # =========================================================================
    # 14. AUTO ACCESSORIES
    # =========================================================================
    {
        "title": "Qubo MagAuto Wireless Car Mount & 15W Qi Fast Magnetic Charger",
        "description": "Strong neodymium magnets securely lock smartphones even on speed bumps. 15W wireless induction charging, 360-degree ball joint for GPS navigation.",
        "price": 1499.0,
        "category": "Auto Accessories",
        "image_url": "https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?auto=format&fit=crop&w=800&q=80",
        "stock": 40,
        "rating": 4.7,
        "rating_count": 2980,
        "is_featured": 1
    },
    {
        "title": "Michelin Digital High Precision 12V Car Tyre Inflator Pump",
        "description": "Inflates a standard tyre from 0 to 35 PSI in under 3 minutes. Backlit digital pressure gauge accurate to +/- 1 PSI with auto-shutoff and bright LED work light.",
        "price": 2899.0,
        "category": "Auto Accessories",
        "image_url": "https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=800&q=80",
        "stock": 25,
        "rating": 4.8,
        "rating_count": 4120,
        "is_featured": 0
    },

    # =========================================================================
    # 15. SPORTS & BALL
    # =========================================================================
    {
        "title": "Nivia Storm Football (Size 5, All-Weather Rubber Moulded, White/Black)",
        "description": "Constructed from 32-panel rubber moulded material with reinforced wound butyl bladder. High abrasion resistance suitable for hard ground, grass, and turf.",
        "price": 449.0,
        "category": "Sports & Ball",
        "image_url": "https://images.unsplash.com/photo-1614632537423-1e6c2e7e0aab?auto=format&fit=crop&w=800&q=80",
        "stock": 60,
        "rating": 4.7,
        "rating_count": 18200,
        "is_featured": 1
    },
    {
        "title": "Yonex Nanoray Light 18i Graphite Badminton Racquet (77g, 30 lbs)",
        "description": "Ultra-lightweight 5U (77 grams) full carbon graphite frame with isometric head shape for larger sweet spot. Allows lightning fast smash returns.",
        "price": 2199.0,
        "category": "Sports & Ball",
        "image_url": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=800&q=80",
        "stock": 30,
        "rating": 4.8,
        "rating_count": 7890,
        "is_featured": 1
    },
    {
        "title": "Cosco Heavy Duty Tournament Cricket Tennis Balls (Pack of 6, Yellow)",
        "description": "Premium woven felt exterior with pressurized rubber core. Consistent high bounce and true trajectory for local gully and club tournament cricket matches.",
        "price": 499.0,
        "category": "Sports & Ball",
        "image_url": "https://images.unsplash.com/photo-1531415074868-036b1c57e329?auto=format&fit=crop&w=800&q=80",
        "stock": 70,
        "rating": 4.8,
        "rating_count": 12400,
        "is_featured": 0
    },

    # =========================================================================
    # 16. BOOKS
    # =========================================================================
    {
        "title": "Atomic Habits: An Easy & Proven Way to Build Good Habits by James Clear",
        "description": "The definitive #1 New York Times bestseller on habit formation. Practical framework for making tiny 1% changes that compound into remarkable results.",
        "price": 549.0,
        "category": "Books",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80",
        "stock": 80,
        "rating": 4.9,
        "rating_count": 48200,
        "is_featured": 1
    },
    {
        "title": "The Psychology of Money: Timeless Lessons on Wealth by Morgan Housel",
        "description": "Engaging short stories exploring the strange ways people think about money, greed, and happiness, and how personal behavior matters more than pure intellect.",
        "price": 299.0,
        "category": "Books",
        "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=800&q=80",
        "stock": 75,
        "rating": 4.8,
        "rating_count": 32100,
        "is_featured": 0
    }
]

def seed_database(force_refresh=True):
    init_db()
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Seed Admin
        cursor.execute("SELECT id FROM users WHERE email = 'admin@store.com'")
        if not cursor.fetchone():
            create_user("Admin Manager", "admin@store.com", "Admin@123", role="admin")
            print("Seeded Admin user: admin@store.com / Admin@123")
            
        # 2. Seed Customer
        cursor.execute("SELECT id FROM users WHERE email = 'user@store.com'")
        if not cursor.fetchone():
            create_user("Afridi Demo", "user@store.com", "User@123", role="customer")
            print("Seeded Demo Customer: user@store.com / User@123")
            
        # 3. Seed Products across all requested categories
        if force_refresh:
            cursor.execute("DELETE FROM products")
            print("Cleared previous products for comprehensive mega catalogue refresh.")

        for p in PRODUCTS:
            cursor.execute("""
                INSERT INTO products (title, description, price, category, image_url, stock, rating, rating_count, is_featured)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["title"], p["description"], p["price"], p["category"],
                p["image_url"], p["stock"], p["rating"], p["rating_count"], p["is_featured"]
            ))
        conn.commit()
        print(f"Successfully seeded {len(PRODUCTS)} products across all requested categories!")

if __name__ == "__main__":
    seed_database(force_refresh=True)
