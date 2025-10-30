import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
    proxy: {
      // Optional: proxy API during dev if you want to avoid CORS in dev
      // '/api': {
      //   target: 'http://localhost:8000',
      //   changeOrigin: true,
      // }
    }
  }
})
