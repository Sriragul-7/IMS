<template>
  <div class="hero-banner" :class="variantClass">
    <div class="hero-bg-shapes" aria-hidden="true">
      <div v-for="i in 5" :key="i" class="hero-shape" :class="`hero-shape--${i}`"></div>
    </div>
    <div class="hero-content" v-if="!compact">
      <div class="hero-greeting" v-if="greeting || time">
        <span class="greeting-text">{{ greeting || computedGreeting }}</span>
        <span class="greeting-divider" v-if="time">·</span>
        <time v-if="time" class="greeting-time" :datetime="dateISO">{{ formattedDate }}</time>
      </div>
      <h1 class="hero-title" v-if="title">{{ title }}</h1>
      <p class="hero-subtitle" v-if="subtitle">{{ subtitle }}</p>
      <div class="hero-meta" v-if="metaItems.length">
        <div v-for="item in metaItems" :key="item.label" class="hero-meta-item">
          <span class="meta-icon" v-html="item.icon"></span>
          <div class="meta-text">
            <span class="meta-label">{{ item.label }}</span>
            <span class="meta-value">{{ item.value }}</span>
          </div>
        </div>
      </div>
      <div class="hero-actions" v-if="$slots.actions">
        <slot name="actions" />
      </div>
    </div>
    <div class="hero-content hero-content--compact" v-else>
      <div class="hero-greeting" v-if="greeting || time">
        <span class="greeting-text">{{ greeting || computedGreeting }}</span>
        <span class="greeting-divider" v-if="time">·</span>
        <time v-if="time" class="greeting-time" :datetime="dateISO">{{ formattedDate }}</time>
      </div>
      <h1 class="hero-title" v-if="title">{{ title }}</h1>
      <div class="hero-actions" v-if="$slots.actions">
        <slot name="actions" />
      </div>
    </div>
    <div class="hero-illustration" v-if="illustration && !compact" aria-hidden="true">
      <component :is="illustrationComponent" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const props = defineProps({
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  greeting: { type: String, default: '' },
  time: { type: Boolean, default: true },
  variant: { type: String, default: 'primary' },
  compact: { type: Boolean, default: false },
  illustration: { type: String, default: '' },
  metaItems: { type: Array, default: () => [] }
})

const now = ref(new Date())
const dateISO = computed(() => now.value.toISOString())

const formattedDate = computed(() => {
  return now.value.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  })
})

const computedGreeting = computed(() => {
  const hour = now.value.getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 17) return 'Good afternoon'
  return 'Good evening'
})

const variantClass = computed(() => `hero-banner--${props.variant}`)

