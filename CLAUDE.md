# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Oxidar.org** website - the official site for the Latin American Rust community. It's a Hugo-based static site that publishes blog posts, articles, and community information about Rust programming in Spanish.

**Mission**: Promote Rust adoption in Latin America through accessible Spanish-language content, collaborative projects, and community building.

## Tech Stack

- **Hugo Extended v0.148.0** - Static site generator
- **FixIt Theme** - Hugo theme (Git submodule at `themes/FixIt`)
- **GitHub Actions** - Automated deployment to GitHub Pages
- **Primary Language**: Spanish (es)

## Essential Commands

### Development
```bash
# Start local development server (includes drafts)
hugo server -D

# Start with specific environment
hugo server -D --environment development

# Access at: http://localhost:1313
```

### Content Creation
```bash
# Create a new blog post
hugo new posts/your-post-title.md

# Example: Create a post with date in folder structure
hugo new posts/2025.01.26-example/example.md
```

### Building
```bash
# Build for production (minified)
hugo --minify

# Build with specific environment
hugo --environment production

# Output directory: public/
```

### Theme Management
```bash
# Update the FixIt theme submodule
cd themes/FixIt
git pull origin master
cd ../..
git add themes/FixIt
git commit -m "Update FixIt theme"

# Initialize/update all submodules (if needed)
git submodule update --init --recursive
```

## Architecture & Content Structure

### Directory Layout
- `content/posts/` - All blog posts and articles in Markdown
- `static/` - Static assets (images, PDFs, etc.)
- `assets/` - SCSS, JS, and processable assets
- `hugo.toml` - Main site configuration
- `archetypes/default.md` - Template for new content
- `public/` - Generated static site (git-ignored)
- `.github/workflows/hugo.yaml` - CI/CD pipeline

### Content Organization Pattern
Posts follow a date-prefixed folder structure:
```
content/posts/
├── 2025.06.12-wasm/wasm.md
├── 2025.06.25-cargo-lambda/cargo-lambda.md
├── 2025.11-27-async-patterns/async-patterns.md
├── about.md
├── contact.md
└── contributors.md
```

### Front Matter Structure
All posts use TOML front matter with this structure:
```toml
+++
date = '2025-01-26T10:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Your Post Title'
description = "SEO-friendly description"
tags = ["rust", "webassembly", "tutorial"]
categories = ["Proyectos", "Eventos"]
+++
```

**Important**:
- Set `draft = false` to publish
- Use `hiddenFromHomePage = true` for pages like About/Contact
- Always include meaningful `title` and `description` for SEO

### Permalinks
Posts use filename-only permalinks (configured in hugo.toml):
```
posts = ":filename"
```
Example: `content/posts/cargo-lambda.md` becomes `oxidar.org/cargo-lambda/`

## Deployment Architecture

### Automated GitHub Pages Deployment
- **Trigger**: Push to `main` branch or manual workflow dispatch
- **Workflow**: `.github/workflows/hugo.yaml`
- **Hugo Version**: 0.148.0 (Extended)
- **Build Process**:
  1. Checkout with recursive submodules
  2. Install Hugo CLI and Dart Sass
  3. Restore Hugo cache
  4. Build with `--gc --minify`
  5. Save cache for subsequent builds
  6. Deploy to GitHub Pages

### Key Deployment Settings
- Environment: `production`
- Timezone: `America/Los_Angeles`
- Base URL: Configured via GitHub Pages
- Permissions: `contents: read`, `pages: write`, `id-token: write`

## Hugo Configuration Highlights

### Theme: FixIt (formerly LoveIt)
The site uses the FixIt theme (configured as `theme = "FixIt"` in hugo.toml). Note that configuration comments reference "LoveIt" as FixIt is a fork/continuation.

### Key Features Enabled
- **Search**: Lunr-based search (`params.search.type = "lunr"`)
- **GitInfo**: Tracks git commit history (`enableGitInfo = true`)
- **Math**: KaTeX support for mathematical formulas
- **Code**: Syntax highlighting with copy buttons
- **Social Sharing**: Reddit and Telegram enabled
- **Analytics**: Google Analytics (ID: G-TZH4L8473F)

### Menu Structure
1. **Posts** (`/posts/`) - Main content hub
2. **Colaboradores** (`/contributors/`) - Contributors page
3. **Acerca de** (`/about/`) - About page
4. **Contacto** (`/contact/`) - Contact information

### Social Links
- GitHub: `oxidar-org`
- LinkedIn: `oxidar-org`
- Telegram: `+7PgAQVPclxIzOGQ0`
- Email: `admin@oxidar.org`

## Content Guidelines

### Language & Style
- **Primary language**: Spanish (es)
- **Audience**: Latin American Rust developers
- **Tone**: Educational, collaborative, community-focused

### Images & Assets
- Store images in `static/images/`
- Reference as `/images/filename.jpg` in markdown
- Optimize images before adding (for performance)

### Embedded Content
The site supports:
- YouTube embeds: `{{< youtube VIDEO_ID >}}`
- Hugo shortcodes for rich content
- HTML in markdown (goldmark renderer has `unsafe = true`)

### Categories & Tags
Common categories: "Proyectos", "Eventos", "Tutoriales"
Common tags: "rust", "webassembly", "wasm", "tutorial", "presentacion"

## Special Considerations

### Submodule Management
The FixIt theme is a Git submodule. Always clone with `--recursive` or run:
```bash
git submodule update --init --recursive
```

### Build Troubleshooting
If builds fail:
1. Verify Hugo version matches 0.148.0 Extended
2. Check submodules are initialized: `git submodule status`
3. Verify front matter syntax in content files
4. Check for missing parameters in hugo.toml

### Output Formats
The site generates multiple output formats (configured in hugo.toml):
- HTML pages
- RSS feeds
- JSON search index
- Markdown versions of pages

## Community & License

- **Website**: https://oxidar.org/
- **GitHub**: https://github.com/oxidar-org
- **Email**: admin@oxidar.org
- **Content License**: CC BY-NC 4.0
