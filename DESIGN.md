---
name: High-Performance Gaming AI
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#c4c5d9'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#8e8fa2'
  outline-variant: '#434656'
  surface-tint: '#b9c3ff'
  primary: '#b9c3ff'
  on-primary: '#00218b'
  primary-container: '#1b4dff'
  on-primary-container: '#dde0ff'
  inverse-primary: '#0b46f9'
  secondary: '#bdf4ff'
  on-secondary: '#00363d'
  secondary-container: '#00e3fd'
  on-secondary-container: '#00616d'
  tertiary: '#cdbdff'
  on-tertiary: '#370096'
  tertiary-container: '#6e3bf0'
  on-tertiary-container: '#e7ddff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#dee1ff'
  primary-fixed-dim: '#b9c3ff'
  on-primary-fixed: '#001258'
  on-primary-fixed-variant: '#0032c3'
  secondary-fixed: '#9cf0ff'
  secondary-fixed-dim: '#00daf3'
  on-secondary-fixed: '#001f24'
  on-secondary-fixed-variant: '#004f58'
  tertiary-fixed: '#e8deff'
  tertiary-fixed-dim: '#cdbdff'
  on-tertiary-fixed: '#20005f'
  on-tertiary-fixed-variant: '#4f00d0'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 57px
    fontWeight: '700'
    lineHeight: 64px
    letterSpacing: -0.25px
  headline-md:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: 0px
  title-lg:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '500'
    lineHeight: 28px
    letterSpacing: 0px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0.5px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0.25px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.5px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin: 20px
---

## Brand & Style
The brand personality is authoritative, technical, and immersive, designed to mirror the high-fidelity environments of modern gaming. It prioritizes performance and responsiveness, ensuring the user feels in control of a sophisticated artificial intelligence.

The design system employs a **Corporate / Modern** style with a specialized "High-Tech" veneer. It bridges the gap between the clean, functional deference of Apple’s Human Interface Guidelines and the structured, expressive elevation of Material Design 3. The aesthetic is "Dark-Mode First," utilizing deep shadows and vibrant primary accents to create a sense of depth and focus that minimizes eye strain during long gaming sessions.

## Colors
The color palette is anchored by a **Deep Electric Blue**, used strategically for primary actions and state indications. This is set against a foundation of **Dark-surface neutrals**, ranging from deep charcoals (#121212) to absolute black (#000000), ensuring maximum contrast for the primary blue and secondary cyan accents.

The secondary color acts as a "technical accent" for data visualization and success states, while the tertiary violet provides a subtle depth for AI-specific features. All interactive elements must maintain a high contrast ratio against the dark backgrounds to meet accessibility standards while maintaining the immersive gaming mood.

## Typography
This design system utilizes **Inter** across all levels to ensure maximum legibility and a neutral, systematic feel. The hierarchy is strictly defined to help users parse complex gaming data and AI chat logs quickly.

- **Headlines:** Bold and tight, used for screen titles and major section headers.
- **Body:** Standardized with generous line-height to ensure readability on mobile screens during motion.
- **Labels:** Medium weights are used for buttons and chips to provide a clear "tappable" affordance.
- **Monospaced elements:** When displaying game code or technical stats, use system monospaced fonts at the `label-md` size.

## Layout & Spacing
The layout follows a **Fluid Grid** model optimized for mobile-first interaction. It utilizes a base 4px spacing increment to ensure mathematical consistency across all components.

The layout uses a standard 4-column grid for mobile, with 16px gutters and 20px side margins to prevent content from touching the screen edges. Chat bubbles and surface containers should adapt to the screen width, while vertical rhythm is maintained through the consistent use of the `md` (16px) and `lg` (24px) spacing tokens between distinct UI blocks.

## Elevation & Depth
Elevation in this design system is conveyed through **Tonal Layers** and **Ambient Shadows**, drawing heavily from Material Design 3's surface container logic.

Higher elevation levels correspond to lighter surface colors. 
- **Level 0:** Pure black (#000000) for the background.
- **Level 1:** Deep charcoal (#121212) for primary content areas.
- **Level 2:** Lighter charcoal (#1E1E1E) for cards and modals, featuring a subtle 8% white overlay.

Shadows are used sparingly to indicate "Level 2" elevation. They are extra-diffused with a low-opacity black tint (0.3) and a 12px blur radius to create a soft "lift" rather than a harsh border. High-priority AI messages may feature a subtle blue "glow" or backdrop blur to signify their importance.

## Shapes
The shape language is consistently **Rounded**, providing a modern, friendly touch to an otherwise technical and dark aesthetic. 

- **Base Components:** 0.5rem (8px) radius.
- **Text Fields & Buttons:** 1rem (16px) radius for a comfortable, modern feel.
- **Large Containers:** 1.5rem (24px) radius for bottom sheets and large cards.

This approach ensures that even with a dark and aggressive color palette, the interface remains approachable and ergonomically optimized for thumb-based mobile interaction.

## Components
Consistent styling of components is critical for the high-tech mood of this design system:

- **Buttons:** Primary buttons use a solid Deep Electric Blue fill with white text. Secondary buttons are outlined with the same blue. Both use 1rem roundedness.
- **Chips:** Follow the MD3 outlined style. They feature a 1px border using the primary color or a neutral mid-grey, with a subtle background tint when active.
- **Input Fields:** Fully rounded (1rem) with a neutral-low background and a clear, primary-blue 2px border on focus.
- **Surface Containers (Cards):** Use Level 1 or Level 2 elevation colors with no borders. Use Level 2 shadows for cards that require user interaction.
- **AI Chat Bubbles:** The AI's messages should have a subtle tertiary gradient or a low-opacity blue surface container to distinguish them from the user's neutral-grey bubbles.
- **Lists:** Clean, edge-to-edge layout with thin dividers (#2C2C2C) and 16px vertical padding for touch targets.