// Inline SVG Illustration Components
const CampusIllustration = {
  template: `
    <svg viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg" class="illustration-svg">
      <defs>
        <linearGradient id="skyGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0f172a" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="#0d9488" stop-opacity="0.1"/>
        </linearGradient>
        <linearGradient id="buildingGradient1" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#1e293b" stop-opacity="0.6"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0.4"/>
        </linearGradient>
        <linearGradient id="buildingGradient2" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0d9488" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="#14b8a6" stop-opacity="0.1"/>
        </linearGradient>
      </defs>
      <rect width="400" height="300" fill="url(#skyGradient)"/>
      <path d="M0 250 Q200 230 400 250 L400 300 L0 300 Z" fill="rgba(15, 23, 42, 0.15)"/>
      <path d="M40 250 L40 120 Q60 100 80 100 L120 100 Q140 100 140 120 L140 250 Z" fill="url(#buildingGradient1)"/>
      <rect x="55" y="140" width="20" height="30" rx="2" fill="rgba(14, 184, 166, 0.4)"/>
      <rect x="90" y="140" width="20" height="30" rx="2" fill="rgba(14, 184, 166, 0.4)"/>
      <rect x="55" y="185" width="20" height="30" rx="2" fill="rgba(14, 184, 166, 0.4)"/>
      <rect x="90" y="185" width="20" height="30" rx="2" fill="rgba(14, 184, 166, 0.4)"/>
      <path d="M180 250 L180 90 Q210 70 240 70 L270 70 Q300 70 300 90 L300 250 Z" fill="url(#buildingGradient2)"/>
      <circle cx="240" cy="110" r="15" fill="rgba(255,255,255,0.1)"/>
      <rect x="200" y="150" width="20" height="25" rx="2" fill="rgba(14, 184, 166, 0.5)"/>
      <rect x="230" y="150" width="20" height="25" rx="2" fill="rgba(14, 184, 166, 0.5)"/>
      <rect x="260" y="150" width="20" height="25" rx="2" fill="rgba(14, 184, 166, 0.5)"/>
      <ellipse cx="350" cy="240" rx="35" ry="25" fill="rgba(5, 150, 105, 0.2)"/>
      <ellipse cx="370" cy="220" rx="25" ry="20" fill="rgba(5, 150, 105, 0.3)"/>
      <rect x="355" y="260" width="10" height="30" fill="rgba(30, 64, 175, 0.2)"/>
      <circle cx="80" cy="60" r="3" fill="rgba(14, 184, 166, 0.4)" class="float-particle" style="animation-delay: 0s"/>
      <circle cx="200" cy="40" r="2" fill="rgba(14, 184, 166, 0.3)" class="float-particle" style="animation-delay: 1s"/>
      <circle cx="320" cy="80" r="2.5" fill="rgba(14, 184, 166, 0.4)" class="float-particle" style="animation-delay: 2s"/>
      <circle cx="150" cy="180" r="2" fill="rgba(14, 184, 166, 0.2)" class="float-particle" style="animation-delay: 0.5s"/>
    </svg>
  `
}

const GraduationIllustration = {
  template: `
    <svg viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg" class="illustration-svg">
      <defs>
        <linearGradient id="capGradient" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#0f172a" stop-opacity="0.5"/>
          <stop offset="100%" stop-color="#0d9488" stop-opacity="0.3"/>
        </linearGradient>
      </defs>
      <path d="M120 180 L120 100 Q200 60 280 100 L280 180 Z" fill="url(#capGradient)" stroke="rgba(14, 184, 166, 0.5)" stroke-width="2"/>
      <path d="M100 180 L300 180" stroke="rgba(14, 184, 166, 0.4)" stroke-width="4" stroke-linecap="round"/>
      <ellipse cx="200" cy="95" rx="90" ry="15" fill="url(#capGradient)"/>
      <path d="M280 100 Q300 120 290 160" stroke="rgba(217, 119, 6, 0.6)" stroke-width="3" stroke-linecap="round" fill="none"/>
      <g stroke="rgba(217, 119, 6, 0.5)" stroke-width="2" stroke-linecap="round">
        <line x1="288" y1="155" x2="288" y2="175"/>
        <line x1="292" y1="155" x2="292" y2="175"/>
        <line x1="284" y1="158" x2="284" y2="172"/>
        <line x1="296" y1="158" x2="296" y2="172"/>
      </g>
      <path d="M160 180 L160 240 Q160 250 170 250 L230 250 Q240 250 240 240 L240 180" fill="rgba(255,255,255,0.1)" stroke="rgba(14, 184, 166, 0.3)" stroke-width="1.5"/>
      <path d="M180 200 L220 200" stroke="rgba(14, 184, 166, 0.4)" stroke-width="1.5"/>
      <path d="M180 215 L210 215" stroke="rgba(14, 184, 166, 0.3)" stroke-width="1"/>
      <path d="M180 230 L200 230" stroke="rgba(14, 184, 166, 0.2)" stroke-width="1"/>
      <g class="star" transform="translate(80, 60)" style="animation-delay: 0s">
        <polygon points="10,0 12,7 20,7 14,11 16,19 10,15 4,19 6,11 0,7 8,7" fill="rgba(217, 119, 6, 0.4)"/>
      </g>
      <g class="star" transform="translate(340, 50)" style="animation-delay: 1s">
        <polygon points="10,0 12,7 20,7 14,11 16,19 10,15 4,19 6,11 0,7 8,7" fill="rgba(14, 184, 166, 0.4)"/>
      </g>
      <g class="star" transform="translate(50, 200)" style="animation-delay: 2s">
        <polygon points="8,0 9,6 15,6 10,10 11,16 8,13 5,16 6,10 0,6 6,6" fill="rgba(217, 119, 6, 0.3)"/>
      </g>
      <g class="star" transform="translate(350, 180)" style="animation-delay: 0.5s">
        <polygon points="8,0 9,6 15,6 10,10 11,16 8,13 5,16 6,10 0,6 6,6" fill="rgba(14, 184, 166, 0.3)"/>
      </g>
    </svg>
  `
}

