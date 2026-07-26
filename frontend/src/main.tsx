import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import PageNotFound from './components/pageNotFound.tsx'
import "./index.css"
import { BrowserRouter, Route, Routes } from 'react-router-dom'

createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<App />} />
      <Route path='/snippet/:id' element={<App />} />

      {/* if a  page is not found */}
      <Route path="/*" element={<PageNotFound />} />
    </Routes>
  </BrowserRouter>
)
