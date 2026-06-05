## Deployment Guide

Comprehensive guide for deploying the AI Application Compiler to production.

### Prerequisites

- Python 3.11+
- OpenRouter API key (free account at https://openrouter.ai)
- Git (optional, for GitHub deployment)
- Docker (optional, for containerized deployment)
- Vercel account (optional, for serverless deployment)

### Quick Start

#### 1. Local Development

```bash
# Clone or navigate to the project
cd /vercel/share/v0-project

# Initialize project (creates .env from example)
python init.py

# Edit .env and set OPENROUTER_API_KEY
nano .env

# Validate configuration
python validate.py

# Run development server
python main.py
```

Visit http://localhost:5000

#### 2. Docker Deployment

```bash
# Build Docker image
docker build -t ai-app-compiler:latest .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

#### 3. Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Set environment variables
vercel env add OPENROUTER_API_KEY
# Paste your API key

# Deploy
vercel deploy

# View production logs
vercel logs
```

The app will be available at `https://<project>.vercel.app`

#### 4. Railway Deployment

```bash
# Install Railway CLI
curl -L railway.app/install | bash

# Login
railway login

# Initialize Railway project
railway init

# Add environment variables
railway variable set OPENROUTER_API_KEY your_key_here

# Deploy
railway deploy

# View logs
railway logs
```

---

### Configuration Management

All configuration is handled through environment variables and the `src/config.py` module.

#### Required Environment Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `OPENROUTER_API_KEY` | — | Yes | API key for LLM calls |
| `ENVIRONMENT` | development | No | Environment: development, test, production |

#### Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | openrouter | LLM provider (only openrouter currently) |
| `LLM_MODEL` | deepseek/deepseek-chat-v3-0324 | LLM model to use |
| `LLM_TEMPERATURE` | 0.1 | Temperature for LLM responses (0.0-2.0) |
| `LLM_MAX_TOKENS` | 4096 | Max tokens for LLM response |
| `PORT` | 5000 | Server port |
| `HOST` | 0.0.0.0 | Server host |
| `LOG_LEVEL` | INFO | Logging level |
| `COMPILER_TIMEOUT` | 60 | Compilation timeout in seconds |
| `COMPILER_MAX_RETRIES` | 3 | Max retries for LLM calls |
| `CORS_ORIGINS` | * | Comma-separated CORS origins |
| `ENABLE_CACHING` | True | Enable result caching |
| `ENABLE_METRICS` | True | Enable metrics collection |

#### Configuration Validation

The system validates configuration on startup. To manually validate:

```bash
python validate.py
```

This checks:
- All required environment variables are set
- API keys are available
- Port is valid
- LLM configuration is correct
- All required files exist
- Dependencies are installed

---

### Deployment Checklist

#### Before Deploying to Production

- [ ] Set `ENVIRONMENT=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Set `LOG_LEVEL=WARNING` (or INFO)
- [ ] Ensure `OPENROUTER_API_KEY` is set securely
- [ ] Verify `CORS_ORIGINS` is restricted
- [ ] Enable caching for better performance
- [ ] Test locally first
- [ ] Review error logs
- [ ] Set up monitoring/logging

#### Deployment Platforms

##### Vercel (Recommended for serverless)

**Pros:**
- Free tier available
- Auto-scaling
- Edge caching
- GitHub integration

**Config:** `vercel.json` is pre-configured
**Note:** Vercel requires `wsgi.py` for Flask apps

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "functions": {
    "main.py": {
      "memory": 1024,
      "maxDuration": 60
    }
  }
}
```

##### Railway (Recommended for simplicity)

**Pros:**
- Simple deployment
- Good free tier
- Easy environment setup
- GitHub integration

**Steps:**
1. Create Railway account
2. Connect GitHub repository
3. Add environment variables
4. Deploy

##### Docker (Recommended for full control)

**Pros:**
- Complete control
- Works everywhere
- Reproducible builds
- Easy scaling

**Deploy to any Docker host:**
```bash
docker build -t compiler:latest .
docker run -p 5000:5000 \
  -e OPENROUTER_API_KEY=your_key \
  -e ENVIRONMENT=production \
  compiler:latest
```

##### AWS/GCP/Azure (Advanced)

**Option 1: App Engine / Cloud Run**
```bash
gcloud app deploy
# or
gcloud run deploy compiler --source .
```

**Option 2: EC2 / VM Instance**
```bash
# SSH into instance
ssh user@instance

# Clone repo
git clone repo

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENROUTER_API_KEY=...

# Run with gunicorn
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

---

### Production Configuration

#### Database Setup (for future use)

Currently the application uses in-memory storage. To add a database:

1. **PostgreSQL (Recommended)**
   ```bash
   # Set database URL
   export DATABASE_URL=postgresql://user:pass@localhost:5432/compiler
   ```

2. **MySQL**
   ```bash
   export DATABASE_URL=mysql://user:pass@localhost:3306/compiler
   ```

3. **SQLite (Simple)**
   ```bash
   export DATABASE_URL=sqlite:///compiler.db
   ```

#### Logging & Monitoring

**Structured Logging:**
- All log messages use structured format: `[Component] Message`
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Production: Use INFO or WARNING

**Monitoring Services:**
- **Sentry:** Set `SENTRY_DSN` for error tracking
- **DataDog:** Agent configuration available
- **CloudWatch:** AWS CloudWatch integration

#### Performance Optimization

1. **Caching:**
   ```bash
   export ENABLE_CACHING=True
   ```

2. **Worker Processes (with Gunicorn):**
   ```bash
   gunicorn --workers 4 --worker-class sync wsgi:app
   ```

3. **Load Balancing:**
   - Use NGINX as reverse proxy
   - Enable gzip compression
   - Set up SSL/TLS

#### Security

**Essential Steps:**
1. Use HTTPS only
2. Set strong secrets
3. Restrict CORS origins
4. Validate all inputs
5. Use environment variables for secrets
6. Keep dependencies updated
7. Monitor logs for suspicious activity

**Security Headers:**
```python
# Add to Flask app
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

### Troubleshooting

#### Configuration Errors

**Error: "OPENROUTER_API_KEY not found"**
```bash
# Check if set
echo $OPENROUTER_API_KEY

# Set it
export OPENROUTER_API_KEY=your_key_here
```

**Error: "Port already in use"**
```bash
# Change port
export PORT=8000
python main.py
```

#### LLM Errors

**Error: "Invalid JSON from LLM"**
- Check API key is valid
- Check LLM model is available
- Try with different temperature
- Check prompt length

**Error: "API rate limit exceeded"**
- Wait before retrying
- Reduce `LLM_MAX_TOKENS`
- Use `COMPILER_MAX_RETRIES`

#### Deployment Issues

**Vercel: Function timeout**
- Increase maxDuration in vercel.json
- Reduce LLM_MAX_TOKENS
- Optimize LLM prompt

**Docker: Image won't build**
- Check Python version: `python --version`
- Check dependencies: `pip install -r requirements.txt`
- Check Dockerfile syntax

---

### Health Checks

Test deployment health:

```bash
# Health endpoint
curl http://localhost:5000/health
# Response: {"status": "healthy", "environment": "production"}

# Status endpoint
curl http://localhost:5000/api/status
# Response: {"status": "ready", "config": {...}}
```

---

### Scaling Considerations

#### Horizontal Scaling

- Use load balancer (NGINX, HAProxy)
- Multiple worker processes
- Share cache layer (Redis for future)
- Use database instead of in-memory storage

#### Vertical Scaling

- Increase worker processes
- Increase memory allocation
- Optimize code performance

#### Database Optimization

- Add indexes on frequently queried columns
- Cache compilation results
- Archive old compilations

---

### Monitoring & Maintenance

#### Regular Tasks

- Check logs daily
- Monitor API usage
- Update dependencies monthly
- Review error rates
- Test disaster recovery

#### Metrics to Track

- Request latency
- Error rate
- Compilation success rate
- LLM call frequency
- Cache hit rate
- Uptime %

---

### Support & Documentation

- **GitHub Issues:** Report bugs and feature requests
- **Documentation:** See README.md, ARCHITECTURE.md
- **API Docs:** See `/api/status` endpoint
- **Config:** See `.env.example` for all options

---

**Version:** 2.1.0  
**Last Updated:** 2024  
**Status:** Production Ready
