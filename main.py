from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import json
import asyncio
from datetime import datetime
import uvicorn
import os

app = FastAPI(title="Smart Data Display", version="1.0.0")

# Data models
class Product(BaseModel):
    id: int
    title: str
    description: str
    price: str
    source: str
    link: str
    category: str
    updated_at: str

class DataResponse(BaseModel):
    products: List[Product]
    total: int
    category: str

# In-memory storage (in production, use a database)
products_data = []

class DataScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_tech_products(self) -> List[dict]:
        """Scrape tech products from multiple sources"""
        products = []
        
        # Sample data for demonstration (in real implementation, scrape from actual sites)
        tech_products = [
            {
                "title": "NVIDIA GeForce RTX 4060",
                "description": "Latest mid-range graphics card with excellent 1080p performance",
                "price": "₹32,999",
                "source": "TechSpecs",
                "link": "https://example.com/rtx4060",
                "category": "Graphics Cards"
            },
            {
                "title": "AMD Ryzen 7 7700X",
                "description": "8-core processor perfect for gaming and content creation",
                "price": "₹28,499",
                "source": "TechSpecs",
                "link": "https://example.com/ryzen7700x",
                "category": "Processors"
            },
            {
                "title": "Samsung 980 PRO 1TB",
                "description": "High-performance NVMe SSD with PCIe 4.0 support",
                "price": "₹8,999",
                "source": "TechSpecs",
                "link": "https://example.com/samsung980pro",
                "category": "Storage"
            },
            {
                "title": "Corsair Vengeance LPX 16GB",
                "description": "DDR4 3200MHz memory kit optimized for performance",
                "price": "₹4,899",
                "source": "TechSpecs",
                "link": "https://example.com/corsair16gb",
                "category": "Memory"
            },
            {
                "title": "ASUS ROG Strix B650E-E",
                "description": "Premium AM5 motherboard with Wi-Fi 6E and PCIe 5.0",
                "price": "₹24,999",
                "source": "TechSpecs",
                "link": "https://example.com/asus-b650e",
                "category": "Motherboards"
            },
            {
                "title": "Logitech G Pro X Superlight",
                "description": "Ultra-lightweight wireless gaming mouse",
                "price": "₹11,999",
                "source": "TechSpecs",
                "link": "https://example.com/logitechgpro",
                "category": "Peripherals"
            },
            {
                "title": "SteelSeries Apex Pro",
                "description": "Mechanical keyboard with adjustable actuation",
                "price": "₹18,999",
                "source": "TechSpecs",
                "link": "https://example.com/steelseries-apex",
                "category": "Peripherals"
            },
            {
                "title": "MSI MAG 274QRF-QD",
                "description": "27-inch 1440p gaming monitor with 165Hz refresh rate",
                "price": "₹26,999",
                "source": "TechSpecs",
                "link": "https://example.com/msi-monitor",
                "category": "Monitors"
            },
            {
                "title": "Cooler Master MasterLiquid ML240L",
                "description": "240mm AIO liquid cooler with RGB lighting",
                "price": "₹7,999",
                "source": "TechSpecs",
                "link": "https://example.com/coolermaster-aio",
                "category": "Cooling"
            },
            {
                "title": "Seasonic Focus GX-850",
                "description": "80+ Gold modular power supply unit",
                "price": "₹12,999",
                "source": "TechSpecs",
                "link": "https://example.com/seasonic-psu",
                "category": "Power Supply"
            },
            {
                "title": "Intel Core i5-13600K",
                "description": "13th gen processor with excellent gaming performance",
                "price": "₹24,999",
                "source": "TechSpecs",
                "link": "https://example.com/intel-i5-13600k",
                "category": "Processors"
            },
            {
                "title": "NVIDIA GeForce RTX 4070",
                "description": "High-performance graphics card for 1440p gaming",
                "price": "₹54,999",
                "source": "TechSpecs",
                "link": "https://example.com/rtx4070",
                "category": "Graphics Cards"
            },
            {
                "title": "G.Skill Trident Z RGB 32GB",
                "description": "DDR4 3600MHz memory kit with RGB lighting",
                "price": "₹12,999",
                "source": "TechSpecs",
                "link": "https://example.com/gskill-32gb",
                "category": "Memory"
            },
            {
                "title": "Western Digital Black SN850X 2TB",
                "description": "High-speed NVMe SSD for gaming and content creation",
                "price": "₹16,999",
                "source": "TechSpecs",
                "link": "https://example.com/wd-black-2tb",
                "category": "Storage"
            },
            {
                "title": "Razer DeathAdder V3",
                "description": "Ergonomic gaming mouse with Focus Pro 30K sensor",
                "price": "₹8,999",
                "source": "TechSpecs",
                "link": "https://example.com/razer-deathadder",
                "category": "Peripherals"
            },
            {
                "title": "LG 27GP850-B",
                "description": "27-inch 1440p IPS monitor with 165Hz and G-Sync",
                "price": "₹29,999",
                "source": "TechSpecs",
                "link": "https://example.com/lg-monitor",
                "category": "Monitors"
            },
            {
                "title": "Noctua NH-D15",
                "description": "Premium dual-tower CPU cooler with excellent cooling",
                "price": "₹8,999",
                "source": "TechSpecs",
                "link": "https://example.com/noctua-nhd15",
                "category": "Cooling"
            },
            {
                "title": "EVGA SuperNOVA 750 G6",
                "description": "80+ Gold fully modular PSU with 10-year warranty",
                "price": "₹10,999",
                "source": "TechSpecs",
                "link": "https://example.com/evga-psu",
                "category": "Power Supply"
            },
            {
                "title": "MSI B550 Gaming Plus",
                "description": "Mid-range AM4 motherboard with PCIe 4.0 support",
                "price": "₹13,999",
                "source": "TechSpecs",
                "link": "https://example.com/msi-b550",
                "category": "Motherboards"
            },
            {
                "title": "HyperX Cloud II",
                "description": "Gaming headset with 7.1 virtual surround sound",
                "price": "₹6,999",
                "source": "TechSpecs",
                "link": "https://example.com/hyperx-cloud2",
                "category": "Peripherals"
            }
        ]
        
        for i, product in enumerate(tech_products):
            products.append({
                "id": i + 1,
                "title": product["title"],
                "description": product["description"],
                "price": product["price"],
                "source": product["source"],
                "link": product["link"],
                "category": product["category"],
                "updated_at": datetime.now().isoformat()
            })
        
        return products

