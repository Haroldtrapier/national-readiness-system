import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { MainLayout } from './layout/MainLayout'
import { National } from './pages/National'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainLayout><National /></MainLayout>} />
      </Routes>
    </Router>
  )
}

export default App
