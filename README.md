# 🚀 Smart Data Display - Tech Products Dashboard

A FastAPI-based web application that displays trending tech products with real-time data gathering, filtering, and search capabilities.

## 🎯 Features

- **Real-time Data**: Displays 20+ tech products across multiple categories
- **Advanced Filtering**: Search by title/description and filter by category
- **Sorting Options**: Sort by title, price, or category
- **Responsive Design**: Modern UI that works on all devices
- **RESTful API**: Clean API endpoints for data access
- **Auto-refresh**: Manual data refresh functionality

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: BeautifulSoup, Requests
- **Server**: Uvicorn

## 📋 Project Structure

```
smart-data-display/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore file
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd smart-data-display
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🌐 API Endpoints

### Core Endpoints

- `GET /` - Main web interface
- `GET /api/products` - Get all products with filtering
- `GET /api/categories` - Get all available categories
- `GET /api/product/{id}` - Get specific product by ID
- `GET /api/stats` - Get data statistics
- `POST /api/refresh` - Refresh product data

### Query Parameters

**GET /api/products**
- `category` (optional): Filter by category
- `search` (optional): Search in title/description
- `limit` (optional): Number of products to return (default: 50)

### Example API Calls

```bash
# Get all products
curl http://localhost:8000/api/products

# Search for graphics cards
curl "http://localhost:8000/api/products?search=graphics"

# Filter by category
curl "http://localhost:8000/api/products?category=Processors"

# Get statistics
curl http://localhost:8000/api/stats
```

## 🚀 Deployment Options

### 1. Render (Recommended)

1. **Create a `render.yaml` file**:
   ```yaml
   services:
     - type: web
       name: smart-data-display
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
       plan: free
   ```

2. **Deploy steps**:
   - Push code to GitHub
   - Connect GitHub repo to Render
   - Deploy automatically

### 2. Vercel

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Create `vercel.json`**:
   ```json
   {
     "builds": [
       {
         "src": "main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "main.py"
       }
     ]
   }
   ```

3. **Deploy**:
   ```bash
   vercel --prod
   ```

### 3. Railway

1. **Create `railway.json`**:
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
     }
   }
   ```

2. **Deploy via CLI**:
   ```bash
   railway login
   railway init
   railway up
   ```

### 4. Heroku

1. **Create `Procfile`**:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### 5. Docker Deployment

1. **Create `Dockerfile`**:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and run**:
   ```bash
   docker build -t smart-data-display .
   docker run -p 8000:8000 smart-data-display
   ```

## 📊 Data Categories

The application includes products from these categories:
- Graphics Cards
- Processors
- Memory (RAM)
- Storage (SSD/HDD)
- Motherboards
- Peripherals (Mouse, Keyboard, Headsets)
- Monitors
- Cooling Solutions
- Power Supplies

## 🔧 Customization

### Adding New Data Sources

1. **Modify the `DataScraper` class** in `main.py`:
   ```python
   def scrape_your_data(self) -> List[dict]:
       # Add your scraping logic here
       # Return list of dictionaries with required fields
       pass
   ```

2. **Required fields** for each product:
   - `title`: Product name
   - `description`: Product description
   - `price`: Product price (string format)
   - `source`: Data source name
   - `link`: Product URL
   - `category`: Product category

### Modifying Categories

Update the `tech_products` list in the `scrape_tech_products()` method to add your own categories and products.

### Styling Customization

The CSS is embedded in the HTML template. Modify the `<style>` section in the `root()` function to change:
- Colors and gradients
- Layout and spacing
- Typography
- Responsive breakpoints

## 🧪 Testing

### Manual Testing

1. **Test API endpoints**:
   ```bash
   # Test basic functionality
   curl http://localhost:8000/api/products
   curl http://localhost:8000/api/categories
   curl http://localhost:8000/api/stats
   
   # Test filtering
   curl "http://localhost:8000/api/products?category=Graphics%20Cards"
   curl "http://localhost:8000/api/products?search=nvidia"
   ```

2. **Test web interface**:
   - Visit http://localhost:8000
   - Try search functionality
   - Test category filtering
   - Test sort options
   - Test refresh button

### Automated Testing

Add these test files for comprehensive testing:

**test_main.py**:
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_get_products():
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert "total" in data

def test_get_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
```

Run tests with:
```bash
pip install pytest
pytest test_main.py
```

## 🔒 Security Considerations

1. **Rate Limiting**: Consider adding rate limiting for API endpoints
2. **Input Validation**: All inputs are validated using Pydantic models
3. **CORS**: Add CORS middleware if needed for cross-origin requests
4. **Environment Variables**: Use environment variables for sensitive data

## 📈 Performance Optimization

1. **Caching**: Implement Redis caching for frequently accessed data
2. **Database**: Replace in-memory storage with PostgreSQL/MongoDB
3. **Background Tasks**: Use Celery for background data scraping
4. **CDN**: Use CDN for static assets in production

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Kill process using port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Module not found**:
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Permission denied**:
   ```bash
   # On Linux/Mac, ensure proper permissions
   chmod +x main.py
   ```

### Debug Mode

Run with debug logging:
```bash
uvicorn main:app --reload --log-level debug
```

## 📱 Mobile Responsiveness

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- BeautifulSoup for web scraping capabilities
- The open-source community

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the troubleshooting section

## 🔄 Version History

- **v1.0.0**: Initial release with basic functionality
- **v1.1.0**: Added search and filtering capabilities
- **v1.2.0**: Improved UI and added statistics

---

**Made with ❤️ for the Maketronics Tech Challenge**
