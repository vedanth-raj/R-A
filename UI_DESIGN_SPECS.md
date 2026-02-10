# 🎨 UI Design Specifications - Futuristic Glassmorphic System

## 🌌 Color Palette

### Primary Colors
- **Deep Black:** `#0a0a0a` - Base background
- **Dark Teal:** `#1a2332` - Mid gradient
- **Dark Orange:** `#2a1810` - Accent gradient
- **Neon Orange:** `#ff4500` - Primary accent
- **Gold:** `#ffd700` - Secondary accent
- **Amber:** `#ff8c00` - Tertiary accent

### Glassmorphic Layers
- **Card Background:** `rgba(20, 20, 40, 0.25)`
- **Login Card:** `rgba(15, 15, 35, 0.3)`
- **Input Fields:** `rgba(30, 30, 50, 0.4)`
- **Table Cells:** `rgba(30, 30, 50, 0.4)`

### Text Colors
- **Primary Text:** `#e0e0e0` (light gray)
- **Secondary Text:** `rgba(255, 255, 255, 0.6)` (dimmed white)
- **Accent Text:** `#ff8c00` (orange)
- **Gold Text:** `#ffd700` (gold)

## 📐 Layout Structure

### Login Screen
```
┌─────────────────────────────────────────┐
│                                         │
│         [Animated Wave Canvas]          │
│                                         │
│     ┌─────────────────────────┐        │
│     │  AI SYSTEMATIC REVIEW   │        │
│     │  [Neon Gradient Title]  │        │
│     │                         │        │
│     │  Username: [_______]    │        │
│     │  Password: [_______]    │        │
│     │                         │        │
│     │   [🚀 SIGN IN Button]   │        │
│     │   [Orange Gradient]     │        │
│     └─────────────────────────┘        │
│                                         │
└─────────────────────────────────────────┘
```

### Dashboard Layout
```
┌──────────────────────────────────────────────────┐
│  AI SYSTEMATIC REVIEW GENERATOR    [User] [Logout]│
├──────────────────────────────────────────────────┤
│                                                  │
│  🎯 Research Configuration                       │
│  ┌────────────────────────────────────────────┐ │
│  │ Research Topic: [________________]         │ │
│  │ Number of Papers: [====●====] 3            │ │
│  │ ▼ Advanced Filters                         │ │
│  │   From: [2020]  To: [2024]  ☑ Open Access │ │
│  │                                            │ │
│  │        [🚀 START RESEARCH]                 │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  Status: [Progress indicator]                    │
│                                                  │
│  📚 Retrieved Papers                             │
│  ┌────────────────────────────────────────────┐ │
│  │ Title    │ Authors  │ Year │ Citations     │ │
│  │──────────┼──────────┼──────┼──────────────│ │
│  │ Paper 1  │ Smith J. │ 2023 │ 150          │ │
│  │ Paper 2  │ Chen L.  │ 2024 │ 89           │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  [🔬 ANALYZE & COMPARE]                          │
│                                                  │
│  🎯 Key Findings                                 │
│  • Theme 1...                                    │
│  • Theme 2...                                    │
│                                                  │
│  [📝 GENERATE DRAFT]                             │
│                                                  │
│  📝 Generated Draft                              │
│  Abstract: ...                                   │
│  Methods: ...                                    │
│  Results: ...                                    │
│                                                  │
├──────────────────────────────────────────────────┤
│ [Revise] [Download PDF] [Download Papers] [Reset]│
└──────────────────────────────────────────────────┘
```

## 🎭 Component Styles

### Buttons

#### Primary Button (START RESEARCH)
```css
Background: linear-gradient(135deg, #ff4500, #ffd700)
Border: none
Border-radius: 14px
Color: #000 (black text)
Font-weight: 600
Padding: 1rem 2.5rem
Shadow: 0 4px 20px rgba(255, 69, 0, 0.4)

Hover:
  Transform: scale(1.08)
  Shadow: 0 8px 40px rgba(255, 69, 0, 0.6)
  Glow: 0 0 60px rgba(255, 140, 0, 0.4)
```

#### Secondary Button (ANALYZE, GENERATE)
```css
Background: rgba(30, 30, 50, 0.5)
Border: 1px solid rgba(255, 140, 0, 0.3)
Border-radius: 12px
Color: #ff8c00
Font-weight: 500
Padding: 0.75rem 1.5rem

Hover:
  Background: rgba(255, 69, 0, 0.2)
  Border: rgba(255, 140, 0, 0.6)
  Shadow: 0 4px 20px rgba(255, 69, 0, 0.3)
  Transform: translateY(-2px)
```

### Input Fields
```css
Background: rgba(30, 30, 50, 0.4)
Border: 1px solid rgba(255, 140, 0, 0.2)
Border-radius: 12px
Color: #e0e0e0
Padding: 0.75rem 1rem

Focus:
  Border: rgba(255, 140, 0, 0.6)
  Shadow: 0 0 20px rgba(255, 69, 0, 0.3)
```

### Glassmorphic Cards
```css
Background: rgba(20, 20, 40, 0.25)
Backdrop-filter: blur(16px) saturate(180%)
Border-radius: 24px
Border: 1px solid rgba(255, 255, 255, 0.1)
Shadow: 
  0 8px 32px rgba(0, 0, 0, 0.37),
  inset 0 1px 0 rgba(255, 255, 255, 0.05),
  0 0 40px rgba(255, 69, 0, 0.1)
Padding: 2rem

Hover:
  Transform: translateY(-4px)
  Shadow: Enhanced glow
  Border: rgba(255, 140, 0, 0.3)
```