const AbstractIllustration = {
  template: `
    <svg viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg" class="illustration-svg">
      <defs>
        <radialGradient id="orb1" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#0d9488" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
        </radialGradient>
        <radialGradient id="orb2" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
        </radialGradient>
        <radialGradient id="orb3" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#d97706" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <circle cx="100" cy="100" r="120" fill="url(#orb1)" class="orb-float" style="animation-delay: 0s"/>
      <circle cx="320" cy="80" r="100" fill="url(#orb2)" class="orb-float" style="animation-delay: 1s"/>
      <circle cx="200" cy="250" r="140" fill="url(#orb3)" class="orb-float" style="animation-delay: 2s"/>
      <g stroke="rgba(14, 184, 166, 0.2)" stroke-width="1.5" fill="none" class="geo-rotate" style="animation-delay: 0s">
        <polygon points="200,50 230,110 170,110"/>
        <polygon points="200,70 220,110 180,110"/>
      </g>
      <g stroke="rgba(124, 58, 237, 0.2)" stroke-width="1.5" fill="none" class="geo-rotate-reverse" style="animation-delay: 1s">
        <rect x="150" y="200" width="100" height="100" rx="10"/>
        <rect x="165" y="215" width="70" height="70" rx="6"/>
      </g>
      <g stroke="rgba(217, 119, 6, 0.15)" stroke-width="1" fill="none" class="geo-pulse" style="animation-delay: 2s">
        <circle cx="200" cy="150" r="30"/>
        <circle cx="200" cy="150" r="50"/>
        <circle cx="200" cy="150" r="70"/>
      </g>
      <g stroke="rgba(14, 184, 166, 0.05)" stroke-width="0.5">
        <line x1="0" y1="0" x2="400" y2="300"/>
        <line x1="400" y1="0" x2="0" y2="300"/>
        <line x1="200" y1="0" x2="200" y2="300"/>
        <line x1="0" y1="150" x2="400" y2="150"/>
      </g>
    </svg>
  `
}

