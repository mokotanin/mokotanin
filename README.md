# Mokotanin Portfolio

![Portfolio Preview](https://github.com/user-attachments/assets/2cce8332-17ff-43c1-b7ad-f0f3b1382cb7)

A modern, minimalist portfolio website with stunning CSS animations and a sleek black UI/UX design.

## Features

### 🎨 Design
- **Modern Minimalist Black Theme** - Clean, professional aesthetic with accent green (#00ff88)
- **Fully Responsive** - Mobile-first design that works on all devices
- **Custom Scrollbar** - Styled to match the overall theme
- **Gradient Effects** - Beautiful gradient backgrounds and icons

### ✨ Animations
- **Hero Section** - Animated glowing text with glitch effect and moving grid background
- **Scroll Animations** - Fade-in effects triggered by scrolling
- **Counter Animations** - Animated statistics that count up when visible
- **Progress Bars** - Skill levels animate on scroll
- **Hover Effects** - Interactive cards and buttons with smooth transitions
- **Custom Cursor** - Optional custom cursor trail effect

### 📱 Sections
1. **Hero/Landing** - Eye-catching introduction with call-to-action buttons
2. **About** - Professional introduction with animated statistics
3. **Skills** - Technology stack with animated progress bars
4. **Projects** - Portfolio showcase with hover overlays
5. **Contact** - Working contact form with social media links

### 🚀 Technical Highlights
- Pure HTML5, CSS3, and vanilla JavaScript (no frameworks)
- Intersection Observer API for efficient scroll animations
- CSS Grid and Flexbox for responsive layouts
- CSS custom properties for easy theming
- Optimized performance with throttled scroll handlers
- RequestAnimationFrame for smooth cursor animations
- No security vulnerabilities (CodeQL verified)

## Getting Started

Simply open `index.html` in your web browser or serve it with any web server:

```bash
# Using Python
python3 -m http.server 8000

# Using Node.js
npx http-server
```

Then navigate to `http://localhost:8000`

## Customization

### Colors
Edit the CSS custom properties in `styles.css`:
```css
:root {
    --primary-color: #ffffff;
    --accent-color: #00ff88;  /* Change this for different accent color */
    --bg-primary: #000000;
    /* ... */
}
```

### Content
- Update text content in `index.html`
- Replace project information in the Projects section
- Update contact information in the Contact section
- Add your own images to the `assets` folder

### Icons
The portfolio uses Font Awesome icons. Replace icon classes to use different icons from [Font Awesome](https://fontawesome.com/icons).

## Browser Support
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance
- Throttled scroll event handlers for optimal performance
- RequestAnimationFrame for smooth animations
- Lazy loading of animations (triggered on scroll)
- Minimal JavaScript for fast load times

## License
This project is open source and available under the MIT License.

## Screenshots

### Hero Section
![Hero](https://github.com/user-attachments/assets/2cce8332-17ff-43c1-b7ad-f0f3b1382cb7)

### About Section
![About](https://github.com/user-attachments/assets/06313522-a99f-4393-bfb0-61c8d0a7b972)

### Skills Section
![Skills](https://github.com/user-attachments/assets/d60d3044-63a7-4dee-ab73-ec34d8ba7634)

### Projects Section
![Projects](https://github.com/user-attachments/assets/5f653324-ce06-41e0-92a9-f67639ef85b2)

### Contact Section
![Contact](https://github.com/user-attachments/assets/b584f48f-a7c1-4cef-b961-5d852cf71ae3)

---

**Built with ❤️ by Mokotanin**

