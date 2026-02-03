# Brand Aesthetics Guide

## Color Palette

### Primary - Teal
| Name | Hex | Usage |
|------|-----|-------|
| Teal | `#40B8A6` | Primary buttons, links, borders, accents |
| Teal Light | `#5EC9B9` | Hover states, secondary accents |
| Teal Dark | `#2F9987` | Active states, darker accents |
| Teal BG | `#E6F7F5` | Light backgrounds, callout boxes |
| Teal BG Light | `#D4F0EC` | Secondary backgrounds, gradients |

### Secondary - Navy
| Name | Hex | Usage |
|------|-----|-------|
| Navy | `#1A3D4D` | Headings, primary text, section labels |
| Navy Dark | `#0F2938` | Deep backgrounds (rarely used) |
| Navy Light | `#2A5568` | Secondary headings |

### Neutrals
| Name | Hex | Usage |
|------|-----|-------|
| Text | `#1A3D4D` | Body text (same as Navy) |
| Text Light | `#4B5563` | Secondary text, captions |
| Gray 50 | `#F9FAFB` | Alt backgrounds, cards |
| Gray 200 | `#E5E7EB` | Borders, dividers |

### Semantic Colors
| Name | Hex | Usage |
|------|-----|-------|
| Success | `#059669` | Correct answers, positive callouts |
| Success BG | `#ecfdf5` | Success callout backgrounds |
| Danger | `#dc2626` | Errors, failure stories |
| Danger BG | `#fef2f2` | Danger callout backgrounds |
| Accent | `#f59e0b` | Warnings, decision points |
| Accent BG | `#fffbeb` | Accent callout backgrounds |

## Typography

- **Font Family:** Inter (Google Fonts)
- **Monospace:** JetBrains Mono, Fira Code
- **Body:** 16px base, line-height 1.7
- **Headings:** Navy color, line-height 1.3

## Design Principles

1. **No rounded corners** - Use `border-radius: 0` for brand consistency
2. **Clean and professional** - Minimal decoration
3. **High contrast** - Navy text on light backgrounds
4. **Teal as accent** - Use sparingly for emphasis

## Mermaid Diagram Theme

```javascript
mermaid.initialize({
  startOnLoad: true,
  theme: 'base',
  themeVariables: {
    primaryColor: '#E6F7F5',
    primaryTextColor: '#1A3D4D',
    primaryBorderColor: '#40B8A6',
    lineColor: '#4B5563',
    secondaryColor: '#D4F0EC',
    tertiaryColor: '#F9FAFB'
  }
});
```

## CSS Variables

```css
:root {
  /* Brand Colors - Teal */
  --primary: #40B8A6;
  --primary-light: #5EC9B9;
  --primary-dark: #2F9987;
  --primary-bg: #E6F7F5;

  /* Brand Colors - Navy */
  --navy: #1A3D4D;
  --navy-dark: #0F2938;
  --navy-light: #2A5568;

  /* Text */
  --text: #1A3D4D;
  --text-light: #4B5563;

  /* Backgrounds */
  --bg: #ffffff;
  --bg-alt: #F9FAFB;
  --border: #E5E7EB;

  /* No rounded corners */
  --radius: 0;
}
```