const BooksIllustration = {
  template: `
    <svg viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg" class="illustration-svg">
      <defs>
        <linearGradient id="book1" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0d9488" stop-opacity="0.4"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0.2"/>
        </linearGradient>
        <linearGradient id="book2" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.4"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0.2"/>
        </linearGradient>
        <linearGradient id="book3" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#d97706" stop-opacity="0.4"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0.2"/>
        </linearGradient>
      </defs>
      <g transform="translate(120, 100)">
        <path d="M0 0 L80 0 L85 5 L85 65 L80 70 L0 70 Z" fill="url(#book1)"/>
        <path d="M80 0 L85 5 L85 65 L80 70" fill="rgba(14, 184, 166, 0.3)"/>
        <rect x="15" y="20" width="50" height="4" rx="2" fill="rgba(255,255,255,0.1)"/>
        <rect x="15" y="30" width="35" height="2" rx="1" fill="rgba(255,255,255,0.08)"/>
        <rect x="15" y="38" width="45" height="2" rx="1" fill="rgba(255,255,255,0.06)"/>
        <path d="M5 -55 L85 -55 L90 -50 L90 10 L85 15 L5 15 Z" fill="url(#book2)"/>
        <path d="M85 -55 L90 -50 L90 10 L85 15" fill="rgba(124, 58, 237, 0.3)"/>
        <rect x="12" y="-45" width="55" height="4" rx="2" fill="rgba(255,255,255,0.15)"/>
        <rect x="12" y="-35" width="40" height="2" rx="1" fill="rgba(255,255,255,0.1)"/>
        <rect x="12" y="-27" width="50" height="2" rx="1" fill="rgba(255,255,255,0.08)"/>
        <path d="M15 -110 L95 -110 L100 -105 L100 -45 L95 -40 L15 -40 Z" fill="url(#book3)"/>
        <path d="M95 -110 L100 -105 L100 -45 L95 -40" fill="rgba(217, 119, 6, 0.3)"/>
        <rect x="25" y="-100" width="45" height="4" rx="2" fill="rgba(255,255,255,0.2)"/>
        <rect x="25" y="-90" width="30" height="2" rx="1" fill="rgba(255,255,255,0.15)"/>
        <rect x="25" y="-82" width="40" height="2" rx="1" fill="rgba(255,255,255,0.1)"/>
        <path d="M95 -70 L105 -60 L105 -50 L95 -60 Z" fill="rgba(255,255,255,0.3)"/>
      </g>
      <g class="float-item" style="animation-delay: 0s" transform="translate(300, 80)">
        <circle r="20" fill="rgba(14, 184, 166, 0.15)"/>
        <path d="M-8 0 L8 0 M0 -8 L0 8" stroke="rgba(14, 184, 166, 0.4)" stroke-width="2" stroke-linecap="round"/>
      </g>
      <g class="float-item" style="animation-delay: 1s" transform="translate(350, 180)">
        <path d="M-12 12 L0 -12 L12 12 Z" fill="none" stroke="rgba(124, 58, 237, 0.4)" stroke-width="2"/>
        <circle r="3" fill="rgba(124, 58, 237, 0.4)"/>
      </g>
      <g class="float-item" style="animation-delay: 2s" transform="translate(280, 240)">
        <rect x="-10" y="-10" width="20" height="20" rx="3" fill="none" stroke="rgba(217, 119, 6, 0.4)" stroke-width="2"/>
        <path d="M-5 0 L5 0 M0 -5 L0 5" stroke="rgba(217, 119, 6, 0.4)" stroke-width="1.5" stroke-linecap="round"/>
      </g>
    </svg>
  `
}

