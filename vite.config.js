import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  // Base path for GitHub Pages (project page): https://ashmitKmishra.github.io/BullDawg-Hackers/
  base: '/BullDawg-Hackers/',
  plugins: [react()],
  optimizeDeps: {
    include: ['animejs']
  },
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
    }
  },
  preview: {
    port: 3000,
    host: true
  }
})