### Progress Bar
```css
Container:
  Background: rgba(30, 30, 50, 0.6)
  Border-radius: 20px
  Height: 8px

Fill:
  Background: linear-gradient(90deg, #ff4500, #ffd700, #ff4500)
  Background-size: 200% 100%
  Animation: Shine effect (2s loop)
  Shadow: 0 0 20px rgba(255, 69, 0, 0.6)
```

### Tables
```css
Header (th):
  Background: rgba(255, 69, 0, 0.2)
  Color: #ffd700
  Padding: 1rem
  Font-weight: 600
  Text-transform: uppercase
  Letter-spacing: 1px

Cell (td):
  Background: rgba(30, 30, 50, 0.4)
  Padding: 1rem
  Border: 1px solid rgba(255, 140, 0, 0.1)

Row Hover:
  Background: rgba(255, 69, 0, 0.1)
```

## 🌊 Canvas Animation Specs

### Wave Configuration
```javascript
Number of waves: 7
Wave spacing: Evenly distributed vertically
Wave color: rgba(255, 69+i*20, 0, 0.3+i*0.1)
Wave amplitude: 30-70px (random)
Wave frequency: 0.01-0.02 (random)
Wave speed: 0.02-0.04 (random)
```

### Mouse Interaction
```javascript
Repulsion radius: 150px
Repulsion force: 30 units
Spring constant: 0.1
Damping factor: 0.85
Update rate: 60fps (requestAnimationFrame)
```

### Glow Effects
```javascript
Shadow blur: 20px (primary), 40px (secondary)
Shadow color: Wave color
Composite operation: 'lighter'
Line width: 3px (primary), 1px (glow)
```

## 📱 Responsive Breakpoints

### Desktop (1920px+)
- Full glassmorphic effects
- All animations enabled
- Multi-column layouts
- Large padding/margins

### Tablet (768px - 1920px)
- Maintained glassmorphism
- Adjusted spacing
- Flexible columns
- Touch-friendly buttons

### Mobile (<768px)
```css
Login card:
  Margin: 5vh 1rem
  Padding: 2rem 1.5rem

Title:
  Font-size: 2rem (reduced from 2.5rem)

Glass containers:
  Padding: 1.5rem (reduced from 2rem)

Buttons:
  Full width on mobile
  Stacked vertically
```

## 🎬 Animation Timings

### Transitions
- Default: `0.3s ease`
- Hover effects: `0.4s cubic-bezier(0.4, 0, 0.2, 1)`
- Scale animations: `0.3s ease`

### Keyframe Animations
```css
fadeInScale: 0.6s ease-out
progressShine: 2s linear infinite
pulse: 2s ease-in-out infinite
fadeIn: 0.5s ease-in
```

## 🔤 Typography

### Font Families
```css
Titles: 'Orbitron', sans-serif
Body: 'Inter', sans-serif
```

### Font Sizes
```css
Main title: 2.5rem (40px)
Section headers: 1.5rem (24px)
Body text: 1rem (16px)
Small text: 0.9rem (14.4px)
Button text: 1.1rem (17.6px)
```

### Font Weights
```css
Orbitron: 400, 700, 900
Inter: 300, 400, 500, 600
```

### Letter Spacing
```css
Titles: 2px
Uppercase text: 1px
Body: normal
```

## 🎨 Gradient Definitions

### Primary Button Gradient
```css
linear-gradient(135deg, #ff4500 0%, #ffd700 100%)
```

### Background Gradient
```css
linear-gradient(135deg, #0a0a0a 0%, #1a2332 50%, #2a1810 100%)
```

### Text Gradient (Titles)
```css
linear-gradient(135deg, #ff4500 0%, #ffd700 100%)
-webkit-background-clip: text
-webkit-text-fill-color: transparent
```

### Progress Bar Gradient
```css
linear-gradient(90deg, #ff4500, #ffd700, #ff4500)
background-size: 200% 100%
```

## 🌟 Special Effects

### Glow on Hover
```css
filter: drop-shadow(0 0 20px rgba(255, 69, 0, 0.6))
```

### Neon Border
```css
border: 2px solid rgba(255, 140, 0, 0.2)
box-shadow: 0 0 80px rgba(255, 69, 0, 0.15)
```

### Status Badge Pulse
```css
@keyframes pulse {
  0%, 100%: opacity 1, scale 1
  50%: opacity 0.8, scale 1.05
}
```

### Card Hover Lift
```css
transform: translateY(-4px)
box-shadow: Enhanced + glow
```

## 📊 Z-Index Layers

```
Canvas background: -2
Base content: 0
Cards: 1
Modals: 100
Tooltips: 200
```

## 🎯 Accessibility

### Contrast Ratios
- Text on dark: 4.5:1 minimum
- Buttons: High contrast black on gradient
- Focus indicators: Visible orange glow

### Interactive Elements
- Minimum touch target: 44x44px
- Keyboard navigation: Full support
- Focus visible: Orange glow outline

## 🔧 Browser Prefixes

```css
backdrop-filter: blur(16px)
-webkit-backdrop-filter: blur(16px)

background-clip: text
-webkit-background-clip: text

text-fill-color: transparent
-webkit-text-fill-color: transparent
```

## 📐 Spacing System

```css
xs: 0.25rem (4px)
sm: 0.5rem (8px)
md: 1rem (16px)
lg: 1.5rem (24px)
xl: 2rem (32px)
2xl: 2.5rem (40px)
3xl: 3rem (48px)
```

## 🎊 Summary

This design system creates a **cohesive, futuristic, sci-fi experience** with:
- Consistent color palette
- Smooth animations
- Glassmorphic depth
- Neon accents
- Interactive elements
- Responsive layout
- Professional polish

**Every pixel designed for the future! 🚀✨**