const DashboardIllustration = {
  template: `
    <svg viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg" class="illustration-svg">
      <defs>
        <linearGradient id="chartArea" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0d9488" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <rect x="40" y="40" width="320" height="220" rx="8" fill="rgba(15, 23, 42, 0.05)" stroke="rgba(14, 184, 166, 0.1)" stroke-width="1"/>
      <g stroke="rgba(14, 184, 166, 0.05)" stroke-width="0.5">
        <line x1="60" y1="60" x2="340" y2="60"/>
        <line x1="60" y1="110" x2="340" y2="110"/>
        <line x1="60" y1="160" x2="340" y2="160"/>
        <line x1="60" y1="210" x2="340" y2="210"/>
        <line x1="100" y1="40" x2="100" y2="240"/>
        <line x1="160" y1="40" x2="160" y2="240"/>
        <line x1="220" y1="40" x2="220" y2="240"/>
        <line x1="280" y1="40" x2="280" y2="240"/>
      </g>
      <path d="M70 200 L110 150 L150 180 L190 120 L230 160 L270 90 L310 130" 
            stroke="url(#chartArea)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" class="chart-line"/>
      <g>
        <circle cx="70" cy="200" r="5" fill="var(--color-accent)" class="chart-point" style="animation-delay: 0.1s"/>
        <circle cx="110" cy="150" r="5" fill="var(--color-accent)" class="chart-point" style="animation-delay: 0.2s"/>
        <circle cx="150" cy="180" r="5" fill="var(--color-accent)" class="chart-point" style="animation-delay: 0.3s"/>
        <circle cx="190" cy="120" r="5" fill="var(--color-accent)" class="chart-point" style="animation-delay: 0.4s"/>
        <circle cx="230" cy="160" r="5" fill="var(--color-accent)" class="chart-point" style="animation-delay: 0.5s"/>
        <circle cx="270" cy="90" r="5" fill="var(--color-accent)" class="chart-point" style="animation-delay: 0.6s"/>
        <circle cx="310" cy="130" r="5" fill="var(--color-accent)" class="chart-point" style="animation-delay: 0.7s"/>
      </g>
      <g class="bars-stagger">
        <rect x="100" y="180" width="30" height="40" rx="2" fill="rgba(14, 184, 166, 0.3)" style="animation-delay: 0.2s"/>
        <rect x="160" y="140" width="30" height="80" rx="2" fill="rgba(14, 184, 166, 0.4)" style="animation-delay: 0.3s"/>
        <rect x="220" y="160" width="30" height="60" rx="2" fill="rgba(14, 184, 166, 0.3)" style="animation-delay: 0.4s"/>
        <rect x="280" y="110" width="30" height="110" rx="2" fill="rgba(14, 184, 166, 0.5)" style="animation-delay: 0.5s"/>
      </g>
      <g class="stat-cards-float">
        <rect x="40" y="270" width="80" height="40" rx="6" fill="rgba(15, 23, 42, 0.1)" stroke="rgba(14, 184, 166, 0.2)" stroke-width="1" style="animation-delay: 0s"/>
        <rect x="160" y="270" width="80" height="40" rx="6" fill="rgba(15, 23, 42, 0.1)" stroke="rgba(124, 58, 237, 0.2)" stroke-width="1" style="animation-delay: 0.2s"/>
        <rect x="280" y="270" width="80" height="40" rx="6" fill="rgba(15, 23, 42, 0.1)" stroke="rgba(217, 119, 6, 0.2)" stroke-width="1" style="animation-delay: 0.4s"/>
      </g>
    </svg>
  `
}

const LoginIllustration = {
  template: `
    <svg viewBox="0 0 400 300" fill="none" xmlns="http://www.w3.org/2000/svg" class="illustration-svg">
      <defs>
        <linearGradient id="loginBg" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0f172a" stop-opacity="0.15"/>
          <stop offset="50%" stop-color="#0d9488" stop-opacity="0.08"/>
          <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.1"/>
        </linearGradient>
        <radialGradient id="orbLogin1" cx="20%" cy="30%" r="40%">
          <stop offset="0%" stop-color="#0d9488" stop-opacity="0.25"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
        </radialGradient>
        <radialGradient id="orbLogin2" cx="80%" cy="70%" r="35%">
          <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
        </radialGradient>
        <radialGradient id="orbLogin3" cx="50%" cy="10%" r="30%">
          <stop offset="0%" stop-color="#d97706" stop-opacity="0.15"/>
          <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="400" height="300" fill="url(#loginBg)"/>
      <circle cx="80" cy="90" r="100" fill="url(#orbLogin1)" class="orb-float" style="animation-delay: 0s"/>
      <circle cx="320" cy="210" r="90" fill="url(#orbLogin2)" class="orb-float" style="animation-delay: 1s"/>
      <circle cx="200" cy="30" r="80" fill="url(#orbLogin3)" class="orb-float" style="animation-delay: 2s"/>
      <g stroke="rgba(14, 184, 166, 0.1)" stroke-width="1" fill="none" class="geo-rotate" style="animation-delay: 0s; transform-origin: 200px 150px;">
        <polygon points="200,40 240,100 160,100"/>
        <polygon points="200,60 220,100 180,100"/>
      </g>
      <g stroke="rgba(124, 58, 237, 0.1)" stroke-width="1" fill="none" class="geo-rotate-reverse" style="animation-delay: 1s; transform-origin: 200px 150px;">
        <rect x="140" y="180" width="120" height="120" rx="12"/>
        <rect x="155" y="195" width="90" height="90" rx="8"/>
      </g>
      <g class="sparkle" style="animation-delay: 0s" transform="translate(60, 60)">
        <path d="M0 -8 L0 8 M-8 0 L8 0 M-6 -6 L6 6 M-6 6 L6 -6" stroke="rgba(14, 184, 166, 0.5)" stroke-width="1.5" stroke-linecap="round"/>
      </g>
      <g class="sparkle" style="animation-delay: 0.5s" transform="translate(340, 50)">
        <path d="M0 -6 L0 6 M-6 0 L6 0 M-4 -4 L4 4 M-4 4 L4 -4" stroke="rgba(217, 119, 6, 0.5)" stroke-width="1" stroke-linecap="round"/>
      </g>
      <g class="sparkle" style="animation-delay: 1s" transform="translate(100, 220)">
        <path d="M0 -7 L0 7 M-7 0 L7 0 M-5 -5 L5 5 M-5 5 L5 -5" stroke="rgba(124, 58, 237, 0.4)" stroke-width="1.5" stroke-linecap="round"/>
      </g>
      <g class="sparkle" style="animation-delay: 1.5s" transform="translate(300, 240)">
        <path d="M0 -5 L0 5 M-5 0 L5 0 M-3 -3 L3 3 M-3 3 L3 -3" stroke="rgba(14, 184, 166, 0.4)" stroke-width="1" stroke-linecap="round"/>
      </g>
    </svg>
  `
}

