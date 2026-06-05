# Quick Start Guide

## 5-Minute Setup

### Prerequisites
- Python 3.11+
- OpenRouter API key (get from https://openrouter.ai)

### Installation

```bash
# Clone the repository
git clone https://github.com/chrg613/ai-app-compiler.git
cd ai-app-compiler

# Install dependencies
/usr/local/bin/python -m pip install flask flask-cors python-dotenv openai requests pydantic --break-system-packages

# Set your API key
export OPENROUTER_API_KEY=your_key_here

# Start the server
python main.py
```

Your app is now running at `http://localhost:5000` 🚀

---

## Using the Web Interface

1. **Visit** `http://localhost:5000`
2. **Describe** your application in the text area
   ```
   Example: "Build a CRM with users, contacts, and role-based access"
   ```
3. **Click Compile** to generate the specification
4. **View Results** in the tabbed interface:
   - **Entities**: Data models extracted
   - **Database**: SQL schema
   - **API**: REST endpoints
   - **UI**: Pages and components
   - **Auth**: Roles and permissions
   - **Diagnostics**: Confidence, assumptions, repairs

---

## Using the API

### Compile an Application

```bash
curl -X POST http://localhost:5000/api/compile \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Build a project management tool with projects, tasks, and team members"
  }'
```

Response:
```json
{
  "status": "SUCCESS",
  "request_id": "2024-06-05T06:23:45.123456",
  "app_name": "Project Management System",
  "entities": [
    {
      "name": "Project",
      "attributes": [
        {"name": "id", "type": "uuid", "nullable": false, "is_primary": true},
        {"name": "name", "type": "text", "nullable": false},
        {"name": "description", "type": "text", "nullable": true}
      ]
    }
  ],
  "database_schema": { ... },
  "api_schema": { ... },
  "ui_schema": { ... },
  "auth_schema": { ... },
  "diagnostics": {
    "confidence": 0.88,
    "assumptions": ["Admin role created", "Email notifications enabled"],
    "repairs": [],
    "warnings": []
  }
}
```

### Retrieve a Previous Compilation

```bash
curl http://localhost:5000/api/schema/REQUEST_ID
```

### Health Check

```bash
curl http://localhost:5000/api/health
```

---

## Example Prompts

### E-Commerce Platform
```
Create an e-commerce platform with products, orders, customers, and inventory.
Include shopping cart, checkout with Stripe payment, and order tracking.
Admins can manage products and view analytics. Users can view order history.
```

### Social Media App
```
Build a social media app with users, posts, comments, likes, and followers.
Include user authentication, activity feed, notifications, and search.
Support media uploads (images/videos) and trending content.
```

### Scheduling System
```
Create a scheduling and booking system for appointments.
Support multiple service providers, customers, and time slots.
Include calendar view, availability management, and email confirmations.
Send reminders 24 hours before appointment.
```

### Task Management
```
Build a task management tool with projects, tasks, assignees, and deadlines.
Support teams, task dependencies, priority levels, and progress tracking.
Include Slack notifications for task updates and due date reminders.
```

---

## Environment Variables

Required:
```bash
export OPENROUTER_API_KEY=your_key_here
```

Optional:
```bash
export FLASK_ENV=production  # or development
export PORT=5000            # custom port
export DEBUG=False          # enable debug mode
```

---

## Deployment

### Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Vercel

```bash
# Prerequisites: Connect to GitHub repository

# Deploy
vercel deploy

# Set environment variable
vercel env add OPENROUTER_API_KEY
```

### Railway

1. Connect GitHub repo to Railway
2. Add `OPENROUTER_API_KEY` environment variable
3. Deploy

---

## Architecture Overview

```
Your Prompt
    ↓
Risk Analysis (check for ambiguity)
    ↓
Intent Extraction (parse into entities)
    ↓
Application IR (create single source of truth)
    ↓
Parallel Schema Generation:
├── Database Schema
├── API Schema
├── UI Schema
└── Auth Schema
    ↓
Validation & Repair
    ↓
Runtime Simulator
    ↓
Diagnostics Report
```

Each stage is deterministic and follows compiler principles.

---

## Troubleshooting

### "OPENROUTER_API_KEY not set"
```bash
export OPENROUTER_API_KEY=your_key_here
python main.py
```

### "Port 5000 already in use"
```bash
python -c "import os; os.environ['PORT']='5001'; exec(open('main.py').read())"
```

### "Module not found"
```bash
# Install all dependencies
/usr/local/bin/python -m pip install -r requirements.txt --break-system-packages
```

### Get an API key

Visit https://openrouter.ai:
1. Sign up (free account available)
2. Navigate to Keys
3. Create a new key
4. Copy and use in your terminal

---

## Next Steps

1. **Explore Examples**: Try different prompts to understand capabilities
2. **Review Documentation**: Read ARCHITECTURE.md for deep dive
3. **Deploy**: Use Docker or Vercel to go live
4. **Integrate**: Use the API in your own applications
5. **Contribute**: Submit issues and pull requests on GitHub

---

## Support

- 📖 **Documentation**: See README.md and ARCHITECTURE.md
- 🐛 **Issues**: GitHub Issues tab
- 💬 **Discussions**: GitHub Discussions tab
- 📧 **Contact**: Check repository for contact info

---

**Happy Compiling! 🎉**
