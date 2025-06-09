# Oxidar.org - Maintainer Guide

> This is the official website for Oxidar, the Latin American Rust community. This README is intended for maintainers and contributors who need to work with the website's codebase.

## 🚀 Quick Start

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) v0.145.0 or later
- [Git](https://git-scm.com/) with submodule support
- [Node.js](https://nodejs.org/) (optional, for additional tooling)

### Local Development Setup

1. **Clone the repository with submodules:**
   ```bash
   git clone --recursive https://github.com/oxidar-org/website.git
   cd website/web
   ```

   If you already cloned without `--recursive`, initialize submodules:
   ```bash
   git submodule update --init --recursive
   ```

2. **Start the development server:**
   ```bash
   hugo server -D
   ```

3. **Access the site:**
   Open http://localhost:1313 in your browser

## 📁 Project Structure

```
web/
├── archetypes/          # Content templates
├── assets/              # SCSS, JS, and other assets
├── content/             # Markdown content files
│   └── posts/          # Blog posts and articles
├── data/               # Data files (YAML, JSON, TOML)
├── i18n/               # Internationalization files
├── layouts/            # Custom HTML templates
├── public/             # Generated static site (git-ignored)
├── resources/          # Hugo's resource cache
├── static/             # Static assets (images, etc.)
├── themes/             # Hugo themes (LoveIt theme as submodule)
├── .github/            # GitHub Actions workflows
├── hugo.toml           # Hugo configuration
└── README.md           # This file
```

## ✍️ Content Management

### Adding New Posts

1. **Create a new post:**
   ```bash
   hugo new posts/your-post-title.md
   ```

2. **Edit the generated file** in `content/posts/` with your content

3. **Front matter example:**
   ```yaml
   +++
   date = '2024-01-15T10:00:00-03:00'
   draft = false
   title = 'Your Post Title'
   description = "Brief description for SEO"
   tags = ["rust", "tutorial"]
   categories = ["Programming"]
   +++
   ```

### Content Guidelines

- **Language:** Primary content is in Spanish (es)
- **Images:** Store in `static/images/` and reference as `/images/filename.jpg`
- **Drafts:** Set `draft = true` to hide from production
- **SEO:** Always include meaningful `title` and `description`

## 🎨 Theme Customization

The site uses the [LoveIt](https://github.com/dillonzq/LoveIt) theme as a Git submodule.

### Updating the Theme

```bash
cd themes/LoveIt
git pull origin master
cd ../..
git add themes/LoveIt
git commit -m "Update LoveIt theme"
```

### Custom Styling

- Add custom CSS in `assets/css/`
- Override theme templates by creating files in `layouts/` with the same structure

## ⚙️ Configuration

Main configuration is in `hugo.toml`. Key sections:

- **Basic Settings:** Site title, URL, language
- **Menu Configuration:** Navigation menu items
- **Social Links:** GitHub, LinkedIn, email
- **Theme Parameters:** LoveIt theme customization
- **SEO Settings:** Meta tags, social sharing

### Environment-Specific Config

For development vs. production differences, use Hugo's environment variables:

```bash
# Development
hugo server -D --environment development

# Production build
hugo --environment production
```

## 🚀 Deployment

### GitHub Pages (Automatic)

The site deploys automatically via GitHub Actions when pushing to the `main` branch.

**Workflow:** `.github/workflows/hugo.yaml`
- Triggers on push to `main`
- Builds with Hugo Extended v0.145.0
- Deploys to GitHub Pages
- Uses caching for faster builds

### Manual Deployment

```bash
# Build for production
hugo --minify

# The generated site will be in the public/ directory
```

## 🔧 Maintenance Tasks

### Regular Updates

1. **Update Hugo:**
   - Check for new Hugo versions
   - Update version in `.github/workflows/hugo.yaml`
   - Test locally before deploying

2. **Update Theme:**
   ```bash
   cd themes/LoveIt
   git pull origin master
   cd ../..
   git add themes/LoveIt
   git commit -m "Update theme to latest version"
   ```

3. **Update Dependencies:**
   - Review and update any Node.js dependencies if present
   - Check for security updates

### Content Review

- Review draft posts regularly
- Check for broken links
- Update outdated information
- Ensure accessibility compliance

## 🐛 Troubleshooting

### Common Issues

**Submodule issues:**
```bash
git submodule update --init --recursive --force
```

**Build errors:**
- Check Hugo version compatibility
- Verify all required parameters in `hugo.toml`
- Check for syntax errors in content files

**Theme not loading:**
- Ensure theme submodule is properly initialized
- Check theme path in `hugo.toml`

### Performance Optimization

- Use `hugo --minify` for production builds
- Optimize images before adding to `static/`
- Monitor build times and cache effectiveness

## 📞 Support & Community

- **Main Site:** https://oxidar.org/
- **Email:** admin@oxidar.org
- **GitHub:** https://github.com/oxidar-org
- **LinkedIn:** https://linkedin.com/company/oxidar-org

## 📄 License

Content is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

For content contributions, please follow our community guidelines and ensure all content aligns with Oxidar's mission of promoting Rust in Latin America.

---

**¡Bienvenide a la comunidad Oxidar! 🦀**