# Initialize scraper
scraper = DataScraper()

@app.on_event("startup")
async def startup_event():
    """Load initial data on startup"""
    global products_data
    products_data = scraper.scrape_tech_products()

@app.get("/")
async def root():
    """Serve the main HTML page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Data Display - Tech Products</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
                color: white;
            }
            
            .header h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .controls {
                background: rgba(255,255,255,0.95);
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            
            .controls-row {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                align-items: center;
            }
            
            .control-group {
                display: flex;
                flex-direction: column;
                gap: 5px;
            }
            
            .control-group label {
                font-weight: 600;
                color: #555;
            }
            
            input, select, button {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
            }
            
            button {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                cursor: pointer;
                border: none;
                font-weight: 600;
                transition: transform 0.2s;
            }
            
            button:hover {
                transform: translateY(-2px);
            }
            
            .stats {
                background: rgba(255,255,255,0.95);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
                font-weight: 600;
            }
            
            .products-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 20px;
            }
            
            .product-card {
                background: rgba(255,255,255,0.95);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s, box-shadow 0.3s;
            }
            
            .product-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }
            
            .product-title {
                font-size: 1.2rem;
                font-weight: 700;
                margin-bottom: 10px;
                color: #333;
            }
            
            .product-description {
                color: #666;
                margin-bottom: 15px;
                line-height: 1.5;
            }
            
            .product-details {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }
            
            .product-price {
                font-size: 1.1rem;
                font-weight: 700;
                color: #e74c3c;
            }
            
            .product-category {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
            }
            
            .product-link {
                display: inline-block;
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                text-decoration: none;
                font-size: 0.9rem;
                font-weight: 600;
                transition: transform 0.2s;
            }
            
            .product-link:hover {
                transform: scale(1.05);
            }
            
            .loading {
                text-align: center;
                padding: 40px;
                color: white;
                font-size: 1.2rem;
            }
            
            .error {
                background: #e74c3c;
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            
            @media (max-width: 768px) {
                .controls-row {
                    flex-direction: column;
                    align-items: stretch;
                }
                
                .products-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Smart Data Display</h1>
                <p>Discover the latest tech products with real-time data</p>
            </div>
            
            <div class="controls">
                <div class="controls-row">
                    <div class="control-group">
                        <label for="searchInput">Search Products:</label>
                        <input type="text" id="searchInput" placeholder="Search by title or description...">
                    </div>
                    <div class="control-group">
                        <label for="categoryFilter">Filter by Category:</label>
                        <select id="categoryFilter">
                            <option value="">All Categories</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label for="sortBy">Sort by:</label>
                        <select id="sortBy">
                            <option value="title">Title</option>
                            <option value="price">Price</option>
                            <option value="category">Category</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label>&nbsp;</label>
                        <button onclick="refreshData()">🔄 Refresh Data</button>
                    </div>
                </div>
            </div>
            
            <div id="stats" class="stats"></div>
            <div id="error" class="error" style="display: none;"></div>
            <div id="loading" class="loading">Loading products...</div>
            <div id="products" class="products-grid"></div>
        </div>
        
        <script>
            let allProducts = [];
            let filteredProducts = [];
            
            async function fetchProducts() {
                try {
                    const response = await fetch('/api/products');
                    const data = await response.json();
                    allProducts = data.products;
                    filteredProducts = [...allProducts];
                    populateCategories();
                    updateStats();
                    renderProducts();
                    hideLoading();
                } catch (error) {
                    showError('Failed to load products. Please try again.');
                    hideLoading();
                }
            }
            
            function populateCategories() {
                const categories = [...new Set(allProducts.map(p => p.category))];
                const categorySelect = document.getElementById('categoryFilter');
                categorySelect.innerHTML = '<option value="">All Categories</option>';
                categories.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category;
                    option.textContent = category;
                    categorySelect.appendChild(option);
                });
            }
            
            function updateStats() {
                const stats = document.getElementById('stats');
                const categories = [...new Set(filteredProducts.map(p => p.category))];
                stats.innerHTML = `
                    📊 Showing ${filteredProducts.length} products from ${categories.length} categories
                `;
            }
            
            function renderProducts() {
                const container = document.getElementById('products');
                container.innerHTML = '';
                
                filteredProducts.forEach(product => {
                    const card = document.createElement('div');
                    card.className = 'product-card';
                    card.innerHTML = `
                        <div class="product-title">${product.title}</div>
                        <div class="product-description">${product.description}</div>
                        <div class="product-details">
                            <div class="product-price">${product.price}</div>
                            <div class="product-category">${product.category}</div>
                        </div>
                        <a href="${product.link}" class="product-link" target="_blank">View Product</a>
                    `;
                    container.appendChild(card);
                });
            }
            
            function filterProducts() {
                const searchTerm = document.getElementById('searchInput').value.toLowerCase();
                const category = document.getElementById('categoryFilter').value;
                const sortBy = document.getElementById('sortBy').value;
                
                filteredProducts = allProducts.filter(product => {
                    const matchesSearch = product.title.toLowerCase().includes(searchTerm) ||
                                        product.description.toLowerCase().includes(searchTerm);
                    const matchesCategory = !category || product.category === category;
                    return matchesSearch && matchesCategory;
                });
                
                // Sort products
                filteredProducts.sort((a, b) => {
                    if (sortBy === 'price') {
                        const priceA = parseInt(a.price.replace(/[^0-9]/g, ''));
                        const priceB = parseInt(b.price.replace(/[^0-9]/g, ''));
                        return priceA - priceB;
                    } else if (sortBy === 'category') {
                        return a.category.localeCompare(b.category);
                    } else {
                        return a.title.localeCompare(b.title);
                    }
                });
                
                updateStats();
                renderProducts();
            }
            
            function showError(message) {
                const error = document.getElementById('error');
                error.textContent = message;
                error.style.display = 'block';
            }
            
            function hideError() {
                document.getElementById('error').style.display = 'none';
            }
            
            function showLoading() {
                document.getElementById('loading').style.display = 'block';
            }
            
            function hideLoading() {
                document.getElementById('loading').style.display = 'none';
            }
            
            async function refreshData() {
                showLoading();
                hideError();
                try {
                    const response = await fetch('/api/refresh', { method: 'POST' });
                    if (response.ok) {
                        await fetchProducts();
                    } else {
                        throw new Error('Failed to refresh data');
                    }
                } catch (error) {
                    showError('Failed to refresh data. Please try again.');
                    hideLoading();
                }
            }
            
            // Event listeners
            document.getElementById('searchInput').addEventListener('input', filterProducts);
            document.getElementById('categoryFilter').addEventListener('change', filterProducts);
            document.getElementById('sortBy').addEventListener('change', filterProducts);
            
            // Initial load
            fetchProducts();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/products", response_model=DataResponse)
async def get_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    limit: int = Query(50, ge=1, le=100, description="Number of products to return")
):
    """Get products with optional filtering"""
    filtered_products = products_data.copy()
    
    if category:
        filtered_products = [p for p in filtered_products if p["category"].lower() == category.lower()]
    
    if search:
        search_term = search.lower()
        filtered_products = [
            p for p in filtered_products 
            if search_term in p["title"].lower() or search_term in p["description"].lower()
        ]
    
    # Apply limit
    filtered_products = filtered_products[:limit]
    
    # Convert to Pydantic models
    products_list = [Product(**product) for product in filtered_products]
    
    return DataResponse(
        products=products_list,
        total=len(products_list),
        category=category or "All Categories"
    )

@app.get("/api/categories")
async def get_categories():
    """Get all available categories"""
    categories = list(set(product["category"] for product in products_data))
    return {"categories": sorted(categories)}

@app.post("/api/refresh")
async def refresh_data():
    """Refresh product data"""
    global products_data
    try:
        products_data = scraper.scrape_tech_products()
        return {"message": "Data refreshed successfully", "total_products": len(products_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh data: {str(e)}")

@app.get("/api/product/{product_id}")
async def get_product(product_id: int):
    """Get a specific product by ID"""
    product = next((p for p in products_data if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

@app.get("/api/stats")
async def get_stats():
    """Get data statistics"""
    categories = {}
    for product in products_data:
        category = product["category"]
        categories[category] = categories.get(category, 0) + 1
    
    return {
        "total_products": len(products_data),
        "categories": categories,
        "last_updated": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)