const illustrationComponent = computed(() => {
  const illustrations = {
    'campus': CampusIllustration,
    'graduation': GraduationIllustration,
    'abstract': AbstractIllustration,
    'books': BooksIllustration,
    'dashboard': DashboardIllustration,
    'login': LoginIllustration
  }
  return illustrations[props.illustration] || CampusIllustration
})

onMounted(() => {
  const interval = setInterval(() => {
    now.value = new Date()
  }, 60000)
  return () => clearInterval(interval)
})
</script>

<style scoped>
.hero-banner {
  position: relative;
  border-radius: var(--radius-2xl);
  padding: var(--space-8);
  overflow: hidden;
  color: white;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.hero-banner--primary { background: var(--gradient-hero); }
.hero-banner--accent { background: var(--gradient-accent); }
.hero-banner--dark { background: var(--gradient-hero-alt); }
.hero-banner--custom { background: transparent; }

.hero-bg-shapes { position: absolute; inset: 0; pointer-events: none; overflow: hidden; }
.hero-shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255,255,255,0.05);
  animation: float 20s ease-in-out infinite;
}
.hero-shape--1 { width: 200px; height: 200px; top: -50px; right: -50px; animation-delay: 0s; }
.hero-shape--2 { width: 150px; height: 150px; bottom: -30px; left: -30px; animation-delay: -5s; }
.hero-shape--3 { width: 100px; height: 100px; top: 20%; right: 10%; animation-delay: -10s; }
.hero-shape--4 { width: 80px; height: 80px; bottom: 30%; left: 15%; animation-delay: -15s; }
.hero-shape--5 { width: 60px; height: 60px; top: 50%; right: 30%; animation-delay: -7s; }

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(20px, -20px) scale(1.05); }
  50% { transform: translate(-15px, 15px) scale(0.95); }
  75% { transform: translate(10px, 10px) scale(1.02); }
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 700px;
  flex: 1;
}
.hero-content--compact { max-width: 100%; }

.hero-greeting {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  font-weight: var(--font-weight-medium);
  opacity: 0.8;
  margin-bottom: var(--space-2);
  flex-wrap: wrap;
}
.greeting-text { text-transform: capitalize; }
.greeting-divider { opacity: 0.5; }
.greeting-time { font-variant-numeric: tabular-nums; opacity: 0.7; }

