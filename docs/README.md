# Daia Documentation

This directory contains the documentation for Daia, built with Jekyll and the Just the Docs theme.

## Documentation Structure

- **index.md** - Home page with overview and key features
- **getting-started.md** - Installation and setup guide
- **configuration-usage.md** - Configuration reference and usage examples
- **development.md** - Guide for contributors and developers
- **project-structure.md** - Codebase architecture and organization
- **roadmap.md** - Future features and development plans
- **quick-reference.md** - Quick reference for common tasks
- **faq.md** - Frequently asked questions
- **troubleshooting.md** - Detailed troubleshooting guide

## Local Development

To preview the documentation locally:

```bash
# Install Jekyll (if not already installed)
gem install bundler jekyll

# Create Gemfile
cat > Gemfile << EOF
source "https://rubygems.org"
gem "jekyll"
gem "just-the-docs"
EOF

# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve

# Open http://localhost:4000/daia/
```

## Deployment

Documentation is automatically deployed to GitHub Pages when changes are pushed to the main branch.

Live site: https://zhiro-labs.github.io/daia/

## Updating Documentation

### Adding a New Page

1. Create a new `.md` file in the `docs/` directory
2. Add front matter:
   ```yaml
   ---
   layout: default
   title: Your Page Title
   nav_order: 10
   ---
   ```
3. Write your content using Markdown
4. Update this README if it's a major section

### Navigation Order

Pages are ordered by the `nav_order` value in the front matter:

1. Home (index.md)
2. Getting Started
3. Configuration & Usage
4. Development
5. Project Structure
6. Roadmap
7. Quick Reference
8. FAQ
9. Troubleshooting

### Style Guidelines

- Use clear, concise language
- Include code examples where relevant
- Add table of contents for long pages
- Use proper heading hierarchy (H1 → H2 → H3)
- Link to related pages
- Keep examples up to date with the codebase

### Images

Place images in `docs/assets/` and reference them:

```markdown
![Alt text](assets/image.png)
```

## Theme Configuration

The site uses the [Just the Docs](https://just-the-docs.github.io/just-the-docs/) theme.

Configuration is in `_config.yml`:
- Site title and description
- Navigation settings
- Search functionality
- Footer content
- Custom links

## Markdown Features

### Code Blocks

\`\`\`python
def example():
    return "Hello, World!"
\`\`\`

### Callouts

{: .note }
> This is a note callout.

{: .warning }
> This is a warning callout.

### Tables

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

### Links

- Internal: [Getting Started](getting-started.html)
- External: [GitHub](https://github.com/zhiro-labs/daia)

## Maintenance

### Regular Updates

- Keep configuration examples current
- Update version numbers
- Verify all links work
- Update screenshots if UI changes
- Review and update roadmap

### Checking for Issues

```bash
# Check for broken links (requires linkchecker)
linkchecker http://localhost:4000/daia/

# Validate markdown
markdownlint docs/*.md
```

## Contributing

When contributing to documentation:

1. Follow the existing style and structure
2. Test locally before submitting
3. Update related pages if needed
4. Check for typos and grammar
5. Ensure code examples work

## Questions?

- Open an issue on GitHub
- Start a discussion
- Contact the maintainers

---

Last updated: 2025-01-09