.hero-title {
  font-size: var(--text-5xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--leading-tight);
  letter-spacing: -0.025em;
  margin-bottom: var(--space-2);
  animation: slideUp var(--transition-slow) ease;
}
.hero-subtitle {
  font-size: var(--text-lg);
  opacity: 0.7;
  max-width: 600px;
  margin-bottom: var(--space-6);
  animation: slideUp var(--transition-slow) 0.1s ease both;
}
.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
  animation: slideUp var(--transition-slow) 0.2s ease both;
}
.hero-meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: rgba(255,255,255,0.1);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.1);
}
.meta-icon { font-size: 1.25rem; opacity: 0.9; }
.meta-text { display: flex; flex-direction: column; }
.meta-label { font-size: var(--text-xs); opacity: 0.6; text-transform: uppercase; letter-spacing: 0.05em; }
.meta-value { font-size: var(--text-sm); font-weight: var(--font-weight-semibold); }

.hero-actions { animation: slideUp var(--transition-slow) 0.3s ease both; }

.hero-illustration {
  position: absolute;
  right: var(--space-8);
  bottom: var(--space-8);
  width: 300px;
  height: 225px;
  opacity: 0.6;
  pointer-events: none;
}
.illustration-svg { width: 100%; height: 100%; }

/* Animation classes for illustrations */
.float-particle { animation: particleFloat 6s ease-in-out infinite; }
@keyframes particleFloat {
  0%, 100% { transform: translateY(0) scale(1); opacity: 0.4; }
  50% { transform: translateY(-15px) scale(1.2); opacity: 0.8; }
}
.star { animation: starPulse 3s ease-in-out infinite; }
@keyframes starPulse {
  0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.4; }
  50% { transform: scale(1.2) rotate(180deg); opacity: 0.8; }
}
.orb-float { animation: orbFloat 15s ease-in-out infinite; }
@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(20px, -15px) scale(1.05); }
  66% { transform: translate(-15px, 10px) scale(0.95); }
}
.geo-rotate { animation: geoRotate 20s linear infinite; transform-origin: center; }
.geo-rotate-reverse { animation: geoRotate 25s linear infinite reverse; transform-origin: center; }
@keyframes geoRotate { to { transform: rotate(360deg); } }
.geo-pulse { animation: geoPulse 4s ease-in-out infinite; transform-origin: center; }
@keyframes geoPulse {
  0%, 100% { transform: scale(1); opacity: 0.15; }
  50% { transform: scale(1.1); opacity: 0.3; }
}
.float-item { animation: itemFloat 5s ease-in-out infinite; }
@keyframes itemFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(5deg); }
}
.chart-line { animation: chartDraw 2s ease-out forwards; stroke-dasharray: 400; stroke-dashoffset: 400; }
@keyframes chartDraw { to { stroke-dashoffset: 0; } }
.chart-point { animation: pointPop 0.4s ease-out backwards; transform-origin: center; }
@keyframes pointPop { from { transform: scale(0); opacity: 0; } to { transform: scale(1); opacity: 1; } }
.bars-stagger rect { animation: barGrow 0.8s ease-out backwards; transform-origin: bottom; }
@keyframes barGrow { from { transform: scaleY(0); opacity: 0; } to { transform: scaleY(1); opacity: 1; } }
.stat-cards-float rect { animation: cardFloat 4s ease-in-out infinite; }
@keyframes cardFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
.sparkle { animation: sparklePulse 2s ease-in-out infinite; }
@keyframes sparklePulse {
  0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.4; }
  50% { transform: scale(1.3) rotate(90deg); opacity: 0.9; }
}

@media (max-width: 1024px) {
  .hero-banner { padding: var(--space-6); min-height: 220px; }
  .hero-title { font-size: var(--text-4xl); }
  .hero-illustration { width: 240px; height: 180px; right: var(--space-6); bottom: var(--space-6); opacity: 0.4; }
}
@media (max-width: 768px) {
  .hero-banner { flex-direction: column; text-align: center; padding: var(--space-6); min-height: auto; }
  .hero-content { max-width: 100%; }
  .hero-greeting { justify-content: center; }
  .hero-meta { justify-content: center; }
  .hero-illustration { display: none; }
}
@media (max-width: 640px) {
  .hero-title { font-size: var(--text-3xl); }
  .hero-subtitle { font-size: var(--text-md); }
}
</style>